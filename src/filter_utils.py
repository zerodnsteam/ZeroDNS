import re

def clean_domain(domain: str) -> str:
    return domain.strip().lower()

def is_valid_domain(domain: str) -> bool:
    if ".." in domain or domain.startswith(".") or domain.endswith("."):
        return False
    if not re.fullmatch(r"[a-z0-9\-\.]+", domain):
        return False
    if domain.count('.') < 1:
        return False
    return True

def remove_subdomains_if_root_exists(domains: set) -> set:
    roots = set(domains)
    result = set()
    for domain in domains:
        parts = domain.split('.')
        for i in range(1, len(parts)):
            parent = ".".join(parts[i:])
            if parent in roots:
                break
        else:
            result.add(domain)
    return result
