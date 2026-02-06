# PocketResearcher

An experimental AI-assisted mathematical proof discovery system that constrains local LLMs to use only specified axioms, proof methods, and previously proven lemmas.

## Overview

PocketResearcher is a proof-of-concept system exploring whether small, local language models can generate mathematical proofs when constrained to a well-defined formal system. The key innovation is **hard constraints**: the LLM can only use:

- **Axioms** we provide (e.g., Peano axioms, arithmetic properties)
- **Proof methods** we define (e.g., direct proof, contradiction, induction)
- **Lemmas** previously proven and validated by a human reviewer

This approach tests whether LLMs can reason mathematically within strict boundaries, building a knowledge base incrementally rather than relying on pre-trained mathematical knowledge.

## Key Findings

### ✅ What Works

1. **Constraint Enforcement**: Local LLMs successfully respect the boundaries we set. When given only Peano axioms and basic proof methods, the models attempt proofs using only those tools.

2. **Lemma Reuse**: The system successfully passes proven lemmas back to the LLM, which can then reference them in subsequent proofs.

3. **Reasonable Attempts**: Even small models (phi-2 with 2.7B parameters) generate structured proof attempts that follow logical patterns.

4. **Incremental Knowledge Building**: By validating and storing proofs as lemmas, we create a growing knowledge base for increasingly complex theorems.

### ⚠️ Challenges Discovered

1. **Proof Validation is Hard**: Automatically determining whether a proof is correct is extremely difficult. We discovered that programmatic validation would essentially require a full theorem prover.

2. **Quality Varies**: The proofs generated are often incomplete or have logical gaps. For example, our "infinitely many primes" proof uses the right ideas (induction, contradiction) but lacks full rigor.

3. **Interactive Review Required**: A human must review and validate each proof before adding it to the knowledge base. This is currently done manually using a Python script.

4. **Model Size Matters**: Larger models produce better reasoning, but even phi-2 (2.7B) shows promise with careful prompt engineering.

### 📊 LLM Model Comparison

**phi-2 (microsoft/phi-2)** - 2.7B parameters
- ✅ Better structured reasoning
- ✅ Follows proof formats more closely
- ✅ Correctly identifies axioms being used
- ⚠️ Output quality varies with temperature (0.7)
- ⚠️ Sometimes generates incomplete proofs
- **Result**: Recommended for this task

**gpt2-medium** - 355M parameters
- ⚠️ Weaker logical reasoning
- ⚠️ Tends to loop or repeat concepts
- ⚠️ Shorter, less structured outputs
- ❌ Often doesn't follow proof patterns
- **Result**: Too small for mathematical reasoning

### 🤔 Why Aren't Results Perfect?

1. **Model Scale**: Even phi-2 is relatively small for complex mathematical reasoning. State-of-the-art models (GPT-4, Claude) are orders of magnitude larger.

2. **Training Data**: These models weren't specifically trained on formal mathematical proofs. They have general reasoning ability but lack specialized proof-writing training.

3. **Temperature Setting**: We use temperature=0.7 for creativity, which introduces randomness. This helps explore different approaches but reduces consistency.

4. **Prompt Complexity**: Mathematical reasoning requires maintaining complex logical chains. Small models have limited context windows and working memory.

5. **Formal vs Natural Language**: The gap between natural language reasoning and formal mathematical proof is significant. Our system uses natural language, which is inherently less precise.

## Dependencies

### Core Libraries

```bash
pip install torch transformers accelerate
```

**Why These Libraries?**

- **torch** (PyTorch): Backend for running transformer models locally. Required for model inference.
  
- **transformers** (HuggingFace): Provides pre-trained language models and tokenizers. Allows us to load models like phi-2 and gpt2-medium with minimal code.
  
- **accelerate**: Required for loading larger models (like phi-2) efficiently. Handles device placement and memory optimization.

### Python Version

- **Python 3.11+** required
- Older versions (3.6, 3.8) have incompatible transformers versions

### Model Storage

Models are automatically downloaded and cached to:
```
~/.cache/huggingface/hub/
```

First run downloads the model (~5GB for phi-2), subsequent runs load from cache.

## Usage

### Running a Proof Attempt

```bash
# Basic usage with default question
python3.11 src/pocketresearcher.py phi2

# Specify a custom question
python3.11 src/pocketresearcher.py phi2 questions/q002_infinitely_many_primes.md

# Try with gpt2-medium (not recommended)
python3.11 src/pocketresearcher.py gpt2-medium
```

### Example Output

```
============================================================
PocketResearcher - Mathematical Proof Explorer
============================================================

🤖 Initializing phi2...
✓ phi2 ready (from local cache)

📚 Loading knowledge base...
✓ Loaded axioms from axioms.md
✓ Loaded proof methods from proof_methods.md
✓ Loaded 2 proven lemma(s)

🎯 Question: Prove there are infinitely many prime numbers

🧠 Asking LLM to prove the statement...

============================================================
LLM RESPONSE
============================================================
To prove that there are infinitely many primes, we will use 
the induction method.

Base case: For n = 1, we have the natural number 1...
[proof attempt continues]
============================================================
```

### Adding Proofs to Memory

After reviewing an LLM-generated proof, if you judge it acceptable:

1. **Create a save script** (or modify existing `save_proof.py`):

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')
from memory import ProofMemory

memory = ProofMemory()

# Create the proof entry
proof_id = memory.create_proof(
    description="Describe what was proven",
    statement="Formal statement of the theorem"
)

# Add the attempt
memory.add_attempt(
    proof_id=proof_id,
    proof_method="contradiction",  # or "induction", "direct proof", etc.
    axioms_used=["Peano successor axiom", "Other axioms used"],
    reasoning="""
    [Paste the LLM's proof text here]
    """,
    success=True
)

# Mark as lemma for future use
memory.mark_as_lemma(
    proof_id=proof_id,
    lemma_statement="Short statement of proven result"
)

memory.print_proof(proof_id)
memory.print_statistics()
```

2. **Run the script**:

```bash
python3.11 save_my_proof.py
```

3. **Verify it was saved**:

```bash
cat proofs/proof_memory.json
```

The lemma is now available for future proof attempts!

## Current Proof Database

### Lemma 1: No Largest Natural Number
**Status**: ✓ Proven  
**Method**: Contradiction (2 attempts)  
**Statement**: For any natural number n, there exists a natural number greater than n

This proof uses the Peano successor axiom to show that assuming a largest natural number leads to contradiction.

### Lemma 2: Infinitely Many Primes
**Status**: ✓ Proven (with caveats)  
**Method**: Induction + Contradiction  
**Statement**: There are infinitely many prime numbers

This proof combines induction and contradiction. While not perfectly rigorous, it demonstrates the right approach and uses correct reasoning patterns. **Good enough for experimental purposes.**

## Project Structure

```
.
├── axioms.md                   # Foundational mathematical axioms
├── proof_methods.md            # Allowed proof techniques
├── questions/                  # Mathematical statements to prove
│   ├── q001_no_largest_natural.md
│   └── q002_infinitely_many_primes.md
├── proofs/                     # Validated proof database
│   └── proof_memory.json       # JSON storage of all proofs
├── src/                        # Source code
│   ├── pocketresearcher.py     # Main orchestrator
│   ├── knowledge_loader.py     # Loads knowledge from files
│   ├── llm_manager.py          # Local LLM interface
│   └── memory.py               # Proof storage system
├── test/                       # Unit tests
│   ├── test_memory.py
│   └── [other tests]
├── save_proof.py               # Template for saving proofs
└── README.md                   # This file
```

## Workflow

1. **Create a question** in `questions/` directory (markdown format)

2. **Run PocketResearcher** with your chosen LLM model:
   ```bash
   python3.11 src/pocketresearcher.py phi2 questions/your_question.md
   ```

3. **Review the output**: Read the LLM's proof attempt. Does it:
   - Use only the provided axioms?
   - Follow a valid proof method?
   - Have sound logical reasoning?
   - Reference available lemmas appropriately?

4. **If acceptable, save it**: Create a script to add the proof to memory, identifying which axioms and methods were used.

5. **The lemma is now available**: Future proof attempts can reference this proven result!

## Experiment Philosophy

This project prioritizes **exploration over perfection**. We're testing whether:

- Local, small LLMs can be constrained to formal systems
- Incremental knowledge building improves proof capabilities  
- The constraint-based approach has merit for AI reasoning

We **do not expect** perfect proofs from 2.7B parameter models. We **do expect** to learn about:

- How LLMs handle mathematical constraints
- What level of reasoning is possible with small models
- Whether lemma reuse improves subsequent proofs
- The challenges of automated proof validation

## Future Directions

1. **Larger Models**: Test with 7B+ parameter models (LLaMA, Mistral)
2. **Better Validation**: Develop heuristics or scoring for proof quality
3. **Formal Language**: Translate to Lean or Coq for mechanical verification
4. **Chain of Thought**: Add explicit reasoning steps to prompts
5. **Fine-tuning**: Train models specifically on formal proofs
6. **Interactive Mode**: Build a REPL for real-time proof exploration

## License

See LICENSE file for details.

## Acknowledgments

- HuggingFace for transformers library and model hosting
- Microsoft Research for phi-2 model
- The mathematical logic and proof theory communities

---

**Note**: This is a research experiment. The proofs generated are not formally verified and should not be considered mathematically authoritative. Always validate mathematical claims through rigorous formal methods or peer review.
