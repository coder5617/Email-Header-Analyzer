# src/email_header_analyzer/core/spoofing.py
import re
from typing import Any, Dict, List
from email_validator import validate_email, EmailNotValidError
from email_header_analyzer.utils.validators import extract_email_domain

class SpoofingDetector:
    def __init__(self):
        self.exec_titles = [
            "ceo", "cfo", "cto", "president", "director",
            "manager", "chief", "vp"
        ]
        self.bec_keywords = [
            "urgent", "wire transfer", "payment",
            "invoice", "confidential", "asap", "immediate"
        ]

    def analyze(self, headers: Dict[str, Any]) -> Dict[str, Any]:
        ds = self._domain_spoof(headers)
        dsn = self._display_spoof(headers)
        bec = self._bec(headers)
        issues = self._compile(ds, dsn, bec)
        score = self._calc_score(ds, dsn, bec)
        return {
            "domain_spoofing": ds,
            "display_name_spoofing": dsn,
            "bec_indicators": bec,
            "issues": issues,
            "risk_score": score
        }

    def _domain_spoof(self, headers: Dict[str, Any]) -> Dict[str, Any]:
        f = headers.get("From", "")
        r = headers.get("Return-Path", "")

        try:
            addr = validate_email(f)
            fd = addr.domain
        except (EmailNotValidError, AttributeError):
            fd = extract_email_domain(f)

        try:
            addr2 = validate_email(r)
            rd = addr2.domain
        except (EmailNotValidError, AttributeError):
            rd = extract_email_domain(r)

        mismatch = bool(fd and rd and fd != rd)

        return {
            "from_domain": fd,
            "return_path_domain": rd,
            "domain_mismatch": mismatch,
            "status": "suspicious" if mismatch else "clean"
        }

    def _display_spoof(self, headers: Dict[str, Any]) -> Dict[str, Any]:
        f = headers.get("From", "")
        m = re.match(r'(?:"?([^"<]+)"?\s*)?<([^>]+)>', f)
        dn = m.group(1).strip() if m and m.group(1) else None
        imp = bool(dn and any(t in dn.lower() for t in self.exec_titles))
        return {
            "display_name": dn,
            "executive_impersonation": imp,
            "status": "suspicious" if imp else "clean"
        }

    def _bec(self, headers: Dict[str, Any]) -> Dict[str, Any]:
        subj = headers.get("Subject", "").lower()
        found = [k for k in self.bec_keywords if k in subj]
        level = "low"
        if len(found) >= 2:
            level = "high"
        elif len(found) == 1:
            level = "medium"
        return {"keywords_found": found, "risk_level": level}

    def _calc_score(self, ds: Dict[str, Any], dsn: Dict[str, Any], bec: Dict[str, Any]) -> int:
        s = 0
        if ds["domain_mismatch"]:
            s += 30
        if dsn["executive_impersonation"]:
            s += 40
        if bec["risk_level"] == "high":
            s += 30
        elif bec["risk_level"] == "medium":
            s += 15
        return min(100, s)

    def _compile(self, ds: Dict[str, Any], dsn: Dict[str, Any], bec: Dict[str, Any]) -> List[str]:
        issues: List[str] = []
        if ds["domain_mismatch"]:
            issues.append("Domain mismatch")
        if dsn["executive_impersonation"]:
            issues.append("Executive impersonation")
        if bec["keywords_found"]:
            issues.append(f"BEC keywords: {', '.join(bec['keywords_found'])}")
        return issues
