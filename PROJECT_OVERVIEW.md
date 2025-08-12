# PocketResearcher v2 - Clean Project Overview

## 🎯 Main Entry Points

### Primary Interface (Use This!)
```bash
# Even number proofs with local model
python pocketresearcher_v2.py direct_proof gpt2-medium

# P vs NP research with advanced model  
python pocketresearcher_v2.py p_vs_np phi2

# See all options
python pocketresearcher_v2.py --help
```

## 📁 Project Structure

### 🔧 Core System
- **`pocketresearcher_v2.py`** - Main research interface with unified configuration
- **`config_unified.py`** - Single source of truth for all configuration

### 📚 Source Modules (`src/`)
- **`memory.py`** - Memory management system
- **`content_filter.py`** - Domain-aware content filtering
- **`formal_proof_engine.py`** - Formal theorem proving with Lean integration
- **`proof_assistant.py`** - Mathematical proof analysis and validation
- **`llm_manager.py`** - LLM interface and management
- **`breakthrough_detector.py`** - Significant result detection
- **`lean_translator.py`** - Natural language to Lean theorem translation

### 💾 Memory Files
- **`memory-even-proof.json`** - Clean even number research data
- **`memory-pvnp.json`** - P vs NP complexity theory research data

### 📊 Tools & Utilities
- **`analyze_techniques.py`** - Research technique analysis
- **`cleanup.py`** - Project cleanup script
- **`test/`** - Unit tests

### 📋 Documentation
- **`README.md`** - Project documentation
- **`requirements.txt`** - Python dependencies
- **`DEMO_SUMMARY.md`** - System capabilities overview

### 🗃️ Legacy Files
- **`archive_legacy/`** - Archived legacy system files
  - Old fragmented configuration files
  - Problem definition files (now in unified config)
  - Development prototypes and demos

## ✨ Key Benefits of Clean Structure

### 🛡️ Contamination Prevention
- ✅ Automatic memory file selection based on problem
- ✅ Domain-specific content validation  
- ✅ Built-in contamination detection and cleaning
- ✅ Impossible to use wrong memory file

### 🎯 Unified Configuration
- ✅ Single command auto-configures everything
- ✅ LLM capabilities determine feature enablement
- ✅ Problem complexity adjusts all settings
- ✅ No manual coordination needed

### 🔄 Easy Maintenance
- ✅ Single source of truth for configuration
- ✅ Clean separation between problems
- ✅ Archived legacy files for reference
- ✅ No duplicate or conflicting configurations

## 🚀 Getting Started

1. **Choose your research problem**: `direct_proof` or `p_vs_np`
2. **Choose your LLM**: `gpt2-medium`, `phi2`, `gemini`, etc.
3. **Run**: `python pocketresearcher_v2.py [problem] [llm]`
4. **The system automatically**:
   - Loads correct memory file
   - Configures content filtering for domain
   - Enables appropriate features for LLM
   - Validates memory consistency
   - Prevents contamination

## 🔧 Configuration Options

The unified system automatically configures based on:

- **LLM Type**: Local models disable API features, enable offline capabilities
- **Problem Complexity**: Complex problems get higher content thresholds
- **Domain**: Number theory vs complexity theory get different keywords
- **Capabilities**: Formal proofs enabled based on LLM reasoning ability

All configuration is handled automatically - no manual setup required!

## 📈 Next Steps

The project is now clean and ready for:
- Adding new problem domains to `config_unified.py`
- Adding new LLM profiles with automatic capability detection
- Extending formal proof capabilities
- Research iteration and discovery

---

*Clean, unified, and contamination-free research system ready for advanced mathematical discovery!* 🎉
