import dns.resolver

class DNSHelper:
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5

    def get_spf_record(self, domain):
        try:
            ans = self.resolver.resolve(domain, 'TXT')
            for r in ans:
                txt = str(r).strip('"')
                if txt.startswith('v=spf1'):
                    return txt
        except Exception:
            pass
        return None

    def get_mx_records(self, domain):
        try:
            ans = self.resolver.resolve(domain, 'MX')
            recs = [{"priority": r.preference, "exchange": str(r.exchange).rstrip('.')} for r in ans]
            return sorted(recs, key=lambda x: x["priority"])
        except Exception as e:
            return [{"error": str(e)}]
