#!/bin/sh
# Temporary helper for git filter-branch index-filter in msys/git bash
git rm --cached --ignore-unmatch "B-Smart Career Navigator/SYSTEM_PROMPT.md" "secure/BSCN_SYSTEM_PROMPT.md" || true
exit 0
