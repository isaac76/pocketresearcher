import unittest
from src.breakthrough_detector import is_breakthrough, BreakthroughDetector

class TestBreakthroughDetector(unittest.TestCase):
    def test_detects_breakthrough(self):
        # Simulate a breakthrough case (matches detector pattern and quality requirements)
        text = "A polynomial time algorithm for SAT has been discovered. This proves P = NP and uses NP-complete reductions. The proof includes a reduction from SAT to a polynomial time algorithm and demonstrates NP-complete properties."
        proof_steps = [
            "intro a", "intro b", "apply reduction", "apply polynomial_time", "apply NP_complete"
        ] * 10  # 50 steps, realistic tactics
        detector = BreakthroughDetector()
        result = detector.analyze_proof_significance({
            "informal_statement": text,
            "proof_steps": proof_steps,
            "theorem": text
        })
        self.assertTrue(result.get("is_breakthrough", False))

    def test_detects_non_breakthrough(self):
        # Simulate a non-breakthrough case
        text = "This is a routine calculation in number theory."
        self.assertFalse(is_breakthrough(text))

if __name__ == "__main__":
    unittest.main()
