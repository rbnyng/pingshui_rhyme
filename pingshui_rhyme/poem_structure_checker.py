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
        # try to split by punctuation or newlines to preserve line structure
        lines = re.split(r'[，。！？；：、,.!?;:\n]+', poem)

        # Remove all whitespace (including internal) from each line and filter empty lines
        lines = [re.sub(r'\s+', '', line) for line in lines]
        lines = [line for line in lines if line]

        # If we got lines from splitting on punctuation/newlines, return those
        if len(lines) > 1:
            return lines

        # Otherwise, the poem has no punctuation/newlines, so split by character count
        # Remove any whitespace
        poem = re.sub(r'\s+', '', poem)
        length = len(poem)

        # Try splitting as lines of 4, 5, 6, 7, or 8 characters
        for char_count in [4, 5, 6, 7, 8]:
            if length % char_count == 0:
                lines = [poem[i:i+char_count] for i in range(0, length, char_count)]
                return lines

        # If nothing worked, return the whole poem as a single line
        return [poem] if poem else []

    def pingze_zh_convert_to_en(self, pattern):
        return pattern.replace('平', 'ping').replace('仄', 'ze')

    def pingze_en_convert_to_zh(self, pattern):
        return pattern.replace('ping', '平').replace('ze', '仄')

    def check_poem_rhyming(self, poem):
        # Split the poem into lines
        lines = self.clean_poem(poem)

        # Check minimum line count
        if len(lines) < 4:
            return False, "Poem must have at least 4 lines."

        # Determine poem type based on line count
        # Regulated verse (Jintishi 近體詩): Jueju (4), Lushi (8), Pailu (10+, even)
        # Ancient verse (Gushi 古詩): Odd line count or non-standard structure
        if len(lines) == 4:
            poem_type = 'jueju'
        elif len(lines) == 8:
            poem_type = 'lushi'
        elif len(lines) >= 10 and len(lines) % 2 == 0:
            # Pailu (排律): Extended regulated verse with even line count >= 10
            # Note: Pailu follows strict tonal rules and should be checked like Lushi
            poem_type = 'pailu'
        else:
            # Gushi (古詩): Odd line count or other non-standard structure
            # Check if all lines have consistent length between 4-8 characters
            characters_per_line = len(lines[0])
            if characters_per_line < 4 or characters_per_line > 8:
                return False, "Each line must have 4-8 characters."

            # Verify all lines have the same length
            for line in lines:
                if len(line) != characters_per_line:
                    return False, "All lines must have consistent character count."

            # Gushi detected - no rhyme checking needed
            return True, "Potential Gushi (古詩) format detected - rhyme and meter checking not applicable."

        # Determine if it's 5-character or 7-character
        characters_per_line = len(lines[0])
        if characters_per_line not in [5, 7]:
            return False, "Each line must have 5 or 7 characters."

        # Classify the ping-ze tone (平仄) of the last characters of each line
        pattern = [self.classifier.classify(line[-1]) for line in lines]

        # Helper function to check if a tone can be ping (including polyphonic)
        def can_be_ping(tone):
            return tone[0] in ['ping', 'polyphonic']

        # Helper function to check if a tone can be ze (including polyphonic)
        def can_be_ze(tone):
            return tone[0] in ['ze', 'polyphonic']

        # 1. Check first line: it can either rhyme or not
        if can_be_ping(pattern[0]):
            first_line_rhymes = True  # If the first line ends in ping or polyphonic, it may rhyme
        elif pattern[0][0] == 'ze':
            first_line_rhymes = False  # If first line ends in ze, that character can't rhyme
        else:
            return False, "First line's last character must be either ping or ze."

        # 2. Check rhyming lines
        if poem_type == 'jueju':
            # Jueju: Check second and fourth lines for rhyming
            # Note: polyphonic characters are allowed since they can be pronounced as ping
            if not can_be_ping(pattern[1]) or not can_be_ping(pattern[3]):
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
            # Note: polyphonic characters are allowed since they can be pronounced as ze
            if not can_be_ze(pattern[2]):
                return False, "Third line must end with a ze character."

        elif poem_type in ['lushi', 'pailu']:
            # Lushi (8 lines) and Pailu (10+ lines): Even lines rhyme
            # Check all even-numbered lines (2, 4, 6, 8, ...) for rhyming
            even_line_indices = [i for i in range(1, len(lines), 2)]

            for i in even_line_indices:
                if not can_be_ping(pattern[i]):
                    return False, f"Line {i+1} must end with a ping character."

            char2 = lines[1][-1]
            for i in even_line_indices[1:]:  # Skip line 2, check lines 4, 6, 8, ...
                if not self.rhyme_checker.do_rhyme(char2, lines[i][-1]):
                    return False, f"Line {i+1} must rhyme with line 2."

            # Odd-numbered lines (except line 1) should not rhyme
            odd_line_indices = [i for i in range(2, len(lines), 2)]
            for i in odd_line_indices:
                if self.rhyme_checker.do_rhyme(char2, lines[i][-1]):
                    return False, f"Line {i+1} must not rhyme with line 2."

            # Optionally, check if the first line rhymes with the even lines if it ends in ping
            if first_line_rhymes:
                char1 = lines[0][-1]
                if not self.rhyme_checker.do_rhyme(char1, char2):
                    return False, "First line must rhyme with even lines if it uses ping."

            # Check odd-numbered lines: must end with ze
            # Note: polyphonic characters are allowed since they can be pronounced as ze
            for i in odd_line_indices:
                if not can_be_ze(pattern[i]):
                    return False, f"Line {i+1} must end with a ze character."

            # Ensure no three consecutive ping or ze in line endings
            for i in range(len(lines) - 2):
                if pattern[i] == pattern[i+1] == pattern[i+2]:
                    return False, "No three consecutive ping or ze are allowed."

        return True, f"Poem follows {poem_type} rhyming rules."

    def check_poem_pingze_meter(self, poem):
        # Clean the poem and split into lines
        lines = self.clean_poem(poem)

        # Check if this is Gushi format, skip pingze checking for Gushi
        # Gushi heuristic: odd line count or < 10 lines that aren't 4 or 8
        if len(lines) < 4:
            return False, "Poem must have at least 4 lines."

        # Only check meter for Jintishi (regulated verse): Jueju (4), Lushi (8), Pailu (10+ even)
        if len(lines) not in [4, 8] and not (len(lines) >= 10 and len(lines) % 2 == 0):
            return True, "Potential Gushi (古詩) format detected - pingze meter checking not applicable."

        # Determine if its 5-character or 7-character
        characters_per_line = len(lines[0])
        if characters_per_line not in [5, 7]:
            return False, "Each line must have 5 or 7 characters."

        # For Jueju (4) and Lushi (8), try strict pattern matching
        # For Pailu (10+), only use fallback logic as patterns are too varied
        if len(lines) in [4, 8]:
            # Check both rhymed (ruyun) and non-rhymed (buruyun) patterns for both pingqi and zeqi
            possible_patterns = self.patterns[characters_per_line]

            # Try all combinations of patterns: pingqi_ruyun, pingqi_buruyun, zeqi_ruyun, zeqi_buruyun
            for pattern_type, expected_patterns in possible_patterns.items():
                all_lines_match = True
                for i, line in enumerate(lines):

                    # 王士禎《律詵定體》 "凡七言第一字俱不論"
                    # For seven-character poems, the first character of each line is not considered.
                    if characters_per_line == 7:
                        expected_pattern_str = '〇' + expected_patterns[i][1:]
                        # Convert expected pattern string to list for classify_with_pattern
                        expected_list = [self.pingze_zh_convert_to_en(c) if c != '〇' else None for c in expected_pattern_str]
                        # Classify with pattern guidance (polyphonic characters use expected pattern)
                        classification = ['unknown'] + self.classifier.classify_with_pattern(line[1:], expected_list[1:])
                        pingze_pattern = '〇' + ''.join([self.pingze_en_convert_to_zh(c) for c in classification[1:]])
                    else:
                        expected_pattern_str = expected_patterns[i]
                        # Convert expected pattern string to list for classify_with_pattern
                        expected_list = [self.pingze_zh_convert_to_en(c) for c in expected_pattern_str]
                        # Classify with pattern guidance (polyphonic characters use expected pattern)
                        classification = self.classifier.classify_with_pattern(line, expected_list)
                        pingze_pattern = ''.join([self.pingze_en_convert_to_zh(c) for c in classification])

                    # Compare to the expected pattern
                    if pingze_pattern != expected_pattern_str:
                        all_lines_match = False
                        break

                # If any one pattern type fully matches, return success
                if all_lines_match:
                    return True, f"Poem follows {pattern_type} ping-ze pattern."

        # If strict pattern checks fail, resort to the less restrictive alternation check
        # 釋真空《新編篇韻貫珠集》 "一三五不論，二四六分明"
        # This checks two rules:
        # Dui (對): Opposition within couplets (lines 1-2, 3-4, 5-6, etc.)
        # Nian (黏): Adhesion between couplets (line 2 sticks to line 3, line 4 to line 5, etc.)

        for i in range(0, len(lines) - 1):
            line1 = lines[i]
            line2 = lines[i + 1]

            # For 7-character lines, consider positions 2, 4, and 6
            if characters_per_line == 7:
                tone_positions = [1, 3, 5]  # 0-based indexing
            else:
                tone_positions = [1, 3]  # 5-character lines

            for pos in tone_positions:
                tone1_raw = self.classifier.classify(line1[pos])[0]
                tone2_raw = self.classifier.classify(line2[pos])[0]

                # Convert to Chinese characters for display
                tone1_zh = self.pingze_en_convert_to_zh(tone1_raw) if tone1_raw in ['ping', 'ze'] else tone1_raw
                tone2_zh = self.pingze_en_convert_to_zh(tone2_raw) if tone2_raw in ['ping', 'ze'] else tone2_raw

                # Check if this is a couplet boundary (i is even: 0-1, 2-3, 4-5, ...)
                # or a couplet connection (i is odd: 1-2, 3-4, 5-6, ...)
                if i % 2 == 0:
                    # Dui (對): Within a couplet, tones should be opposite
                    # If either character is polyphonic, we can't definitively check, so allow it
                    if tone1_raw == 'polyphonic' or tone2_raw == 'polyphonic':
                        continue  # Skip this check for polyphonic characters
                    if tone1_raw == tone2_raw:
                        return False, f"Dui (對) violation: Lines {i+1} and {i+2} should have opposite tones at position {pos+1}, but both are {tone1_zh}."
                else:
                    # Nian (黏): Between couplets, tones should be the same ("sticky")
                    # If either character is polyphonic, we can't definitively check, so allow it
                    if tone1_raw == 'polyphonic' or tone2_raw == 'polyphonic':
                        continue  # Skip this check for polyphonic characters
                    if tone1_raw != tone2_raw:
                        return False, f"Nian (黏) violation: Lines {i+1} and {i+2} should have same tones at position {pos+1}, but found {tone1_zh} and {tone2_zh}."

        return True, "Poem follows the Dui (對) and Nian (黏) rules for ping-ze alternation in 2nd, 4th, and 6th characters."