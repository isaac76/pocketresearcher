#!/usr/bin/env python3
"""
PocketResearcher - AI-Assisted Mathematical Proof Discovery

A system for exploring mathematical proofs using local LLMs, axioms, and proof methods.
"""

import sys
import os

# Add src directory to path if running from project root
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from llm_manager import LocalLLM
from memory import ProofMemory
from knowledge_loader import KnowledgeLoader


def main():
    """Main entry point for PocketResearcher"""
    
    print("=" * 60)
    print("PocketResearcher - Mathematical Proof Explorer")
    print("=" * 60)
    print()
    
    # Parse command line arguments
    model_name = "gpt2-medium"  # default
    question_file = "questions/q001_no_largest_natural.md"  # default
    
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
    if len(sys.argv) > 2:
        question_file = sys.argv[2]
    
    # Initialize components
    print("🔧 Initializing system...")
    print()
    
    # Initialize LLM
    llm = LocalLLM(model_name=model_name, max_tokens=300, temperature=0.7)
    print()
    
    # Initialize memory
    memory = ProofMemory()
    print()
    
    # Initialize knowledge loader
    # Navigate to project root (one level up from src/)
    project_root = os.path.dirname(current_dir)
    loader = KnowledgeLoader(project_root)
    print()
    
    # Load axioms, proof methods, and lemmas
    print("📚 Loading knowledge base...")
    axioms = loader.load_axioms()
    proof_methods = loader.load_proof_methods()
    lemmas = loader.load_lemmas()
    question = loader.load_question(os.path.join(project_root, question_file))
    print()
    
    # Show current statistics
    if len(memory.get_all_proofs()) > 0:
        print("📊 Current proof database:")
        memory.print_statistics()
    else:
        print("📊 Starting with empty proof database")
        print()
    
    # Build constrained prompt
    print("🎯 Question:", question['title'])
    print("📝 Statement:", question['statement'])
    print()
    print("🤔 Building constrained prompt for LLM...")
    prompt = loader.build_constrained_prompt(axioms, proof_methods, question, lemmas=lemmas, compact=True)
    print(f"   Prompt size: {len(prompt)} characters")
    print()
    
    # Generate proof attempt
    print("🧠 Asking LLM to prove the statement...")
    print("   (This may take a moment...)")
    print()
    response = llm.generate(prompt, max_tokens=200)
    
    # Display result
    print("=" * 60)
    print("LLM RESPONSE")
    print("=" * 60)
    print(response)
    print("=" * 60)
    print()
    print("✓ Proof generation complete!")
    print()


if __name__ == "__main__":
    main()
