def merge_domains(domains, logger):
    before = len(domains)
    # 서브도메인 유지, 루트만 남기려면 여기서 별도 처리
    filtered = set(d for d in domains if d.count('.') >= 1 and '--' not in d)
    stats = {"원본": before, "정제후": len(filtered)}
    logger.log(f"      → 정제/중복제거: {before:,}→{len(filtered):,}")
    return filtered, stats
