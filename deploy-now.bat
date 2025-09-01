@echo off
echo Deploying Hash & Hedge to GitHub...
echo.

cd /d C:\Users\gnul\hashnhedge

echo Step 1: Adding all changes...
git add -A

echo Step 2: Committing changes...
git commit -m "feat: Complete monetization setup - AdSense, Analytics, SEO, and new high-value content"

echo Step 3: Pushing to GitHub (this will trigger auto-deployment)...
git push origin main

echo.
echo ✅ Deployment initiated! Your site will be live in 2-3 minutes.
echo.
echo Check deployment status at:
echo https://github.com/knol3j/hashnhedge/actions
echo.
pause