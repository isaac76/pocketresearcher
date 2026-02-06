# Mathematical Axioms

This document contains fundamental mathematical axioms that can be used as building blocks for proofs.

## Common Arithmetic Properties

### Commutative Properties
- **Addition**: $a + b = b + a$
- **Multiplication**: $a \cdot b = b \cdot a$

### Associative Properties
- **Addition**: $(a + b) + c = a + (b + c)$
- **Multiplication**: $(a \cdot b) \cdot c = a \cdot (b \cdot c)$

### Distributive Property
- $a \cdot (b + c) = a \cdot b + a \cdot c$

### Identity Properties
- **Additive Identity**: $a + 0 = a$
- **Multiplicative Identity**: $a \cdot 1 = a$

### Inverse Properties
- **Additive Inverse**: $a + (-a) = 0$
- **Multiplicative Inverse**: $a \cdot a^{-1} = 1$ (for $a \neq 0$)

## Divisibility and Prime Numbers

### Divisibility
- **Definition**: We say $a$ divides $b$ (written $a \mid b$) if there exists an integer $k$ such that $b = a \cdot k$
- **Reflexive**: Every integer divides itself: $a \mid a$
- **Transitive**: If $a \mid b$ and $b \mid c$, then $a \mid c$
- **Linear Combination**: If $a \mid b$ and $a \mid c$, then $a \mid (bx + cy)$ for any integers $x$ and $y$

### Prime Numbers
- **Definition of Prime**: A natural number $p > 1$ is prime if its only positive divisors are $1$ and $p$ itself
- **Definition of Composite**: A natural number $n > 1$ is composite if it has a divisor $d$ where $1 < d < n$
- **Two is Prime**: $2$ is a prime number
- **Fundamental Property**: If $p$ is prime and $p \mid ab$, then $p \mid a$ or $p \mid b$
- **Existence of Prime Divisors**: Every integer $n > 1$ has at least one prime divisor

### Division Algorithm
- For any integers $a$ and $b$ with $b > 0$, there exist unique integers $q$ (quotient) and $r$ (remainder) such that:
  - $a = bq + r$
  - $0 \leq r < b$

## Peano Axioms (Natural Numbers)

1. **Zero is a natural number**: $0 \in \mathbb{N}$
2. **Successor function**: Every natural number $n$ has a successor $S(n)$ which is also a natural number
3. **Zero has no predecessor**: There is no natural number whose successor is $0$
4. **Successor is injective**: If $S(m) = S(n)$, then $m = n$
5. **Induction principle**: If a property holds for $0$ and holds for $S(n)$ whenever it holds for $n$, then it holds for all natural numbers

## Ordering Properties

### For Natural Numbers
- **Trichotomy**: For any two natural numbers $a$ and $b$, exactly one of the following is true: $a < b$, $a = b$, or $a > b$
- **Transitivity**: If $a < b$ and $b < c$, then $a < c$
- **Well-ordering**: Every non-empty set of natural numbers has a least element

### Addition and Order
- If $a < b$, then $a + c < b + c$
- If $a < b$ and $c > 0$, then $a \cdot c < b \cdot c$

## Exponentiation Axioms

### Fundamental Rules
- **Zero Exponent**: $a^0 = 1$ for any $a \neq 0$
- **Multiplication Rule (Same Base)**: $a^m \cdot a^n = a^{m+n}$
- **Division Rule (Same Base)**: $\frac{a^m}{a^n} = a^{m-n}$ for $a \neq 0$
- **Power of a Power**: $(a^m)^n = a^{mn}$
- **Power of a Product**: $(ab)^n = a^n b^n$
- **Negative Exponent**: $a^{-n} = \frac{1}{a^n}$ for $a \neq 0$
- **Fractional Exponent**: $a^{\frac{1}{n}} = \sqrt[n]{a}$ (the $n$-th root of $a$)

### Properties of Exponentiation
- **Not Commutative**: In general, $a^b \neq b^a$
- **Not Associative**: In general, $(a^b)^c \neq a^{(b^c)}$
- **Order of Operations**: In stacked notation $a^{b^c}$, evaluate as $a^{(b^c)}$ (top-down)

## Logical Axioms

### Basic Logic
- **Law of Identity**: $P \equiv P$ (a proposition is equivalent to itself)
- **Law of Excluded Middle**: $P \lor \neg P$ (a proposition is either true or its negation is true)
- **Law of Non-Contradiction**: $\neg(P \land \neg P)$ (a proposition and its negation cannot both be true)

### Inference Rules
- **Modus Ponens**: From $P$ and $P \rightarrow Q$, infer $Q$
- **Modus Tollens**: From $\neg Q$ and $P \rightarrow Q$, infer $\neg P$

## Set Theory Basics

- **Empty Set**: There exists a set with no elements, denoted $\emptyset$
- **Subset**: $A \subseteq B$ means every element of $A$ is also in $B$
- **Set Equality**: Two sets are equal if and only if they have the same elements
- **Union**: $x \in A \cup B$ if and only if $x \in A$ or $x \in B$
- **Intersection**: $x \in A \cap B$ if and only if $x \in A$ and $x \in B$
