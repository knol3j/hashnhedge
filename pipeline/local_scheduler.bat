@echo off
REM Local Content Scheduler - Because trusting the cloud is like trusting a fart after Taco Bell
REM Run this as a scheduled task in Windows Task Scheduler at 9am, 12pm, and 5pm

echo ============================================
echo Hash ^& Hedge Local Content Generator
echo "Making content while you make excuses"
echo ============================================
echo.

REM Navigate to your project directory like we're lost in a digital maze
cd /d C:\Users\gnul\hashnhedge

REM Activate virtual environment if you're fancy like that
REM call venv\Scripts\activate

REM Generate one post because consistency is key to disappointing regularly
echo [%date% %time%] Generating content...
python pipeline\generate_posts.py --count 1 --site-path site

REM Fetch images because walls of text are so 1995
echo [%date% %time%] Stealing images from the internet...
python pipeline\fetch_images.py

REM Git operations - commit our sins to the repository
echo [%date% %time%] Pushing to GitHub...
git add -A
git commit -m "content: scheduled post - %date% %time%"
git push origin main

REM Trigger a manual rebuild if you're paranoid (you should be)
REM curl -X POST https://api.github.com/repos/knol3j/hashnhedge/dispatches ^
REM      -H "Authorization: token YOUR_GITHUB_TOKEN" ^
REM      -d "{\"event_type\": \"manual-build\"}"

echo.
echo [%date% %time%] Done. Another piece of content released into the void.
echo ============================================
pause