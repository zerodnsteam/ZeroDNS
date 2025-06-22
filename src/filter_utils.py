import re
import unicodedata

TLD_ONLY = {
    "com", "net", "org", "kr", "cn", "jp", "de", "tv", "ru", "us",
    "info", "biz", "top", "shop", "xyz", "co", "io", "ai", "uk"
}
FAKE_TLD = {
    "local", "localhost", "test", "invalid", "example"
}

def clean_domain(domain: str) -> str:
    domain = unicodedata.normalize("NFKC", domain)
    domain = domain.strip().lower()
    while domain.endswith('.'):
        domain = domain[:-1]
    domain = re.sub(r'\s+', '', domain)
    if domain.startswith('www.') and domain.count('.') >= 2:
        domain = domain[4:]
    domain = re.sub(r'[^\w\.-]', '', domain)
    return domain

def is_garbage_domain(domain: str) -> bool:
    if not domain or domain in TLD_ONLY or domain in FAKE_TLD:
        return True
    if ".." in domain:
        return True
    if re.search(r'\s', domain):
        return True
    if any(c in domain for c in ['/', '@', ':', '?']):
        return True
    if len(domain) < 4:
        return True
    if len(domain) > 255:
        return True
    if re.match(r'.*\.[0-9]+$', domain):
        return True
    if domain.startswith("xn--"):
        if len(domain) < 5 or not re.match(r'^xn--[a-z0-9-]+$', domain):
            return True
    if "xn--" in domain and not re.match(r'^(xn--[a-z0-9-]+\.)+[a-z]{2,}$', domain):
        return True
    return False

def is_valid_domain(domain: str) -> bool:
    return re.match(r'^[a-z0-9][a-z0-9\-\.]+\.[a-z]{2,}$', domain) is not None
