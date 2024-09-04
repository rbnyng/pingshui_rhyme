import unittest
from pingze_classifier import PingZeClassifier

class TestPingZeClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = PingZeClassifier()

    def test_classify(self):
        sentence = "知否？知否？應是綠肥紅瘦。"
        result = self.classifier.classify(sentence)
        expected = ['ping', 'ze', 'unknown', 'ping', 'ze', 'unknown', 'ping', 'ze', 'ze', 'ping', 'ping', 'ze', 'unknown']
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
