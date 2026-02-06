"""
Knowledge Loader - Reads axioms, proof methods, questions, and lemmas
"""

import os
import json


class KnowledgeLoader:
    """Loads mathematical knowledge from markdown files"""
    
    def __init__(self, base_dir: str = "."):
        """
        Initialize loader
        
        Args:
            base_dir: Base directory where .md files are located
        """
        self.base_dir = base_dir
    
    def load_axioms(self, filename: str = "axioms.md") -> str:
        """Load axioms from markdown file"""
        filepath = os.path.join(self.base_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Axioms file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        print(f"✓ Loaded axioms from {filename}")
        return content
    
    def load_proof_methods(self, filename: str = "proof_methods.md") -> str:
        """Load proof methods from markdown file"""
        filepath = os.path.join(self.base_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Proof methods file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        print(f"✓ Loaded proof methods from {filename}")
        return content
    
    def load_lemmas(self, memory_file: str = "proofs/proof_memory.json") -> list:
        """Load proven lemmas from memory"""
        filepath = os.path.join(self.base_dir, memory_file)
        
        if not os.path.exists(filepath):
            print("⚠ No lemmas found (no memory file yet)")
            return []
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Extract only successful proofs marked as lemmas
        lemmas = []
        for proof in data.get('proofs', []):
            if proof.get('success', False) and proof.get('lemma'):
                lemmas.append({
                    'statement': proof.get('lemma'),
                    'description': proof.get('description'),
                    'methods': list(set(att['proof_method'] for att in proof['attempts'] if att.get('success', False)))
                })
        
        print(f"✓ Loaded {len(lemmas)} proven lemma(s)")
        return lemmas
    
    def load_question(self, filepath: str) -> dict:
        """
        Load a question from a markdown file
        
        Returns a dict with:
            - title: Question title
            - statement: What to prove
            - content: Full file content
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Question file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Parse the question (simple parsing - look for title and statement)
        lines = content.strip().split('\n')
        title = ""
        statement = ""
        
        for i, line in enumerate(lines):
            if line.startswith('# '):
                title = line[2:].strip()
            elif line.startswith('**Statement:**'):
                # Statement is on the same line after the marker
                statement = line.replace('**Statement:**', '').strip()
            elif line.startswith('Statement:'):
                # Next line is likely the statement
                if i + 1 < len(lines):
                    statement = lines[i + 1].strip()
        
        print(f"✓ Loaded question: {title or 'Untitled'}")
        
        return {
            'title': title,
            'statement': statement,
            'content': content
        }
    
    def build_constrained_prompt(self, axioms: str, proof_methods: str, question: dict, lemmas: list = None, compact: bool = True) -> str:
        """
        Build a prompt that constrains the LLM to only use provided axioms and methods
        
        Args:
            axioms: Content of axioms.md
            proof_methods: Content of proof_methods.md
            question: Question dict from load_question()
            lemmas: List of proven lemmas (optional)
            compact: If True, extract only essential info to fit smaller models
        
        Returns:
            Formatted prompt string
        """
        if compact:
            # Extract just the key axioms and methods (compact version for small models)
            lemma_text = ""
            if lemmas:
                lemma_text = "\n\nYou may also use these PROVEN lemmas:\n"
                for i, lemma in enumerate(lemmas, 1):
                    lemma_text += f"- Lemma {i}: {lemma['statement']}\n"
            
            prompt = f"""You are proving: {question['statement'] or question['title']}

Use ONLY these axioms:
- Peano: 0 is natural, S(n) is successor, no n has S(n)=0, S injective
- Induction: If P(0) and P(n)→P(S(n)), then P holds for all n
- Order: For all a,b either a<b, a=b, or a>b{lemma_text}

Use ONLY these methods:
- Direct proof: Start with axioms, deduce conclusion
- Contradiction: Assume negation, derive contradiction
- Construction: Build explicit example
- Induction: Base case + inductive step

Proof (state axioms and method used):"""
        else:
            # Full version for larger models
            lemma_section = ""
            if lemmas:
                lemma_section = "\n=== AVAILABLE LEMMAS (ALREADY PROVEN) ===\n"
                for i, lemma in enumerate(lemmas, 1):
                    lemma_section += f"\nLemma {i}: {lemma['statement']}\n"
                    lemma_section += f"(Proven using: {', '.join(lemma['methods'])})\n"
            
            prompt = f"""You are a mathematical reasoning system. You must prove the following statement using ONLY the axioms and proof methods provided below. Do not use any external knowledge.

=== AVAILABLE AXIOMS ===
{axioms}

=== AVAILABLE PROOF METHODS ===
{proof_methods}{lemma_section}

=== QUESTION ===
{question['content']}

IMPORTANT CONSTRAINTS:
1. You may ONLY use axioms listed in the "AVAILABLE AXIOMS" section
2. You may ONLY use proof methods listed in the "AVAILABLE PROOF METHODS" section
3. You may use any proven lemmas listed in the "AVAILABLE LEMMAS" section
4. Cite which axioms, methods, and lemmas you are using
5. Provide clear, step-by-step reasoning
6. If you cannot prove it with the given axioms and methods, state that clearly

Your proof:"""
        
        return prompt


# Test the loader
if __name__ == "__main__":
    print("Testing KnowledgeLoader\n")
    
    # Go up one directory to project root
    loader = KnowledgeLoader("..")
    
    # Load axioms
    axioms = loader.load_axioms()
    print(f"Axioms length: {len(axioms)} chars\n")
    
    # Load proof methods
    methods = loader.load_proof_methods()
    print(f"Proof methods length: {len(methods)} chars\n")
