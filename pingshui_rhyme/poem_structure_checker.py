import re
from .classifier import PingZeClassifier
from .rhymechecker import RhymeChecker

class PoemStructureChecker:
    def __init__(self):
        self.classifier = PingZeClassifier()
        self.rhyme_checker = RhymeChecker()
        self.patterns = self._generate_patterns()

    def _generate_patterns(self):
        # Define the line structures for both 5 and 7-character lines
        line_structures = {
            'a': {5: '仄仄平平仄', 7: '平平仄仄平平仄'},
            'A': {5: '仄仄仄平平', 7: '平平仄仄仄平平'},
            'b': {5: '平平平仄仄', 7: '仄仄平平平仄仄'},
            'B': {5: '平平仄仄平', 7: '仄仄平平仄仄平'}
        }

        # General pattern sequences for 5 and 7-character Lushi
        patterns_generalized = {
            5: {
                'even_tone_rhymed': ['BA', 'aB', 'bA', 'aB'],      # 平起首句入韻 (pingqi_ruyun)
                'even_tone_unrhymed': ['bA', 'aB', 'bA', 'aB'],    # 平起首句不入韻 (pingqi_buruyun)
                'oblique_tone_rhymed': ['AB', 'bA', 'aB', 'bA'],   # 仄起首句入韻 (zeqi_ruyun)
                'oblique_tone_unrhymed': ['aB', 'bA', 'aB', 'bA']  # 仄起首句不入韻 (zeqi_buruyun)
            },
            7: {
                'even_tone_rhymed': ['AB', 'bA', 'aB', 'bA'],      # 平起首句入韻 (pingqi_ruyun)
                'even_tone_unrhymed': ['aB', 'bA', 'aB', 'bA'],    # 平起首句不入韻 (pingqi_buruyun)
                'oblique_tone_rhymed': ['BA', 'aB', 'bA', 'aB'],   # 仄起首句入韻 (zeqi_ruyun)
                'oblique_tone_unrhymed': ['bA', 'aB', 'bA', 'aB']  # 仄起首句不入韻 (zeqi_buruyun)
            }
        }

        # Function to generate the patterns dict based on generalized rules
        patterns = {5: {}, 7: {}}
        
        for char_count in [5, 7]:
            for scheme, pattern_sequence in patterns_generalized[char_count].items():
                patterns[char_count][scheme] = []
                for pattern_key in pattern_sequence:
                    # Replace each pattern letter with the corresponding line structure
                    line_pattern = [line_structures[char][char_count] for char in pattern_key]
                    for line in line_pattern:
                        patterns[char_count][scheme].append(line)
        
        return patterns

    def clean_poem(self, poem):
        """
        Cleans and reformats a poem by:
        - Removing any punctuation.
        - Splitting the poem into individual lines based on punctuation or line length (5 or 7 characters).
        - Stripping extra spaces or newlines.
        """
        # Remove any punctuation (commas, periods, etc.)
        poem = re.sub(r'[，。！？；：、]', '', poem)

        # Strip extra whitespace or newlines
        poem = poem.replace('\n', '').strip()

        # Automatically detect the character count per line (5 or 7 characters)
        # If the poem has no punctuation or spaces, split it based on typical 5 or 7 characters per line
        length = len(poem)
        
        # Try splitting as 4 or 8 lines of 5 or 7 characters
        if length % 5 == 0:
            # 5-character poem
            lines = [poem[i:i+5] for i in range(0, length, 5)]
        elif length % 7 == 0:
            # 7-character poem
            lines = [poem[i:i+7] for i in range(0, length, 7)]
        else:
            # Default: assume input is already spaced or punctuated and split by newlines
            lines = poem.split('\n')

        # Remove any leading or trailing whitespace from each line
        lines = [line.strip() for line in lines if line.strip()]

        return lines

    def pingze_zh_convert_to_en(self, pattern):
        return pattern.replace('平', 'ping').replace('仄', 'ze')

    def pingze_en_convert_to_zh(self, pattern):
        return pattern.replace('ping', '平').replace('ze', '仄')

    def check_poem_rhyming(self, poem):
        # Split the poem into lines
        lines = self.clean_poem(poem)

        # Determine if it's a Jueju (4 lines) or Lushi (8 lines)
        if len(lines) == 4:
            poem_type = 'jueju'
        elif len(lines) == 8:
            poem_type = 'lushi'
        else:
            return False, "Poem must have either 4 lines (Jueju) or 8 lines (Lushi)."

        # Determine if it's 5-character or 7-character
        characters_per_line = len(lines[0])
        if characters_per_line not in [5, 7]:
            return False, "Each line must have 5 or 7 characters."

        # Classify the ping-ze tone (平仄) of the last characters of each line
        pattern = [self.classifier.classify(line[-1]) for line in lines]

        # 1. Check first line: it can either rhyme or not
        if pattern[0][0] == 'ping':
            first_line_rhymes = True  # If the first line ends in ping, it may rhyme
        elif pattern[0][0] == 'ze':
            first_line_rhymes = False  # If first line ends in ze, that character can't rhyme
        else:
            return False, "First line's last character must be either ping or ze."

        # 2. Check rhyming lines
        if poem_type == 'jueju':
            # Jueju: Check second and fourth lines for rhyming
            if pattern[1][0] != 'ping' or pattern[3][0] != 'ping':
                return False, "Second and fourth lines must end with ping characters."
            char2 = lines[1][-1]
            char4 = lines[3][-1]
            if not self.rhyme_checker.do_rhyme(char2, char4):
                return False, "Second and fourth lines must rhyme."

            # Optionally, check if the first line rhymes with the second and fourth lines
            if first_line_rhymes:
                char1 = lines[0][-1]
                if not self.rhyme_checker.do_rhyme(char1, char2):
                    return False, "First line must rhyme with the second and fourth lines if it uses ping."

            # Check third line: must end with ze
            if pattern[2][0] != 'ze':
                return False, "Third line must end with a ze character."

        elif poem_type == 'lushi':
            # Lushi: Check second, fourth, sixth, and eighth lines for rhyming
            for i in [1, 3, 5, 7]:
                if pattern[i][0] != 'ping':
                    return False, f"Line {i+1} must end with a ping character."
            
            char2 = lines[1][-1]
            for i in [3, 5, 7]:
                if not self.rhyme_checker.do_rhyme(char2, lines[i][-1]):
                    return False, f"Line {i+1} must rhyme with line 2."
            
            # Except for line 1, odd-numbered lines (3, 5, 7) are not allowed to rhyme.
            for i in [2, 4, 6]:
                if self.rhyme_checker.do_rhyme(char2, lines[i][-1]):
                    return False, f"Line {i+1} must not rhyme with line 2."

            # Optionally, check if the first line rhymes with the even lines if it ends in ping
            if first_line_rhymes:
                char1 = lines[0][-1]
                if not self.rhyme_checker.do_rhyme(char1, char2):
                    return False, "First line must rhyme with even lines if it uses ping."

            # Check third, fifth, and seventh lines: must end with ze
            for i in [2, 4, 6]:
                if pattern[i][0] != 'ze':
                    return False, f"Line {i+1} must end with a ze character."

            # Ensure no three consecutive ping or ze in line endings
            for i in range(6):
                if pattern[i] == pattern[i+1] == pattern[i+2]:
                    return False, "No three consecutive ping or ze are allowed."

        return True, f"Poem follows {poem_type} rhyming rules."

    def check_poem_pingze_meter(self, poem):
        # Clean the poem and split into lines
        lines = self.clean_poem(poem)

        # Determine if it's 5-character or 7-character
        characters_per_line = len(lines[0])
        if characters_per_line not in [5, 7]:
            return False, "Each line must have 5 or 7 characters."

        # Check both rhymed (ruyun) and non-rhymed (buruyun) patterns for both pingqi and zeqi
        possible_patterns = self.patterns[characters_per_line]

        # Try all combinations of patterns: pingqi_ruyun, pingqi_buruyun, zeqi_ruyun, zeqi_buruyun
        for pattern_type, expected_patterns in possible_patterns.items():
            all_lines_match = True
            for i, line in enumerate(lines):

                # 王士禎《律詵定體》 "凡七言第一字俱不論"
                # For seven-character poems, the first character of each line is not considered.
                if characters_per_line == 7:
                    # Replace the first character with a blank instead of removing it
                    pingze_pattern = '〇' + ''.join([self.pingze_en_convert_to_zh(self.classifier.classify(char)[0]) for char in line[1:]])
                    expected_pattern = '〇' + expected_patterns[i][1:]  # Add a space at the beginning to match
                else:
                    pingze_pattern = ''.join([self.pingze_en_convert_to_zh(self.classifier.classify(char)[0]) for char in line])
                    expected_pattern = expected_patterns[i]

                # Compare to the expected pattern
                if pingze_pattern != expected_pattern:
                    all_lines_match = False
                    break

            # If any one pattern type fully matches, return success
            if all_lines_match:
                return True, f"Poem follows {pattern_type} ping-ze pattern."

        # If strict pattern checks fail, resort to the less restrictive 2nd, 4th, 6th character alternation check
        # 釋真空《新編篇韻貫珠集》 "一三五不論，二四六分明"
        for i in range(0, len(lines) - 1, 2):
            line1 = lines[i]
            line2 = lines[i + 1]

            # For 7-character lines, consider positions 2, 4, and 6
            if characters_per_line == 7:
                tone_positions = [1, 3, 5]  # 0-based indexing
            else:
                tone_positions = [1, 3]  # 5-character lines only have two positions to check

            for pos in tone_positions:
                tone1 = self.pingze_en_convert_to_zh(self.classifier.classify(line1[pos])[0])
                tone2 = self.pingze_en_convert_to_zh(self.classifier.classify(line2[pos])[0])

                # Check if tones are opposite: ping (平) and ze (仄)
                if tone1 == tone2:
                    return False, f"Ping ze tone mismatch between line {i+1} and line {i+2} at character position {pos+1}."

        return True, "Poem follows the less restrictive ping-ze alternation pattern in 2nd, 4th, and 6th characters."