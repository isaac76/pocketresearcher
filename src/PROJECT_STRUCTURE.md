# PocketResearcher Source Code Overview

This document provides a detailed overview of each file in the PocketResearcher project, including their purpose, external dependencies, and how they interact. The goal of PocketResearcher is to enable querying a large language model (LLM) with plain-text math questions and receive Lean-formatted theorems and proofs, which are then refined and validated using Lean Dojo. If a proof is found, it is considered a mathematical discovery; if not, the system iteratively improves prompts and proof attempts until success.

---

## File-by-File Overview

### Top-Level Files

- **README.md**: Project introduction, setup, and usage instructions.
- **LICENSE**: Project license information.
- **DEMO_SUMMARY.md**: Example outputs and demo results.
- **memory.json / memory-even-proof.json**: Persistent memory files storing facts, ideas, and formal proofs.
- **research_log.md**: Log of research iterations and results.
- **analyze_techniques.py**: (If present) Analyzes proof techniques and strategies used in the project.

### `src/` Folder

- **pocketresearcher.py**
  - **Purpose**: Main entry point and research loop. Handles configuration, LLM selection, and orchestrates the overall workflow.
  - **External Libraries**: `os`, `json`, `argparse`, LLM APIs (Anthropic, Google Gemini, OpenAI), Lean Dojo (optional), project modules.
  - **Interactions**: Loads configuration, initializes the LLM, manages memory, and coordinates translation, proof, and validation steps.

- **lean_translator.py**
  - **Purpose**: Translates plain English math statements into Lean 4 theorem statements and proof attempts. Handles prompt engineering, post-processing, and syntax correction.
  - **External Libraries**: `re`, LLM APIs, project modules.
  - **Interactions**: Called by the main loop and `formal_proof_engine.py` to generate and refine Lean code.

- **formal_proof_engine.py**
  - **Purpose**: Manages the iterative proof refinement process. Attempts to prove theorems using Lean, parses feedback, and generates improved prompts for the LLM.
  - **External Libraries**: `subprocess`, `tempfile`, project modules.
  - **Interactions**: Uses `lean_translator.py` for translation, calls Lean for validation, and parses feedback to drive further attempts.

- **proof_assistant.py**
  - **Purpose**: (If present) Provides additional proof automation, symbolic math, or integration with tools like SymPy.
  - **External Libraries**: `sympy`, project modules.
  - **Interactions**: May be used by the main loop or proof engine for advanced math reasoning.

- **breakthrough_detector.py**
  - **Purpose**: Detects when a new mathematical breakthrough or significant result has been found.
  - **External Libraries**: Standard Python.
  - **Interactions**: Monitors memory and proof results.

- **content_filter.py**
  - **Purpose**: Filters and scores generated content for relevance and quality.
  - **External Libraries**: Standard Python.
  - **Interactions**: Used by the main loop to select high-quality facts and ideas.

- **filter_memory.py**
  - **Purpose**: Manages and filters the persistent memory files.
  - **External Libraries**: Standard Python.
  - **Interactions**: Reads/writes memory files, used by the main loop and proof engine.

- **memory.py**
  - **Purpose**: Handles in-memory storage and retrieval of facts, ideas, and proofs during a session.
  - **External Libraries**: Standard Python.
  - **Interactions**: Used throughout the project for state management.

---

## External Libraries Used

- **LLM APIs**: Anthropic (Claude), Google Gemini, OpenAI (GPT-4), via their respective Python SDKs.
- **Lean Dojo**: For Lean 4 theorem validation and feedback (optional, recommended for full automation).
- **SymPy**: For symbolic math (optional, used in `proof_assistant.py`).
- **Standard Python**: `os`, `json`, `re`, `argparse`, `subprocess`, `tempfile`, etc.

---

## File Interactions Diagram

```
[User Query]
    ↓
[pocketresearcher.py]
    ↓
[lean_translator.py] ←→ [formal_proof_engine.py] ←→ [proof_assistant.py]
    ↓
[Lean (via subprocess or Lean Dojo)]
    ↓
[memory.py, filter_memory.py, content_filter.py, breakthrough_detector.py]
    ↓
[memory-even-proof.json, research_log.md]
```

---

## Next Steps & Improvements

1. **Mathlib Compatibility**: Improve prompt engineering and post-processing to always use Mathlib's definitions (e.g., `Even n ↔ ∃ k, n = 2 * k`).
2. **Error Feedback Loop**: Enhance feedback parsing to better extract actionable suggestions from Lean errors.
3. **Lean Dojo Integration**: Fully automate proof validation and counterexample generation using Lean Dojo.
4. **Proof Generalization**: Add support for more general theorem templates and proof strategies.
5. **UI/UX**: Build a web or CLI interface for interactive querying and result visualization.
6. **Documentation**: Expand this documentation with more examples, API references, and developer guides.
7. **Testing**: Add more unit and integration tests for all modules.
8. **Performance**: Optimize LLM prompt/response cycles and Lean validation for speed.

---

## Project Goal (Summary)

PocketResearcher aims to bridge natural language math queries and formal Lean proofs, using LLMs for translation and Lean/Lean Dojo for validation. The system iteratively refines prompts and proof attempts, learning from feedback, until a valid proof is found or the search space is exhausted.

---

*This document is auto-generated and should be updated as the project evolves.*
