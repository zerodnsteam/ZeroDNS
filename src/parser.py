from filter_utils import clean_domain, is_garbage_domain, is_valid_domain

def parse_domains(files, logger):
    domains = set()
    errors = []
    raw_total = 0

    for name, fn in files.items():
        if not fn:
            continue
        logger.log(f"    {name} 도메인 추출 중…")
        with open(fn, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                raw_total += 1
                try:
                    d = clean_domain(line)
                    if d and is_valid_domain(d) and not is_garbage_domain(d):
                        domains.add(d)
                    else:
                        errors.append(f"{name}:{i}:{line.strip()}")
                except Exception as e:
                    errors.append(f"{name}:{i}: (파싱 오류) {str(e)} : {line.strip()}")

    logger.log(f"      → 원본 줄 수: {raw_total:,}줄")
    logger.log(f"      → 정제 후 도메인: {len(domains):,}개")
    if errors:
        logger.log(f"      → 이상한 줄: {len(errors):,}개 (output/parse_errors.txt)")
        with open("output/parse_errors.txt", "w", encoding="utf-8") as f:
            for e in errors:
                f.write(e + "\n")
    return domains, errors, raw_total
