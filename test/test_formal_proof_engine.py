import unittest
from unittest.mock import patch, MagicMock
from src.formal_proof_engine import FormalProofEngine

class TestFormalProofEngine(unittest.TestCase):
    @patch('src.formal_proof_engine.FormalProofEngine.test_with_lean')
    def test_even_sum_proof_success(self, mock_lean):
        # Mock Lean validation to always succeed
        mock_lean.return_value = {"success": True, "error": None, "output": "valid"}
        engine = FormalProofEngine()
        theorem = engine.generate_formal_conjecture("The sum of two even numbers is even.")
        result = engine.attempt_proof(theorem)
        self.assertTrue(result["success"])
        self.assertIn("Even.add", " ".join(result["tactics_tried"]))

if __name__ == "__main__":
    unittest.main()
