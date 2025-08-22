# Retry push after allowing the secret on GitHub
cd C:\Users\gnul\hashnhedge
git push origin main

Write-Host "Push complete! The GitHub Actions workflow should now deploy your site." -ForegroundColor Green
Write-Host "Check the deployment status at: https://github.com/knol3j/hashnhedge/actions" -ForegroundColor Yellow
Write-Host "Your site will be live at: https://hashnhedge.com" -ForegroundColor Cyan
