"""
VUC-2026 Ghost Auditor
Shadowban monitor + autonomous proxy/fingerprint rotation

Monitors channel health for shadowban signals, proxy health,
and autonomously rotates identities when detection is triggered.
"""

import logging
import asyncio
import random
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

from app.agents.devops_agent import devops_agent

logger = logging.getLogger(__name__)

SHADOWBAN_SIGNALS = {
    "view_velocity_drop": {"threshold": -0.40, "severity": "critical"},   # -40% view drop
    "comment_suppression": {"threshold": -0.60, "severity": "critical"},  # -60% comment drop
    "subscriber_spike_loss": {"threshold": -0.30, "severity": "high"},
    "impressions_collapse": {"threshold": -0.50, "severity": "critical"},
    "ctr_drop": {"threshold": -0.25, "severity": "high"},
    "search_ranking_loss": {"threshold": -5, "severity": "high"},         # positions dropped
    "suggested_video_removal": {"threshold": True, "severity": "medium"},
}

PROXY_HEALTH_THRESHOLDS = {
    "max_failure_rate": 0.15,      # 15% failure = rotate
    "max_latency_ms": 3000,
    "min_anonymity": "high",
    "max_age_hours": 6,            # Rotate proxy after 6 hours
}


class GhostAuditor:
    """Autonomous shadowban detection and recovery agent"""

    def __init__(self):
        self.monitoring_sessions: Dict[str, Dict[str, Any]] = {}
        self.proxy_registry: Dict[str, Dict[str, Any]] = {}
        self.fingerprint_registry: Dict[str, Dict[str, Any]] = {}
        self.alert_history: List[Dict[str, Any]] = []
        self.rotation_history: List[Dict[str, Any]] = []
        self.auto_recovery_enabled = True

    async def start_channel_audit(self, channel_id: str,
                                   channel_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start shadowban audit for a channel.

        Args:
            channel_id: Channel identifier
            channel_metrics: Current and historical metrics

        Returns:
            Audit results with recommended actions
        """
        try:
            logger.info(f"Ghost Audit başlatıldı: {channel_id}")

            # Analyze for shadowban signals
            signals_detected = self._analyze_shadowban_signals(channel_metrics)

            # Check proxy health
            proxy_health = self._check_proxy_health(channel_id)

            # Check fingerprint freshness
            fingerprint_status = self._check_fingerprint_status(channel_id)

            # Determine overall risk level
            risk_level = self._calculate_risk_level(
                signals_detected, proxy_health, fingerprint_status
            )

            # Auto-recovery plan
            recovery_plan = None
            if risk_level in ["high", "critical"] and self.auto_recovery_enabled:
                recovery_plan = await self._execute_auto_recovery(
                    channel_id, signals_detected, proxy_health, fingerprint_status
                )

            audit_result = {
                "channel_id": channel_id,
                "audit_timestamp": datetime.now().isoformat(),
                "risk_level": risk_level,
                "signals_detected": signals_detected,
                "proxy_health": proxy_health,
                "fingerprint_status": fingerprint_status,
                "recovery_plan": recovery_plan,
                "auto_recovery_executed": recovery_plan is not None,
                "next_audit_in": self._calculate_next_audit_interval(risk_level),
                "recommendations": self._generate_audit_recommendations(
                    risk_level, signals_detected
                )
            }

            self.monitoring_sessions[channel_id] = audit_result

            # Log to DevOps agent if critical
            if risk_level == "critical":
                devops_agent.record_error(
                    "ghost_auditor",
                    f"Kritik shadowban riski: {channel_id}",
                    {"risk_level": risk_level, "signals": signals_detected}
                )

            logger.info(f"Ghost Audit tamamlandı: {channel_id} — Risk: {risk_level}")
            return audit_result

        except Exception as e:
            logger.error(f"Ghost Audit hatası: {e}")
            return {"success": False, "error": str(e), "channel_id": channel_id}

    def _analyze_shadowban_signals(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze metrics for shadowban signals"""
        detected = []

        # View velocity check
        views_7d = metrics.get("views_7d", 0)
        views_prev_7d = metrics.get("views_prev_7d", 1)
        if views_prev_7d > 0:
            view_change = (views_7d - views_prev_7d) / views_prev_7d
            threshold = SHADOWBAN_SIGNALS["view_velocity_drop"]["threshold"]
            if view_change < threshold:
                detected.append({
                    "signal": "view_velocity_drop",
                    "value": round(view_change * 100, 1),
                    "threshold": threshold * 100,
                    "severity": SHADOWBAN_SIGNALS["view_velocity_drop"]["severity"],
                    "description": f"İzlenme hızı %{abs(view_change * 100):.1f} düştü"
                })

        # CTR check
        ctr = metrics.get("ctr", 0)
        ctr_prev = metrics.get("ctr_prev", 0)
        if ctr_prev > 0:
            ctr_change = (ctr - ctr_prev) / ctr_prev
            if ctr_change < SHADOWBAN_SIGNALS["ctr_drop"]["threshold"]:
                detected.append({
                    "signal": "ctr_drop",
                    "value": round(ctr_change * 100, 1),
                    "threshold": SHADOWBAN_SIGNALS["ctr_drop"]["threshold"] * 100,
                    "severity": SHADOWBAN_SIGNALS["ctr_drop"]["severity"],
                    "description": f"CTR %{abs(ctr_change * 100):.1f} düştü"
                })

        # Comment suppression
        comments_7d = metrics.get("comments_7d", 0)
        comments_prev = metrics.get("comments_prev_7d", 1)
        if comments_prev > 0:
            comment_change = (comments_7d - comments_prev) / comments_prev
            if comment_change < SHADOWBAN_SIGNALS["comment_suppression"]["threshold"]:
                detected.append({
                    "signal": "comment_suppression",
                    "value": round(comment_change * 100, 1),
                    "threshold": SHADOWBAN_SIGNALS["comment_suppression"]["threshold"] * 100,
                    "severity": SHADOWBAN_SIGNALS["comment_suppression"]["severity"],
                    "description": f"Yorumlar %{abs(comment_change * 100):.1f} baskılandı"
                })

        # Search ranking
        search_position = metrics.get("search_position", 10)
        search_prev = metrics.get("search_position_prev", 10)
        position_drop = search_position - search_prev
        if position_drop >= 5:
            detected.append({
                "signal": "search_ranking_loss",
                "value": position_drop,
                "threshold": 5,
                "severity": SHADOWBAN_SIGNALS["search_ranking_loss"]["severity"],
                "description": f"Arama sıralaması {position_drop} basamak düştü"
            })

        return detected

    def _check_proxy_health(self, channel_id: str) -> Dict[str, Any]:
        """Check proxy health for channel"""
        proxy_info = self.proxy_registry.get(channel_id)

        if not proxy_info:
            return {
                "status": "no_proxy",
                "health": "unknown",
                "recommendation": "Proxy atama gerekli"
            }

        assigned_at = datetime.fromisoformat(proxy_info.get("assigned_at", datetime.now().isoformat()))
        age_hours = (datetime.now() - assigned_at).total_seconds() / 3600

        failure_rate = proxy_info.get("failure_rate", 0.0)
        latency_ms = proxy_info.get("latency_ms", 1000)

        # Health checks
        issues = []
        if age_hours > PROXY_HEALTH_THRESHOLDS["max_age_hours"]:
            issues.append(f"Proxy {age_hours:.1f}s süredir aktif (max: {PROXY_HEALTH_THRESHOLDS['max_age_hours']}s)")
        if failure_rate > PROXY_HEALTH_THRESHOLDS["max_failure_rate"]:
            issues.append(f"Başarısızlık oranı %{failure_rate*100:.1f} yüksek")
        if latency_ms > PROXY_HEALTH_THRESHOLDS["max_latency_ms"]:
            issues.append(f"Gecikme {latency_ms}ms yüksek")

        health = "healthy" if not issues else "degraded" if len(issues) == 1 else "critical"

        return {
            "status": "assigned",
            "health": health,
            "age_hours": round(age_hours, 1),
            "failure_rate": failure_rate,
            "latency_ms": latency_ms,
            "issues": issues,
            "needs_rotation": health in ["degraded", "critical"],
            "proxy_host": proxy_info.get("host", "unknown")
        }

    def _check_fingerprint_status(self, channel_id: str) -> Dict[str, Any]:
        """Check digital fingerprint freshness"""
        fp_info = self.fingerprint_registry.get(channel_id)

        if not fp_info:
            return {
                "status": "no_fingerprint",
                "fresh": False,
                "recommendation": "Fingerprint oluşturma gerekli"
            }

        created_at = datetime.fromisoformat(fp_info.get("created_at", datetime.now().isoformat()))
        age_hours = (datetime.now() - created_at).total_seconds() / 3600

        return {
            "status": "active",
            "fresh": age_hours < 24,
            "age_hours": round(age_hours, 1),
            "canvas_hash": fp_info.get("canvas_hash", ""),
            "user_agent": fp_info.get("user_agent", ""),
            "needs_refresh": age_hours >= 24
        }

    def _calculate_risk_level(self, signals: List[Dict], proxy: Dict,
                               fingerprint: Dict) -> str:
        """Calculate overall detection risk level"""
        risk_score = 0

        # Signal severities
        for signal in signals:
            if signal["severity"] == "critical":
                risk_score += 40
            elif signal["severity"] == "high":
                risk_score += 25
            elif signal["severity"] == "medium":
                risk_score += 10

        # Proxy health
        if proxy.get("health") == "critical":
            risk_score += 30
        elif proxy.get("health") == "degraded":
            risk_score += 15
        elif proxy.get("status") == "no_proxy":
            risk_score += 20

        # Fingerprint
        if not fingerprint.get("fresh"):
            risk_score += 15

        if risk_score >= 60:
            return "critical"
        elif risk_score >= 35:
            return "high"
        elif risk_score >= 15:
            return "medium"
        else:
            return "low"

    async def _execute_auto_recovery(self, channel_id: str, signals: List[Dict],
                                      proxy: Dict, fingerprint: Dict) -> Dict[str, Any]:
        """Autonomously execute recovery actions"""
        actions_taken = []

        # Rotate proxy if needed
        if proxy.get("needs_rotation") or proxy.get("status") == "no_proxy":
            new_proxy = await self._rotate_proxy(channel_id)
            actions_taken.append({
                "action": "proxy_rotation",
                "status": "executed",
                "new_proxy": new_proxy.get("host", "unknown"),
                "timestamp": datetime.now().isoformat()
            })

        # Refresh fingerprint if needed
        if fingerprint.get("needs_refresh") or fingerprint.get("status") == "no_fingerprint":
            new_fp = self._generate_fingerprint(channel_id)
            actions_taken.append({
                "action": "fingerprint_refresh",
                "status": "executed",
                "new_canvas_hash": new_fp.get("canvas_hash"),
                "timestamp": datetime.now().isoformat()
            })

        # Critical signal: pause uploads for cooling-off
        critical_signals = [s for s in signals if s["severity"] == "critical"]
        if critical_signals:
            cooling_hours = random.uniform(12, 48)
            actions_taken.append({
                "action": "upload_pause",
                "status": "scheduled",
                "cooling_off_hours": round(cooling_hours, 1),
                "resume_at": (datetime.now() + timedelta(hours=cooling_hours)).isoformat(),
                "reason": f"{len(critical_signals)} kritik sinyal tespit edildi",
                "timestamp": datetime.now().isoformat()
            })

        # Record rotation
        self.rotation_history.append({
            "channel_id": channel_id,
            "actions": actions_taken,
            "trigger_signals": [s["signal"] for s in signals],
            "timestamp": datetime.now().isoformat()
        })

        logger.info(f"Otomatik kurtarma: {channel_id} — {len(actions_taken)} eylem")

        return {
            "recovery_executed": True,
            "actions_taken": actions_taken,
            "total_actions": len(actions_taken)
        }

    async def _rotate_proxy(self, channel_id: str) -> Dict[str, Any]:
        """Rotate to a new residential proxy"""
        # Simulated proxy pool rotation
        new_proxy = {
            "host": f"residential_{random.randint(100, 999)}.proxy.pool",
            "port": random.choice([8080, 1080, 3128]),
            "type": "residential",
            "country": random.choice(["TR", "DE", "US", "NL"]),
            "anonymity": "high",
            "assigned_at": datetime.now().isoformat(),
            "failure_rate": 0.0,
            "latency_ms": random.randint(200, 800)
        }

        self.proxy_registry[channel_id] = new_proxy
        logger.info(f"Proxy rotasyonu: {channel_id} → {new_proxy['host']}")
        return new_proxy

    def _generate_fingerprint(self, channel_id: str) -> Dict[str, Any]:
        """Generate new browser fingerprint"""
        ua_pool = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edg/120.0.0.0",
        ]

        fp = {
            "canvas_hash": f"fp_{random.randint(1000000, 9999999):x}",
            "webgl_hash": f"wg_{random.randint(1000000, 9999999):x}",
            "audio_hash": f"au_{random.randint(100000, 999999):x}",
            "user_agent": random.choice(ua_pool),
            "screen": random.choice(["1920x1080", "2560x1440", "1366x768"]),
            "timezone": "Europe/Istanbul",
            "language": "tr-TR,tr;q=0.9,en-US;q=0.8",
            "created_at": datetime.now().isoformat()
        }

        self.fingerprint_registry[channel_id] = fp
        logger.info(f"Fingerprint yenilendi: {channel_id}")
        return fp

    def _calculate_next_audit_interval(self, risk_level: str) -> str:
        """Calculate next audit timing based on risk"""
        intervals = {
            "critical": "1 saat",
            "high": "3 saat",
            "medium": "6 saat",
            "low": "24 saat"
        }
        return intervals.get(risk_level, "24 saat")

    def _generate_audit_recommendations(self, risk_level: str,
                                         signals: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recs = []

        if risk_level == "critical":
            recs.append("🚨 Yüklemeyi DERHAL durdur — 24-48 saat soğuma süresi uygula")
            recs.append("🔄 Proxy ve fingerprint rotasyonu acil yapıldı")
            recs.append("📊 Kanal metriklerini 1 saat içinde tekrar kontrol et")
        elif risk_level == "high":
            recs.append("⚠️ Yükleme sıklığını %50 azalt")
            recs.append("🔄 Ghost persona aktivitelerini 12 saat durdur")
            recs.append("📈 Organik etkileşimi artırmak için Lurker protokolü çalıştır")
        elif risk_level == "medium":
            recs.append("📉 Yükleme sıklığını %25 azalt")
            recs.append("✅ Proxy sağlığını kontrol et")
            recs.append("👁️ 48 saat boyunca yakından izle")
        else:
            recs.append("✅ Sistem normal çalışıyor")
            recs.append("📊 Haftalık derin audit planla")

        for signal in signals[:3]:
            recs.append(f"→ {signal['description']}: {signal.get('value', '')}%")

        return recs

    def get_audit_summary(self) -> Dict[str, Any]:
        """Get audit dashboard summary"""
        total_channels = len(self.monitoring_sessions)
        risk_distribution: Dict[str, int] = {}

        for session in self.monitoring_sessions.values():
            risk = session.get("risk_level", "unknown")
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1

        return {
            "total_monitored_channels": total_channels,
            "risk_distribution": risk_distribution,
            "critical_channels": [
                cid for cid, s in self.monitoring_sessions.items()
                if s.get("risk_level") == "critical"
            ],
            "total_rotations": len(self.rotation_history),
            "auto_recovery_enabled": self.auto_recovery_enabled,
            "active_proxies": len(self.proxy_registry),
            "active_fingerprints": len(self.fingerprint_registry),
            "last_audit": max(
                (s["audit_timestamp"] for s in self.monitoring_sessions.values()),
                default=None
            )
        }


# Global instance
ghost_auditor = GhostAuditor()
