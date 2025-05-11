#!/bin/bash

REPO="Kyoura-DE/entotjawa"
TOKEN="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"
WORKFLOW_FILE="main.yml"
BRANCH="main"

# 1. Ambil ID dari workflow run terbaru yang masih aktif
RUN_ID=$(curl -s -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$REPO/actions/runs?branch=$BRANCH&status=in_progress" \
  | jq '.workflow_runs[] | select(.name == "Debug via tmate") | .id' | head -n1)

if [ -n "$RUN_ID" ]; then
  echo "🛑 Workflow sedang berjalan, menghentikan run ID: $RUN_ID"

  # 2. Stop workflow run yang sedang berjalan
  curl -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$REPO/actions/runs/$RUN_ID/cancel"

  # Tunggu hingga run benar-benar dihentikan
  echo "⏳ Menunggu 10 detik agar benar-benar stop..."
  sleep 10
else
  echo "✅ Tidak ada workflow yang sedang berjalan."
fi

# 3. Jalankan ulang workflow-nya
echo "🚀 Menjalankan ulang workflow $WORKFLOW_FILE..."
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$REPO/actions/workflows/$WORKFLOW_FILE/dispatches" \
  -d "{\"ref\":\"$BRANCH\"}"
