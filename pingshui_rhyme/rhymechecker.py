import json
import pkg_resources

class RhymeChecker:
    def __init__(self, json_file_path=None):
        if json_file_path is None:
            json_file_path = pkg_resources.resource_filename(
                __name__, 'data/organized_ping_ze_rhyme_dict.json'
            )

        with open(json_file_path, 'r', encoding='utf-8') as file:
            self.ping_ze_dict = json.load(file)

        self.rhyme_dict = self._build_rhyme_dict()

    def _build_rhyme_dict(self):
        """
        Builds a dictionary where the keys are characters, and the values are lists of their rhyme groups.
        """
        rhyme_dict = {}
        for tone_type in self.ping_ze_dict:
            for tone_group in self.ping_ze_dict[tone_type]:
                for rhyme_category, characters in self.ping_ze_dict[tone_type][tone_group].items():
                    for char_group in characters:
                        for char in char_group:
                            rhyme_group = (tone_type, tone_group, rhyme_category)
                            if char in rhyme_dict:
                                rhyme_dict[char].append(rhyme_group)
                            else:
                                rhyme_dict[char] = [rhyme_group]
        return rhyme_dict
    
    def get_rhyme_group(self, char):
        """
        Returns the list of rhyme groups for a given character, or None if the character is not found.
        """
        return self.rhyme_dict.get(char)

    def do_rhyme(self, char1, char2):
        """
        Determines if two characters rhyme by comparing their rhyme groups and tone types.
        """
        rhyme_groups1 = self.get_rhyme_group(char1)
        rhyme_groups2 = self.get_rhyme_group(char2)

        if not rhyme_groups1 or not rhyme_groups2:
            return False  # One or both characters are not in the rhyme data

        # Check if there's any matching rhyme group between the two characters
        for rhyme_group1 in rhyme_groups1:
            for rhyme_group2 in rhyme_groups2:
                if rhyme_group1 == rhyme_group2:
                    return True
        
        return False
    
    def get_rhyme_type(self, char):
        """
        Returns the full list of rhyme types (e.g., ["上平聲二冬", "下平聲一東"]) of the given character.
        """
        return self.get_rhyme_group(char)
