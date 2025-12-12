import json
from bs4 import BeautifulSoup
import requests
import os
import argparse  

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_ping_ze_rhyme(force_refresh=False):
    output_file = os.path.join(os.path.dirname(__file__), 'data', 'organized_ping_ze_rhyme_dict.json')

    # Check if the file exists and if force_refresh is False
    if os.path.exists(output_file) and not force_refresh:
        print(f"JSON file already exists at {output_file}. Use `force_refresh=True` to regenerate.")
        return
    
    # Load the page
    url = 'https://zh.wikisource.org/wiki/%E5%B9%B3%E6%B0%B4%E9%9F%BB'
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize an empty hash map (dictionary)
    rhyme_dict = {}
    current_section_title = None

    # Locate the main content where rhyme data is present
    content = soup.find('div', class_='mw-parser-output')

    if not content:
        print("Error: Could not find the main content div ('mw-parser-output'). The website structure may have changed.")
        return
    
    declaration_marker = "本作品在全世界都属于公有领域"

    # Iterate through all <p> tags that contain the rhyme data
    for paragraph in content.find_all('p'):
        text = paragraph.get_text(strip=True)

        if declaration_marker in text:
            text = text.split(declaration_marker)[0].strip()
        
        if not text: # Skip empty paragraphs after cleaning
            continue

        # Check if the paragraph contains a rhyme section title (e.g., 上平聲一東)
        if text.startswith('上平聲') or text.startswith('下平聲') or text.startswith('上聲') or text.startswith('去聲') or text.startswith('入聲'):
            current_section_title = text.strip()
            rhyme_dict[current_section_title] = []  # Initialize an empty list for this section
        elif current_section_title:
            if '【詞】' in text or '【辭】' in text:
                text = text.replace('【詞】', '').replace('【辭】', '').strip()
            words = text.split()
            rhyme_dict[current_section_title].extend(words)
        elif text.startswith('【詞】') or text.startswith('【辭】'):
            text = text.replace('【詞】', '').replace('【辭】', '').strip()
            words = text.split()
            rhyme_dict[current_section_title].extend(words)

    def collapse_strings_in_dict(d):
        for key, value in d.items():
            if isinstance(value, list):
                d[key] = [''.join(value)  ]
            elif isinstance(value, dict):
                collapse_strings_in_dict(value) 
    collapse_strings_in_dict(rhyme_dict)

    organized_rhyme_dict = {
        "ping": {
            "上平聲部": {},
            "下平聲部": {}
        },
        "ze": {
            "上聲部": {},
            "去聲部": {},
            "入聲部": {}
        }
    }

    # Organize into ping and ze categories based on section names
    for section, words in rhyme_dict.items():
        if section.startswith("上平聲"):
            organized_rhyme_dict["ping"]["上平聲部"][section] = words
        elif section.startswith("下平聲"):
            organized_rhyme_dict["ping"]["下平聲部"][section] = words
        elif section.startswith("上聲"):
            organized_rhyme_dict["ze"]["上聲部"][section] = words
        elif section.startswith("去聲"):
            organized_rhyme_dict["ze"]["去聲部"][section] = words
        elif section.startswith("入聲"):
            organized_rhyme_dict["ze"]["入聲部"][section] = words

    # Save the result as a JSON structure
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(organized_rhyme_dict, f, ensure_ascii=False, indent=4)

    print(f"Rhyme dictionary successfully scraped and saved to {output_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Pingshui Rhyme data from WikiSource.")
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Force the scraper to run even if the JSON file already exists."
    )
    args = parser.parse_args()

    scrape_ping_ze_rhyme(force_refresh=args.force_refresh)