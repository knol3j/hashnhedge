#!/usr/bin/env python3
"""Test script to verify MCP agent installation."""

import os
import sys
from pathlib import Path

def test_installation():
    """Test that all components are properly installed."""
    
    print("🔍 Testing HashNHedge Image Agent Installation...")
    print("-" * 50)
    
    # Check Python version
    print(f"✓ Python version: {sys.version}")
    
    # Check required packages
    required_packages = [
        'mcp', 'requests', 'httpx', 'PIL', 'frontmatter', 
        'yaml', 'dotenv', 'bs4', 'tenacity'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ Package '{package}' is installed")
        except ImportError:
            missing.append(package)
            print(f"✗ Package '{package}' is NOT installed")
    
    # Check directory structure
    base_dir = Path(__file__).parent
    required_dirs = [
        'image_agent', 'image_agent/utils', 'image_agent/sources',
        'scripts', 'logs', '.cache/downloads'
    ]
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"✓ Directory '{dir_name}' exists")
        else:
            print(f"✗ Directory '{dir_name}' is missing")
    
    # Check configuration files
    config_files = ['settings.yaml', '.env', 'manifest.json', 'README.md']
    for file_name in config_files:
        file_path = base_dir / file_name
        if file_path.exists():
            print(f"✓ Config file '{file_name}' exists")
        else:
            print(f"✗ Config file '{file_name}' is missing")
    
    # Check Hugo project
    hugo_root = Path(os.getenv('HASHNHEDGE_PROJECT_ROOT', 'C:\\Users\\gnul\\hashnhedge'))
    if hugo_root.exists():
        print(f"✓ Hugo project found at: {hugo_root}")
        
        # Check content directory
        content_dir = hugo_root / 'content'
        if content_dir.exists():
            md_files = list(content_dir.rglob('*.md'))
            print(f"✓ Found {len(md_files)} markdown files in content directory")
    else:
        print(f"✗ Hugo project not found at: {hugo_root}")
    
    print("-" * 50)
    
    if missing:
        print(f"⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: .venv\\Scripts\\pip install -r requirements.txt")
        return False
    else:
        print("✅ All components are properly installed!")
        print("\n📌 Next steps:")
        print("1. Add your API keys to the .env file")
        print("2. Restart Claude Desktop")
        print("3. Use the MCP tools in Claude:")
        print("   - scan_articles")
        print("   - search_images")
        print("   - download_image")
        print("   - batch_autofetch")
        return True

if __name__ == "__main__":
    success = test_installation()
    sys.exit(0 if success else 1)
