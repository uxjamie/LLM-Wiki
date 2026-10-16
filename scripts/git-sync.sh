#!/usr/bin/env bash
# Owner-triggered git sync for a brain whose folder is mounted into a sandbox
# that refuses deletes and renames.
#
# Why this exists: git creates and removes lock files on nearly every write. In a
# mounted folder that refuses deletes, commits fail ("cannot lock ref") or leave a
# stale lock that breaks the next one. This script does the git work in a fresh
# temporary copy of .git outside the mount (where deletes work), with the brain
# folder as the work tree, then pushes. The mounted .git is never written.
#
# When git runs directly in the folder (no sandbox mount), ordinary
# git add / commit / push is simpler. See CLAUDE.md.
#
# Run only when the owner asks for a sync:
#     bash scripts/git-sync.sh "<action>: <description>"
#
# Needs: a remote named origin, and user.name / user.email set in the repo's
# config (git config user.name "..."), which the copy carries with it.
set -euo pipefail

MSG="${1:?commit message required, for example \"ingest: onboarding notes\"}"
BRANCH="${BRANCH:-main}"

WT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -d "$WT/.git" ] || { echo "No .git folder in $WT. Set up git first." >&2; exit 2; }
git --git-dir="$WT/.git" remote get-url origin >/dev/null 2>&1 || {
  echo "This script needs a remote named origin: it commits in a temporary copy and keeps" >&2
  echo "nothing locally, so without a push the commit would be lost. Add one with" >&2
  echo "  git remote add origin <url>" >&2
  echo "or, for git without a remote, run git in the folder from a terminal outside the sandbox." >&2
  exit 2
}
mask() { sed -E 's#https://[^@/]*@#https://***@#g'; }

# A fresh temp folder per run. A fixed path can be left behind, owned by another
# sandbox user, and break every later run. The trap removes it on exit.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
GD="$TMP/git"

echo "brain:    $WT"
echo "git-dir:  $GD (outside the mount)"

cp -a "$WT/.git" "$GD"
find "$GD" -name '*.lock' -delete 2>/dev/null || true

GIT=(git --git-dir="$GD" --work-tree="$WT")

if [ -z "$("${GIT[@]}" config user.name || true)" ] || [ -z "$("${GIT[@]}" config user.email || true)" ]; then
  echo "Set user.name and user.email in this repo first:" >&2
  echo "  git config user.name \"Your Name\"; git config user.email \"you@example.com\"" >&2
  exit 2
fi

# Reconcile with the remote BEFORE committing. The mounted .git never advances
# past pushes made from a copy, so its base is stale. The folder holds the
# current content, so resetting HEAD and the index to the remote branch (work
# tree untouched) and then staging gives exactly the new changes, as a clean
# fast-forward.
set +e
"${GIT[@]}" fetch --quiet origin 2>&1 | mask
rc=${PIPESTATUS[0]}
set -e
[ "$rc" -eq 0 ] || { echo "FETCH FAILED (see the message above). Check the remote URL and access." >&2; exit 4; }
if "${GIT[@]}" rev-parse --verify --quiet "origin/$BRANCH" >/dev/null; then
  "${GIT[@]}" reset --mixed --quiet "origin/$BRANCH"
fi

"${GIT[@]}" add -A
if "${GIT[@]}" diff --cached --quiet; then
  echo "Nothing to commit. The folder matches origin/$BRANCH."
  exit 0
fi
"${GIT[@]}" commit --quiet -m "$MSG"

# Mask any token embedded in the remote URL before it reaches the screen.
set +e
OUTPUT="$("${GIT[@]}" push --quiet origin "HEAD:$BRANCH" 2>&1)"
rc=$?
set -e
[ -z "$OUTPUT" ] || printf '%s\n' "$OUTPUT" | mask
if [ "$rc" -ne 0 ]; then
  if printf '%s' "$OUTPUT" | grep -qiE 'rejected|non-fast-forward|fetch first'; then
    echo "PUSH REJECTED: origin/$BRANCH moved during the sync. Run it again. Nothing was forced."
    exit 3
  fi
  echo "PUSH FAILED (see the message above). Often access: check the token or credentials." >&2
  exit 4
fi

echo "OK. origin/$BRANCH is now at:"
"${GIT[@]}" log --oneline -1
