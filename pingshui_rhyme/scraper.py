import json
from bs4 import BeautifulSoup
import requests
import os

def scrape_ping_ze_rhyme(force_refresh=False):
    output_file = os.path.join(os.path.dirname(__file__), 'data', 'organized_ping_ze_rhyme_dict.json')

    # Check if the file exists and if force_refresh is False
    if os.path.exists(output_file) and not force_refresh:
        print(f"JSON file already exists at {output_file}. Use `force_refresh=True` to regenerate.")
        return
    
    # Load the page
    url = 'https://zh.wikisource.org/wiki/%E5%B9%B3%E6%B0%B4%E9%9F%BB'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize an empty hash map (dictionary)
    rhyme_dict = {}
    current_section_title = None

    # Locate the main content where rhyme data is present
    content = soup.find('div', class_='mw-parser-output')

    # Iterate through all <p> tags that contain the rhyme data
    for paragraph in content.find_all('p'):
        text = paragraph.get_text(strip=True)

        # Check if the paragraph contains a rhyme section title (e.g., 上平聲一東)
        if text.startswith('上平聲') or text.startswith('下平聲') or text.startswith('上聲') or text.startswith('去聲') or text.startswith('入聲'):
            current_section_title = text.strip()
            rhyme_dict[current_section_title] = []  # Initialize an empty list for this section
        elif current_section_title:
            if '【詞】' in text:
                text = text.replace('【詞】', '').strip()
            words = text.split()  # Split by whitespace to get individual words
            rhyme_dict[current_section_title].extend(words)
            current_section_title = None  # Reset the section title

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
    scrape_ping_ze_rhyme()
