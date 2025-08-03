import time
import requests
from typing import Any, Dict, List, Optional
from email_header_analyzer.utils.ip_helper import extract_ips_from_headers

class GeographicAnalyzer:
    def analyze(self, headers) -> Dict[str, Any]:
        ips = extract_ips_from_headers(headers)
        geo = {}
        for ip in ips:
            geo[ip] = self._get_geo(ip)
        risks = self._identify(geo)
        return {"sender_ips": ips, "geolocation": geo, "risk_factors": risks, "issues": risks}

    def _get_geo(self, ip):
        attempt = 0
        while attempt < 3:
            try:
                r = requests.get(f"http://ip-api.com/json/{ip}", timeout=int(__import__("os").environ.get("DEFAULT_TIMEOUT", 10)))
                if r.status_code == 200:
                    d = r.json()
                    if d.get("status") == "success":
                        return {"country": d.get("country"), "city": d.get("city"), "isp": d.get("isp"), "status": "found"}
                break
            except Exception:
                attempt += 1
                time.sleep(2 ** attempt)
        return {"status": "unknown"}

    def _identify(self, geo):
        countries = {v.get("country") for v in geo.values() if v.get("country")}
        if len(countries) > 2:
            return [f"Multiple countries: {', '.join(countries)}"]
        return []
