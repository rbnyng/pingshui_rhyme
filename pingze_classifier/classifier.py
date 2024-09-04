import json
import os

class PingZeClassifier:
    def __init__(self, json_file_path=None):
        if json_file_path is None:
            # Default to the JSON in the package data folder
            current_dir = os.path.dirname(__file__)
            json_file_path = os.path.join(current_dir, 'data', 'organized_ping_ze_rhyme_dict.json')

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
        ping_characters = "".join([char for rhyme_group in ping_dict.values() for rhymes in rhyme_group.values() for char in rhymes])

        # Extract all characters from ze
        ze_characters = "".join([char for rhyme_group in ze_dict.values() for rhymes in rhyme_group.values() for char in rhymes])

        return ping_characters, ze_characters

    def classify(self, sentence):
        """Classifies each character in a sentence as 'ping', 'ze', or 'unknown'."""
        classification = []

        # Classify each character in the sentence
        for char in sentence:
            if char in self.ping_characters:
                classification.append('ping')
            elif char in self.ze_characters:
                classification.append('ze')
            else:
                classification.append('unknown')
        
        return classification
