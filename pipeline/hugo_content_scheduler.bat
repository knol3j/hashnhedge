@echo off
REM Hugo Content Generation Scheduler
REM Runs 3 times daily to generate fresh content

cd /d C:\Users\gnul\hashnhedge

echo [%date% %time%] Starting content generation... >> logs\scheduler.log

REM Generate new content
echo Generating new posts...
python pipeline\generate_hugo_content.py

REM Fetch images for new posts
echo Fetching images...
python pipeline\fetch_images.py

REM Build the site
echo Building Hugo site...
cd site
hugo --gc --minify
cd ..

REM Optional: Auto-deploy
REM git add -A
REM git commit -m "Auto: Content update %date% %time%"
REM git push origin main

echo [%date% %time%] Content generation complete >> logs\scheduler.log
