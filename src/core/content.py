import re
from typing import Any, Dict, List, Optional

class ContentAnalyzer:
    def analyze(self, headers) -> Dict[str, Any]:
        subj = headers.get("Subject", "")
        lower = subj.lower()
        urg = any(w in lower for w in ["urgent", "asap", "immediate", "emergency"])
        fin = any(w in lower for w in ["payment", "invoice", "wire", "bank"])
        caps = subj.isupper() and len(subj) > 5
        patterns = []
        if urg:
            patterns.append("Urgency indicators")
        if caps:
            patterns.append("All caps subject")
        if "confirm your account" in lower:
            patterns.append("Confirm account prompt")
        score = min(100, (20 if urg else 0) + (25 if fin else 0) + (15 if caps else 0))
        issues = [f"Subject: {p}" for p in patterns]
        return {"subject_analysis": {"subject": subj, "length": len(subj), "suspicious_patterns": patterns}, "risk_score": score, "issues": issues}
