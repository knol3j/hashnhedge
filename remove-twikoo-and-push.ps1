# Remove Twikoo and recommit
cd C:\Users\gnul\hashnhedge

# Remove the problematic Twikoo file from git
git rm -r site/themes/seven/assets/js/third-party/twikoo

# Commit the removal
git commit -m "Remove unused Twikoo comment system to resolve push protection issue"

# Push to GitHub
git push origin main

Write-Host "Twikoo removed and pushed successfully!" -ForegroundColor Green
Write-Host "Check deployment at: https://github.com/knol3j/hashnhedge/actions" -ForegroundColor Yellow
