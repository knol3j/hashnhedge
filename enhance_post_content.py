#!/usr/bin/env python3
"""
Content Enhancement System - Oliver Perry Voice & 500+ Word Minimum
Transforms generic posts into Oliver Perry's distinctive editorial style
"""

import os
import re
import random
from datetime import datetime

POSTS_DIR = "site/content/posts"
BACKUP_DIR = "backup/original_posts"
MIN_WORDS = 500

class OliverPerryVoice:
    """Oliver Perry's distinctive editorial voice patterns"""
    
    def __init__(self):
        # Signature phrases and expressions
        self.signature_phrases = [
            "Christ almighty",
            "These beautiful bastards",
            "Here's the beautiful part",
            "Here's where it gets properly weird",
            "Here's what gets me harder than Chinese algebra",
            "The beautiful truth is",
            "And that's not nothing. That's everything.",
            "But here's the nihilistic optimism kicking in"
        ]
        
        self.profane_descriptors = [
            "beautiful bastards",
            "magnificent degenerates", 
            "these digital cowboys",
            "these crypto prophets",
            "beautiful madmen",
            "digital alchemists"
        ]
        
        self.analogies = [
            "like asking a tornado to please knock politely before it destroys your trailer park",
            "like Al Capone consulting on prohibition policy",
            "more confused than a Mormon in a strip club",
            "like watching Rome burn in high definition",
            "harder than Chinese algebra",
            "like mainlining pure capitalism mixed with algorithmic cocaine"
        ]
        
        self.financial_metaphors = [
            "this digital gold rush",
            "the weight of a goddamn dollar",
            "internet funny money",
            "Monopoly money",
            "the grand old whore of Wall Street",
            "bureaucratic musical chairs while Rome burns"
        ]
        
        self.existential_observations = [
            "It's like the universe is teaching us economics at the molecular level",
            "We're all just cells in this massive organism called civilization",
            "The revolution won't be televised because it's happening in spreadsheets",
            "We're not watching the end of the world—we're watching the world figure out how to be something new",
            "This is evolution in real time"
        ]

def analyze_oliver_perry_style():
    """Analyze key elements of Oliver Perry's voice"""
    return {
        'tone': 'nihilistic optimism with profane eloquence',
        'structure': 'punchy headlines, conversational flow, existential conclusions',
        'language': 'high-low mix: intellectual concepts with street language',
        'perspective': 'embedded journalist reporting from the future',
        'themes': 'crypto/finance as human evolution, bureaucratic chaos, molecular metaphors',
        'signature': 'profanity as punctuation, beautiful contradictions, systematic chaos'
    }

def count_words(text):
    """Count words in text, excluding frontmatter"""
    # Remove frontmatter
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = parts[2]
    
    # Remove markdown formatting
    text = re.sub(r'[#*_`\[\]()]', '', text)
    words = text.split()
    return len([word for word in words if word.strip()])

def extract_post_info(content):
    """Extract title, summary, and main content from post"""
    frontmatter_match = re.search(r'---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not frontmatter_match:
        return None, None, content
    
    frontmatter, body = frontmatter_match.groups()
    
    # Extract title
    title_match = re.search(r'title:\s*["\']([^"\']+)["\']', frontmatter)
    title = title_match.group(1) if title_match else "Untitled"
    
    # Extract summary/description
    summary_match = re.search(r'(?:summary|description):\s*["\']([^"\']+)["\']', frontmatter)
    summary = summary_match.group(1) if summary_match else ""
    
    return title, summary, body

def create_oliver_perry_intro(title, summary):
    """Create Oliver Perry style introduction"""
    voice = OliverPerryVoice()
    
    intros = [
        f"Christ almighty, I just dove headfirst into {title.lower()} and I feel like I've been {random.choice(['mainlining pure digital chaos', 'wrestling with algorithmic angels', 'drinking from the fountain of financial absurdity'])}. {random.choice(voice.profane_descriptors).title()} are {random.choice(['rewriting the rules of money itself', 'dancing on the grave of traditional finance', 'building tomorrow while today burns'])}.",
        
        f"Sweet merciful fuck, the {title.lower().replace('and', '').strip()} situation has me more wired than a {random.choice(['hedge fund manager on election night', 'day trader with insider information', 'central banker during a currency collapse'])}. These {random.choice(voice.profane_descriptors)} are {summary.lower() if summary else 'reshaping reality one transaction at a time'}.",
        
        f"Here's what gets me harder than Chinese algebra about {title.lower()}: {random.choice(voice.profane_descriptors)} have figured out how to {random.choice(['turn chaos into profit', 'make beautiful music from market mayhem', 'find zen in the space between greed and terror'])}. {summary if summary else 'And the implications are more profound than most people realize.'}",
        
        f"I just crawled through the {title.lower()} data and sweet Jesus, it's {random.choice(['beautiful and terrifying', 'chaos with perfect mathematical precision', 'like watching evolution happen in real time'])}. These {random.choice(voice.profane_descriptors)} aren't just {summary.lower() if summary else 'changing the game'}—they're {random.choice(['rewriting the entire fucking rulebook', 'building cathedrals out of code', 'turning digital dreams into analog reality'])}."
    ]
    
    return random.choice(intros)

def enhance_section_headers(content):
    """Transform boring headers into Oliver Perry style"""
    voice = OliverPerryVoice()
    
    header_transformations = {
        r'## Key Highlights': '## The Beautiful Chaos Unfolds',
        r'## Market Impact': '## The Weight of Digital Destiny', 
        r'## Analysis': '## The Nihilistic Optimism of It All',
        r'## Overview': '## The Grand Theater of Financial Evolution',
        r'## Conclusion': '## The Beautiful Truth',
        r'## Looking Forward': '## The Optimistic Apocalypse',
        r'## Expert Analysis': '## What the Digital Prophets Are Saying',
        r'## Technical Details': '## The Beautiful Mechanics of Chaos',
        r'## Market Trends': '## Reading the Tea Leaves of Tomorrow'
    }
    
    for old_header, new_header in header_transformations.items():
        content = re.sub(old_header, new_header, content, flags=re.IGNORECASE)
    
    return content

def add_oliver_perry_flavor(content, title):
    """Inject Oliver Perry voice throughout content"""
    voice = OliverPerryVoice()
    
    # Add signature phrases at strategic points
    paragraphs = content.split('\n\n')
    enhanced_paragraphs = []
    
    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip() and not paragraph.startswith('#'):
            # Add signature phrases to some paragraphs
            if i % 4 == 1 and len(paragraph) > 100:
                phrase = random.choice(voice.signature_phrases)
                paragraph = f"{phrase}, {paragraph[0].lower()}{paragraph[1:]}"
            
            # Add analogies occasionally
            elif i % 5 == 3 and len(paragraph) > 80:
                if '.' in paragraph:
                    parts = paragraph.split('.', 1)
                    if len(parts) == 2:
                        analogy = random.choice(voice.analogies)
                        paragraph = f"{parts[0]}—{analogy}. {parts[1]}"
            
            # Replace generic terms with Oliver Perry language
            replacements = {
                r'\bcompanies\b': random.choice(['these magnificent degenerates', 'these beautiful bastards', 'these digital alchemists']),
                r'\btraders\b': 'digital cowboys',
                r'\binvestors\b': 'beautiful madmen',
                r'\bmarket participants\b': 'financial prophets',
                r'\bthe cryptocurrency market\b': 'this digital gold rush',
                r'\btraditional finance\b': 'the grand old whore of Wall Street',
                r'\bregulators\b': 'bureaucratic shepherds',
                r'\bthis development\b': 'this beautiful chaos',
                r'\bsignificant\b': 'profound',
                r'\bimportant\b': 'crucial as a heartbeat',
                r'\binteresting\b': 'gorgeous in its implications'
            }
            
            for pattern, replacement in replacements.items():
                if random.random() < 0.3:  # Don't replace everything
                    paragraph = re.sub(pattern, replacement, paragraph, flags=re.IGNORECASE)
        
        enhanced_paragraphs.append(paragraph)
    
    return '\n\n'.join(enhanced_paragraphs)

def add_existential_conclusion(content, title):
    """Add Oliver Perry's signature existential conclusion"""
    voice = OliverPerryVoice()
    
    conclusions = [
        f"\n\n## The Beautiful Truth\n\nHere's what gets me about {title.lower()}: none of this is chaos. This is evolution in real time. {random.choice(voice.profane_descriptors).title()} aren't just changing the game—they're proving that maybe, just maybe, we're all learning to dance with forces bigger than any government, any corporation, any traditional understanding of value itself.\n\nThe nihilistic optimism isn't in believing this will save us. It's in recognizing that we're saving ourselves, one transaction and smart contract at a time. We're not watching the end of the world—we're watching the world figure out how to be something new.\n\nAnd that's not nothing. That's everything.",
        
        f"\n\n## The Optimistic Apocalypse\n\nThe beautiful truth about {title.lower()} is that it's all connected to something larger than spreadsheets and price charts. We're documenting the intersection where technology meets human nature, where greed transforms into something resembling wisdom, where chaos organizes itself into patterns that would make a mathematician weep.\n\n{random.choice(voice.existential_observations)} The revolution won't be televised because it's happening in code, in consensus algorithms, and in the space between traditional finance and whatever comes next.\n\nAnd somehow, that makes it more beautiful than any revolution that came before.",
        
        f"\n\n## The Weight of Digital Destiny\n\nThis {title.lower()} story isn't just news—it's a field report from humanity's next phase. {random.choice(voice.profane_descriptors).title()} are writing the future in real time, and what they're really proving is that maybe we're all just cells in this massive organism called civilization, learning when to grow and when to consolidate.\n\nThe nihilistic optimism kicks in when you realize this isn't about getting rich quick or disrupting for disruption's sake. This is about humanity figuring out new ways to organize value, trust, and power. And that's not just beautiful—that's essential.\n\nWe're not watching chaos. We're watching order emerge from complexity, and that's the most hopeful thing I've seen in decades."
    ]
    
    return content + random.choice(conclusions)

def expand_content_to_minimum(content, title, current_word_count):
    """Expand content to meet 500+ word minimum while maintaining voice"""
    if current_word_count >= MIN_WORDS:
        return content
    
    voice = OliverPerryVoice()
    words_needed = MIN_WORDS - current_word_count + 50  # Buffer
    
    # Add substantial analysis sections
    expansions = [
        f"\n\n## The Deeper Implications\n\nBut here's where it gets properly weird and beautiful: {title.lower()} isn't happening in isolation. This is part of a larger transformation where {random.choice(['traditional financial structures are learning to dance with digital reality', 'bureaucratic systems are evolving or dying', 'human behavior is adapting to algorithmic environments'])}.\n\nThe {random.choice(voice.profane_descriptors)} driving this change understand something that most analysts miss: {random.choice(['we are all just participants in a massive economic experiment', 'the old rules are suggestions and the new rules are being written in real time', 'every transaction is a vote for the kind of future we want to build'])}. {random.choice(voice.analogies).capitalize()}.\n\nWhat makes this particularly gorgeous is how {title.lower()} demonstrates the intersection of {random.choice(['technology and human psychology', 'greed and innovation', 'chaos and mathematical precision'])}. We are watching {random.choice(['evolution happen in spreadsheets', 'the future negotiate with the present', 'humanity teach itself new ways to organize trust'])}.",
        
        f"\n\n## The Human Element\n\nHere's what gets me harder than Chinese algebra: behind every data point in {title.lower()} are real people making decisions that will echo through generations. These aren't just numbers—they're {random.choice(['votes of confidence in a digital future', 'bets on human adaptability', 'prayers disguised as transactions'])}.\n\nThe beautiful bastards participating in this transformation are writing economic poetry with their wallets. Every purchase, every trade, every smart contract execution is a line in the collective narrative of how civilization learns to organize itself around new definitions of value and trust.\n\n{random.choice(voice.existential_observations)} The participants in {title.lower()} are proving that maybe, just maybe, we can teach old systems new tricks without burning everything down. Though admittedly, a little controlled burning never hurt anybody.\n\nThis isn't just about the technology—it's about human beings figuring out how to be human beings in an environment where the rules are being written in real time.",
        
        f"\n\n## The Systemic Beauty\n\nThe nihilistic optimism of {title.lower()} becomes clear when you realize this is all part of a larger pattern. {random.choice(voice.profane_descriptors).title()} aren't just {random.choice(['disrupting for the sake of disruption', 'chasing profits in digital gold rushes', 'playing with technological toys'])}—they're {random.choice(['solving fundamental problems about trust and value', 'building infrastructure for post-scarcity economics', 'creating systems that work even when humans behave badly'])}.\n\nWhat makes this particularly beautiful is how {title.lower()} demonstrates that {random.choice(['chaos and order are not opposites but dance partners', 'individual greed can aggregate into collective benefit', 'mathematical precision can emerge from human messiness'])}. {random.choice(voice.analogies).capitalize()}.\n\nThe profound implications extend beyond immediate market effects to fundamental questions about how humans organize themselves. We are witnessing {random.choice(['the birth of post-traditional economics', 'evolution happening in smart contracts', 'the intersection where technology meets enlightenment'])}."
    ]
    
    # Add expansions until we hit word count
    expanded_content = content
    for expansion in expansions:
        if count_words(expanded_content) >= MIN_WORDS:
            break
        expanded_content += expansion
    
    return expanded_content

def enhance_post_content(filepath):
    """Transform a post into Oliver Perry's voice with 500+ words"""
    try:
        # Read original content
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            original_content = f.read()
        
        # Extract post information
        title, summary, body = extract_post_info(original_content)
        if not title:
            print(f"Could not extract title from {filepath}")
            return False
        
        # Check current word count
        current_words = count_words(body)
        
        print(f"Processing: {title}")
        print(f"Current word count: {current_words}")
        
        # Create enhanced content
        enhanced_body = body
        
        # Add Oliver Perry intro if content is too short
        if current_words < 300:
            intro = create_oliver_perry_intro(title, summary)
            enhanced_body = f"{intro}\n\n{enhanced_body}"
        
        # Enhance section headers
        enhanced_body = enhance_section_headers(enhanced_body)
        
        # Add Oliver Perry voice throughout
        enhanced_body = add_oliver_perry_flavor(enhanced_body, title)
        
        # Expand to minimum word count
        enhanced_body = expand_content_to_minimum(enhanced_body, title, count_words(enhanced_body))
        
        # Add existential conclusion
        enhanced_body = add_existential_conclusion(enhanced_body, title)
        
        # Reconstruct full content with frontmatter
        if original_content.startswith('---'):
            parts = original_content.split('---', 2)
            if len(parts) >= 3:
                enhanced_content = f"---{parts[1]}---\n{enhanced_body}"
            else:
                enhanced_content = enhanced_body
        else:
            enhanced_content = enhanced_body
        
        # Backup original
        os.makedirs(BACKUP_DIR, exist_ok=True)
        backup_path = os.path.join(BACKUP_DIR, os.path.basename(filepath))
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # Write enhanced content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        
        final_words = count_words(enhanced_body)
        print(f"Enhanced word count: {final_words}")
        print(f"[ENHANCED] {os.path.basename(filepath)}")
        
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def process_all_posts():
    """Process all posts to Oliver Perry voice and 500+ words"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    processed = 0
    enhanced = 0
    
    for filename in sorted(os.listdir(POSTS_DIR)):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            
            if enhance_post_content(filepath):
                enhanced += 1
            processed += 1
    
    print(f"\nProcessing complete!")
    print(f"Posts processed: {processed}")
    print(f"Posts enhanced: {enhanced}")
    print(f"Originals backed up to: {BACKUP_DIR}")

if __name__ == "__main__":
    print("Oliver Perry Voice Enhancement System")
    print("=" * 50)
    print("Converting posts to Oliver Perry's distinctive voice")
    print("Minimum 500 words per post")
    print(f"Originals will be backed up to: {BACKUP_DIR}")
    print()
    
    confirmation = input("Proceed with enhancement? (y/n): ")
    if confirmation.lower() == 'y':
        process_all_posts()
    else:
        print("Enhancement cancelled.")