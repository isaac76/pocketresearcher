# PocketResearcher: AI-Driven Research with Memory and Learning

I have always been curious about mathematics and proofs, but unfortunately wasn't very good at them and focused on getting an engineering degree instead. However, I never lost my interest in mathematics.

I have recently started delving into AI algorithms, specifically those focused on neural networks. These studies covered linear algebra and some calculus, but mostly focused on neural network structure and concepts like forward passes and backpropagation. 

I wanted to turn my attention to LLMs and how they might help lead us to new discoveries. One challenge with LLMs is that they only know what they know—they are not designed for continuous learning. At their core, they are trying to fill in missing context, but they have access to enormous amounts of data, so what they can produce is quite incredible.

However, I wanted to explore a system that could use existing open-source libraries to generate mathematical proofs and then learn from what we discover. This would require memory management so that we can retain and use what we have learned so far.

To be clear, this is NOT a project that expects to discover anything new. Really smart mathematicians and computer scientists are working on similar approaches and will hopefully use LLMs to discover new theories and proofs, and will hopefully advance mathematics and science. I just wanted to try to understand some of what they are doing and how we might implement continuous learning in conjunction with LLMs.

So I created a project that makes use of various open-source Python libraries and an LLM to start experimenting with mathematical proofs and trying to discover something new. I'm hoping that the concept is at least similar to what might be done to really discover new theories and proofs.

Note that I used AI to help generate this project. 

## LLM Configuration

PocketResearcher supports multiple language models with automatic fallback:

### Supported Models
- **Google Gemini (default)**: High-quality API-based model with rate limiting (15 requests/minute)
- **Microsoft Phi-2**: Local model for offline use and backup when API limits are reached
- **GPT-2**: Alternative local model option

### Configuration
The system uses `config.py` for all settings:

```python
# LLM Selection
DEFAULT_LLM = "gemini"        # Primary model to use
FALLBACK_LOCAL_MODEL = "phi2" # Backup when API fails

# API Keys
GEMINI_API_KEY = "your_key_here"  # Get from Google AI Studio
OPENAI_API_KEY = None             # Optional OpenAI integration

# Rate Limiting
GEMINI_RATE_LIMIT = 15      # Requests per minute (free tier)
ENABLE_RATE_LIMITING = True # Automatic throttling
```

### Automatic Fallback
- System tries Gemini first (if API key available)
- Falls back to local Phi-2 model when:
  - API quota exceeded
  - Network issues
  - Invalid API key
- Seamless switching with no interruption

### API Setup
1. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. Update `GEMINI_API_KEY` in `config.py`
3. System will automatically use Gemini with rate limiting

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

- **Python 3.8+**: Core language for the project
- **google-generativeai**: Google Gemini API for high-quality text generation
- **transformers**: Local LLM support (Phi-2, GPT-2) for offline operation
- **sympy**: Symbolic mathematics, theorem generation, and proof attempts
- **lean_dojo**: Formal proof experiments and Lean theorem interaction
- **numpy, scipy**: Numerical and scientific computations
- **torch**: PyTorch for running local transformer models
- **requests**: HTTP requests for external data (if needed)
- **rich, loguru**: Enhanced logging and output formatting
- **pytest, unittest**: Unit testing frameworks

See `requirements.txt` for complete dependency list with versions.

## How to Run

### Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Copy configuration template: `cp config.py.sample config.py`
3. (Optional) Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/)
4. Edit `config.py` to add your API key (or use local models only)
5. Run the main script: `python src/pocketresearcher.py`
6. Review output in `memory.json` and console logs

### Configuration Options
- **With Gemini API**: High-quality generation with automatic rate limiting
- **Local only**: Works offline using Phi-2 model (no API key needed)
- **Hybrid mode**: Starts with Gemini, falls back to local when needed

### Model Selection
Edit `config.py` to change the default model:
```python
DEFAULT_LLM = "gemini"  # or "phi2", "gpt2"
```

## Expected Output

- Generated mathematical statements and attempted proofs
- Analysis of proof significance and quality
- Persistent memory of discoveries and breakthroughs