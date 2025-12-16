@echo off
REM Temporary helper for git filter-branch index-filter on Windows
git rm --cached --ignore-unmatch -- "B-Smart Career Navigator/SYSTEM_PROMPT.md" "secure/BSCN_SYSTEM_PROMPT.md"
exit /b 0
