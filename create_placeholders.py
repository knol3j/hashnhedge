import os
from pathlib import Path

# Simpler approach - create SVG placeholders
def create_svg_placeholder(title, width=1200, height=630):
    """Create simple SVG placeholder"""
    return f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" fill="#2c3e50"/>
  <text x="50%" y="30%" font-family="Arial, sans-serif" font-size="48" fill="white" text-anchor="middle">Hash & Hedge</text>
  <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="36" fill="white" text-anchor="middle">{title}</text>
</svg>"""

site_path = Path(r"C:\Users\gnul\hashnhedge\site")
images_path = site_path / "static" / "images" / "posts"
images_path.mkdir(parents=True, exist_ok=True)

# Create placeholder SVGs
placeholders = [
    ("Bitcoin Breaks $100K", "bitcoin-100k.svg"),
    ("Bitcoin Resistance", "bitcoin-breaks-resistance.svg"),
]

for title, filename in placeholders:
    svg_content = create_svg_placeholder(title)
    with open(images_path / filename, 'w') as f:
        f.write(svg_content)
    print(f"Created: {filename}")

print("SVG placeholders created!")