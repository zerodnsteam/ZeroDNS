import os
from filter_utils import clean_domain, is_valid_domain, remove_subdomains_if_root_exists

def parse_domains(files, logger):
    raw_domains = []
    raw_total = 0

    for name, fn in files.items():
        if not fn or not os.path.isfile(fn):
            logger.warning(f"      → {name}: 파일 없음, 건너뜀 ({fn})")
            continue
        logger.info(f"    {name} 도메인 추출 중…")
        with open(fn, encoding="utf-8") as f:
            for line in f:
                raw_total += 1
                d = clean_domain(line)
                if d and is_valid_domain(d):
                    raw_domains.append(d)
    logger.info(f"      → 원본 줄 수: {raw_total:,}줄")
    # 1. 이상 도메인 삭제 & 중복 제거
    unique_domains = set(raw_domains)
    # 2. 루트 도메인 있으면 하위 서브도메인 자동 삭제
    final_domains = remove_subdomains_if_root_exists(unique_domains)
    logger.info(f"      → 정제 후 도메인: {len(final_domains):,}개")
    return final_domains, [], raw_total  # errors 빈 리스트로 반환
