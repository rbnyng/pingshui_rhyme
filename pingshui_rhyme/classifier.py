import json
import pkg_resources

class PingZeClassifier:
    def __init__(self, json_file_path=None):
        if json_file_path is None:
            # Default to the JSON in the package data folder
            json_file_path = pkg_resources.resource_filename(
                __name__, 'data/organized_ping_ze_rhyme_dict.json'
            )

        # Load the ping-ze rhyme dictionary from the provided JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            self.ping_ze_dict = json.load(file)
                    
        # Collapse the ping and ze characters into strings
        self.ping_characters, self.ze_characters = self._collapse_ping_ze()

    def _collapse_ping_ze(self):
        """Helper function to collapse all characters in the ping and ze sections into strings."""
        ping_dict = self.ping_ze_dict.get('ping', {})
        ze_dict = self.ping_ze_dict.get('ze', {})

        # Extract all characters from ping
        ping_characters = {
            char for rhyme_group in ping_dict.values()
            for rhymes_list in rhyme_group.values()
            for rhyme_string in rhymes_list
            for char in rhyme_string
        }

        # Extract all characters from ze
        ze_characters = {
            char for rhyme_group in ze_dict.values()
            for rhymes_list in rhyme_group.values()
            for rhyme_string in rhymes_list
            for char in rhyme_string
        }

        return ping_characters, ze_characters

    def is_polyphonic(self, char):
        # Check if a character can be both ping and ze (polyphonic).
        return char in self.ping_characters and char in self.ze_characters

    def get_polyphonic_characters(self):
        return self.ping_characters & self.ze_characters

    def classify(self, sentence):
        # Classifies each character in a sentence as 'ping', 'ze', 'polyphonic', or 'unknown'.
        classification = []

        for char in sentence:
            is_ping = char in self.ping_characters
            is_ze = char in self.ze_characters

            if is_ping and is_ze:
                # Polyphonic character - can be either ping or ze depending on context
                classification.append('polyphonic')
            elif is_ping:
                classification.append('ping')
            elif is_ze:
                classification.append('ze')
            else:
                classification.append('unknown')

        return classification

    def classify_with_pattern(self, sentence, expected_pattern=None):
        """
        Classifies characters using expected meter pattern to disambiguate polyphonic characters.

        This method assumes that classical poets intentionally chose pronunciations
        to fit required meter patterns. When a character can be both ping and ze (polyphonic),
        the expected pattern determines which pronunciation the poet intended.
        """
        classification = []

        if expected_pattern:
            normalized_pattern = []
            for tone in expected_pattern:
                if tone == '平':
                    normalized_pattern.append('ping')
                elif tone == '仄':
                    normalized_pattern.append('ze')
                else:
                    normalized_pattern.append(tone)
            expected_pattern = normalized_pattern

        for i, char in enumerate(sentence):
            is_ping = char in self.ping_characters
            is_ze = char in self.ze_characters

            if is_ping and is_ze:  # Polyphonic character
                if expected_pattern and i < len(expected_pattern):
                    # Use the meter pattern to disambiguate
                    expected_tone = expected_pattern[i]
                    if expected_tone in ['ping', 'ze']:
                        classification.append(expected_tone)
                    else:
                        # Pattern position is '〇' (flexible) or invalid
                        classification.append('polyphonic')
                else:
                    # No pattern guidance available
                    classification.append('polyphonic')
            elif is_ping:
                classification.append('ping')
            elif is_ze:
                classification.append('ze')
            else:
                classification.append('unknown')

        return classification
