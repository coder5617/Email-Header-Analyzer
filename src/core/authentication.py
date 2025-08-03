import re
from typing import Any, Dict

class AuthenticationAnalyzer:
    def analyze(self, headers: Dict[str, Any]) -> Dict[str, Any]:
        spf = self._analyze_spf(headers)
        dkim = self._analyze_dkim(headers)
        dmarc = self._analyze_dmarc(headers)
        issues = self._identify_issues(spf, dkim, dmarc)
        score = self._calculate_score(spf, dkim, dmarc)
        return {"spf": spf, "dkim": dkim, "dmarc": dmarc, "issues": issues, "score": score}

    def _analyze_spf(self, headers):
        data = {"status": "not_found", "result": None}
        val = headers.get("Received-SPF", "")
        if val:
            data["status"] = "found"
            data["details"] = val
            for r in ["pass", "fail", "softfail", "neutral", "none"]:
                if r in val.lower():
                    data["result"] = r
                    break
        return data

    def _analyze_dkim(self, headers):
        data = {"status": "not_found", "domains": []}
        sigs = headers.get("DKIM-Signature", [])
        if isinstance(sigs, str):
            sigs = [sigs]
        for sig in sigs:
            m = re.search(r"d=([^;]+)", sig)
            if m:
                data["domains"].append(m.group(1))
        if data["domains"]:
            data["status"] = "found"
        return data

    def _analyze_dmarc(self, headers):
        data = {"status": "not_found", "result": None}
        ar = headers.get("Authentication-Results", "")
        m = re.search(r"dmarc=([^;,\s]+)", ar, re.IGNORECASE)
        if m:
            data["status"] = "found"
            data["result"] = m.group(1)
        return data

    def _calculate_score(self, spf, dkim, dmarc):
        s = 0
        if spf.get("result") == "pass":
            s += 35
        if dkim["status"] == "found":
            s += 30
        if dmarc.get("result") == "pass":
            s += 35
        if spf.get("result") == "fail":
            s -= 20
        if dmarc.get("result") == "fail":
            s -= 15
        return max(0, min(100, s))

    def _identify_issues(self, spf, dkim, dmarc):
        issues = []
        if spf.get("result") == "fail":
            issues.append("SPF failed")
        if dkim["status"] != "found":
            issues.append("DKIM missing")
        if dmarc.get("result") == "fail":
            issues.append("DMARC failed")
        return issues
