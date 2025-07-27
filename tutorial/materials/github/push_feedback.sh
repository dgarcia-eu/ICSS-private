#!/bin/bash

# Push all updated feedback_a01.txt files
find . -mindepth 1 -maxdepth 1 -type d -exec bash -c '
  echo "Push for: $0"
  git -C "$0" add feedback_a01.txt
  git -C "$0" commit -m "upload feedback"
  git -C "$0" push
' {} \;
