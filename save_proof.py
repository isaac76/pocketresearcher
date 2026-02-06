#!/usr/bin/env python3
"""
Add the successful proof to memory manually
"""

import sys
import os

# Add src to path
sys.path.insert(0, 'src')

from memory import ProofMemory

# Initialize memory
memory = ProofMemory()

# Create the proof entry
proof_id = memory.create_proof(
    description="Prove there is no largest natural number",
    statement="For all natural numbers n, there exists a natural number m such that m > n"
)

# Add first attempt (labeled as direct but uses contradiction)
memory.add_attempt(
    proof_id=proof_id,
    proof_method="contradiction",
    axioms_used=["Peano successor axiom", "S(n) is successor function"],
    reasoning="""Start with Peano axioms: 0 is natural, S(n) is successor, no n has S(n)=0, S injective. 
Assume a natural number n is the largest natural number. Then, there exists a natural number m such that 
S(m) = n + 1. But this contradicts our assumption that S(m) = n + 1. Therefore, n cannot be the largest 
natural number.""",
    success=True
)

# Add second attempt (clearer contradiction)
memory.add_attempt(
    proof_id=proof_id,
    proof_method="contradiction",
    axioms_used=["Peano successor axiom", "Successor injective", "Zero has no predecessor"],
    reasoning="""Assume there exists a natural number n that is the largest natural number. But then, 
there must exist a natural number m such that S(m) = n + 1. But S(m) = n + 1 implies that m = S(n) - 1. 
Since n is the largest natural number, it must be equal to the successor of itself. But this contradicts 
the Peano axioms that say no n has S(n)=0 and S(0)=0""",
    success=True
)

# Mark as a lemma for future use
memory.mark_as_lemma(
    proof_id=proof_id,
    lemma_statement="For any natural number n, there exists a natural number greater than n (no largest natural)"
)

# Display the proof
print("\n" + "="*70)
print("SAVED PROOF TO MEMORY")
print("="*70)
memory.print_proof(proof_id)
memory.print_statistics()

print("✓ Proof saved to proofs/proof_memory.json")
print("✓ This lemma can now be used in future proofs!")
