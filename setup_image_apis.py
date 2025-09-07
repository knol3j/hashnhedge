#!/usr/bin/env python3
"""
Setup script for configuring image API keys
"""

import os
import sys

def setup_unsplash_api():
    """Setup Unsplash API access"""
    print("=== Unsplash API Setup ===")
    print("1. Go to https://unsplash.com/developers")
    print("2. Create a developer account")
    print("3. Create a new application")
    print("4. Copy your Access Key")
    print()
    
    access_key = input("Enter your Unsplash Access Key (or press Enter to skip): ").strip()
    if access_key:
        return access_key
    return None

def setup_pexels_api():
    """Setup Pexels API access"""
    print("\n=== Pexels API Setup ===")
    print("1. Go to https://www.pexels.com/api/")
    print("2. Create a free account")
    print("3. Generate an API key")
    print("4. Copy your API key")
    print()
    
    api_key = input("Enter your Pexels API Key (or press Enter to skip): ").strip()
    if api_key:
        return api_key
    return None

def create_env_file(unsplash_key, pexels_key):
    """Create .env file with API keys"""
    env_content = []
    
    if unsplash_key:
        env_content.append(f"UNSPLASH_ACCESS_KEY={unsplash_key}")
    
    if pexels_key:
        env_content.append(f"PEXELS_API_KEY={pexels_key}")
    
    if env_content:
        with open('.env', 'w') as f:
            f.write('\n'.join(env_content) + '\n')
        print(f"✓ Created .env file with {len(env_content)} API key(s)")
        return True
    
    return False

def install_requirements():
    """Install required packages"""
    required_packages = [
        'requests',
        'beautifulsoup4',
        'python-dotenv'
    ]
    
    print(f"\n=== Installing Required Packages ===")
    for package in required_packages:
        print(f"Installing {package}...")
        os.system(f"pip install {package}")
    
    print("✓ All packages installed")

def main():
    print("Hash & Hedge Image Scraping Setup")
    print("=" * 40)
    print()
    print("This script will help you configure API keys for image scraping.")
    print("You can use either Unsplash, Pexels, or both for better coverage.")
    print()
    
    # Install requirements
    install_choice = input("Install required Python packages? (y/n): ").lower().strip()
    if install_choice == 'y':
        install_requirements()
    
    # Setup API keys
    unsplash_key = setup_unsplash_api()
    pexels_key = setup_pexels_api()
    
    if unsplash_key or pexels_key:
        create_env_file(unsplash_key, pexels_key)
        print("\n✓ Setup complete!")
        print("\nNext steps:")
        print("1. Run: python scrape_and_generate_images.py")
        print("2. The script will download photos when possible")
        print("3. SVG images will be generated as fallbacks")
    else:
        print("\n⚠️  No API keys configured.")
        print("The script will work but only generate SVG images.")
        print("To get photos, run this setup again with API keys.")
    
    print(f"\n📁 Images will be saved to: {os.path.abspath('site/static/images/posts')}")

if __name__ == "__main__":
    main()