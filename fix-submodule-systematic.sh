#!/bin/bash
# Comprehensive Submodule Reconfiguration Script
# Systematic Resolution of GitHub Actions Build Failures

echo "🔧 Hash & Hedge Infrastructure Remediation"
echo "Systematic Submodule Reconfiguration Process"
echo "=============================================="

# Phase 1: Current State Analysis
echo "📊 Phase 1: Infrastructure Assessment"
echo "Analyzing current submodule configuration..."

if [ -f ".gitmodules" ]; then
    echo "✅ .gitmodules file exists"
    echo "Current configuration:"
    cat .gitmodules
else
    echo "❌ .gitmodules file missing"
    exit 1
fi

# Phase 2: Systematic Submodule Reset
echo ""
echo "🔄 Phase 2: Submodule Reset & Reconfiguration"

# Remove existing submodule configuration
echo "Removing existing submodule configuration..."
git submodule deinit -f site/themes/newsroom 2>/dev/null || true
git rm -f site/themes/newsroom 2>/dev/null || true

# Clean any remaining references
rm -rf site/themes/newsroom
rm -rf .git/modules/site/themes/newsroom

# Phase 3: Fresh Submodule Addition
echo ""
echo "➕ Phase 3: Fresh Submodule Installation"
git submodule add https://github.com/onweru/newsroom.git site/themes/newsroom

# Phase 4: Validation & Initialization
echo ""
echo "✅ Phase 4: Validation & Testing"
git submodule update --init --recursive

# Verify theme installation
if [ -f "site/themes/newsroom/theme.toml" ]; then
    echo "✅ Theme successfully installed and configured"
    echo "Theme details:"
    head -10 site/themes/newsroom/theme.toml
else
    echo "❌ Theme installation validation failed"
    exit 1
fi

# Phase 5: Local Build Validation
echo ""
echo "🏗️ Phase 5: Local Build Testing"
cd site
hugo --gc --minify -D
BUILD_STATUS=$?

if [ $BUILD_STATUS -eq 0 ]; then
    echo "✅ Local build successful - ready for deployment"
else
    echo "❌ Local build failed - requires additional troubleshooting"
    exit 1
fi

cd ..

# Phase 6: Commit Changes
echo ""
echo "💾 Phase 6: Committing Infrastructure Improvements"
git add .
git commit -m "fix: systematic submodule reconfiguration and infrastructure optimization

- Reconfigured newsroom theme submodule for reliable CI/CD
- Enhanced GitHub Actions workflow with recursive submodule support
- Validated local build process and theme integration
- Implemented comprehensive AdSense and SEO infrastructure
- Established automated content generation pipeline"

echo ""
echo "🚀 Infrastructure remediation complete!"
echo "Next steps:"
echo "1. git push origin main"
echo "2. Monitor GitHub Actions deployment"
echo "3. Verify site functionality at hashnhedge.com"
echo "4. Activate content generation pipeline"
