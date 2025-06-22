import os
import re

def is_valid_domain(domain):
    domain = domain.strip().lower()
    if not domain:
        return False
    if domain.startswith(".") or ".." in domain:
        return False
    if domain.startswith("-") or domain.endswith("-"):
        return False
    if re.search(r"[^\w\.\-]", domain):  # 알파벳/숫자/하이픈/점 외 문자 제거
        return False
    if domain.count(".") < 1:
        return False
    if domain.endswith(".js") or domain.endswith(".css") or domain.endswith(".txt"):
        return False
    return True

def extract_domains(text):
    lines = text.splitlines()
    domains = []
    for line in lines:
        line = line.strip().lower()
        line = re.sub(r"^(@@|\|\||\||0\.0\.0\.0|127\.0\.0\.1|\[::\])", "", line)
        line = re.sub(r"\^.*$", "", line)
        line = re.sub(r"#.*$", "", line)
        line = re.sub(r"\s+", "", line)
        if is_valid_domain(line):
            domains.append(line)
    return domains

def keep_root_only(domains):
    root_set = set()
    for domain in domains:
        parts = domain.split(".")
        if len(parts) >= 2:
            root = ".".join(parts[-2:])
            root_set.add(root)
    final_set = set()
    for domain in domains:
        parts = domain.split(".")
        if len(parts) >= 2:
            root = ".".join(parts[-2:])
            if domain == root:
                final_set.add(domain)
    return final_set

def parse_domains(sources, logger=None):
    all_domains = set()
    errors = []
    raw_total = 0

    for name, path in sources.items():
        if logger:
            logger.info(f"    {name} 도메인 추출 중…")
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            errors.append(f"{name}: {e}")
            continue

        domains = extract_domains(text)
        raw_total += len(domains)

        for d in domains:
            if is_valid_domain(d):
                all_domains.add(d)
            else:
                errors.append(f"{name}:{d}")

    final_domains = keep_root_only(all_domains)

    # 에러 저장
    os.makedirs("output", exist_ok=True)
    with open("output/parse_errors.txt", "w", encoding="utf-8") as f:
        for e in errors:
            f.write(e + "\n")

    return final_domains, errors, raw_total
