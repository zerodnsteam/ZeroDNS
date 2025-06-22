import requests

FILTER_URLS = {
    "OISD": "https://cdn.jsdelivr.net/gh/cbuijs/oisd@master/big/domains",
    "HAGEZI ULTIMATE": "https://cdn.jsdelivr.net/gh/cbuijs/hagezi@main/lists/ultimate/domains",
    "HAGEZI NATIVE-APPLE": "https://cdn.jsdelivr.net/gh/cbuijs/hagezi@main/lists/native-apple/domains",
    "1HOSTS PRO": "https://cdn.jsdelivr.net/gh/cbuijs/1hosts@main/Pro/domains",
    "LIST-KR": "https://cdn.jsdelivr.net/gh/adguardteam/HostlistsRegistry@main/assets/filter_25.txt",
    "ADGUARD DNS": "https://cdn.jsdelivr.net/gh/adguardteam/AdGuardSDNSFilter@gh-pages/Filters/filter.txt"
}

def download_sources(out_dir, logger):
    results = {}
    for name, url in FILTER_URLS.items():
        logger.log(f"  - {name} 다운로드 중…")
        try:
            resp = requests.get(url, timeout=40)
            resp.raise_for_status()
            fn = f"{out_dir}/{name.replace(' ', '_')}.txt"
            with open(fn, "w", encoding="utf-8") as f:
                f.write(resp.text)
            results[name] = fn
            logger.log(f"    성공: {fn} ({len(resp.text.splitlines()):,}줄)")
        except Exception as e:
            logger.log(f"    실패: {name} ({e})")
            results[name] = None
    return results
