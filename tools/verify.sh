#!/usr/bin/env bash
# Thin wrapper so agents/humans can just run: bash tools/verify.sh
# --offline skips all network calls (structure/schema check only).
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

if ! command -v python3 >/dev/null 2>&1; then echo "python3 is required"; exit 127; fi

rc=0
echo "== structure & schema =="
python3 tools/build.py --check || rc=1
python3 tools/check_schema.py  || rc=1

if [[ "${1:-}" == "--offline" ]]; then
  echo; echo "offline mode: skipping live checks"; exit $rc
fi

command -v curl >/dev/null 2>&1 || { echo "curl not found -> running offline only"; exit $rc; }

echo "== live re-verification =="
python3 tools/verify.py || rc=1

echo
if [[ $rc -eq 0 ]]; then echo "RESULT: OK — repo is internally consistent and live checks did not drift"; else
  echo "RESULT: NEEDS ATTENTION — see DRIFT/FAIL/SKIP lines above"; fi
exit $rc
