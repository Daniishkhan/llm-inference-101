#!/usr/bin/env bash
# Install the pre-commit hook, once per clone:   tools/install-hooks.sh
#
# The hook checks the staged version of every staged Python file with ruff: it must be formatted
# (ruff format --check) and pass the lint rules in pyproject.toml (ruff check). It changes nothing;
# when it refuses a commit, run `uv run ruff format <file>`, look at what it changed, stage, commit.
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
hook="$root/.git/hooks/pre-commit"

cat > "$hook" <<'HOOK'
#!/usr/bin/env bash
# Installed by tools/install-hooks.sh: checks staged Python files with ruff, and changes nothing.
set -uo pipefail
root="$(git rev-parse --show-toplevel)"
ruff="$root/.venv/bin/ruff"
[ -x "$ruff" ] || ruff="uv run --quiet ruff"

fail=0
while IFS= read -r -d '' file; do
    if ! git show ":$file" | $ruff format --check --quiet --stdin-filename "$file" - >/dev/null; then
        echo "pre-commit: $file is not formatted; run: uv run ruff format $file" >&2
        fail=1
    fi
    if ! git show ":$file" | $ruff check --quiet --stdin-filename "$file" -; then
        echo "pre-commit: $file has lint findings (above); fix them and stage again" >&2
        fail=1
    fi
done < <(git diff --cached --name-only --diff-filter=ACM -z -- '*.py')
exit $fail
HOOK

chmod +x "$hook"
echo "installed $hook"
