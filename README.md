# PingZeClassifier

**PingZeClassifier** is a Python package designed to classify Chinese characters as 'ping' (平) or 'ze' (仄) based on the [Pingshui Rhyme](https://zh.wikisource.org/wiki/%E5%B9%B3%E6%B0%B4%E9%9F%BB) (平水韻) rhyme scheme. The package includes a pre-scraped JSON file that contains the complete data from the rhyme dictionary, and also provides a scraper to update the data if necessary.

## Features

- **Classify Chinese characters**: Easily classify characters as 'ping' or 'ze' based on the Pingshui Rhyme scheme.
- **Pre-packaged data**: Includes a pre-scraped JSON file with the complete rhyme data.
- **Scraper**: An optional scraper is included to regenerate the JSON file when the source data changes.

## Installation

You can install the package by running:

```bash
pip install pingze_classifier
```

## Usage

###　Classifying Characters

Once installed, you can use the PingZeClassifier to classify Chinese characters based on the Pingshui Rhyme (平水韻) scheme:

```python
from pingze_classifier import PingZeClassifier

# Initialize the classifier (uses pre-packaged JSON by default)
classifier = PingZeClassifier()

# Classify a sentence
sentence = "知否？知否？應是綠肥紅瘦。"
result = classifier.classify(sentence)
print(result)
# Output: ['ping', 'ze', 'unknown', 'ping', 'ze', 'unknown', 'ping', 'ze', 'ze', 'ping', 'ping', 'ze', 'unknown']
```

### Scraping and Regenerating the JSON Data

The package includes a pre-generated JSON file, but if the Pingshui Rhyme source from wikisource changes you can run the scraper.

#### Running the Scraper

By default, the scraper won't run if the JSON file already exists. To force a refresh and regenerate the JSON data, run the following command:

```bash
scrape-pingze --force-refresh
```

This will scrape the latest data from the source and regenerate the `organized_ping_ze_rhyme_dict.json` file.

## Dependencies

    `requests`: For web scraping the Pingshui Rhyme data.
    `beautifulsoup4`: For parsing the HTML content from the Pingshui Rhyme source page.