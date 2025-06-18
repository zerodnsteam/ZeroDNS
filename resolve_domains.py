import concurrent.futures
import dns.resolver
from pathlib import Path

DNS_SERVERS = [
    "1.1.1.1",
    "8.8.8.8",
    "76.76.2.0",
    "208.67.222.222"
]
EXTRA_DNS = "185.222.222.222"  # DNS.SB 예외

MAX_WORKERS = 15
TIMEOUT = 1.5

input_path = Path("ZeroDNS_raw.txt")
output_path = Path("ZeroDNS_resolved.txt")

def resolve(domain_rule):
    domain = domain_rule[2:-1]
    # 4개 글로벌 DNS에서 먼저 시도
    for dns_ip in DNS_SERVERS:
        try:
            resolver = dns.resolver.Resolver(configure=False)
            resolver.nameservers = [dns_ip]
            resolver.timeout = TIMEOUT
            resolver.lifetime = TIMEOUT
            answers = resolver.resolve(domain, "A")
            if answers:
                return domain_rule
        except Exception:
            continue
    # 모두 실패시 DNS.SB에서 한 번 더 시도
    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [EXTRA_DNS]
        resolver.timeout = TIMEOUT
        resolver.lifetime = TIMEOUT
        answers = resolver.resolve(domain, "A")
        if answers:
            return domain_rule
    except Exception:
        pass
    return None

with input_path.open("r", encoding="utf-8") as f:
    domains = [line.strip() for line in f if line.strip()]

resolved = []
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(resolve, d): d for d in domains}
    for idx, future in enumerate(concurrent.futures.as_completed(futures), 1):
        result = future.result()
        if result:
            resolved.append(result)
        if idx % 5000 == 0 or idx == len(domains):
            print(f"{idx} / {len(domains)} 처리 완료")

with output_path.open("w", encoding="utf-8") as f:
    for d in sorted(set(resolved)):
        f.write(d + "\n")

print(f"ZeroDNS DNS 응답 확인 완료! ({len(resolved):,}개)")
