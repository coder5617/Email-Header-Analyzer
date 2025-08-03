import email
import email.header
from typing import Any, Dict, List

class EmailHeaderParser:
    def parse_headers(self, raw_headers: str) -> Dict[str, Any]:
        if not raw_headers.strip():
            raise ValueError("No email headers provided")
        msg = email.message_from_string(raw_headers)
        parsed = {}
        for name, value in msg.items():
            decoded = email.header.decode_header(value)
            parts = []
            for part, enc in decoded:
                if isinstance(part, bytes):
                    parts.append(part.decode(enc or "utf-8", errors="ignore"))
                else:
                    parts.append(part)
            full = "".join(parts).strip()
            if name in parsed:
                if not isinstance(parsed[name], list):
                    parsed[name] = [parsed[name]]
                parsed[name].append(full)
            else:
                parsed[name] = full
        return parsed

    def analyze_headers(self, raw_headers: str) -> Dict[str, Any]:
        headers = self.parse_headers(raw_headers)
        from email_header_analyzer.core.authentication import AuthenticationAnalyzer
        from email_header_analyzer.core.routing import RoutingAnalyzer
        from email_header_analyzer.core.spoofing import SpoofingDetector
        from email_header_analyzer.core.geographic import GeographicAnalyzer
        from email_header_analyzer.core.content import ContentAnalyzer

        auth = AuthenticationAnalyzer().analyze(headers)
        routing = RoutingAnalyzer().analyze(headers)
        spoof = SpoofingDetector().analyze(headers)
        geo = GeographicAnalyzer().analyze(headers)
        content = ContentAnalyzer().analyze(headers)
        summary = self._generate_summary(headers)

        return {
            "parsed_headers": headers,
            "authentication": auth,
            "routing": routing,
            "spoofing": spoof,
            "geographic": geo,
            "content": content,
            "summary": summary
        }

    def _generate_summary(self, headers: Dict[str, Any]) -> Dict[str, Any]:
        required = ["From", "Date", "Message-ID"]
        missing = [h for h in required if h not in headers]
        return {"total_headers": len(headers), "critical_issues": missing}
