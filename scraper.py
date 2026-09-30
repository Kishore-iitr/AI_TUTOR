import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
from datetime import datetime

MASTER_URL = "https://www.geeksforgeeks.org/physics/cbse-class-10-science-notes/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def is_math_or_chemistry(text):
    # Heuristic to detect chemical equations or math
    # Looks for things like 2H2 + O2 -> 2H2O or basic math equations
    if re.search(r'\b[A-Z][a-z]?\d*(?:\s*\+\s*[A-Z][a-z]?\d*)+\s*(?:->||\=)\s*', text):
        return True
    if re.search(r'\$\$|\\\[|\\\(', text):
        return True
    return False

def parse_subtopic(url):
    print(f"    Scraping subtopic: {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"    Failed to fetch {url}: {e}")
        return []

    soup = BeautifulSoup(r.content, 'html.parser')
    article = soup.find('div', class_='text') or soup.find('article')
    
    if not article:
        return []
        
    # Preprocess Math elements before extraction
    for sup in article.find_all('sup'):
        sup.replace_with(f"^{sup.get_text()}")
    for sub in article.find_all('sub'):
        sub.replace_with(f"_{sub.get_text()}")
    for tex in article.find_all('gfg-tex'):
        tex.replace_with(f"$${tex.get_text(strip=True)}$$")

    content_elements = []

    for el in article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'table', 'img', 'pre', 'code']):
        # Skip elements that are inside tables, lists or pre tags (we process them when we hit the parent)
        parent_names = [p.name for p in el.parents]
        if el.name != 'table' and 'table' in parent_names: continue
        if el.name != 'ul' and el.name != 'ol' and ('ul' in parent_names or 'ol' in parent_names): continue
        if el.name != 'pre' and 'pre' in parent_names: continue
        
        # Handle paragraphs
        if el.name == 'p':
            text = el.get_text(separator=' ', strip=True)
            text = re.sub(r'\s+', ' ', text) # normalize spaces
            if not text:
                continue
            if is_math_or_chemistry(text) or '→' in text or '⇒' in text or '^' in text or '_' in text:
                # Wrap in $$ if not already
                if not text.startswith('$$'):
                    text = f"$${text}$$"
                content_elements.append({"type": "formula", "text": text})
            else:
                content_elements.append({"type": "paragraph", "text": text})
                
        # Handle headings
        elif el.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            text = el.get_text(separator=' ', strip=True)
            if text:
                level = int(el.name[1])
                content_elements.append({"type": "heading", "level": level, "text": text})
                
        # Handle lists
        elif el.name in ['ul', 'ol']:
            items = [li.get_text(separator=' ', strip=True) for li in el.find_all('li') if li.get_text(separator=' ', strip=True)]
            if items:
                content_elements.append({
                    "type": "list",
                    "list_type": "unordered" if el.name == 'ul' else "ordered",
                    "items": items
                })
                
        # Handle tables
        elif el.name == 'table':
            headers = []
            rows = []
            
            # Extract headers
            for th in el.find_all('th'):
                headers.append(th.get_text(strip=True))
                
            # Extract rows
            for tr in el.find_all('tr'):
                tds = tr.find_all('td')
                if tds:
                    rows.append([td.get_text(strip=True) for td in tds])
                    
            if not headers and rows:
                headers = rows[0]
                rows = rows[1:]
                
            if headers or rows:
                content_elements.append({
                    "type": "table",
                    "headers": headers,
                    "rows": rows
                })
                
        # Handle images
        elif el.name == 'img':
            src = el.get('src')
            alt = el.get('alt', '')
            if src:
                content_elements.append({
                    "type": "image",
                    "src": src,
                    "alt": alt
                })
                
        # Handle pre/code blocks which might be formulas
        elif el.name == 'pre' or el.name == 'code':
            text = el.get_text(strip=True)
            if text:
                if is_math_or_chemistry(text):
                    if not text.startswith('$$'):
                        text = f"$${text}$$"
                    content_elements.append({"type": "formula", "text": text})
                else:
                    content_elements.append({"type": "paragraph", "text": text})

    return content_elements

def scrape_notes(subset_only=True):
    print("Fetching master index...")
    r = requests.get(MASTER_URL, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'html.parser')
    article = soup.find('div', class_='text') or soup.find('article')

    dataset = {
        "book_metadata": {
            "source_master_url": MASTER_URL,
            "board": "CBSE",
            "class": "Class 10",
            "subject": "Science",
            "scraped_at": datetime.now().strftime("%Y-%m-%d")
        },
        "chapters": []
    }

    current_chapter_title = None
    current_chapter_num = 0

    for el in article.find_all(['h2', 'h3', 'ul']):
        if el.name in ['h2', 'h3']:
            title = el.get_text(strip=True)
            match = re.search(r'Chapter\s*(\d+)', title)
            if match and 'Class 10 Science Notes' in title:
                current_chapter_num = int(match.group(1))
                current_chapter_title = title.split(f"Chapter {current_chapter_num}")[-1].strip(": ")

                print(f"\nProcessing Chapter {current_chapter_num}: {current_chapter_title}")
                
                # If subset, only do 1 chapter
                if subset_only and len(dataset['chapters']) >= 1:
                    break
                    
                dataset['chapters'].append({
                    "chapter_number": current_chapter_num,
                    "chapter_title": current_chapter_title,
                    "subtopics": []
                })
            
        elif el.name == 'ul' and current_chapter_title:
            links = el.find_all('a')
            
            # Find the target chapter dict
            target_chap = dataset['chapters'][-1]
            
            count = 0
            for a in links:
                if subset_only and count >= 2:
                    break
                
                sub_title = a.get_text(strip=True)
                
                # Skip NCERT and RD Sharma solutions
                sub_title_upper = sub_title.upper()
                if 'NCERT' in sub_title_upper or 'RD SHARMA' in sub_title_upper or 'R D SHARMA' in sub_title_upper:
                    continue
                    
                sub_url = a.get('href')
                
                if not sub_url.startswith('http'):
                    continue
                
                elements = parse_subtopic(sub_url)
                
                target_chap['subtopics'].append({
                    "subtopic_title": sub_title,
                    "source_url": sub_url,
                    "content_elements": elements
                })
                count += 1
                
                time.sleep(1) # Polite delay
                
            current_chapter_title = None

    # Write to file
    out_file = 'cbse_science_scraped_dataset.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
        
    print(f"\nDone! Dataset saved to {out_file}")

if __name__ == "__main__":
    import sys
    subset = True
    if len(sys.argv) > 1 and sys.argv[1] == 'full':
        subset = False
    scrape_notes(subset_only=subset)
