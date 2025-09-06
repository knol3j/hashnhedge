from pathlib import Path

def create_svg_placeholder(title, subtitle="", width=1200, height=630):
    """Create SVG placeholder with gradient background"""
    return f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#grad1)"/>
  <text x="50%" y="25%" font-family="Arial, sans-serif" font-size="54" font-weight="bold" fill="white" text-anchor="middle">Hash & Hedge</text>
  <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="42" fill="white" text-anchor="middle">{title}</text>
  <text x="50%" y="65%" font-family="Arial, sans-serif" font-size="24" fill="white" opacity="0.9" text-anchor="middle">{subtitle}</text>
</svg>"""

site_path = Path(r"C:\Users\gnul\hashnhedge\site")
images_path = site_path / "static" / "images" / "posts"
images_path.mkdir(parents=True, exist_ok=True)

# Create comprehensive set of placeholder images
posts = [
    ("Ethereum L2 Scaling", "Complete Guide 2025", "ethereum-l2-scaling.svg"),
    ("DeFi Yield Farming", "180B Opportunity", "defi-yield-farming-2025.svg"),
    ("Crypto Security", "Protect Your Assets", "crypto-security-guide.svg"),
    ("NFT Market Analysis", "2025 Trends", "nft-market-2025.svg"),
    ("Stablecoin Wars", "USDC vs USDT", "stablecoin-analysis.svg"),
    ("Web3 Gaming", "Play to Earn", "web3-gaming-revolution.svg"),
    ("AI Crypto Tokens", "Next Big Thing", "ai-crypto-tokens.svg"),
    ("Meme Coins", "Risk & Reward", "meme-coins-guide.svg"),
]

for title, subtitle, filename in posts:
    svg_content = create_svg_placeholder(title, subtitle)
    with open(images_path / filename, 'w') as f:
        f.write(svg_content)
    print(f"Created: {filename}")

# Also create default images
defaults = [
    ("Hash & Hedge", "Crypto Intelligence", "default-hero.svg"),
    ("Hash & Hedge", "Smart Investing", "og-default.svg"),
]

for title, subtitle, filename in defaults:
    svg_content = create_svg_placeholder(title, subtitle)
    filepath = site_path / "static" / "images" / filename
    with open(filepath, 'w') as f:
        f.write(svg_content)
    print(f"Created default: {filename}")

print("All placeholder images created successfully!")