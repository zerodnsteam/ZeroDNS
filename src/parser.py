from filter_utils import clean_domain, is_valid_domain, remove_subdomains_if_root_exists

def parse_domains(sources: dict, logger):
    domains = set()
    errors = []
    raw_total = 0

    for name, fn in sources.items():
        logger.info(f"    {name} 도메인 추출 중…")
        try:
            with open(fn, encoding="utf-8") as f:
                lines = f.read().splitlines()
            for line in lines:
                line = clean_domain(line)
                if not line or line.startswith("!") or line.startswith("#"):
                    continue
                if not is_valid_domain(line):
                    continue  # 오류 기록 제거됨 (조용히 무시)
                domains.add(line)
            raw_total += len(lines)
        except Exception as e:
            logger.warning(f"    {name} 파일 처리 중 오류 발생: {e}")

    refined = remove_subdomains_if_root_exists(domains)
    return refined, [], raw_total
