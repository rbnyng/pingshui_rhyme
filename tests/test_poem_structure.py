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
        # A poem with 6 characters per line (invalid)
        poem = '''
        床前看明月光，
        疑是看地上霜。
        舉頭看望明月，
        低頭看思故鄉。
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertFalse(result)
        self.assertIn("Poem must have either 4 lines (Jueju) or 8 lines (Lushi)", message)

    def test_invalid_line_count(self):
        # A poem with only 3 lines (invalid)
        poem = '''
        床前明月光，
        疑是地上霜。
        舉頭望明月。
        '''
        result, message = self.checker.check_poem_rhyming(poem)
        self.assertFalse(result)
        self.assertIn("Poem must have either 4 lines (Jueju) or 8 lines (Lushi)", message)

if __name__ == '__main__':
    unittest.main()