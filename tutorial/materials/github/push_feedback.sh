#!/bin/bash
set -euo pipefail

TOKEN=""
ORG="ICSS-2025"
FEEDBACK_FILE="feedback_a01.txt"

find . -mindepth 1 -maxdepth 1 -type d -exec bash -c '
  set -euo pipefail

  repo="$1"
  TOKEN="$2"
  ORG="$3"
  FEEDBACK_FILE="$4"

  name=$(basename "$repo")
  origin="https://git:${TOKEN}@github.com/${ORG}/${name}.git"

  echo "=== $name ==="
  echo "Setze remote origin auf: $origin"
  git -C "$repo" remote set-url origin "$origin"

  echo "Pull for: $repo"
  git -C "$repo" pull

  if [ -f "$repo/$FEEDBACK_FILE" ]; then
    echo "Push for: $repo"
    git -C "$repo" add "$FEEDBACK_FILE"

    if git -C "$repo" diff --cached --quiet; then
      echo "No change in $repo"
    else
      git -C "$repo" commit -m "upload feedback"
      git -C "$repo" push
    fi
  else
    echo "Found no $FEEDBACK_FILE in $repo, skip"
  fi
' bash {} "$TOKEN" "$ORG" "$FEEDBACK_FILE" \;
