import unittest
from pingshui_rhyme import PoemStructureChecker

class TestPoemStructure(unittest.TestCase):
    def setUp(self):
        self.checker = PoemStructureChecker()

    def test_jueju_rhyming(self):
        poem = '''
        床前明月光，
        疑是地上霜。
        舉頭望明月，
        低頭思故鄉。
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertTrue(result)
        self.assertEqual(message, "Poem follows jueju rhyming rules.")

    def test_lushi_rhyming(self):
        poem = '''
        昔人已乘黃鶴去，
        此地空餘黃鶴樓。
        黃鶴一去不復返，
        白雲千載空悠悠。
        晴川歷歷漢陽樹，
        芳草萋萋鸚鵡洲。
        日暮鄉關何處是，
        煙波江上使人愁。
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertTrue(result)
        self.assertEqual(message, "Poem follows lushi rhyming rules.")

    def test_pingze_meter(self):
        poem = '''
        歲莫陰陽催短景，天涯霜雪霽寒霄。
        五更鼓角聲悲壯，三峽星河影動搖。
        野哭千家聞戰伐，夷歌幾處起漁樵。
        臥龍躍馬終黃土，人事音書漫寂寥。 
        '''
        result, message = self.checker.check_poem_pingze_meter(poem)
        self.assertTrue(result)
        self.assertEqual(message, "Poem follows the less restrictive ping-ze alternation pattern in 2nd, 4th, and 6th characters.")

    def test_messy_format(self):
        # A poem with tabs, weird spacing, and English punctuation
        poem = '''
        床前   明月光,
        疑是\t地上霜.
        舉頭   望明月;
        低頭\t思故鄉!
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertTrue(result)
        self.assertEqual(message, "Poem follows jueju rhyming rules.")

    def test_invalid_line_length(self):
        # A poem with 6 characters per line (invalid for jueju - must be 5 or 7)
        poem = '''
        床前看明月光，
        疑是看地上霜。
        舉頭看望明月，
        低頭看思故鄉。
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertFalse(result)
        # With 4 lines, this is treated as jueju, which requires 5 or 7 chars per line
        self.assertIn("Each line must have 5 or 7 characters", message)

    def test_invalid_line_count(self):
        # A poem with only 3 lines (invalid)
        poem = '''
        床前明月光，
        疑是地上霜。
        舉頭望明月。
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertFalse(result)
        self.assertIn("Poem must have at least 4 lines", message)

    def test_gushi_valid_5_char_10_lines(self):
        # A valid gushi with 10 lines, 5 characters each
        poem = '''
        明月何皎皎，照我羅牀幃
        憂愁不能寐，覽衣起徘徊
        客行雖云樂，不如早旋歸
        出戶獨彷徨，愁思當告誰
        引領還入房，淚下沾裳衣
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertTrue(result)
        self.assertEqual(message, "Potential Gushi (古詩) format detected - rhyme and meter checking not applicable.")

    def test_gushi_valid_7_char_10_lines(self):
        # A valid gushi with 10 lines, 7 characters each
        poem = '''
        昔人已乘黃鶴去，
        此地空餘黃鶴樓。
        黃鶴一去不復返，
        白雲千載空悠悠。
        晴川歷歷漢陽樹，
        芳草萋萋鸚鵡洲。
        日暮鄉關何處是，
        煙波江上使人愁。
        風起雲湧天地間，
        萬里江山入畫圖。
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertTrue(result)
        self.assertEqual(message, "Potential Gushi (古詩) format detected - rhyme and meter checking not applicable.")

    def test_gushi_invalid_too_few_lines(self):
        # Invalid gushi - only 3 lines
        poem = '''
        白日依山盡，
        黃河入海流。
        欲窮千里目。
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertFalse(result)
        self.assertEqual(message, "Poem must have at least 4 lines.")

    def test_gushi_invalid_inconsistent_length(self):
        # Invalid gushi - inconsistent line lengths
        poem = '''
        白日依山盡，
        黃河入海流。
        欲窮千里目去，
        更上一層樓。
        登高望遠處，
        天地共悠悠。
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertFalse(result)
        self.assertEqual(message, "All lines in Gushi must have consistent character count.")

    def test_gushi_invalid_chars_too_short(self):
        # Invalid gushi - lines too short (3 chars)
        poem = '''
        白日山，
        黃河流。
        欲千里，
        更層樓。
        登望處，
        天悠悠。
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertFalse(result)
        self.assertEqual(message, "Each line in Gushi must have 4-8 characters.")

    def test_gushi_invalid_chars_too_long(self):
        # Invalid gushi - lines too long (9 chars)
        poem = '''
        白日依山盡黃河入海，
        黃河入海流欲窮千里，
        欲窮千里目更上一層，
        更上一層樓上一層樓，
        一層樓一層樓一層樓，
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertFalse(result)
        self.assertEqual(message, "Each line in Gushi must have 4-8 characters.")

    def test_gushi_pingze_skipped(self):
        # Test that pingze meter check is skipped for gushi
        poem = '''
        青青河畔草，鬱鬱園中柳
        盈盈樓上女，皎皎當窗牖
        娥娥紅粉妝，纖纖出素手
        昔為倡家女，今為蕩子婦
        蕩子行不歸，空床難獨守
        '''
        result, message = self.checker.check_poem_pingze_meter(poem)
        self.assertTrue(result)
        self.assertEqual(message, "Potential Gushi (古詩) format detected - pingze meter checking not applicable.")

if __name__ == '__main__':
    unittest.main()