import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
from datetime import datetime

MASTER_URL = "https://www.geeksforgeeks.org/maths/cbse-class-10-maths-notes/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def is_math_or_chemistry(text):
    if re.search(r'\b[A-Z][a-z]?\d*(?:\s*\+\s*[A-Z][a-z]?\d*)+\s*(?:->||\=)\s*', text): return True
    if re.search(r'\$\$|\\\[|\\\(', text): return True
    if '²' in text or '³' in text or '√' in text or 'θ' in text or 'π' in text: return True
    if re.search(r'=[a-zA-Z0-9\+\-\/\*]+', text) and len(text) < 50: return True
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
    if not article: return []

    content_elements = []
    for el in article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'table', 'img', 'pre', 'code']):
        parent_names = [p.name for p in el.parents]
        if el.name != 'table' and 'table' in parent_names: continue
        if el.name != 'ul' and el.name != 'ol' and ('ul' in parent_names or 'ol' in parent_names): continue
        if el.name != 'pre' and 'pre' in parent_names: continue
        
        if el.name == 'p':
            text = el.get_text(strip=True)
            if not text: continue
            if is_math_or_chemistry(text) or '→' in text or '⇒' in text:
                if not text.startswith('$$'): text = f"$${text}$$"
                content_elements.append({"type": "formula", "text": text})
            else:
                content_elements.append({"type": "paragraph", "text": text})
        elif el.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            text = el.get_text(strip=True)
            if text:
                level = int(el.name[1])
                content_elements.append({"type": "heading", "level": level, "text": text})
        elif el.name in ['ul', 'ol']:
            items = [li.get_text(strip=True) for li in el.find_all('li') if li.get_text(strip=True)]
            if items:
                content_elements.append({"type": "list", "list_type": "unordered" if el.name == 'ul' else "ordered", "items": items})
        elif el.name == 'table':
            headers = []
            rows = []
            for th in el.find_all('th'): headers.append(th.get_text(strip=True))
            for tr in el.find_all('tr'):
                tds = tr.find_all('td')
                if tds: rows.append([td.get_text(strip=True) for td in tds])
            if not headers and rows:
                headers = rows[0]
                rows = rows[1:]
            if headers or rows:
                content_elements.append({"type": "table", "headers": headers, "rows": rows})
        elif el.name == 'img':
            src = el.get('src')
            if src: content_elements.append({"type": "image", "src": src, "alt": el.get('alt', '')})
        elif el.name in ['pre', 'code']:
            text = el.get_text(strip=True)
            if text:
                if not text.startswith('$$'): text = f"$${text}$$"
                content_elements.append({"type": "formula", "text": text})
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
            "subject": "Mathematics",
            "scraped_at": datetime.now().strftime("%Y-%m-%d")
        },
        "chapters": []
    }

    processed_chapters = set()

    for h in article.find_all(['h2', 'h3']):
        if 'Chapter' in h.text:
            match = re.search(r'Chapter\s*(\d+)', h.text)
            if match:
                c_num = int(match.group(1))
                if c_num in processed_chapters:
                    continue # Skip duplicates like 'Important Points'
                
                title = h.text.strip().replace(f'Chapter {c_num}:', '').strip()
                if 'Important' in title or 'Formulas' in title:
                    continue
                
                print(f"\nProcessing Chapter {c_num}: {title}")
                processed_chapters.add(c_num)
                
                if subset_only and len(dataset['chapters']) >= 1:
                    break
                    
                target_chap = {
                    "chapter_number": c_num,
                    "chapter_title": title,
                    "subtopics": []
                }
                
                for sib in h.next_siblings:
                    if sib.name in ['h2', 'h3']:
                        break
                    if sib.name in ['table', 'ul']:
                        links = sib.find_all('a')
                        count = 0
                        for a in links:
                            if subset_only and count >= 2: break
                            sub_title = a.get_text(strip=True)
                            
                            # Skip NCERT and RD Sharma solutions
                            sub_title_upper = sub_title.upper()
                            if 'NCERT' in sub_title_upper or 'RD SHARMA' in sub_title_upper or 'R D SHARMA' in sub_title_upper:
                                continue
                                
                            sub_url = a.get('href')
                            if not sub_url.startswith('http'): continue
                            
                            elements = parse_subtopic(sub_url)
                            target_chap['subtopics'].append({
                                "subtopic_title": sub_title,
                                "source_url": sub_url,
                                "content_elements": elements
                            })
                            count += 1
                            time.sleep(1)
                        break
                
                dataset['chapters'].append(target_chap)

    out_file = 'cbse_maths_scraped_dataset.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
        
    print(f"\nDone! Dataset saved to {out_file}")

if __name__ == "__main__":
    import sys
    subset = False if len(sys.argv) > 1 and sys.argv[1] == 'full' else True
    scrape_notes(subset_only=subset)
