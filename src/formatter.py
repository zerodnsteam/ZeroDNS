def format_adguard(domains, logger):
    fn = "output/ZeroDNS.txt"
    with open(fn, "w", encoding="utf-8") as f:
        for d in sorted(domains):
            f.write(f"||{d}^\n")
    logger.log(f"      → 최종 필터 {len(domains):,}줄 저장: {fn}")
    return len(domains)
