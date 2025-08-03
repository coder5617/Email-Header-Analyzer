from email_validator import validate_email, EmailNotValidError

def is_valid_email(addr):
    try:
        validate_email(addr)
        return True
    except EmailNotValidError:
        return False

def extract_email_domain(header):
    import re
    m = re.search(r'<([^>]+)>', header)
    email = m.group(1) if m else header
    return email.split('@')[-1].strip() if '@' in email else None
