# Internal Linking Optimizer
$posts = Get-ChildItem -Path "content\posts" -Filter "*.md" -Recurse
$linkMap = @{}

# Build keyword map
foreach ($post in $posts) {
    $content = Get-Content $post.FullName -Raw
    if ($content -match "tags:\s*\[(.*?)\]") {
        $tags = $matches[1] -split "," | ForEach-Object { $_.Trim().Trim('"') }
        foreach ($tag in $tags) {
            if (!$linkMap.ContainsKey($tag)) {
                $linkMap[$tag] = @()
            }
            $linkMap[$tag] += $post.BaseName
        }
    }
}

# Add contextual internal links
foreach ($post in $posts) {
    $content = Get-Content $post.FullName -Raw
    $modified = $false
    
    foreach ($keyword in $linkMap.Keys) {
        if ($linkMap[$keyword].Count -gt 1) {
            # Find other posts with same keyword
            $relatedPosts = $linkMap[$keyword] | Where-Object { $_ -ne $post.BaseName } | Select-Object -First 3
            
            if ($relatedPosts -and $content -notmatch "## Related Articles") {
                $relatedSection = "`n`n## Related Articles`n`n"
                foreach ($related in $relatedPosts) {
                    $relatedSection += "- [Read more about $keyword](/posts/$related/)`n"
                }
                $content += $relatedSection
                $modified = $true
            }
        }
    }
    
    if ($modified) {
        Set-Content -Path $post.FullName -Value $content
    }
}
