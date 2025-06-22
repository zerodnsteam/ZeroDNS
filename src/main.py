import os
from downloader import download_sources
from parser import parse_domains
from merger import merge_domains
from formatter import format_adguard
from vibes import get_random_message
from notify import send_telegram
from progress import ProgressLogger

def ensure_dirs():
    for d in ["filters", "output"]:
        os.makedirs(d, exist_ok=True)

def main():
    logger = ProgressLogger()
    ensure_dirs()
    logger.log("[1/7] 소스 다운로드")
    sources = download_sources("filters", logger)
    logger.log("[2/7] 도메인 추출/정제")
    domains, errors = parse_domains(sources, logger)
    logger.log("[3/7] 중복제거/불필요도메인 필터")
    clean_domains, filter_stats = merge_domains(domains, logger)
    logger.log("[4/7] AdGuard 변환 및 저장")
    line_count = format_adguard(clean_domains, logger)
    logger.log("[5/7] 통계/변화량 집계 및 로그 저장")
    logger.save()
    logger.log("[6/7] 텔레그램 알림 전송")
    status = "success" if line_count > 0 and not errors else "fail" if errors else "nochange"
    msg = get_random_message(status, line_count, filter_stats, errors)
    send_telegram(msg, logger)
    logger.log(f"[7/7] 전체 작업 완료! (라인 수: {line_count:,})")

if __name__ == "__main__":
    main()
