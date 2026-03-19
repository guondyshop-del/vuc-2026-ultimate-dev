"""
VUC-2026 Connection Diagnostics Tool
Advanced connection troubleshooting and repair utilities
"""

import asyncio
import aiohttp
import socket
import ssl
import dns.resolver
import ping3
import subprocess
import platform
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json
import logging
from urllib.parse import urlparse
import time

from app.core.connection_resilience import connection_resilience, ConnectionConfig

logger = logging.getLogger(__name__)

class ConnectionDiagnostics:
    """Advanced connection diagnostics and repair"""
    
    def __init__(self):
        self.logger = logging.getLogger("vuc_connection_diagnostics")
        
    async def comprehensive_diagnosis(self, url: str) -> Dict[str, Any]:
        """Perform comprehensive connection diagnosis"""
        
        diagnosis = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {
                "overall_status": "unknown",
                "issues_found": 0,
                "recommendations": []
            }
        }
        
        # Parse URL
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            diagnosis["parsed_url"] = {
                "scheme": parsed.scheme,
                "domain": domain,
                "port": port,
                "path": parsed.path
            }
        except Exception as e:
            diagnosis["tests"]["url_parsing"] = {
                "status": "failed",
                "error": str(e)
            }
            diagnosis["summary"]["overall_status"] = "invalid_url"
            return diagnosis
        
        # Run diagnostic tests
        tests = [
            ("dns_resolution", self._test_dns_resolution, domain),
            ("network_connectivity", self._test_network_connectivity, domain, port),
            ("ssl_certificate", self._test_ssl_certificate, domain, port),
            ("http_response", self._test_http_response, url),
            ("ping_test", self._test_ping, domain),
            ("trace_route", self._test_trace_route, domain),
            ("dns_servers", self._test_dns_servers, domain),
            ("port_scan", self._test_port_scan, domain, port)
        ]
        
        for test_name, test_func, *args in tests:
            try:
                result = await test_func(*args)
                diagnosis["tests"][test_name] = result
                
                if result["status"] == "failed":
                    diagnosis["summary"]["issues_found"] += 1
                    
            except Exception as e:
                diagnosis["tests"][test_name] = {
                    "status": "error",
                    "error": str(e)
                }
                diagnosis["summary"]["issues_found"] += 1
        
        # Generate recommendations
        diagnosis["summary"]["recommendations"] = self._generate_recommendations(diagnosis["tests"])
        
        # Determine overall status
        if diagnosis["summary"]["issues_found"] == 0:
            diagnosis["summary"]["overall_status"] = "healthy"
        elif diagnosis["summary"]["issues_found"] <= 2:
            diagnosis["summary"]["overall_status"] = "degraded"
        else:
            diagnosis["summary"]["overall_status"] = "unhealthy"
        
        return diagnosis
    
    async def _test_dns_resolution(self, domain: str) -> Dict[str, Any]:
        """Test DNS resolution"""
        result = {
            "status": "passed",
            "details": {},
            "duration": 0
        }
        
        start_time = time.time()
        
        try:
            # Test with system DNS
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(domain, 'A')
            ips = [str(ip) for ip in answers]
            
            result["details"]["system_dns"] = {
                "ips": ips,
                "count": len(ips)
            }
            
            # Test with alternative DNS servers
            alt_dns_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
            alt_results = {}
            
            for server in alt_dns_servers:
                try:
                    resolver.nameservers = [server]
                    answers = resolver.resolve(domain, 'A')
                    alt_ips = [str(ip) for ip in answers]
                    alt_results[server] = {
                        "status": "success",
                        "ips": alt_ips,
                        "count": len(alt_ips)
                    }
                except Exception as e:
                    alt_results[server] = {
                        "status": "failed",
                        "error": str(e)
                    }
            
            result["details"]["alternative_dns"] = alt_results
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
        
        result["duration"] = time.time() - start_time
        return result
    
    async def _test_network_connectivity(self, domain: str, port: int) -> Dict[str, Any]:
        """Test network connectivity"""
        result = {
            "status": "passed",
            "details": {},
            "duration": 0
        }
        
        start_time = time.time()
        
        try:
            # Test TCP connection
            future = asyncio.open_connection(domain, port)
            reader, writer = await asyncio.wait_for(future, timeout=10.0)
            
            result["details"]["tcp_connection"] = {
                "status": "success",
                "local_address": writer.get_extra_info('sockname'),
                "remote_address": writer.get_extra_info('peername')
            }
            
            writer.close()
            await writer.wait_closed()
            
        except asyncio.TimeoutError:
            result["status"] = "failed"
            result["error"] = "Connection timeout"
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
        
        result["duration"] = time.time() - start_time
        return result
    
    async def _test_ssl_certificate(self, domain: str, port: int) -> Dict[str, Any]:
        """Test SSL certificate"""
        result = {
            "status": "skipped",
            "details": {},
            "duration": 0
        }
        
        if port != 443:
            return result
        
        start_time = time.time()
        
        try:
            # Create SSL context
            context = ssl.create_default_context()
            
            # Get certificate
            future = asyncio.open_connection(domain, port, ssl=context)
            reader, writer = await asyncio.wait_for(future, timeout=10.0)
            
            # Get certificate info
            ssl_object = writer.get_extra_info('ssl_object')
            cert = ssl_object.getpeercert()
            
            result["status"] = "passed"
            result["details"]["certificate"] = {
                "subject": cert.get('subject'),
                "issuer": cert.get('issuer'),
                "version": cert.get('version'),
                "serial_number": cert.get('serialNumber'),
                "not_before": cert.get('notBefore'),
                "not_after": cert.get('notAfter'),
                "subject_alt_names": cert.get('subjectAltName', [])
            }
            
            # Check certificate validity
            import datetime as dt
            not_after = dt.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            if not_after < dt.datetime.now():
                result["status"] = "failed"
                result["error"] = "Certificate has expired"
            elif not_after < dt.datetime.now() + dt.timedelta(days=30):
                result["status"] = "warning"
                result["warning"] = "Certificate expires soon"
            
            writer.close()
            await writer.wait_closed()
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
        
        result["duration"] = time.time() - start_time
        return result
    
    async def _test_http_response(self, url: str) -> Dict[str, Any]:
        """Test HTTP response"""
        result = {
            "status": "passed",
            "details": {},
            "duration": 0
        }
        
        start_time = time.time()
        
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    result["details"]["http_response"] = {
                        "status_code": response.status,
                        "status_text": response.reason,
                        "headers": dict(response.headers),
                        "content_type": response.headers.get('content-type'),
                        "content_length": response.headers.get('content-length')
                    }
                    
                    if response.status >= 400:
                        result["status"] = "failed" if response.status >= 500 else "warning"
                        result["error"] = f"HTTP {response.status}: {response.reason}"
                    
        except asyncio.TimeoutError:
            result["status"] = "failed"
            result["error"] = "HTTP request timeout"
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
        
        result["duration"] = time.time() - start_time
        return result
    
    async def _test_ping(self, domain: str) -> Dict[str, Any]:
        """Test ping connectivity"""
        result = {
            "status": "passed",
            "details": {},
            "duration": 0
        }
        
        start_time = time.time()
        
        try:
            # Use ping3 for async ping
            ping_time = ping3.ping(domain, timeout=5)
            
            if ping_time is not None:
                result["details"]["ping"] = {
                    "status": "success",
                    "time_ms": ping_time * 1000
                }
            else:
                result["status"] = "failed"
                result["error"] = "Ping failed"
                
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
        
        result["duration"] = time.time() - start_time
        return result
    
    async def _test_trace_route(self, domain: str) -> Dict[str, Any]:
        """Test trace route"""
        result = {
            "status": "skipped",
            "details": {},
            "duration": 0
        }
        
        # Platform-specific trace route
        try:
            if platform.system().lower() == 'windows':
                cmd = ['tracert', domain]
            else:
                cmd = ['traceroute', domain]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                result["status"] = "passed"
                result["details"]["trace_route"] = {
                    "output": stdout.decode(),
                    "hops": len(stdout.decode().split('\n')) - 2
                }
            else:
                result["status"] = "failed"
                result["error"] = stderr.decode()
                
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def _test_dns_servers(self, domain: str) -> Dict[str, Any]:
        """Test multiple DNS servers"""
        result = {
            "status": "passed",
            "details": {},
            "duration": 0
        }
        
        start_time = time.time()
        
        dns_servers = [
            ("Google DNS", "8.8.8.8"),
            ("Cloudflare DNS", "1.1.1.1"),
            ("OpenDNS", "208.67.222.222"),
            ("Quad9 DNS", "9.9.9.9"),
            ("Comodo DNS", "8.26.56.26")
        ]
        
        for name, server in dns_servers:
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [server]
                answers = resolver.resolve(domain, 'A')
                ips = [str(ip) for ip in answers]
                
                result["details"][name] = {
                    "status": "success",
                    "server": server,
                    "ips": ips,
                    "response_time": time.time() - start_time
                }
                
            except Exception as e:
                result["details"][name] = {
                    "status": "failed",
                    "server": server,
                    "error": str(e)
                }
        
        result["duration"] = time.time() - start_time
        return result
    
    async def _test_port_scan(self, domain: str, port: int) -> Dict[str, Any]:
        """Test port connectivity"""
        result = {
            "status": "passed",
            "details": {},
            "duration": 0
        }
        
        start_time = time.time()
        
        # Common ports to test
        common_ports = [80, 443, 8080, 8443, 3000, 5000, 8000, 9000]
        
        for test_port in common_ports:
            try:
                future = asyncio.open_connection(domain, test_port)
                reader, writer = await asyncio.wait_for(future, timeout=3.0)
                
                result["details"][f"port_{test_port}"] = {
                    "status": "open",
                    "service": self._identify_service(test_port)
                }
                
                writer.close()
                await writer.wait_closed()
                
            except Exception:
                result["details"][f"port_{test_port}"] = {
                    "status": "closed",
                    "service": self._identify_service(test_port)
                }
        
        result["duration"] = time.time() - start_time
        return result
    
    def _identify_service(self, port: int) -> str:
        """Identify service by port number"""
        services = {
            80: "HTTP",
            443: "HTTPS",
            8080: "HTTP-Alt",
            8443: "HTTPS-Alt",
            3000: "Node.js",
            5000: "Flask/Django",
            8000: "Dev Server",
            9000: "SonarQube/Portainer"
        }
        return services.get(port, "Unknown")
    
    def _generate_recommendations(self, tests: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # DNS issues
        if "dns_resolution" in tests and tests["dns_resolution"]["status"] == "failed":
            recommendations.append("Check DNS configuration and try alternative DNS servers (8.8.8.8, 1.1.1.1)")
            recommendations.append("Verify domain name spelling and availability")
        
        # Network connectivity issues
        if "network_connectivity" in tests and tests["network_connectivity"]["status"] == "failed":
            recommendations.append("Check firewall settings and network connectivity")
            recommendations.append("Verify if the target server is running and accessible")
        
        # SSL certificate issues
        if "ssl_certificate" in tests and tests["ssl_certificate"]["status"] in ["failed", "warning"]:
            recommendations.append("Update SSL certificate or check certificate validity")
            recommendations.append("Verify system date and time settings")
        
        # HTTP response issues
        if "http_response" in tests and tests["http_response"]["status"] == "failed":
            recommendations.append("Check if the web server is running and responding")
            recommendations.append("Verify URL endpoints and API availability")
        
        # High response times
        for test_name, test_result in tests.items():
            if test_result.get("duration", 0) > 5.0:
                recommendations.append(f"High response time detected in {test_name} - consider optimization")
        
        # Ping failures
        if "ping_test" in tests and tests["ping_test"]["status"] == "failed":
            recommendations.append("Network connectivity issues detected - check network configuration")
        
        return recommendations
    
    async def auto_repair(self, url: str) -> Dict[str, Any]:
        """Attempt automatic repair of connection issues"""
        
        repair_result = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "actions_taken": [],
            "success": False,
            "message": ""
        }
        
        # First, run diagnosis
        diagnosis = await self.comprehensive_diagnosis(url)
        
        # Attempt repairs based on diagnosis
        try:
            # Clear DNS cache
            if "dns_resolution" in diagnosis["tests"] and diagnosis["tests"]["dns_resolution"]["status"] == "failed":
                await self._clear_dns_cache()
                repair_result["actions_taken"].append("DNS cache cleared")
            
            # Flush socket connections
            await self._flush_connections()
            repair_result["actions_taken"].append("Socket connections flushed")
            
            # Reset connection pool
            await connection_resilience.pool_manager.cleanup()
            repair_result["actions_taken"].append("Connection pools reset")
            
            # Re-test connection
            retest = await self.comprehensive_diagnosis(url)
            
            if retest["summary"]["issues_found"] < diagnosis["summary"]["issues_found"]:
                repair_result["success"] = True
                repair_result["message"] = "Connection issues partially resolved"
            elif retest["summary"]["issues_found"] == 0:
                repair_result["success"] = True
                repair_result["message"] = "All connection issues resolved"
            else:
                repair_result["success"] = False
                repair_result["message"] = "Connection issues persist - manual intervention required"
            
        except Exception as e:
            repair_result["message"] = f"Auto-repair failed: {str(e)}"
        
        repair_result["diagnosis_before"] = diagnosis["summary"]
        repair_result["diagnosis_after"] = retest["summary"] if 'retest' in locals() else diagnosis["summary"]
        
        return repair_result
    
    async def _clear_dns_cache(self):
        """Clear DNS cache"""
        try:
            if platform.system().lower() == 'windows':
                subprocess.run(['ipconfig', '/flushdns'], check=True, capture_output=True)
            else:
                subprocess.run(['sudo', 'systemd-resolve', '--flush-caches'], check=True, capture_output=True)
        except Exception:
            pass  # DNS cache clearing is optional
    
    async def _flush_connections(self):
        """Flush existing connections"""
        # This would typically involve closing existing connections
        # In our case, the connection pool cleanup handles this
        pass

# Global diagnostics instance
connection_diagnostics = ConnectionDiagnostics()
