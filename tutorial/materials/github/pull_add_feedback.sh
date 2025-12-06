#!/bin/bash

# Token and Feedback File
TOKEN=""
FEEDBACK_FILE="feedback_a02.txt"

# For all Repos:
# - git pull
find . -mindepth 1 -maxdepth 1 -type d -exec bash -c '
  echo "Bearbeite Repository: $0"
  git -C "$0" pull
  cp "'"$FEEDBACK_FILE"'" "$0"/
' {} \;
