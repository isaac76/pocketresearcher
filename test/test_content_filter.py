import unittest
from src.content_filter import ContentFilter

class TestContentFilter(unittest.TestCase):
    def setUp(self):
        self.filter = ContentFilter({
            "min_mathematical_relevance": 0.3,
            "min_length": 10,
            "max_length": 500,
            "allow_simple_statements": True,
            "domain_keywords": ["even", "odd", "number", "integer", "sum", "addition", "proof", "algebra"]
        })

    def test_keep_high_quality_fact(self):
        fact = "The sum of two even numbers is always even."
        keep, reason = self.filter.should_keep_content(fact, "fact")
        self.assertTrue(keep)
        self.assertIn("Quality content", reason)

    def test_reject_short_fact(self):
        fact = "Even."
        keep, reason = self.filter.should_keep_content(fact, "fact")
        self.assertFalse(keep)
        self.assertIn("too short", reason)

    def test_reject_noise(self):
        fact = "Once upon a time, Mark asked Sarah about the database caching mechanism."
        keep, reason = self.filter.should_keep_content(fact, "fact")
        self.assertFalse(keep)
        self.assertIn("noise", reason.lower())

if __name__ == "__main__":
    unittest.main()
