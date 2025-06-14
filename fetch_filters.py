import requests

filter_sources = [
    # 순서대로 자동 다운로드
    ("native.apple.txt", "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@main/adblock/native.apple.txt"),
    ("ultimate.mini.txt", "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@main/adblock/ultimate.mini.txt"),
    ("adblock.txt", "https://cdn.jsdelivr.net/gh/badmojr/1Hosts@master/Lite/adblock.txt"),
    ("oisd_small.txt", "https://cdn.jsdelivr.net/gh/sjhgvr/oisd@main/oisd_small.txt"),
    ("filter_25.txt", "https://cdn.jsdelivr.net/gh/adguardteam/HostlistsRegistry@main/assets/filter_25.txt"),
    ("filter_1_ios.txt", "https://filters.adtidy.org/dns/filter_1_ios.txt"),
]

for fname, url in filter_sources:
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(f"filters/{fname}", "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"Downloaded: {fname}")
    except Exception as e:
        print(f"Failed {fname}: {e}")
