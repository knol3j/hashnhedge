import os
import io
import re

def fix_file(filepath):
    """Fix nested quotes in YAML front matter"""
    try:
        with io.open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Check if the file has YAML front matter
        if not content.startswith('---'):
            return False
            
        # Split into front matter and content
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False
            
        front_matter = parts[1]
        body = parts[2] if len(parts) > 2 else ""
        
        # Fix nested quotes in the title field
        lines = front_matter.split('\n')
        fixed_lines = []
        
        for line in lines:
            if line.startswith('title:'):
                # Extract the title value
                title_match = re.match(r'^title:\s*"(.+)"?\s*$', line)
                if title_match:
                    title_content = title_match.group(1)
                    # Remove trailing quote if exists
                    title_content = title_content.rstrip('"')
                    # Replace internal quotes with single quotes
                    title_content = title_content.replace('"', "'")
                    fixed_lines.append(f'title: "{title_content}"')
                else:
                    fixed_lines.append(line)
            elif 'title:' in line and 'seo:' not in line:
                # Handle SEO title fields
                fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        # Check if we need to fix the seo section
        in_seo = False
        final_lines = []
        for line in fixed_lines:
            if line.strip() == 'seo:':
                in_seo = True
                final_lines.append(line)
            elif in_seo and line.startswith('  title:'):
                # Fix SEO title
                seo_title_match = re.match(r'^  title:\s*"(.+)"?\s*$', line)
                if seo_title_match:
                    seo_title_content = seo_title_match.group(1)
                    seo_title_content = seo_title_content.rstrip('"')
                    seo_title_content = seo_title_content.replace('"', "'")
                    final_lines.append(f'  title: "{seo_title_content}"')
                else:
                    final_lines.append(line)
            elif in_seo and not line.startswith('  ') and line.strip():
                in_seo = False
                final_lines.append(line)
            else:
                final_lines.append(line)
        
        # Reconstruct the file
        fixed_content = '---' + '\n'.join(final_lines) + '---' + body
        
        # Write back
        with io.open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Fix files in briefs directory
    briefs_dir = 'content/briefs'
    count = 0
    
    for root, dirs, files in os.walk(briefs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if fix_file(filepath):
                    count += 1
                    print(f"Fixed: {filepath}")
    
    print(f"\nTotal files fixed: {count}")

if __name__ == "__main__":
    main()
