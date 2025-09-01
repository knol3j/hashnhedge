# PowerShell script to fix specific file issues
$file1 = "C:\Users\gnul\hashnhedge\site\content\posts\2025\08\crypto-scam-sites-make-up-a-fifth-of-asic-s-twoyear-takedown\index.md"

# Read and fix the first file
$content = Get-Content $file1 -Raw -Encoding UTF8

# Replace the problematic title line
$content = $content -replace 'title: "Crypto Scam Sites Make Up a Fifth of ASIC.*Two-Year Takedown"', 'title: "Crypto Scam Sites Make Up a Fifth of ASIC Two-Year Takedown"'
$content = $content -replace 'slug: "crypto scam sites make up a fifth of asic.*twoyear takedown"', 'slug: "crypto-scam-sites-make-up-a-fifth-of-asic-twoyear-takedown"'

# Save the file
Set-Content -Path $file1 -Value $content -Encoding UTF8 -NoNewline

Write-Host "Fixed the crypto scam file"
