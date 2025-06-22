import re
from typing import Set

def clean_domain(domain: str) -> str:
    return domain.strip().lower()

def is_valid_domain(domain: str) -> bool:
    if ".." in domain:
        return False
    if not re.match(r"^[a-z0-9\-\.]+$", domain):  # ASCII, -, .만 허용
        return False
    if domain.count('.') < 1:
        return False  # 최소 example.com 형태
    return True

def remove_subdomains_if_root_exists(domains: Set[str]) -> Set[str]:
    # 루트 도메인이 있으면 하위 서브도메인 제거
    result = set()
    sorted_domains = sorted(domains, key=lambda x: x.count('.'))
    seen_roots = set()
    for domain in sorted_domains:
        parts = domain.split(".")
        redundant = False
        # check if any parent domain is already in result
        for i in range(1, len(parts)):
            parent = ".".join(parts[i:])
            if parent in seen_roots:
                redundant = True
                break
        if not redundant:
            result.add(domain)
            seen_roots.add(domain)
    return result
