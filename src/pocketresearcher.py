#!/usr/bin/env python3
"""
PocketResearcher - AI-Assisted Mathematical Proof Discovery

A system for exploring mathematical proofs using local LLMs, axioms, and proof methods.
"""

import sys
import os
import argparse

# Add src directory to path if running from project root
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from llm_manager import LocalLLM
from memory import ProofMemory
from knowledge_loader import KnowledgeLoader


def main():
    """Main entry point for PocketResearcher"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='PocketResearcher - Mathematical Proof Explorer')
    parser.add_argument('model', nargs='?', default='gpt2-medium',
                        help='LLM model name (phi2, gpt2-medium, etc.)')
    parser.add_argument('question', nargs='?', default='questions/q001_no_largest_natural.md',
                        help='Path to question file')
    parser.add_argument('--show-full-prompt', action='store_true',
                        help='Display the full prompt (all axioms, methods, lemmas)')
    parser.add_argument('--show-compact-prompt', action='store_true',
                        help='Display the compact prompt used for small models')
    parser.add_argument('--max-tokens', type=int, default=300,
                        help='Maximum tokens for LLM response (default: 300)')
    
    args = parser.parse_args()
    
    model_name = args.model
    question_file = args.question
    
    print("=" * 60)
    print("PocketResearcher - Mathematical Proof Explorer")
    print("=" * 60)
    print()
    
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
    
    # Load axioms, proof methods, lemmas, and failures
    print("📚 Loading knowledge base...")
    axioms = loader.load_axioms()
    proof_methods = loader.load_proof_methods()
    lemmas = loader.load_lemmas()
    failures = loader.load_failures()
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
    
    # Phi-2 has 2048 token limit, needs compact prompt
    # Larger models can handle full prompt
    use_compact = model_name in ["phi2", "gpt2", "gpt2-medium", "gpt2-large"]
    prompt = loader.build_constrained_prompt(axioms, proof_methods, question, lemmas=lemmas, failures=failures, compact=use_compact)
    print(f"   Prompt type: {'Compact' if use_compact else 'Full'}")
    print(f"   Prompt size: {len(prompt)} characters")
    print()
    
    # Display prompts if requested via flags
    if args.show_full_prompt:
        full_prompt = loader.build_constrained_prompt(axioms, proof_methods, question, lemmas=lemmas, failures=failures, compact=False)
        print("=" * 60)
        print("FULL PROMPT (ALL AXIOMS AND METHODS)")
        print("=" * 60)
        print(full_prompt)
        print("=" * 60)
        print()
    
    if args.show_compact_prompt:
        compact_prompt = loader.build_constrained_prompt(axioms, proof_methods, question, lemmas=lemmas, failures=failures, compact=True)
        print("=" * 60)
        print("COMPACT PROMPT (SUMMARIZED)")
        print("=" * 60)
        print(compact_prompt)
        print("=" * 60)
        print()
    
    # Generate proof attempt
    print("🧠 Asking LLM to prove the statement...")
    print(f"   Max tokens: {args.max_tokens}")
    print("   (This may take a moment...)")
    print()
    response = llm.generate(prompt, max_tokens=args.max_tokens)
    
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
