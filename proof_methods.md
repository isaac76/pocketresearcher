# Proof Methods

This document describes fundamental proof techniques used in mathematics.

## 1. Direct Proof

**Description**: Start with known facts or axioms and use logical steps to arrive at the conclusion.

**Structure**:
1. State what you want to prove
2. Start with assumptions or known facts
3. Apply logical reasoning and axioms
4. Arrive at the desired conclusion

**Example Use Case**: Prove that the sum of two even numbers is even.

**Template**:
```
To prove: [Statement]
Assume: [Given facts]
Step 1: [Apply definition/axiom]
Step 2: [Logical deduction]
...
Therefore: [Conclusion]
```

---

## 2. Proof by Contradiction

**Description**: Assume the opposite of what you want to prove, then show this leads to a logical contradiction.

**Structure**:
1. State what you want to prove
2. Assume the negation of the statement
3. Use logical reasoning to derive a contradiction
4. Conclude that the original statement must be true

**Example Use Case**: Prove that $\sqrt{2}$ is irrational, or prove there is no largest natural number.

**Template**:
```
To prove: [Statement P]
Assume for contradiction: [Not P]
Step 1: [Logical deduction]
Step 2: [Further reasoning]
...
Contradiction: [Show something impossible]
Therefore: [P must be true]
```

---

## 3. Mathematical Induction

**Description**: Prove a statement for all natural numbers by proving it for a base case and showing it holds for $n+1$ if it holds for $n$.

**Structure**:
1. **Base Case**: Prove the statement for $n = 0$ (or $n = 1$)
2. **Inductive Hypothesis**: Assume the statement holds for some arbitrary $n$
3. **Inductive Step**: Prove the statement holds for $n + 1$ using the hypothesis
4. Conclude it holds for all natural numbers

**Example Use Case**: Prove that $1 + 2 + 3 + \cdots + n = \frac{n(n+1)}{2}$ for all natural numbers.

**Template**:
```
To prove: P(n) for all n ∈ ℕ
Base Case: Show P(0) [or P(1)] is true
Inductive Hypothesis: Assume P(k) is true for some k
Inductive Step: Prove P(k+1) using the hypothesis
Therefore: P(n) holds for all n ∈ ℕ
```

---

## 4. Proof by Contrapositive

**Description**: To prove $P \rightarrow Q$, instead prove $\neg Q \rightarrow \neg P$ (which is logically equivalent).

**Structure**:
1. State the implication you want to prove: $P \rightarrow Q$
2. Consider the contrapositive: $\neg Q \rightarrow \neg P$
3. Prove the contrapositive directly
4. Conclude the original statement is true

**Example Use Case**: Prove "If $n^2$ is even, then $n$ is even."

**Template**:
```
To prove: If P then Q
Contrapositive: If not Q, then not P
Assume: not Q
Step 1: [Logical deduction]
...
Therefore: not P
Conclusion: The original statement (P → Q) is true
```

---

## 5. Proof by Cases (Case Analysis)

**Description**: Break the problem into exhaustive cases and prove the statement for each case separately.

**Structure**:
1. Identify all possible cases
2. Prove the statement for Case 1
3. Prove the statement for Case 2
4. ... (continue for all cases)
5. Conclude the statement holds in all cases

**Example Use Case**: Prove that $n^2 + n$ is even for any natural number $n$.

**Template**:
```
To prove: [Statement]
Case 1: [Condition A]
  [Proof for Case 1]
Case 2: [Condition B]
  [Proof for Case 2]
...
Therefore: Statement holds in all cases
```

---

## 6. Constructive Proof (Proof by Construction)

**Description**: Prove existence by explicitly constructing an example that satisfies the property.

**Structure**:
1. State what you want to prove exists
2. Provide an explicit construction
3. Verify the construction satisfies all required properties

**Example Use Case**: Prove that for every natural number $n$, there exists a number greater than $n$.

**Template**:
```
To prove: There exists an x such that P(x)
Construction: Let x = [explicit formula/construction]
Verification: [Show P(x) holds]
Therefore: Such an x exists
```

---

## 7. Proof by Counterexample

**Description**: Disprove a universal statement by finding a single counterexample.

**Structure**:
1. State the claim being disproved (usually "for all x, P(x)")
2. Provide a specific example where the claim fails
3. Verify the counterexample
4. Conclude the claim is false

**Example Use Case**: Disprove "All prime numbers are odd."

**Template**:
```
Claim: For all x, P(x)
Counterexample: Consider x = [specific value]
Verification: [Show P(x) is false]
Therefore: The claim is false
```

---

## Choosing a Proof Method

- Use **direct proof** when you can clearly see a path from assumptions to conclusion
- Use **contradiction** when the negation seems easier to work with
- Use **induction** for statements about all natural numbers
- Use **contrapositive** when the negation of the conclusion gives you more to work with
- Use **cases** when the statement naturally divides into scenarios
- Use **construction** when proving existence and you can build an example
- Use **counterexample** when trying to disprove a universal claim
