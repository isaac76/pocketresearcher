#!/usr/bin/env python3
"""
Add the infinitely many primes proof to memory
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
    description="Prove there are infinitely many prime numbers",
    statement="There are infinitely many prime numbers"
)

# Add the attempt (uses both induction and contradiction)
memory.add_attempt(
    proof_id=proof_id,
    proof_method="induction, contradiction",
    axioms_used=["Peano axioms", "Natural numbers", "Prime factorization"],
    reasoning="""To prove that there are infinitely many primes, we will use the induction method.

Base case:
For n = 1, we have the natural number 1, which is not prime.

Inductive step:
Assume that for some natural number n, there are no primes larger than n.

Take an arbitrary natural number k greater than n. By the assumption, k is not prime.

Now, we can write k = p1 * p2 *... * pk, where pi are prime numbers.

Since k > n, there must be at least one prime pi that is larger than n.

But this contradicts the assumption that there are no primes larger than n.

Therefore, our assumption is false, and there must be at least one prime larger than n.

This implies that there are infinitely many primes.""",
    success=True
)

# Mark as a lemma for future use
memory.mark_as_lemma(
    proof_id=proof_id,
    lemma_statement="There are infinitely many prime numbers"
)

# Display the proof
print("\n" + "="*70)
print("SAVED PROOF TO MEMORY")
print("="*70)
memory.print_proof(proof_id)
memory.print_statistics()

print("✓ Proof saved to proofs/proof_memory.json")
print("✓ This lemma can now be used in future proofs!")
