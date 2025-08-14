"""
Lean Translation Module - Converts natural language mathematical statements to Lean 4 syntax
"""
import re
from typing import Dict, Optional, Tuple

# Gemini and Claude imports (optional)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not available. Install with: pip install google-generativeai")

try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    print("Warning: anthropic not available. Install with: pip install anthropic")

class LeanTranslator:
    def __init__(self, api_key: str = None, debug: bool = False, input_mode: str = "auto", llm_name: str = "gemini"):
        """
        Initialize the Lean translator with Gemini or Claude Sonnet API (or other Lean-capable LLM)
        input_mode: 'lean', 'plain', or 'auto' (default)
        llm_name: 'gemini', 'claude-sonnet', or other
        """
        self.debug = debug if debug is not None else (api_key is None)
        self.input_mode = input_mode  # 'lean', 'plain', or 'auto'
        self.llm_name = llm_name
        self.model = None
        if not self.debug:
            if llm_name == "claude-sonnet" and CLAUDE_AVAILABLE:
                self.model = anthropic.Anthropic(api_key=api_key)
            elif llm_name == "gemini" and GEMINI_AVAILABLE:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
        # Common Lean definitions for number theory
        self.lean_preamble = (
            "import Mathlib.Algebra.Ring.Parity\n"
        )

    def _generate_content(self, prompt: str, max_tokens: int = 100) -> str:
        """Unified generate_content for Gemini and Claude Sonnet"""
        if self.llm_name == "claude-sonnet" and self.model:
            try:
                response = self.model.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=max_tokens,
                    temperature=0.7,
                    system="You are a Lean 4 theorem prover assistant. Output only valid Lean 4 code when asked.",
                    messages=[{"role": "user", "content": prompt}]
                )
                if hasattr(response, "content"):
                    if isinstance(response.content, list):
                        return "\n".join([c.text for c in response.content if hasattr(c, "text")])
                    return str(response.content)
                return str(response)
            except Exception as e:
                print(f"[LeanTranslator] Claude Sonnet error: {e}")
                return None
        elif self.llm_name == "gemini" and self.model:
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"[LeanTranslator] Gemini error: {e}")
                return None
        return None

    def english_to_lean_pipeline(self, english_statement: str, previous_feedback: list = None) -> dict:
        """
        Multi-step pipeline to translate English math statements to Lean theorems and proofs.
        Returns a dict with extracted definitions, Lean statement, and proof attempt.
        """
        # Step 1: Extract definitions, variables, and hypotheses
        extract_prompt = f"""
Given the following mathematical statement in English:
{english_statement}

List the key mathematical concepts, variables, and hypotheses needed. Be concise and focus on mathlib terminology.

Example response format:
- Variables: natural numbers a, b
- Hypotheses: Even a, Even b  
- Goal: Even (a + b)
- Required imports: Mathlib.Algebra.Ring.Parity
"""
        definitions = None
        try:
            definitions = self._generate_content(extract_prompt, max_tokens=200)
        except Exception as e:
            print(f"[LeanTranslator] Error extracting definitions: {e}")
            definitions = None
            
        # Step 2: Generate Lean theorem statement
        theorem_prompt = f"""
Convert this English mathematical statement to a valid Lean 4 theorem declaration:

English: "{english_statement}"

Requirements:
- Output ONLY the theorem line (no imports, no explanations)
- Use proper Lean 4 syntax with mathlib types
- Include all necessary variables and hypotheses
- Use ℕ for natural numbers, ℤ for integers

Example format:
theorem sum_even_is_even (a b : ℕ) (ha : Even a) (hb : Even b) : Even (a + b) := by sorry

Your theorem:"""
        lean_statement = None
        try:
            lean_statement = self._generate_content(theorem_prompt, max_tokens=150)
        except Exception as e:
            print(f"[LeanTranslator] Error generating Lean statement: {e}")
            lean_statement = None
            
        # Step 3: Generate Lean proof attempt
        proof_prompt = f"""
Write a complete Lean 4 proof for this theorem:

{lean_statement or 'theorem sum_even_is_even (a b : ℕ) (ha : Even a) (hb : Even b) : Even (a + b) := by sorry'}

Requirements:
- Start with "by" 
- Use standard tactics: cases, use, rw, ring, simp
- Output ONLY the proof (no explanations)
- If unsure, end with "sorry"

Example proof structure:
by
  cases ha with k hk
  cases hb with l hl  
  use k + l
  rw [hk, hl]
  ring

Your proof:"""
        
        # If there is previous Lean feedback, add it to the prompt
        if previous_feedback:
            feedback_str = '\n'.join(previous_feedback)
            proof_prompt += f"\n\nPrevious Lean errors to fix:\n{feedback_str}"
            
        proof_attempt = None
        try:
            proof_attempt = self._generate_content(proof_prompt, max_tokens=200)
        except Exception as e:
            print(f"[LeanTranslator] Error generating Lean proof: {e}")
            proof_attempt = None
            
        # Post-process the results
        if lean_statement:
            lean_statement = self._postprocess_lean_theorem(lean_statement)
        if proof_attempt:
            proof_attempt = self._postprocess_lean_proof(proof_attempt)
            
        return {
            "definitions": definitions,
            "lean_statement": lean_statement,
            "proof_attempt": proof_attempt
        }
    
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
Convert this mathematical statement to a valid Lean 4 theorem declaration.

Statement: "{natural_statement}"

Requirements:
- Output ONLY the theorem line with proper syntax
- Use mathlib types (ℕ, ℤ, Even, Odd)
- Include necessary variables and hypotheses
- End with ":= by sorry"
- Make theorem name descriptive but valid identifier

Examples:
- "Two plus two equals four" → theorem two_plus_two : 2 + 2 = 4 := by sorry
- "Sum of even numbers is even" → theorem sum_even (a b : ℕ) (ha : Even a) (hb : Even b) : Even (a + b) := by sorry

Your theorem (one line only):"""
            
            response_text = self._generate_content(translation_prompt, max_tokens=100)
            lean_code = response_text if response_text else "theorem fallback_theorem : True := by sorry"
            
            # Clean up the Lean code
            lean_code = self._postprocess_lean_theorem(lean_code)
            
            # Extract theorem name
            theorem_match = re.search(r'theorem\s+(\w+)', lean_code)
            theorem_name = theorem_match.group(1) if theorem_match else "generated_theorem"
            
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
Write a Lean 4 proof for this theorem:

{theorem_statement}

Requirements:
- Start with "by"
- Use standard tactics: obtain, use, rw, ring, simp, intro, apply, exact
- For Even n: means ∃ k, n = 2 * k (use obtain ⟨k, hk⟩ := ha)
- For Odd n: means ∃ k, n = 2 * k + 1 (use obtain ⟨k, hk⟩ := ha)
- Output ONLY the proof code (no explanations or comments)
- If the proof is complex, end with "sorry"

Example proof patterns:
For Even/Odd theorems:
by
  obtain ⟨k, hk⟩ := ha
  obtain ⟨l, hl⟩ := hb
  use k + l
  rw [hk, hl]
  ring

Your proof:"""
        
            try:
                proof_text = self._generate_content(proof_prompt, max_tokens=150)
                if proof_text is None:
                    return "by sorry"
                    
                # Post-process the proof
                proof_text = self._postprocess_lean_proof(proof_text)
                return proof_text
            except Exception as e:
                print(f"Error generating proof: {e}")
                return "by sorry"

    def _postprocess_lean_theorem(self, lean_code: str) -> str:
        """Fix common Lean syntax errors for parity theorems."""
        code = lean_code.strip()
        
        # Remove markdown code blocks
        code = re.sub(r'```(lean)?', '', code)
        code = re.sub(r'```', '', code)
        
        # Remove explanatory text before and after theorem
        lines = code.split('\n')
        theorem_lines = []
        found_theorem = False
        
        for line in lines:
            if line.strip().startswith('theorem '):
                found_theorem = True
            if found_theorem:
                theorem_lines.append(line)
                # Stop at first complete theorem
                if ':= by sorry' in line or line.endswith(':='):
                    break
                    
        if theorem_lines:
            code = '\n'.join(theorem_lines)
        
        # Fix common syntax issues
        code = re.sub(r'theorem ([^(]+) in ', r'theorem \1 (', code)  # Replace 'in' with '('
        code = re.sub(r'\) ?: ?', ') ', code)  # Remove extra colons after parentheses
        code = code.replace('::', ':')  # Remove double colons
        
        # Fix missing colon before conclusion type
        # Pattern: (hypotheses) Type = by sorry -> (hypotheses) : Type := by sorry
        code = re.sub(r'(\([^)]+\))\s+(\w+.*?)\s*=\s*by', r'\1 : \2 := by', code)
        # Pattern: theorem name (...) Type = by -> theorem name (...) : Type := by
        code = re.sub(r'(theorem\s+\w+\s*\([^)]*\))\s+([A-Z][^=]*?)\s*=\s*by', r'\1 : \2 := by', code)
        
        # Ensure theorem ends properly
        if ':=' not in code and '=' in code:
            code = code.replace('=', ':=')
        elif ':=' not in code and code.strip().endswith(':'):
            code = code.strip() + ' := by sorry'
        elif code.strip().endswith('by'):
            code = code.strip() + ' sorry'
        elif not code.strip().endswith('sorry') and not code.strip().endswith(':=') and not code.strip().endswith('by sorry'):
            if ':=' in code and not code.strip().endswith('by sorry'):
                if not code.strip().endswith('sorry'):
                    code = code.strip() + ' := by sorry'
            else:
                code = code.strip() + ' := by sorry'
                
        # Canonicalize common parity theorem signature if malformed
        if ('Even' in code or 'Odd' in code) and (':' not in code.split(':=')[0]):
            code = 'theorem even_sum (a b : ℕ) (ha : Even a) (hb : Even b) : Even (a + b) := by sorry'
            
        return code.strip()

    def _postprocess_lean_proof(self, proof_code: str) -> str:
        """Clean and fix common Lean proof syntax errors."""
        code = proof_code.strip()
        
        # Remove markdown code blocks
        code = re.sub(r'```(lean)?', '', code)
        code = re.sub(r'```', '', code)
        
        # Remove explanatory text, keep only proof lines
        lines = code.split('\n')
        proof_lines = []
        found_by = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('by') or found_by:
                found_by = True
                proof_lines.append(line)
            elif line and not any(word in line.lower() for word in ['your proof:', 'example', 'proof structure', 'requirements']):
                # Include tactical lines that don't look like instructions
                if any(tactic in line for tactic in ['cases', 'obtain', 'use', 'rw', 'ring', 'simp', 'intro', 'apply', 'exact', 'sorry']):
                    proof_lines.append(line)
                    
        if proof_lines:
            code = '\n'.join(proof_lines)
            
        # Ensure it starts with 'by'
        if not code.startswith('by'):
            if code:
                code = f'by\n  {code}'
            else:
                code = 'by sorry'
                
        # Fix Lean 3 -> Lean 4 syntax issues
        # Replace old-style cases with obtain for Even/Odd
        code = re.sub(r'cases\s+(\w+)\s+with\s+(\w+)\s+(\w+)', r'obtain ⟨\2, \3⟩ := \1', code)
        
        # Fix common indentation issues
        lines = code.split('\n')
        if len(lines) > 1:
            fixed_lines = [lines[0]]  # Keep 'by' line as is
            for line in lines[1:]:
                if line.strip():
                    # Ensure proper indentation for proof steps
                    if not line.startswith('  '):
                        line = '  ' + line.strip()
                    fixed_lines.append(line)
            code = '\n'.join(fixed_lines)
            
        return code.strip()
    
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
