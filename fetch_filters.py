import requests

filter_sources = [
    # 순서대로 다운로드
    ("ultimate.txt", "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@main/adblock/ultimate.txt"),
    ("1hosts-Xtra_adblock.txt", "https://cdn.jsdelivr.net/gh/zerodnsteam/ZeroDNS@main/filters/1hosts-Xtra_adblock.txt"),
    ("oisd_big.txt", "https://cdn.jsdelivr.net/gh/sjhgvr/oisd@main/oisd_big.txt"),
    ("native.apple.txt", "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@main/adblock/native.apple.txt"),
    ("filter_25.txt", "https://cdn.jsdelivr.net/gh/adguardteam/HostlistsRegistry@main/assets/filter_25.txt"),
    ("filter_1_ios.txt", "https://filters.adtidy.org/dns/filter_1_ios.txt"),
]

for fname, url in filter_sources:
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(f"filters/{fname}", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"✔ {fname} 다운로드 성공")
    except Exception as e:
        print(f"✗ {fname} 실패: {e}")
