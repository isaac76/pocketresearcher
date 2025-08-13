import unittest
from unittest.mock import MagicMock
from src.lean_translator import LeanTranslator

class TestLeanTranslator(unittest.TestCase):
    def setUp(self):
        # Mock the LLM model
        self.translator = LeanTranslator(api_key="fake-key")
        self.translator.model = MagicMock()

    def test_translate_even_sum(self):
        # Mock LLM response for even sum theorem
        self.translator.model.generate_content.return_value = MagicMock(text="theorem even_sum (a b : ℕ) (ha : Even a) (hb : Even b) : Even (a + b) := by sorry")
        lean_code, theorem_name = self.translator.translate_statement_to_lean("The sum of two even numbers is even.")
        self.assertIn("theorem even_sum", lean_code)
        self.assertEqual(theorem_name, "even_sum")

    def test_translate_p_vs_np(self):
        # Mock LLM response for P vs NP
        self.translator.model.generate_content.return_value = MagicMock(text="theorem p_eq_np : P = NP := by sorry")
        lean_code, theorem_name = self.translator.translate_statement_to_lean("P equals NP.")
        self.assertIn("theorem p_eq_np", lean_code)
        self.assertEqual(theorem_name, "p_eq_np")

    def test_generate_proof_attempt(self):
        # Mock LLM response for proof attempt
        self.translator.model.generate_content.return_value = MagicMock(text="by intro a; intro b; apply Even.add; exact ha; exact hb")
        proof = self.translator.generate_proof_attempt("theorem even_sum (a b : ℕ) (ha : Even a) (hb : Even b) : Even (a + b) := by sorry")
        self.assertTrue(proof.startswith("by"))
        self.assertIn("apply Even.add", proof)

if __name__ == "__main__":
    unittest.main()
