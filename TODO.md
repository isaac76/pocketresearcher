# TODO & Discussion Summary

## Project Recap

- **Goal:** Use an LLM constrained by specific math axioms, proof methods, and lemmas to prove mathematical statements. For example: "No largest natural number" and "Infinitely many primes".
- **Current Status:** Small LLMs do well with simple natural language proofs but struggle with formal Lean syntax and deeper math.
- **Future Aim:** Use larger LLMs (GPT-5, Anthropic, Claude, etc.) to generate proofs in Lean, verify them locally, and automatically track which axioms/methods/lemmas were used.

---

## Suggested Improvements

- Implement automated proof scoring and verification.
- Formalize proofs in Lean and verify them locally.
- Expand database to track the provenance of proofs: axioms, lemmas, and methods used.
- Prompt LLMs for explicit resource lists before proof generation.
- Store proof status, method, and provenance in DB entries.

---

## Challenges

### 1. Generating Lean-formatted Proofs with Large LLMs

- Larger LLMs are much better at producing valid Lean syntax, but:
  - They may still hallucinate or invent non-existent lemmas, axioms, or functions.
  - They can produce code that "looks correct" but fails Lean’s strict verification.
  - Even advanced models occasionally misunderstand Lean’s standard library or syntax nuances.
- **Mitigation:** Use chain-of-thought prompts and request explicit lists of resources; cross-validate outputs between different models.

### 2. Testing Lean Proofs Locally

- Local Lean verification ("lean --make filename.lean") is reliable but:
  - Requires clean, compilable Lean code.
  - Some proofs may rely on nonstandard libraries or versions; compatibility can be tricky.
  - Automation needs robust error handling for failed proofs, syntax errors, or compilation issues.
- **Mitigation:** Provide LLMs with project-specific Lean setup info and handle verification results gracefully; automate error logging and retry strategies.

### 3. Tracking Proof Provenance

- Parsing which axioms, lemmas, and proof methods were used can be tricky if not explicitly outlined in the proof or Lean code.
- Larger LLMs can be prompted to explicitly list these before or after the proof, but consistency needs to be enforced.

---

## Next Steps

- Develop/expand DB schema for storing lemma provenance and proof status.
- Design prompt templates for chain-of-thought, resource listing, and Lean code output.
- Build the pipeline for:
  1. LLM proof suggestion (natural language).
  2. Lean formalization.
  3. Local Lean verification.
  4. Automated DB update if successful.
- Cross-validate Lean proofs or resource lists with multiple LLMs for increased reliability.

---

*Last updated: 2026-02-06*