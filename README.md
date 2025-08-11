# PocketResearcher: AI-Driven Research with Memory and Learning

I have always been curious about mathematics and proofs but unfortunately wasn't very good at them and focused on getting an engineering degree instead. But I never lost my interest in mathematics.

I have recently started delving into AI algorithms and specifically algorithms focused on neural networks. These studies focused on linear algebra, some calculus, but mostly the focus was on the structure of a neural network and things like forward passes and backpropagation. 

I wanted to turn my attention to LLMs and how they might help lead us to new discoveries. One challenge about LLMs is that they only know what they know. They are not designed for continuous learning. And at their core they are really just trying to fill in missing context, but they have an enormous amount of data so what they can produce is quite incredible.

But I wanted to look into a system that could use existing open source libraries to generate mathematical proofs, and then try to learn from what we discover. This would require some sort of memory management so that we can retain and use what we have so far learned.

To be clear, this is NOT a project that expects to discover anything new. Much smarter people than I, with access to giant LLMs will hopefully make the scientific discoveries. But I wanted to at least understand how they will use AI in their pursuit of knowledge.

So I created a project that makes use of various open source Python libraries and an LLM in order to start experimenting with mathematical proofs, and trying to discover something new. I'm hoping that the concept is at least similar to what might be done to really discover new theories and proofs.

Note that I used AI to help generate this project. 

## LLM

PocketResearcher uses a lightweight local language model (LLM) to generate mathematical statements, suggest possible theorems, and attempt informal and formal proofs. The LLM is not expected to solve major open problems, but it demonstrates how AI can assist in mathematical exploration and reasoning.

## Memory

The system maintains a persistent memory of facts, ideas, proofs, and breakthroughs. This memory is stored in `memory.json` and is updated as new discoveries are made. The memory allows the project to learn from previous attempts and avoid repeating the same steps.

## Filtering

To ensure quality, PocketResearcher uses a content filtering module that removes irrelevant, low-quality, or duplicate information from memory. Only substantial mathematical content is retained, helping the system focus on meaningful progress.

## Discovery

The project is designed to simulate the process of mathematical discovery. It generates new statements, attempts proofs, analyzes significance, and records breakthroughs. While it is unlikely to solve major problems, it provides a framework for experimenting with AI-driven research.

## Project Structure

- `src/`: Main source code, including proof generation, memory management, filtering, and analysis modules.
- `test/`: Unit tests for core functionality.
- `memory.json`: Persistent storage for learned facts, ideas, and proofs.

## Dependencies

- Python 3.8+: Core language for the project.
- transformers: Runs the local LLM for generating mathematical statements and proofs.
- sympy: Symbolic mathematics, theorem generation, and proof attempts.
- lean_dojo: Formal proof experiments and Lean theorem interaction.
- numpy, scipy: Numerical and scientific computations.
- pymongo, memcache (optional): Database/memory backend support.
- requests: HTTP requests for external data (if needed).
- rich, loguru: Enhanced logging and output formatting.
- pytest, unittest: Unit testing frameworks.

## How to Run

1. Install dependencies: `pip install -r requirements.txt`
2. Run the main script: `python src/pocketresearcher.py`
3. Review output in `memory.json`

## Expected Output

- Generated mathematical statements and attempted proofs
- Analysis of proof significance and quality
- Persistent memory of discoveries and breakthroughs