# ZeroDNS AdGuard DNS Filter

ZeroDNS AdGuard DNS Filter는 oisd big, ultimate-mini, tif-mini, popupads의 Top-N 도메인 블록리스트를 매일 병합·중복 제거하여 AdGuard DNS(Adblock-style) 문법으로 자동 생성하는 프로젝트입니다.

---

## 📂 저장소 구조

```
/
├─ .github/
│   └─ workflows/
│      └─ update-filters.yml   # 매일 자동으로 필터 생성·커밋하는 GitHub Actions 워크플로
├─ ZeroDNS-AdGuard-DNS-Filter.txt  # 매일 갱신되는 최종 필터 파일
└─ README.md                  # 이 파일
```

---

## 🚀 사용 방법

1. **AdGuard Home** 또는 **AdGuard DNS** 설정에서 아래 URL 중 하나를 필터 목록에 추가하세요:

   ```
   https://cdn.jsdelivr.net/gh/zerodnsteam/ZeroDNS@main/ZeroDNS-AdGuard-DNS-Filter.txt
   ```
   또는
   ```
   https://raw.githack.com/zerodnsteam/ZeroDNS/main/ZeroDNS-AdGuard-DNS-Filter.txt
   ```

2. 필터를 추가한 뒤 **동기화** 또는 **새로 고침**을 실행하면 최신 도메인이 차단됩니다.

---

## ⚙️ 자동 업데이트

- **GitHub Actions**  
  - 매일 KST 자정(UTC 15:00)에 `.github/workflows/update-filters.yml` 워크플로가 실행됩니다.  
  - oisd big, ultimate-mini, tif-mini, popupads 4개 소스에서 필터를 내려받아 병합·중복 제거 후  
    Adblock-style(`||도메인^`) 포맷으로 `ZeroDNS-AdGuard-DNS-Filter.txt` 생성 → 커밋 & 푸시  
  - 도메인 변화가 없으면 커밋 없이 종료하여 불필요한 커밋을 방지합니다.

- **CDN 배포**  
  - jsDelivr 글로벌 엣지 캐시에 자동 배포됩니다.  
  - `@main` 대신 태그나 커밋 해시를 지정하여 고정 URL로 사용할 수도 있습니다.

---

## 📄 필터 포맷

- **주석**: `!` 로 시작하며, Title/Description/Version/Updated/Source 등의 메타정보 포함  
- **차단 룰**: `||example.org^` 형태의 Adblock-style 문법  
  - `||`: 서브도메인 포함 차단  
  - `^`: 도메인 경계 표시

---

## 🤝 기여

1. 이슈 또는 PR 환영  
2. 새로운 소스를 추가하려면 `.github/workflows/update-filters.yml`의 `sources` 섹션 수정  
3. 포맷·버그 리포트·기능 개선 제안 모두 환영합니다!

---

## 📜 라이선스

라이선스: 없음  
이 프로젝트는 별도의 라이선스 없이 배포됩니다.
