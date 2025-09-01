# Hash & Hedge Comprehensive Site Fix and Content Management Script
# Purpose: Fix all issues, add images, create new content, and deploy

Write-Host "Starting Hash & Hedge Comprehensive Site Fix..." -ForegroundColor Cyan

# 1. First, ensure all posts have unique images
Write-Host "`n1. Checking and fetching images for all posts..." -ForegroundColor Yellow

# Get all markdown files in posts directory
$posts = Get-ChildItem -Path ".\content\posts" -Filter "*.md" -Recurse
$briefs = Get-ChildItem -Path ".\content\briefs" -Filter "*.md" -Recurse

Write-Host "Found $($posts.Count) posts and $($briefs.Count) briefs to process"

# Function to extract frontmatter from markdown
function Get-FrontMatter {
    param($filePath)
    $content = Get-Content $filePath -Raw
    if ($content -match '(?s)^---\s*\n(.*?)\n---') {
        return $matches[1]
    }
    return $null
}

# Function to update frontmatter with image
function Update-PostImage {
    param($filePath, $imagePath)
    $content = Get-Content $filePath -Raw
    $fileName = [System.IO.Path]::GetFileNameWithoutExtension($filePath)
    
    # Check if image field exists
    if ($content -match 'image:\s*".*?"') {
        # Update existing image field
        $content = $content -replace 'image:\s*".*?"', "image: `"$imagePath`""
    } elseif ($content -match '(?s)^---\s*\n(.*?)\n---') {
        # Add image field to frontmatter
        $frontmatter = $matches[1]
        $newFrontmatter = $frontmatter + "`nimage: `"$imagePath`""
        $content = $content -replace '(?s)^---\s*\n.*?\n---', "---`n$newFrontmatter`n---"
    }
    
    Set-Content -Path $filePath -Value $content -Encoding UTF8
}

# Process each post to ensure it has an image
foreach ($post in $posts) {
    $frontmatter = Get-FrontMatter $post.FullName
    $fileName = [System.IO.Path]::GetFileNameWithoutExtension($post.Name)
    
    # Check if post has an image
    if ($frontmatter -notmatch 'image:') {
        Write-Host "  Adding image for: $($post.Name)" -ForegroundColor Gray
        $imagePath = "/images/generated/posts/$fileName.jpg"
        Update-PostImage $post.FullName $imagePath
    }
}

# Process briefs
foreach ($brief in $briefs) {
    $frontmatter = Get-FrontMatter $brief.FullName
    $fileName = [System.IO.Path]::GetFileNameWithoutExtension($brief.Name)
    
    if ($frontmatter -notmatch 'image:') {
        Write-Host "  Adding image for brief: $($brief.Name)" -ForegroundColor Gray
        $imagePath = "/images/generated/briefs/$fileName.jpg"
        Update-PostImage $brief.FullName $imagePath
    }
}

Write-Host "`n2. Generating images for posts without them..." -ForegroundColor Yellow

# Create image generation script
$imageGenScript = @'
import os
import hashlib
from PIL import Image, ImageDraw, ImageFont
import random

def generate_unique_image(title, output_path):
    """Generate a unique image based on title"""
    # Create unique color based on title hash
    title_hash = hashlib.md5(title.encode()).hexdigest()
    
    # Generate colors from hash
    r = int(title_hash[:2], 16)
    g = int(title_hash[2:4], 16)
    b = int(title_hash[4:6], 16)
    
    # Create gradient background
    width, height = 1200, 630
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Create gradient
    for y in range(height):
        intensity = int(255 * (1 - y / height))
        color = (
            min(255, r + intensity // 3),
            min(255, g + intensity // 3),
            min(255, b + intensity // 3)
        )
        draw.rectangle([(0, y), (width, y + 1)], fill=color)
    
    # Add geometric patterns
    pattern_seed = int(title_hash[6:8], 16)
    random.seed(pattern_seed)
    
    for _ in range(15):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(20, 100)
        opacity = random.randint(20, 60)
        
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        shape_color = (
            random.randint(200, 255),
            random.randint(200, 255),
            random.randint(200, 255),
            opacity
        )
        
        if random.choice([True, False]):
            overlay_draw.ellipse([x, y, x + size, y + size], fill=shape_color)
        else:
            overlay_draw.rectangle([x, y, x + size, y + size], fill=shape_color)
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Add title text
    draw = ImageDraw.Draw(img)
    
    # Try to use a better font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 48)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
        small_font = font
    
    # Add title with shadow
    title_lines = []
    words = title.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if len(test_line) > 40:
            if current_line:
                title_lines.append(current_line)
                current_line = word
            else:
                title_lines.append(test_line)
                current_line = ""
        else:
            current_line = test_line
    
    if current_line:
        title_lines.append(current_line)
    
    y_offset = height // 2 - (len(title_lines) * 60) // 2
    
    for line in title_lines:
        # Shadow
        draw.text((width // 2 + 2, y_offset + 2), line, fill=(0, 0, 0), font=font, anchor="mm")
        # Text
        draw.text((width // 2, y_offset), line, fill=(255, 255, 255), font=font, anchor="mm")
        y_offset += 60
    
    # Add branding
    draw.text((width // 2, height - 40), "Hash & Hedge", fill=(255, 255, 255), font=small_font, anchor="mm")
    
    # Save image
    img.save(output_path, quality=95, optimize=True)
    print(f"Generated: {output_path}")

# Generate images for all posts
posts_dir = r"C:\Users\gnul\hashnhedge\content\posts"
briefs_dir = r"C:\Users\gnul\hashnhedge\content\briefs"
images_dir = r"C:\Users\gnul\hashnhedge\static\images\generated"

# Create directories if they don't exist
os.makedirs(os.path.join(images_dir, "posts"), exist_ok=True)
os.makedirs(os.path.join(images_dir, "briefs"), exist_ok=True)

# Process posts
for root, dirs, files in os.walk(posts_dir):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(root, file)
            file_name = os.path.splitext(file)[0]
            image_path = os.path.join(images_dir, "posts", f"{file_name}.jpg")
            
            # Generate image if it doesn't exist
            if not os.path.exists(image_path):
                # Extract title from file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'title:' in content:
                        title_line = [line for line in content.split('\n') if line.startswith('title:')][0]
                        title = title_line.split('title:')[1].strip().strip('"')
                        generate_unique_image(title, image_path)

# Process briefs
if os.path.exists(briefs_dir):
    for root, dirs, files in os.walk(briefs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                file_name = os.path.splitext(file)[0]
                image_path = os.path.join(images_dir, "briefs", f"{file_name}.jpg")
                
                if not os.path.exists(image_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'title:' in content:
                            title_line = [line for line in content.split('\n') if line.startswith('title:')][0]
                            title = title_line.split('title:')[1].strip().strip('"')
                            generate_unique_image(title, image_path)

print("Image generation complete!")
'@

# Save and run Python script
$imageGenScript | Out-File -FilePath ".\generate_images.py" -Encoding UTF8

Write-Host "Running image generation script..."
python .\generate_images.py 2>$null

Write-Host "`n3. Creating Oliver Perry editorial content..." -ForegroundColor Yellow
