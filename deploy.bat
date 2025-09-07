@echo off
echo Building and deploying Hugo site to GitHub...
echo.

REM Navigate to site directory
cd site

REM Build the site
echo Building site...
hugo --gc --minify

REM Check if build was successful
if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo Build successful!
echo.

REM Go back to root
cd ..

REM Add, commit and push changes
echo Pushing to GitHub...
git add -A
git commit -m "Update site content"
git push origin main

echo.
echo Deployment complete! 
echo GitHub Actions will now build and deploy your site.
echo Check the Actions tab on GitHub to monitor the deployment.
pause