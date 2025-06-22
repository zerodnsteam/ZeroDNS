import re

def parse_domains(sources, logger):
    domains = set()
    errors = []
    for name, fn in sources.items():
        if not fn:
            continue
        logger.log(f"    {name} 도메인 추출 중…")
        with open(fn, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                s = line.strip().lower()
                if not s or s.startswith("#"):
                    continue
                # 일반 도메인만 (영문/숫자/하이픈/점)
                if re.fullmatch(r"[a-z0-9\.\-]+", s) and ".." not in s and " " not in s:
                    domains.add(s)
                # AdGuard 구문 (||domain^ 등)
                elif s.startswith("||") and s.endswith("^"):
                    d = s[2:-1]
                    if re.fullmatch(r"[a-z0-9\.\-]+", d) and ".." not in d and " " not in d:
                        domains.add(d)
                    else:
                        errors.append(f"{name}:{i}:{line.strip()}")
                else:
                    errors.append(f"{name}:{i}:{line.strip()}")
    logger.log(f"      → 도메인 {len(domains):,}개 추출")
    if errors:
        logger.log(f"      → 이상행 {len(errors)}개 (output/parse_errors.txt)")
        with open("output/parse_errors.txt", "w", encoding="utf-8") as f:
            for e in errors:
                f.write(e + "\n")
    return domains, errors
