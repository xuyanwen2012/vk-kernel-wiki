#!/usr/bin/env bash
# Run the whole offline test suite. Exit code 0 only if every step passes.
#
#   bash tests/run_all.sh
#
# No network, no pytest, no site-packages: everything runs under `python3 -S`.
set -uo pipefail

TESTS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$TESTS_DIR/.." && pwd)"
cd "$REPO_ROOT"
export PYTHONDONTWRITEBYTECODE=1
unset VK_KERNEL_WIKI_ROOT

passed=0
failed=0
failed_steps=()

run_step() {
    local name="$1"
    shift
    echo "=== $name"
    if "$@"; then
        passed=$((passed + 1))
        echo "--- PASS: $name"
    else
        failed=$((failed + 1))
        failed_steps+=("$name")
        echo "--- FAIL: $name"
    fi
    echo
}

unit_tests() {
    python3 -S "$TESTS_DIR/test_wiki.py" 2>&1
}

run_step "yaml fallback (python3 -S)" bash "$TESTS_DIR/check_yaml_fallback.sh"
run_step "unit tests (tests/test_wiki.py)" unit_tests

echo "Steps: $passed passed, $failed failed"
if [ "$failed" -ne 0 ]; then
    printf 'Failed step: %s\n' "${failed_steps[@]}"
    exit 1
fi
echo "ALL TESTS PASSED"
