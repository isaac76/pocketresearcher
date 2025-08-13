"""
Lean Translation Module - Converts natural language mathematical statements to Lean 4 syntax
"""
import re
from typing import Dict, Optional, Tuple
import google.generativeai as genai

class LeanTranslator:
    def __init__(self, api_key: str = None, debug: bool = False):
        """Initialize the Lean translator with Gemini API (or other Lean-capable LLM)"""
        self.debug = debug if debug is not None else (api_key is None)
        if not self.debug:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
        # Common Lean definitions for number theory
        self.lean_preamble = """
import Mathlib.Data.Nat.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
"""
    
    def translate_statement_to_lean(self, natural_statement: str) -> Tuple[str, str]:
        """
        Translate a natural language mathematical statement to Lean 4 syntax using a Lean-capable LLM.
        Returns: (lean_theorem_statement, theorem_name)
        """
        if self.debug:
            # Improved debug mode: return full Lean proofs for standard theorems
            s = natural_statement.lower()
            print(f"[LeanTranslator DEBUG] Input statement: {natural_statement}")
            if "even" in s and "sum" in s:
                print("[LeanTranslator DEBUG] Matched: sum of two even numbers is even")
                lean_code = (
                    "theorem even_sum (a b : ℤ) (ha : Even a) (hb : Even b) : Even (a + b) :=\n"
                    "by\n"
                    "  obtain ⟨k, rfl⟩ := ha\n"
                    "  obtain ⟨l, rfl⟩ := hb\n"
                    "  use k + l\n"
                    "  ring"
                )
                print(f"[LeanTranslator DEBUG] Returning Lean code:\n{lean_code}")
                return (lean_code, "even_sum")
            elif "odd" in s and "sum" in s:
                print("[LeanTranslator DEBUG] Matched: sum of even and odd is odd")
                lean_code = (
                    "theorem sum_even_odd_is_odd (n m : ℤ) (hn : Even n) (hm : Odd m) : Odd (n + m) :=\n"
                    "by\n"
                    "  obtain ⟨k, rfl⟩ := hn\n"
                    "  obtain ⟨l, rfl⟩ := hm\n"
                    "  use k + l\n"
                    "  ring"
                )
                print(f"[LeanTranslator DEBUG] Returning Lean code:\n{lean_code}")
                return (lean_code, "sum_even_odd_is_odd")
            elif "odd" in s and "product" in s:
                print("[LeanTranslator DEBUG] Matched: product of odd and even is even")
                lean_code = (
                    "theorem prod_odd_even_is_even (n m : ℤ) (hn : Odd n) (hm : Even m) : Even (n * m) :=\n"
                    "by\n"
                    "  obtain ⟨k, rfl⟩ := hn\n"
                    "  obtain ⟨l, rfl⟩ := hm\n"
                    "  use (2 * k * l + k * l)\n"
                    "  ring"
                )
                print(f"[LeanTranslator DEBUG] Returning Lean code:\n{lean_code}")
                return (lean_code, "prod_odd_even_is_even")
            elif "odd_example" in s:
                print("[LeanTranslator DEBUG] Matched: odd_example")
                return ("theorem odd_example : Odd 3 := by trivial", "odd_example")
            else:
                print("[LeanTranslator DEBUG] No match, returning fallback_theorem")
                return ("theorem fallback_theorem : True := by trivial", "fallback_theorem")
        else:
            translation_prompt = f"""
Convert this mathematical statement to valid Lean 4 theorem syntax.

Statement to convert: "{natural_statement}"

Provide only the theorem declaration in this format:
theorem theorem_name (variables) : conclusion := by sorry

Make the theorem name descriptive but valid Lean identifier (letters, numbers, underscores only).
If the statement is unclear or invalid, return a simpler related theorem.
"""
            response = self.model.generate_content(translation_prompt)
            lean_code = response.text.strip()
            # Extract theorem name
            theorem_match = re.search(r'theorem\s+(\w+)', lean_code)
            theorem_name = theorem_match.group(1) if theorem_match else "generated_theorem"
            # Clean up the Lean code
            lean_code = self._clean_lean_code(lean_code)
            return lean_code, theorem_name
    
    def _clean_lean_code(self, lean_code: str) -> str:
        """Clean and validate Lean code"""
        # Remove markdown formatting if present
        lean_code = re.sub(r'```lean\n?', '', lean_code)
        lean_code = re.sub(r'```\n?', '', lean_code)
        
        # Ensure it starts with 'theorem'
        if not lean_code.strip().startswith('theorem'):
            # Try to extract theorem from the text
            theorem_match = re.search(r'theorem\s+.*?:=\s+by\s+sorry', lean_code, re.DOTALL)
            if theorem_match:
                lean_code = theorem_match.group(0)
            else:
                lean_code = "theorem default_theorem : True := by sorry"
        
        return lean_code.strip()
    
    def generate_proof_attempt(self, theorem_statement: str) -> str:
        """
        Generate a proof attempt for a given Lean theorem
        Returns the proof steps (still may end with sorry)
        """
        if self.debug:
            # Return the proof script matching the debug theorem
            print(f"[LeanTranslator DEBUG] Proof attempt for: {theorem_statement}")
            if "even_sum" in theorem_statement:
                proof = "by\n  obtain ⟨k, rfl⟩ := ha\n  obtain ⟨l, rfl⟩ := hb\n  use k + l\n  ring"
                print(f"[LeanTranslator DEBUG] Returning proof attempt:\n{proof}")
                return proof
            elif "sum_even_odd_is_odd" in theorem_statement:
                proof = "by\n  obtain ⟨k, rfl⟩ := hn\n  obtain ⟨l, rfl⟩ := hm\n  use k + l\n  ring"
                print(f"[LeanTranslator DEBUG] Returning proof attempt:\n{proof}")
                return proof
            elif "prod_odd_even_is_even" in theorem_statement:
                proof = "by\n  obtain ⟨k, rfl⟩ := hn\n  obtain ⟨l, rfl⟩ := hm\n  use (2 * k * l + k * l)\n  ring"
                print(f"[LeanTranslator DEBUG] Returning proof attempt:\n{proof}")
                return proof
            elif "odd_example" in theorem_statement:
                print(f"[LeanTranslator DEBUG] Returning proof attempt: by trivial")
                return "by trivial"
            else:
                print(f"[LeanTranslator DEBUG] No match, returning proof attempt: by trivial")
                return "by trivial"
        else:
            proof_prompt = f"""
Given this Lean 4 theorem:
{theorem_statement}

Suggest specific Lean 4 proof tactics to prove this theorem. Use common tactics like:
- intro, intros
- apply, exact
- rw, simp
- cases, induction
- by_contra
- use (for existential)

Provide the proof in this format:
by
  tactic1
  tactic2
  sorry  -- if you can't complete the proof

If the theorem is not provable or too complex, just return "by sorry".
"""
        
        try:
            response = self.model.generate_content(proof_prompt)
            proof_text = response.text.strip()
            
            # Clean proof text
            if not proof_text.startswith('by'):
                proof_text = f"by\n  {proof_text}"
            
            return proof_text
            
        except Exception as e:
            print(f"Error generating proof: {e}")
            return "by sorry"
    
    def format_for_memory(self, lean_theorem: str, informal_statement: str, proof_attempt: str) -> Dict:
        """
        Format a theorem and proof attempt for storage in memory.json
        """
        # Extract theorem name
        theorem_match = re.search(r'theorem\s+(\w+)', lean_theorem)
        theorem_name = theorem_match.group(1) if theorem_match else "unknown_theorem"
        
        # Parse proof steps
        proof_lines = proof_attempt.split('\n')
        proof_steps = []
        for line in proof_lines:
            line = line.strip()
            if line and not line.startswith('by') and not line.startswith('--'):
                proof_steps.append(line)
        
        return {
            "theorem_name": theorem_name,
            "lean_statement": lean_theorem,
            "informal_statement": informal_statement,
            "proof_attempt": proof_attempt,
            "proof_steps": proof_steps,
            "tactics_tried": [],  # For consistency with formal_proof_engine expectations
            "verification_status": "unverified",  # Would be updated after Lean verification
            "timestamp": None  # Will be set by caller
        }
