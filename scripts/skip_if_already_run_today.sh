#!/usr/bin/env bash
# 오늘 날짜(UTC)
TODAY=$(date -u +%Y-%m-%d)
if git log --since="$TODAY 00:00" --until="$TODAY 23:59" --oneline | grep -q "auto: update ZeroDNS"; then
  echo "::notice title=ZeroDNS::오늘 이미 자동 커밋 있음 - 스킵"
  exit 0
fi
