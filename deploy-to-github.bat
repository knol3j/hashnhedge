@echo off
echo Setting up GitHub remote and pushing...

cd C:\Users\gnul\hashnhedge\site

REM Replace YOUR-GITHUB-USERNAME with your actual GitHub username
git branch -M main
git remote add origin https://github.com/knol3j/hashnhedge.git
git push -u origin main

echo.
echo Push complete! Now enable GitHub Pages in your repository settings.
pause