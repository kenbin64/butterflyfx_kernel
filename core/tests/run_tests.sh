#!/usr/bin/env bash
# run_tests.sh
#
# Run the full pytest suite for the project.
# Place this file at the repository root and make it executable:
#   chmod +x run_tests.sh
#
# The script:
# - ensures the repository root is on PYTHONPATH so `core` imports resolve
# - runs pytest for the tests/ directory
# - exits with pytest's exit code so CI systems can detect failures

set -euo pipefail

# Determine repository root (directory containing this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

# Export PYTHONPATH so tests can import the `core` package
export PYTHONPATH="$REPO_ROOT:$PYTHONPATH"

# Optional: show Python and pytest versions for debugging
echo "Python: $(python -V 2>&1)"
if command -v pytest >/dev/null 2>&1; then
  echo "pytest: $(pytest --version)"
else
  echo "pytest not found in PATH. Install with: pip install pytest"
  exit 1
fi

# Run pytest on the tests directory with verbose output
echo "Running tests..."
pytest -q "$REPO_ROOT/tests"

# Capture and forward pytest exit code (should be handled by set -e, but explicit is clearer)
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
  echo "All tests passed."
else
  echo "Some tests failed. Exit code: $EXIT_CODE"
fi

exit $EXIT_CODE
