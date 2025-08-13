import unittest
from src.quality_assessor import ProofQualityAssessor

class TestProofQualityAssessor(unittest.TestCase):
    def setUp(self):
        self.assessor = ProofQualityAssessor()

    def test_placeholder_proof(self):
        code = "theorem foo : True := by sorry"
        result = self.assessor.assess_proof_quality(code, "foo")
        self.assertEqual(result["quality_score"], 0.0)
        self.assertTrue(result["is_placeholder"])
        self.assertIn("sorry", result["explanation"])
        self.assertEqual(result["mathematical_substance"], "placeholder")

    def test_low_quality_proof(self):
        code = "theorem foo : True := by trivial"
        result = self.assessor.assess_proof_quality(code, "foo")
        self.assertLess(result["quality_score"], 0.4)
        self.assertTrue(result["is_placeholder"])
        self.assertIn("trivial", result["explanation"])
        self.assertEqual(result["mathematical_substance"], "trivial_proof")

    def test_high_quality_proof(self):
        code = "theorem even_sum (a b : ℕ) (ha : Even a) (hb : Even b) : Even (a + b) := by\n  intro a\n  intro b\n  apply Even.add\n  exact ha\n  exact hb\n  ring"
        result = self.assessor.assess_proof_quality(code, "even_sum (a b : ℕ) (ha : Even a) (hb : Even b) : Even (a + b)")
        self.assertGreater(result["quality_score"], 0.7)
        self.assertTrue(result["is_meaningful"])
        self.assertIn("High-quality", result["explanation"])
        self.assertIn(result["mathematical_substance"], ["algebraic_manipulation", "proof_construction", "logical_reasoning"])

if __name__ == "__main__":
    unittest.main()
