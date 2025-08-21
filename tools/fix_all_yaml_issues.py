import os
import io
import re

def fix_yaml_frontmatter(content):
    """Fix common YAML issues in front matter"""
    if not content.startswith('---'):
        return content
    
    # Split into front matter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content
    
    front_matter = parts[1]
    body = parts[2] if len(parts) > 2 else ""
    
    lines = front_matter.split('\n')
    fixed_lines = []
    in_seo = False
    skip_next = False
    
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
            
        # Fix date fields with trailing quotes and control chars
        if line.strip().startswith('date:'):
            date_match = re.match(r'^(\s*date:\s*")([^"]+).*$', line)
            if date_match:
                indent = date_match.group(1)
                date_val = date_match.group(2).rstrip("'\\r\\n")
                fixed_lines.append(f'{indent}{date_val}"')
            else:
                fixed_lines.append(line)
                
        # Handle SEO section
        elif line.strip() == 'seo:':
            in_seo = True
            fixed_lines.append(line)
            
        # Fix keywords in SEO section
        elif in_seo and 'keywords:' in line:
            # Check if next lines are list items
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('-'):
                # Collect all keyword list items
                keywords = []
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith('-'):
                    keyword = lines[j].strip()[1:].strip().strip('"')
                    keywords.append(keyword)
                    j += 1
                # Write as proper list
                fixed_lines.append('  keywords:')
                for kw in keywords:
                    fixed_lines.append(f'    - "{kw}"')
                # Skip the lines we've processed
                for _ in range(j - i - 1):
                    if i + 1 < len(lines):
                        lines[i + 1] = '__SKIP__'
            else:
                # Handle inline keywords
                fixed_lines.append(line)
                
        elif line == '__SKIP__':
            continue
            
        elif in_seo and not line.startswith('  ') and line.strip():
            in_seo = False
            fixed_lines.append(line)
            
        else:
            fixed_lines.append(line)
    
    # Reconstruct the file
    fixed_content = '---' + '\n'.join(fixed_lines) + '---' + body
    
    # Remove any special characters that might cause issues
    fixed_content = fixed_content.replace('\x9d', '')
    fixed_content = fixed_content.replace('\x81', '')
    # Remove corrupted UTF-8 sequences
    fixed_content = re.sub(r'[\x80-\x9f]', '', fixed_content)
    
    return fixed_content

def fix_file(filepath):
    """Fix a single markdown file"""
    try:
        with io.open(filepath, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
        
        fixed_content = fix_yaml_frontmatter(content)
        
        if fixed_content != content:
            with io.open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Fix files in posts directory
    posts_dir = 'content/posts'
    count = 0
    
    for root, dirs, files in os.walk(posts_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if fix_file(filepath):
                    count += 1
                    print(f"Fixed: {filepath}")
    
    print(f"\nTotal files fixed: {count}")

if __name__ == "__main__":
    main()
