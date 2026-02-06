#!/usr/bin/env python3
"""
Save the failed Mersenne primes proof attempt with analysis
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
    description="Prove there are infinitely many Mersenne prime numbers",
    statement="There are infinitely many prime numbers of the form 2^p - 1 where p is prime"
)

# Add the failed attempt with analysis
memory.add_attempt(
    proof_id=proof_id,
    proof_method="contradiction (attempted)",
    axioms_used=["Lemma 2: infinitely many primes", "Peano axioms", "Divisibility"],
    reasoning="""We know from Lemma 2 that there are infinitely many prime numbers. Let's assume there are only finitely many prime numbers: p1, p2, p3,..., pn. 

Since every natural number has a prime divisor, for any natural number n > pn, it has a prime divisor p that is not in the list p1, p2, p3,..., pn. 

Now, let's consider the next prime number, p1p2. It is greater than any prime number in our list p1, p2, p3,..., pn. 

This means that p1p2 has a prime divisor that is not in our list p1, p2, p3,..., pn. 

But this contradicts our assumption that there are only finitely many prime numbers. 

Therefore, there are infinitely many prime numbers.

Answer: There are infinitely many Mersenne prime numbers.""",
    success=False,
    failure_analysis="""This proof fails for several reasons:

1. **Wrong target**: The proof attempts to prove there are infinitely many primes (which is already Lemma 2), not that there are infinitely many MERSENNE primes (2^p - 1).

2. **Ignored the problem statement**: Never mentions or uses the Mersenne form 2^p - 1. The proof would work for regular primes but not for the specific subset of Mersenne primes.

3. **Unjustified leap**: The conclusion "There are infinitely many Mersenne prime numbers" doesn't follow from proving there are infinitely many primes in general. Mersenne primes are a specific subset.

4. **Misused lemma**: Started correctly by citing Lemma 2, but then tried to re-prove it instead of building on it.

Correct approach would need to: 
- Use the fact that there are infinitely many primes (Lemma 2)
- Show construction of Mersenne numbers from primes (2^p - 1)
- Prove infinitely many of these Mersenne numbers are prime
- This is actually an open problem in mathematics!"""
)

# Display the proof
print("\n" + "="*70)
print("SAVED FAILED PROOF ATTEMPT TO MEMORY")
print("="*70)
memory.print_proof(proof_id)
memory.print_statistics()

print("\n✓ Failed proof saved with analysis")
print("✓ This failure analysis can help guide future attempts!")
