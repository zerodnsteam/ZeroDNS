import re
from typing import Set

def clean_domain(domain: str) -> str:
    return domain.strip().lower()

def is_valid_domain(domain: str) -> bool:
    # 공백/맨앞·맨뒤 점/연속 점/비ASCII/최소한 . 포함 등
    if ".." in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False
    if not re.match(r"^[a-z0-9\-\.]+$", domain):
        return False
    if domain.count('.') < 1:
        return False  # TLD만 있는 경우 등 제거
    return True

def remove_subdomains_if_root_exists(domains: Set[str]) -> Set[str]:
    # 루트 도메인이 있으면 하위 서브도메인 자동 삭제
    result = set()
    sorted_domains = sorted(domains, key=lambda x: x.count('.'))
    seen_roots = set()
    for domain in sorted_domains:
        parts = domain.split(".")
        redundant = False
        for i in range(1, len(parts)):
            parent = ".".join(parts[i:])
            if parent in seen_roots:
                redundant = True
                break
        if not redundant:
            result.add(domain)
            seen_roots.add(domain)
    return result
