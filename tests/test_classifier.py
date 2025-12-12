import unittest
from pingshui_rhyme import PingZeClassifier

class TestPingZeClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = PingZeClassifier()

    def test_classify(self):
        sentence = "知否？知否？應是綠肥紅瘦。"
        result = self.classifier.classify(sentence)
        # 應 at index 6 is polyphonic (can be both ping and ze)
        # it is ping here, but it's a test of polyphonism
        expected = ['ping', 'ze', 'unknown', 'ping', 'ze', 'unknown', 'polyphonic', 'ze', 'ze', 'ping', 'ping', 'ze', 'unknown']
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
