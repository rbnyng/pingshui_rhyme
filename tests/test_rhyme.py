import unittest
from pingshui_rhyme import RhymeChecker

class TestRhymeChecker(unittest.TestCase):

    def setUp(self):
        self.rhymechecker = RhymeChecker()

    def test_do_rhyme_true(self):
        char1 = "東"
        char2 = "同"
        result = self.rhymechecker.do_rhyme(char1, char2)
        self.assertTrue(result)

    def test_do_rhyme_false(self):
        char1 = "東"
        char3 = "董"
        result = self.rhymechecker.do_rhyme(char1, char3)
        self.assertFalse(result)

    def test_get_rhyme_type(self):
        char = "東"
        result = self.rhymechecker.get_rhyme_type(char)
        expected = ('ping', '上平聲部', '上平聲一東')
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
