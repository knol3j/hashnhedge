@echo off
REM Hugo Content Scheduler - Automated content generation and deployment
REM Run this as a scheduled task at desired intervals

echo ============================================
echo Hash ^& Hedge Hugo Content Generator
echo Automated content pipeline running...
echo ============================================
echo.

REM Navigate to project directory
cd /d C:\Users\gnul\hashnhedge

REM Generate new post
echo [%date% %time%] Generating new content...
python pipeline\generate_hugo_posts.py --count 1 --site-path site

REM Fetch images for posts
echo [%date% %time%] Fetching images...
python pipeline\fetch_images_fixed.py

REM Build Hugo site
echo [%date% %time%] Building Hugo site...
cd site
hugo --gc --minify
cd ..

REM Git operations
echo [%date% %time%] Committing to GitHub...
git add -A
git commit -m "content: automated post - %date% %time%"
git push origin main

echo.
echo [%date% %time%] Done! Site will deploy via GitHub Actions.
echo ============================================