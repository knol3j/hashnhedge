#!/usr/bin/env python3
"""
Generate unique images for blog posts based on title text
Uses simple geometric patterns with different colors for each post
"""

import os
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random
import colorsys

def text_to_color(text):
    """Generate a consistent color from text using hash"""
    hash_obj = hashlib.md5(text.encode())
    hash_hex = hash_obj.hexdigest()
    
    # Extract values for hue (0-360), saturation (40-80%), lightness (30-70%)
    hue = int(hash_hex[:3], 16) % 360
    sat = 40 + (int(hash_hex[3:5], 16) % 40)
    light = 30 + (int(hash_hex[5:7], 16) % 40)
    
    # Convert HSL to RGB
    r, g, b = colorsys.hls_to_rgb(hue/360, light/100, sat/100)
    return (int(r*255), int(g*255), int(b*255))

def create_pattern_image(title, width=1200, height=630):
    """Create a unique pattern image based on title"""
    # Create base image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Get colors from title
    primary_color = text_to_color(title)
    secondary_color = text_to_color(title[::-1])  # Reverse for different color
    
    # Generate pattern based on hash
    hash_val = int(hashlib.md5(title.encode()).hexdigest()[:8], 16)
    pattern_type = hash_val % 5
    
    if pattern_type == 0:
        # Circles pattern
        for i in range(0, width + 100, 80):
            for j in range(0, height + 100, 80):
                size = 20 + (hash_val % 30)
                if (i + j) % 160 == 0:
                    draw.ellipse([i, j, i+size*2, j+size*2], fill=primary_color, outline=secondary_color, width=2)
                else:
                    draw.ellipse([i, j, i+size, j+size], fill=secondary_color, outline=primary_color, width=1)
    
    elif pattern_type == 1:
        # Lines pattern
        line_spacing = 20 + (hash_val % 20)
        for i in range(0, width + height, line_spacing):
            if i % (line_spacing * 2) == 0:
                draw.line([(0, i), (width, i)], fill=primary_color, width=3)
                draw.line([(i, 0), (i, height)], fill=secondary_color, width=2)
            else:
                draw.line([(0, i), (width, i)], fill=secondary_color, width=1)
    
    elif pattern_type == 2:
        # Squares pattern
        square_size = 40 + (hash_val % 40)
        for x in range(0, width, square_size):
            for y in range(0, height, square_size):
                if (x + y) % (square_size * 2) == 0:
                    draw.rectangle([x, y, x+square_size-2, y+square_size-2], fill=primary_color, outline=secondary_color)
                else:
                    draw.rectangle([x, y, x+square_size-2, y+square_size-2], outline=primary_color, width=2)
    
    elif pattern_type == 3:
        # Triangles pattern
        tri_size = 60 + (hash_val % 40)
        for x in range(0, width, tri_size):
            for y in range(0, height, tri_size):
                if (x + y) % (tri_size * 2) == 0:
                    points = [(x, y+tri_size), (x+tri_size/2, y), (x+tri_size, y+tri_size)]
                    draw.polygon(points, fill=primary_color, outline=secondary_color)
    
    else:
        # Gradient with shapes
        for y in range(height):
            ratio = y / height
            r = int(primary_color[0] * (1-ratio) + secondary_color[0] * ratio)
            g = int(primary_color[1] * (1-ratio) + secondary_color[1] * ratio)
            b = int(primary_color[2] * (1-ratio) + secondary_color[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add some circles
        for _ in range(15):
            x = random.Random(hash_val).randint(0, width)
            y = random.Random(hash_val + 1).randint(0, height)
            size = random.Random(hash_val + 2).randint(20, 100)
            draw.ellipse([x, y, x+size, y+size], fill=None, outline='white', width=3)
    
    # Add semi-transparent overlay for text area
    overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([(width//4, height//3), (3*width//4, 2*height//3)], 
                          fill=(255, 255, 255, 180))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Add title text
    try:
        # Try to use a nice font if available
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        # Fall back to default font
        font = ImageFont.load_default()
    
    # Wrap text if too long
    max_width = width // 2
    words = title.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw text lines
    y_text = height // 2 - (len(lines) * 40) // 2
    for line in lines[:3]:  # Max 3 lines
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_text = (width - text_width) // 2
        
        # Draw text shadow
        draw.text((x_text+2, y_text+2), line, fill=(50, 50, 50), font=font)
        # Draw main text
        draw.text((x_text, y_text), line, fill=primary_color, font=font)
        y_text += 45
    
    return img

def process_content_files(content_dir, output_dir):
    """Process all content files and generate images"""
    content_path = Path(content_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    processed = 0
    errors = []
    
    # Process all markdown files
    for md_file in content_path.rglob("*.md"):
        try:
            # Read the file to get the title
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            title = None
            for line in lines[:10]:  # Check first 10 lines for title
                if line.startswith('title:'):
                    title = line.replace('title:', '').strip().strip('"').strip("'")
                    break
            
            if not title:
                title = md_file.stem.replace('-', ' ').replace('_', ' ').title()
            
            # Generate image filename from the markdown filename
            image_name = md_file.stem + '.jpg'
            relative_path = md_file.parent.relative_to(content_path)
            
            # Create output directory structure
            img_output_dir = output_path / 'generated' / relative_path
            img_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate and save image
            img = create_pattern_image(title)
            img_path = img_output_dir / image_name
            img.save(img_path, 'JPEG', quality=85, optimize=True)
            
            print(f"✓ Generated image for: {title[:50]}...")
            processed += 1
            
            # Update the markdown file to use the generated image
            updated_lines = []
            image_updated = False
            for i, line in enumerate(lines):
                if line.startswith('image:') and not image_updated:
                    # Update image path
                    new_image_path = f'/images/generated/{relative_path.as_posix()}/{image_name}'
                    updated_lines.append(f'image: "{new_image_path}"\n')
                    image_updated = True
                elif '\rimage:' in line:
                    # Fix the carriage return issue
                    parts = line.split('\r')
                    new_image_path = f'/images/generated/{relative_path.as_posix()}/{image_name}'
                    updated_lines.append(parts[0] + '\n')
                    updated_lines.append(f'image: "{new_image_path}"\n')
                    image_updated = True
                else:
                    updated_lines.append(line)
            
            # Write back the updated content
            with open(md_file, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
                
        except Exception as e:
            errors.append(f"Error processing {md_file}: {str(e)}")
            print(f"✗ Error processing {md_file.name}: {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"Processed {processed} files")
    if errors:
        print(f"Errors: {len(errors)}")
        for error in errors[:5]:
            print(f"  - {error}")
    
    return processed, errors

if __name__ == "__main__":
    # Set paths
    content_dir = r"C:\Users\gnul\hashnhedge\content"
    output_dir = r"C:\Users\gnul\hashnhedge\static\images"
    
    print("Starting image generation for content files...")
    print(f"Content directory: {content_dir}")
    print(f"Output directory: {output_dir}")
    print("="*50)
    
    processed, errors = process_content_files(content_dir, output_dir)
    
    print(f"\nImage generation complete!")
    print(f"Total files processed: {processed}")
    if errors:
        print(f"Total errors: {len(errors)}")
