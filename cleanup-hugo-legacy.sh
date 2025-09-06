#!/bin/bash

echo "🧹 Cleaning up Hugo legacy files and configurations..."

# Remove Hugo configuration files
echo "Removing Hugo configurations..."
rm -f config.toml hugo.toml config.toml.backup-*

# Remove Netlify configuration (conflicts with GitHub Pages)
echo "Removing Netlify configuration..."
rm -f netlify.toml

# Remove Hugo-specific directories (but preserve content for reference)
echo "Backing up and removing Hugo directories..."
if [ -d "content" ]; then
    if [ ! -d "content_backup_$(date +%Y%m%d)" ]; then
        cp -r content content_backup_$(date +%Y%m%d)_hugo_cleanup
    fi
    rm -rf content
fi

# Remove Hugo themes
echo "Removing Hugo themes directory..."
rm -rf themes

# Remove Hugo layouts
echo "Removing Hugo layouts directory..."
rm -rf layouts layouts-custom-backup layouts.bak

# Remove Hugo-specific static assets that might conflict
echo "Checking for Hugo-specific assets..."
if [ -d "static" ]; then
    mv static static_hugo_backup_$(date +%Y%m%d)
fi

# Clean up PowerShell scripts that might be Hugo-specific
echo "Cleaning up legacy PowerShell scripts..."
rm -f *.ps1

# Clean up other Hugo artifacts
rm -f go.mod
rm -f public -rf
rm -f resources -rf

echo "✅ Cleanup complete!"
echo ""
echo "📋 Summary of actions:"
echo "- Removed Hugo configuration files (config.toml, hugo.toml)"
echo "- Removed Netlify configuration (netlify.toml)"
echo "- Backed up and removed Hugo content directory"
echo "- Removed Hugo themes and layouts"
echo "- Cleaned up PowerShell deployment scripts"
echo "- Removed Hugo module files"
echo ""
echo "🚀 Site is now clean for Jekyll-only operation"