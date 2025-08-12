"""
Lean Translation Module - Converts natural language mathematical statements to Lean 4 syntax
"""
import re
from typing import Dict, Optional, Tuple
import google.generativeai as genai

class LeanTranslator:
    def __init__(self, api_key: str):
        """Initialize the Lean translator with Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Common Lean definitions for complexity theory
        self.lean_preamble = """
-- Complexity theory definitions for Lean 4
variable (Problem : Type)
variable (P NP : Set Problem)
variable (NPComplete : Problem → Prop)
variable (PolynomialTimeReduction : Problem → Problem → Prop)
variable (PolynomialTime : Problem → Prop)
"""
    
    def translate_statement_to_lean(self, natural_statement: str) -> Tuple[str, str]:
        """
        Translate a natural language mathematical statement to Lean 4 syntax
        Returns: (lean_theorem_statement, theorem_name)
        """
        translation_prompt = f"""
Convert this mathematical statement about computational complexity to valid Lean 4 theorem syntax.

Use these type definitions:
- Problem : Type (represents computational problems)
- P, NP : Set Problem (complexity classes)
- NPComplete : Problem → Prop (predicate for NP-complete problems)
- PolynomialTimeReduction : Problem → Problem → Prop
- PolynomialTime : Problem → Prop

Statement to convert: "{natural_statement}"

Provide only the theorem declaration in this format:
theorem theorem_name (variables) : conclusion := by sorry

Make the theorem name descriptive but valid Lean identifier (letters, numbers, underscores only).
If the statement is unclear or invalid, return a simpler related theorem about P and NP.
"""
        
        try:
            response = self.model.generate_content(translation_prompt)
            lean_code = response.text.strip()
            
            # Extract theorem name
            theorem_match = re.search(r'theorem\s+(\w+)', lean_code)
            theorem_name = theorem_match.group(1) if theorem_match else "generated_theorem"
            
            # Clean up the Lean code
            lean_code = self._clean_lean_code(lean_code)
            
            return lean_code, theorem_name
            
        except Exception as e:
            print(f"Error translating to Lean: {e}")
            # Fallback to a simple theorem
            fallback_name = "fallback_theorem"
            fallback_code = f"theorem {fallback_name} : P ⊆ NP := by sorry"
            return fallback_code, fallback_name
    
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
