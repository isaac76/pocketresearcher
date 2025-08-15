import unittest

from src.formal_proof_engine import FormalProofEngine


class TestLeanFeedbackHandler(unittest.TestCase):
    def setUp(self):
        # Use a debug translator (no API key) to keep the engine lightweight for tests
        self.engine = FormalProofEngine(api_key=None, llm_name='phi2')

    def test_missing_identifier_add_succ(self):
        feedback = ["Import or define missing identifier: add_succ"]
        suggestion = self.engine._handle_missing_identifier_feedback(feedback, "theorem add_zero (n : ℕ) : n + 0 = n")
        self.assertIsNotNone(suggestion)
        self.assertIn("Mathlib.Init.Data.Nat.Basic", suggestion)

    def test_missing_import_module(self):
        feedback = ["error: module 'Mathlib.Foo' does not exist - missing import"]
        suggestion = self.engine._handle_missing_identifier_feedback(feedback, "theorem foo : True")
        self.assertIsNotNone(suggestion)
        self.assertIn("missing import", suggestion.lower())

    def test_no_feedback_returns_none(self):
        suggestion = self.engine._handle_missing_identifier_feedback([], "theorem foo : True")
        self.assertIsNone(suggestion)


if __name__ == '__main__':
    unittest.main()
