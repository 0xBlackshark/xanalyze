#!/usr/bin/env bash
# Publish this repo to GitHub. The token is NEVER stored in the repo or in git config.
#
#   GITHUB_TOKEN=github_pat_xxx bash tools/push-github.sh [owner/repo] [branch] [private|public]
#
# Token needs, for fine-grained PAT: Contents: Read+write (+ Administration: Read+write only if the
# repo must be created by the script). For classic PAT: scope "repo".
# If you already created the repo on the website, pass it as $1 and the script skips creation.
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

REPO="${1:-${GITHUB_REPO:-}}"
BRANCH="${2:-main}"
VIS="${3:-private}"

if [[ -z "$REPO" || "$REPO" != */* ]]; then
  echo "usage: GITHUB_TOKEN=... bash tools/push-github.sh owner/repo [branch] [private|public]"; exit 2
fi
if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "GITHUB_TOKEN is not set. Options:"
  echo "  A) export GITHUB_TOKEN=<fine-grained PAT>  then re-run this script (I can push for you if you paste it here)"
  echo "  B) create an empty repo named ${REPO##*/} on github.com yourself, then:"
  echo "     git init -b ${BRANCH} && git add -A && git commit -m 'DD corpus' && \\"
  echo "     git remote add origin https://github.com/${REPO}.git && git push -u origin ${BRANCH}"
  echo "  C) with gh CLI:  gh repo create ${REPO} --${VIS} --source=. --push"
  exit 3
fi

API="https://api.github.com"
OWNER="${REPO%%/*}"; NAME="${REPO##*/}"
auth=(-H "Authorization: Bearer ${GITHUB_TOKEN}" -H "Accept: application/vnd.github+json" -H "X-API-Version: 2022-11-28")

if ! curl -sf "${auth[@]}" "${API}/repos/${OWNER}/${NAME}" -o /dev/null; then
  echo "creating repo ${REPO} (${VIS}) ..."
  curl -sf "${auth[@]}" -X POST "${API}/user/repos" \
    -d "{\"name\":\"${NAME}\",\"private\":$([ "$VIS" = private ] && echo true || echo false),\"description\":\"Crypto/NFT due-diligence corpus (Thai, agent-readable)\",\"has_issues\":false,\"has_wiki\":false}" \
    -o /dev/null || { echo "repo creation failed — check token scopes/owner"; exit 1; }
else
  echo "repo ${REPO} already exists — reusing it"
fi

[[ -d .git ]] || git init -q -b "${BRANCH}"
git config user.name  >/dev/null 2>&1 || git config user.name  "due-diligence-bot"
git config user.email >/dev/null 2>&1 || git config user.email "noreply@local"
git add -A
git commit -q -m "crypto/NFT due-diligence corpus: $(git ls-files | wc -l | tr -d ' ') files" || echo "nothing new to commit"

# push with an in-memory header so the token never lands in .git/config or the remote URL
git -c credential.helper= push -q "${auth[@]/#/-c http.extraHeader=}" 2>/dev/null || true
if git remote get-url origin >/dev/null 2>&1; then git remote set-url origin "https://github.com/${REPO}.git"; else git remote add origin "https://github.com/${REPO}.git"; fi
git -c http.extraHeader="Authorization: Bearer ${GITHUB_TOKEN}" push -u origin "${BRANCH}"

echo "pushed → https://github.com/${REPO} (branch ${BRANCH})"
