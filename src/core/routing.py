import re
from typing import Any, Dict
from email_header_analyzer.utils.ip_helper import extract_ip_from_received, is_private_ip

class RoutingAnalyzer:
    def analyze(self, headers: Dict[str, Any]) -> Dict[str, Any]:
        rec = headers.get("Received", [])
        if isinstance(rec, str):
            rec = [rec]
        hops = []
        for idx, raw in enumerate(rec):
            hop = self._parse_hop(raw, idx)
            if hop:
                hops.append(hop)
        hops = list(reversed(hops))
        suspicious = [h for h in hops if h["is_suspicious"]]
        issues = []
        if suspicious:
            issues.append(f"{len(suspicious)} suspicious hops")
        if len(hops) < 2:
            issues.append("Too few hops")
        if len(hops) > 15:
            issues.append("Too many hops")
        return {"hops": hops, "total_hops": len(hops), "suspicious_hops": suspicious, "issues": issues}

    def _parse_hop(self, raw, idx):
        hop = {"index": idx, "raw": raw, "from_ip": None, "from_host": None, "by_host": None, "is_suspicious": False}
        m1 = re.search(r"from\s+([\S]+)", raw, re.IGNORECASE)
        if m1:
            hop["from_host"] = m1.group(1)
        ip = extract_ip_from_received(raw)
        if ip:
            hop["from_ip"] = ip
            hop["is_suspicious"] = is_private_ip(ip) and hop["from_host"] and not any(k in hop["from_host"].lower() for k in ["internal", "local", "corp"])
        m2 = re.search(r"by\s+([\S]+)", raw, re.IGNORECASE)
        if m2:
            hop["by_host"] = m2.group(1)
        if hop["from_ip"] == "127.0.0.1":
            hop["is_suspicious"] = True
        return hop
