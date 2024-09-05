import json
import pkg_resources

class RhymeChecker:
    def __init__(self):
        if json_file_path is None:
            json_file_path = pkg_resources.resource_filename(
                __name__, 'data/organized_ping_ze_rhyme_dict.json'
            )

        with open(json_file_path, 'r', encoding='utf-8') as file:
            self.ping_ze_dict = json.load(file)

        self.rhyme_dict = self._build_rhyme_dict()

    def _build_rhyme_dict(self):
        """
        Builds a dictionary where the keys are characters, and the values are their rhyme groups.
        """
        rhyme_dict = {}
        for tone_type in self.rhyme_data:
            for tone_group in self.rhyme_data[tone_type]:
                for rhyme_category, characters in self.rhyme_data[tone_type][tone_group].items():
                    for char_group in characters:
                        for char in char_group:
                            rhyme_dict[char] = (tone_type, tone_group, rhyme_category)
        return rhyme_dict
    
    def get_rhyme_group(self, char):
        """
        Returns the rhyme group of a given character.
        """
        return self.rhyme_dict.get(char)

    def do_rhyme(self, char1, char2):
        """
        Determines if two characters rhyme by comparing their rhyme group and tone type.
        """
        rhyme_group1 = self.get_rhyme_group(char1)
        rhyme_group2 = self.get_rhyme_group(char2)

        if not rhyme_group1 or not rhyme_group2:
            return False  # One or both characters are not in the rhyme data
        
        # Check if they share the same rhyme group (same tone, same rhyme category)
        return rhyme_group1 == rhyme_group2
    
    def get_rhyme_type(self, char):
        """
        Returns the full rhyme type (e.g., "上平聲二冬") of the given character.
        """
        return self.get_rhyme_group(char)
