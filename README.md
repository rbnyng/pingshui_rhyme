# Pingshui Rhyme

**Pingshui Rhyme** is a Python package designed to classify tonal patterns ("ping" 平 and "ze" 仄 tones) and rhyme categories ("韻腳") of Chinese characters based on the [Pingshui Rhyme](https://zh.wikisource.org/wiki/%E5%B9%B3%E6%B0%B4%E9%9F%BB) (平水韻) rhyme scheme. You can read more about ping-ze, or tonal patterns, [here.](https://en.wikipedia.org/wiki/Tone_pattern) Modern Chinese varieties are not suitable for determining the phonological values of characters in middle Chinese due to sound changes, thus this package was built to use period accurate data to retrieve info about characters.

The package includes a pre-scraped JSON file that contains the complete data from the rhyme dictionary, and also provides a scraper to update the data if necessary.

## Features

- **Classify Chinese characters**: Easily classify characters as 'ping' or 'ze' based on the Pingshui Rhyme scheme.
- **Rhyme comparison**: Check if two characters rhyme based on their tonal and rhyme categories.
- **Rhyme group lookup**: Get detailed rhyme group information, such as tone type, tone group, and specific rhyme category for any given character.
- **Pre-packaged data**: Includes a pre-scraped JSON file with the complete rhyme data.
- **Scraper**: An optional scraper is included to regenerate the JSON file when the source data changes.
- **Poem structure checking**: Analyze and verify the structure of classical Chinese poems (Jueju and Lushi forms).

## Installation

You can install the package by running:

```bash
pip install pingshui_rhyme
```

## Usage

### Classifying Characters

Once installed, you can use the `PingZeClassifier` class to classify Chinese characters based on their tone as either "ping" (平) or "ze" (仄) tones:

```python
from pingshui_rhyme import PingZeClassifier

# Initialize the classifier (uses pre-packaged JSON by default)
classifier = PingZeClassifier()

# Classify a sentence
sentence = "知否？知否？應是綠肥紅瘦。"
result = classifier.classify(sentence)
print(result)
# Output: ['ping', 'ze', 'unknown', 'ping', 'ze', 'unknown', 'ping', 'ze', 'ze', 'ping', 'ping', 'ze', 'unknown']
```

### Rhyme Checking

You can also use the `RhymeChecker` class to check if two characters rhyme based on their tone group and rhyme category.

```python
from pingshui_rhyme import RhymeChecker

# Initialize the rhyme checker
rhyme_checker = RhymeChecker()

# Check if two characters rhyme
char1 = "東"
char2 = "同"
do_they_rhyme = rhyme_checker.do_rhyme(char1, char2)
print(do_they_rhyme)  # Output: True

# Get the rhyme group of a character
rhyme_group = rhyme_checker.get_rhyme_group(char1)
print(rhyme_group)
# Output: ('ping', '上平聲部', '上平聲一東')
```

### Poem Structure Checking

The `PoemStructureChecker` class allows you to analyze and verify the structure of classical Chinese poems (Jueju and Lushi forms).

```python
from pingshui_rhyme import PoemStructureChecker

# Initialize the poem structure checker
poem_checker = PoemStructureChecker()

# Check a Jueju poem
jueju_poem = '''
床前明月光，
疑是地上霜。
舉頭望明月，
低頭思故鄉。
'''
result, message = checker.check_poem_rhyming(jueju_poem)
print(result)  # Output: True
print(message)  # Output: "Poem follows jueju rhyming rules."

# Check a Lushi poem
lushi_poem = '''
昔人已乘黃鶴去，
此地空餘黃鶴樓。
黃鶴一去不復返，
白雲千載空悠悠。
晴川歷歷漢陽樹，
芳草萋萋鸚鵡洲。
日暮鄉關何處是，
煙波江上使人愁。
'''
result, message = checker.check_poem_rhyming(lushi_poem)
print(result)  # Output: True
print(message)  # Output: "Poem follows lushi rhyming rules."

# Check ping-ze meter
pingze_poem = '''
歲莫陰陽催短景，天涯霜雪霽寒霄。
五更鼓角聲悲壯，三峽星河影動搖。
野哭千家聞戰伐，夷歌幾處起漁樵。
臥龍躍馬終黃土，人事音書漫寂寥。 
'''
result, message = checker.check_poem_pingze_meter(pingze_poem)
print(result)  # Output: True
print(message)  # Output: "Poem follows the less restrictive ping-ze alternation pattern in 2nd, 4th, and 6th characters."
```                     

The `PoemStructureChecker` provides two main methods:

1. `check_poem_rhyming(poem)`: Checks if the poem follows the proper rhyme scheme for Jueju or Lushi forms.
2. `check_poem_pingze_meter(poem)`: Verifies if the poem follows the correct tonal pattern (ping-ze meter) according to classical Chinese poetry rules.

These methods return a tuple containing a boolean (indicating whether the poem passes the check) and a message explaining the result.

### Ping-Ze Label Conversion

The `PoemStructureChecker` class also provides methods to convert ping-ze labels between Chinese and English:

```python
from pingshui_rhyme import PoemStructureChecker

checker = PoemStructureChecker()

# Convert ping-ze labels to Chinese
chinese_labels = checker.pingze_en_convert_to_zh('ping')
print(chinese_labels)  # Output: '平'
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

## Running Unit Tests

Unit tests for the classifiers and rhyme checker are included. You can run the tests using `unittest`:

```bash
python -m unittest discover
```

## License

This package is licensed under the MIT License. See the LICENSE[LICENSE] file for details.

