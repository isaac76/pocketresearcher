# PocketResearcher Unified Configuration System
# 
# This unified config automatically configures all aspects of the system
# based on LLM choice and problem selection.

import os
from typing import Dict, Any, Optional

# =============================================================================
# LLM PROFILES - Self-configuring based on model capabilities
# =============================================================================

LLM_PROFILES = {
    "gemini": {
        "api_key": "<key>",  # Your actual key
        "type": "api",
        "rate_limit": 15,
        "max_tokens": 100,
        "supports_complex_reasoning": True,
        "enable_lean_translation": False,  # Disabled to avoid quota issues
        "fallback_model": "gpt2-medium"
    },
    "gpt2": {
        "model_path": "gpt2",
        "type": "local",
        "max_tokens": 100,
        "supports_complex_reasoning": False,
        "enable_lean_translation": False,  # Local model, use pattern matching
        "fallback_model": None
    },
    "gpt2-medium": {
        "model_path": "gpt2-medium",
        "type": "local", 
        "max_tokens": 100,
        "supports_complex_reasoning": True,
        "enable_lean_translation": False,  # Local model, use pattern matching
        "fallback_model": "gpt2"
    },
    "phi2": {
        "model_path": "microsoft/phi-2",
        "type": "local",
        "max_tokens": 100,
        "supports_complex_reasoning": True,
        "enable_lean_translation": False,  # Local model, use pattern matching
        "fallback_model": "gpt2"
    }
}

# =============================================================================
# PROBLEM DEFINITIONS - All problem configs in one place
# =============================================================================

PROBLEM_DEFINITIONS = {
    "p_vs_np": {
        "name": "P vs NP",
        "memory_file": "memory-pvnp.json",
        "complexity": "high",
        "domain": "complexity_theory",
        "initial_facts": [
            "P = NP is one of the seven Millennium Prize Problems in mathematics.",
            "P is the class of problems solvable in polynomial time by a deterministic Turing machine.",
            "NP is the class of problems for which a solution can be verified in polynomial time by a deterministic Turing machine.",
            "It is unknown whether P = NP or P != NP; neither has been proven.",
            "Many important problems, such as SAT and 3-SAT, are NP-complete.",
            "If any NP-complete problem can be solved in polynomial time, then P = NP.",
            "No polynomial-time algorithm is known for any NP-complete problem.",
            "Attempts to prove P != NP include diagonalization, circuit complexity, and relativization techniques.",
            "Baker-Gill-Solovay theorem shows that relativization techniques cannot resolve P vs NP.",
            "Natural proofs barrier (Razborov-Rudich) limits certain types of circuit lower bounds."
        ],
        "initial_ideas": [
            "Try to find a polynomial-time algorithm for SAT or 3-SAT.",
            "Investigate circuit complexity lower bounds for NP-complete problems.",
            "Explore diagonalization arguments to separate P from NP.",
            "Consider the role of oracles and relativization in previous proofs.",
            "Analyze the limitations of current proof techniques and seek new approaches."
        ],
        "fact_prompt_template": "P vs NP complexity theory. Recent research: {recent_fact}. New fact: ",
        "idea_prompt_template": "Complexity theory research ideas. Previous approaches: {recent_idea}. New research idea: ",
        "content_filter_config": {
            "min_mathematical_relevance": 0.3,  # High threshold for complex problems
            "min_length": 15,
            "max_length": 1000,
            "allow_simple_statements": False,
            "domain_keywords": ["complexity", "polynomial", "NP", "algorithm", "proof", "class", "reduction", "SAT"]
        }
    },
    
    "direct_proof": {
        "name": "Even Sum",
        "memory_file": "memory-even-proof.json", 
        "complexity": "low",
        "domain": "number_theory",
        "initial_facts": [
            "An even number is defined as an integer that is divisible by 2.",
            "Even numbers can be written in the form 2k, where k is an integer.",
            "Addition is a binary operation on integers.",
            "The sum of two integers is also an integer.",
            "Odd numbers are integers not divisible by 2."
        ],
        "initial_ideas": [
            "To prove that the sum of two even numbers is even we can try to form an algebraic expression."
        ],
        "fact_prompt_template": "Number theory. Recent fact: {recent_fact}. State a new fact about even numbers or their sums:",
        "idea_prompt_template": "Number theory research ideas. Previous approach: {recent_idea}. Suggest a new idea for proving properties of even numbers:",
        "content_filter_config": {
            "min_mathematical_relevance": 0.1,  # Lower threshold for basic problems
            "min_length": 10,
            "max_length": 500,
            "allow_simple_statements": True,
            "domain_keywords": ["even", "odd", "number", "integer", "sum", "addition", "proof", "algebra"]
        }
    }
}

# =============================================================================
# UNIFIED CONFIGURATION CLASS
# =============================================================================

class UnifiedConfig:
    """
    Unified configuration that automatically adapts based on LLM and problem choices.
    """
    
    def __init__(self, llm_name: str = "gpt2-medium", problem_name: str = "direct_proof"):
        self.llm_name = llm_name
        self.problem_name = problem_name
        
        # Load LLM profile
        if llm_name not in LLM_PROFILES:
            raise ValueError(f"Unknown LLM: {llm_name}. Available: {list(LLM_PROFILES.keys())}")
        self.llm_profile = LLM_PROFILES[llm_name]
        
        # Load problem definition  
        if problem_name not in PROBLEM_DEFINITIONS:
            raise ValueError(f"Unknown problem: {problem_name}. Available: {list(PROBLEM_DEFINITIONS.keys())}")
        self.problem_def = PROBLEM_DEFINITIONS[problem_name]
        
        # Configure all settings
        self._configure_llm_settings()
        self._configure_problem_settings()
        self._configure_formal_proof_settings()
        self._configure_research_settings()
    
    def _configure_llm_settings(self):
        """Configure LLM-specific settings"""
        self.DEFAULT_LLM = self.llm_name
        self.LLM_TYPE = self.llm_profile["type"]
        
        if self.LLM_TYPE == "api":
            self.GEMINI_API_KEY = self.llm_profile["api_key"]
            self.ENABLE_RATE_LIMITING = True
            self.RATE_LIMIT = self.llm_profile["rate_limit"]
        else:
            self.GEMINI_API_KEY = None
            self.ENABLE_RATE_LIMITING = False
            self.RATE_LIMIT = None
            
        self.MAX_TOKENS = self.llm_profile["max_tokens"]
        self.FALLBACK_LOCAL_MODEL = self.llm_profile.get("fallback_model", "gpt2")
    
    def _configure_problem_settings(self):
        """Configure problem-specific settings"""
        self.PROBLEM_NAME = self.problem_def["name"]
        self.MEMORY_FILE = self.problem_def["memory_file"]
        self.PROBLEM_COMPLEXITY = self.problem_def["complexity"]
        self.PROBLEM_DOMAIN = self.problem_def["domain"]
        
        self.INITIAL_FACTS = self.problem_def["initial_facts"]
        self.INITIAL_IDEAS = self.problem_def["initial_ideas"]
        self.FACT_PROMPT = self.problem_def["fact_prompt_template"]
        self.IDEA_PROMPT = self.problem_def["idea_prompt_template"]
        
        self.CONTENT_FILTER_CONFIG = self.problem_def["content_filter_config"]
    
    def _configure_formal_proof_settings(self):
        """Configure formal proof settings based on LLM capabilities"""
        # Enable Lean translation only if LLM supports it AND has valid API key
        api_available = (self.LLM_TYPE == "api" and 
                        self.GEMINI_API_KEY and 
                        self.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE")
        
        self.ENABLE_LEAN_TRANSLATION = (
            self.llm_profile["enable_lean_translation"] and api_available
        )
        
        # Adjust proof generation frequency based on problem complexity
        if self.PROBLEM_COMPLEXITY == "high":
            self.PROOF_GENERATION_FREQUENCY = 5  # Less frequent for complex problems
        else:
            self.PROOF_GENERATION_FREQUENCY = 3  # More frequent for simple problems
            
        # Enable formal proofs if we have reasoning capability
        self.ENABLE_FORMAL_PROOFS = self.llm_profile["supports_complex_reasoning"]
    
    def _configure_research_settings(self):
        """Configure research-specific settings"""
        self.TEMPERATURE = 0.7
        self.VERBOSE_OUTPUT = True
        self.LOG_API_CALLS = False
        
        # Adjust generation parameters based on problem complexity
        if self.PROBLEM_COMPLEXITY == "high":
            self.TEMPERATURE = 0.8  # More creativity for hard problems
        else:
            self.TEMPERATURE = 0.6  # More deterministic for simple problems
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration dictionary for backwards compatibility"""
        return {
            "gemini": {
                "api_key": "GEMINI_API_KEY",
                "rate_limit": self.RATE_LIMIT or 15,
                "max_tokens": self.MAX_TOKENS
            },
            self.llm_name: self.llm_profile
        }
    
    def summary(self) -> str:
        """Get a summary of current configuration"""
        return f"""
🤖 LLM: {self.llm_name} ({self.LLM_TYPE})
🧮 Problem: {self.PROBLEM_NAME} ({self.PROBLEM_COMPLEXITY} complexity)
🔧 Lean Translation: {'✅' if self.ENABLE_LEAN_TRANSLATION else '❌'}
📝 Formal Proofs: {'✅' if self.ENABLE_FORMAL_PROOFS else '❌'}
⚡ Rate Limiting: {'✅' if self.ENABLE_RATE_LIMITING else '❌'}
📊 Proof Frequency: Every {self.PROOF_GENERATION_FREQUENCY} iterations
🎛️  Temperature: {self.TEMPERATURE}
💾 Memory File: {self.MEMORY_FILE}
        """.strip()

# =============================================================================
# EASY ACCESS FUNCTIONS
# =============================================================================

def create_config(llm: str = "gpt2-medium", problem: str = "direct_proof") -> UnifiedConfig:
    """Create a unified configuration with automatic settings"""
    return UnifiedConfig(llm, problem)

def list_available_llms():
    """List all available LLM options"""
    return list(LLM_PROFILES.keys())

def list_available_problems():
    """List all available problem definitions"""
    return list(PROBLEM_DEFINITIONS.keys())

# =============================================================================
# BACKWARDS COMPATIBILITY - Export key variables for existing code
# =============================================================================

# Create default configuration (can be overridden by importing code)
_default_config = create_config("gpt2-medium", "direct_proof")

# Export key variables for backwards compatibility
DEFAULT_LLM = _default_config.DEFAULT_LLM
GEMINI_API_KEY = _default_config.GEMINI_API_KEY
ENABLE_LEAN_TRANSLATION = _default_config.ENABLE_LEAN_TRANSLATION
ENABLE_RATE_LIMITING = _default_config.ENABLE_RATE_LIMITING
PROOF_GENERATION_FREQUENCY = _default_config.PROOF_GENERATION_FREQUENCY
LLM_CONFIG = _default_config.get_llm_config()
MAX_TOKENS = _default_config.MAX_TOKENS
TEMPERATURE = _default_config.TEMPERATURE
FALLBACK_LOCAL_MODEL = _default_config.FALLBACK_LOCAL_MODEL
VERBOSE_OUTPUT = _default_config.VERBOSE_OUTPUT
LOG_API_CALLS = _default_config.LOG_API_CALLS

# Export for problem access
CURRENT_PROBLEM_CONFIG = _default_config

if __name__ == "__main__":
    # Example usage and testing
    print("=== Testing Unified Configuration ===")
    
    # Test different combinations
    configs = [
        ("gemini", "p_vs_np"),
        ("gpt2-medium", "direct_proof"),
        ("phi2", "p_vs_np")
    ]
    
    for llm, problem in configs:
        print(f"\n--- {llm} + {problem} ---")
        try:
            config = create_config(llm, problem)
            print(config.summary())
        except Exception as e:
            print(f"Error: {e}")
