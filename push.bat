@echo off
chcp 65001 > nul
set "PATH=C:\Program Files\Git\cmd;%PATH%"

echo ========================================================
echo   [ThePathLab] 메인 포털 (chicstory.github.io) 배포기
echo   원격 저장소: https://github.com/chicstory/chicstory.github.io.git
echo ========================================================

cd /d "%~dp0"

if not exist ".git" (
    echo [1/4] Git 저장소 초기화 중...
    git init
    git branch -M main
    git remote add origin https://github.com/chicstory/chicstory.github.io.git
)

echo [2/4] 변경 사항 추적 및 스테이징...
git add index.html guide.html about.html contact.html privacy.html robots.txt sitemap.xml docs/

echo [3/4] 커밋 생성 중...
git commit -m "feat: ThePathLab Main Portal Hub & AdSense Essential Pages"

echo [4/4] GitHub로 푸시 중 (main 브랜치)...
git push -u origin main

echo.
echo ========================================================
echo   배포가 완료되었습니다!
echo   접속 주소: https://chicstory.github.io/
echo ========================================================
pause
