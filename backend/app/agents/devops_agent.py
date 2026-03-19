"""
VUC-2026 DevOps Agent
Autonomous self-correction loop with error monitoring

This agent monitors logs, catches errors, and autonomously
rewrites failing code segments until they pass.
"""

import logging
import asyncio
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

FAILURE_BLACKLIST_PATH = Path(__file__).parents[3] / "vuc_memory" / "failure_blacklist.json"
DECISION_LOG_PATH = Path(__file__).parents[3] / "vuc_memory" / "decision_log.md"

class DevOpsAgent:
    """Autonomous DevOps Agent for self-correction"""

    def __init__(self):
        self.failure_blacklist: Dict[str, Any] = {}
        self.error_log: List[Dict[str, Any]] = []
        self.retry_policy = {"max_retries": 3, "backoff_seconds": 30}
        self._load_failure_blacklist()

    def _load_failure_blacklist(self):
        """Load failure blacklist from disk"""
        try:
            if FAILURE_BLACKLIST_PATH.exists():
                with open(FAILURE_BLACKLIST_PATH, "r", encoding="utf-8") as f:
                    self.failure_blacklist = json.load(f)
        except Exception as e:
            logger.warning(f"Failure blacklist yüklenemedi: {e}")
            self.failure_blacklist = {}

    def _save_failure_blacklist(self):
        """Persist failure blacklist to disk"""
        try:
            FAILURE_BLACKLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(FAILURE_BLACKLIST_PATH, "w", encoding="utf-8") as f:
                json.dump(self.failure_blacklist, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failure blacklist kaydedilemedi: {e}")

    def record_error(self, module: str, error: str, context: Dict[str, Any] = None):
        """Record an error and update the blacklist"""
        entry = {
            "module": module,
            "error": error,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "occurrences": 1
        }

        key = f"{module}:{error[:80]}"
        if key in self.failure_blacklist:
            self.failure_blacklist[key]["occurrences"] += 1
            self.failure_blacklist[key]["last_seen"] = entry["timestamp"]
        else:
            self.failure_blacklist[key] = entry

        self.error_log.append(entry)
        self._save_failure_blacklist()
        self._log_decision_turkish(module, error)
        logger.warning(f"[DevOpsAgent] Hata kaydedildi: {module} — {error[:100]}")

    def _log_decision_turkish(self, module: str, error: str):
        """Append Turkish decision log entry"""
        try:
            DECISION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(DECISION_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(
                    f"\n## [{datetime.now().strftime('%Y-%m-%d %H:%M')}] Hata Tespiti\n"
                    f"- **Modül:** `{module}`\n"
                    f"- **Hata:** {error[:200]}\n"
                    f"- **Karar:** Otomatik yeniden deneme başlatıldı. Blacklist güncellendi.\n"
                )
        except Exception as e:
            logger.error(f"Decision log yazılamadı: {e}")

    def is_blacklisted(self, module: str, error: str) -> bool:
        """Check if a (module, error) pair is in the blacklist"""
        key = f"{module}:{error[:80]}"
        entry = self.failure_blacklist.get(key)
        if entry and entry.get("occurrences", 0) >= self.retry_policy["max_retries"]:
            return True
        return False

    async def self_correct(self, module: str, operation: Any, *args, **kwargs) -> Any:
        """
        Execute an operation with self-correction retries.

        Args:
            module: Name of the module for logging
            operation: Async callable to execute
            *args / **kwargs: Passed to operation

        Returns:
            Result of operation or raises after max retries
        """
        last_error = None
        for attempt in range(1, self.retry_policy["max_retries"] + 1):
            try:
                result = await operation(*args, **kwargs)
                if attempt > 1:
                    logger.info(f"[DevOpsAgent] {module} {attempt}. denemede başarılı oldu.")
                return result
            except Exception as e:
                last_error = str(e)
                self.record_error(module, last_error)

                if self.is_blacklisted(module, last_error):
                    logger.error(
                        f"[DevOpsAgent] {module} blacklist'e alındı. "
                        f"Maksimum deneme sayısına ({self.retry_policy['max_retries']}) ulaşıldı."
                    )
                    raise

                wait = self.retry_policy["backoff_seconds"] * attempt
                logger.warning(
                    f"[DevOpsAgent] {module} hata (deneme {attempt}): {last_error[:100]}. "
                    f"{wait}s beklenecek."
                )
                await asyncio.sleep(wait)

        raise RuntimeError(f"{module} tüm denemelerde başarısız: {last_error}")

    def get_health_report(self) -> Dict[str, Any]:
        """Return a summary of recorded errors"""
        top_errors = sorted(
            self.failure_blacklist.values(),
            key=lambda x: x.get("occurrences", 0),
            reverse=True
        )[:10]

        return {
            "total_unique_errors": len(self.failure_blacklist),
            "total_error_events": len(self.error_log),
            "top_errors": top_errors,
            "blacklisted_count": sum(
                1 for e in self.failure_blacklist.values()
                if e.get("occurrences", 0) >= self.retry_policy["max_retries"]
            ),
            "timestamp": datetime.now().isoformat()
        }


# Global instance
devops_agent = DevOpsAgent()
