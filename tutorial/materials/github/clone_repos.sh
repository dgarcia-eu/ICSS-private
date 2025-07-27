#!/bin/bash

# Token and Feedback File
TOKEN=""
FEEDBACK_FILE="feedback_a01.txt"

if [ ! -f "$FEEDBACK_FILE" ]; then
  echo "Error: $FEEDBACK_FILE not found!"
  exit 1
fi

# Clone all Repos of the Organisation
curl -s -H "Authorization: token $TOKEN" \
"https://api.github.com/orgs/ICSS-Test/repos?per_page=100" \
| jq -r --arg token "$TOKEN" '.[] | "https://\($token)@github.com/" + .full_name + ".git"' \
| xargs -L1 git clone

# For all Repos:
# - git pull
# - insert empty feedback_a01.txt 
find . -mindepth 1 -maxdepth 1 -type d -exec bash -c '
  echo "Bearbeite Repository: $0"
  git -C "$0" pull
  cp "'"$FEEDBACK_FILE"'" "$0"/
' {} \;
