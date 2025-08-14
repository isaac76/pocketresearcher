"""
LLM Manager - Unified interface for multiple language models with rate limiting
"""
import time
from collections import deque
from typing import Optional, Dict, Any
import sys
import os

# LLM configuration (can be overridden by passing config to LLMManager)
DEFAULT_CONFIG = {
    "GEMINI_API_KEY": None,
    "GEMINI_RATE_LIMIT": 15,
    "OPENAI_RATE_LIMIT": 60,
    "LOCAL_MODELS": {
        "phi2": "microsoft/phi-2",
        "gpt2": "gpt2",
        "gpt2-medium": "gpt2-medium",
        "gpt2-large": "gpt2-large"
    },
    "FALLBACK_LOCAL_MODEL": "gpt2",
    "MAX_TOKENS": 100,
    "TEMPERATURE": 0.7,
    "VERBOSE_OUTPUT": True,
    "ENABLE_RATE_LIMITING": True,
    "LOG_API_CALLS": False
}


# Conditional imports based on availability
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not available. Install with: pip install google-generativeai")

try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    print("Warning: anthropic not available. Install with: pip install anthropic")

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers not available. Install with: pip install transformers")

class RateLimiter:
    """Simple rate limiter using a sliding window"""
    def __init__(self, max_requests: int, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def can_make_request(self) -> bool:
        """Check if we can make a request without exceeding rate limit"""
        now = time.time()
        # Remove old requests outside the time window
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()
        
        return len(self.requests) < self.max_requests
    
    def record_request(self):
        """Record that a request was made"""
        self.requests.append(time.time())
    
    def wait_if_needed(self):
        """Wait if necessary to respect rate limits"""
        if not self.can_make_request():
            # Calculate how long to wait
            oldest_request = self.requests[0]
            wait_time = (oldest_request + self.time_window) - time.time()
            if wait_time > 0:
                if self.config.get("VERBOSE_OUTPUT", True):
                    print(f"Rate limit reached. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time + 0.1)  # Add small buffer

class LLMManager:
    """Unified manager for multiple LLM backends"""
    
    def __init__(self, preferred_model: str = None, config: dict = None):
        # Use provided config or default
        self.config = config or DEFAULT_CONFIG
        self.preferred_model = preferred_model or "gpt2-medium"
        self.current_model = None
        self.local_pipeline = None
        
        # Rate limiters for different APIs
        self.rate_limiters = {
            "gemini": RateLimiter(self.config.get("GEMINI_RATE_LIMIT", 15)),
            "openai": RateLimiter(self.config.get("OPENAI_RATE_LIMIT", 60))
        }
        
        # Initialize the preferred model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the preferred model or fallback to available ones"""
        if self.preferred_model == "gemini" and self._init_gemini():
            self.current_model = "gemini"
        elif self.preferred_model == "claude-sonnet" and self._init_claude():
            self.current_model = "claude-sonnet"
        elif self.preferred_model in self.config.get("LOCAL_MODELS", {}) and self._init_local_model(self.preferred_model):
            self.current_model = self.preferred_model
        else:
            # Try fallback options
            fallback_model = self.config.get("FALLBACK_LOCAL_MODEL", "gpt2")
            if self._init_local_model(fallback_model):
                self.current_model = fallback_model
                print(f"Falling back to local model: {fallback_model}")
            else:
                print("❌ No available models found!")
                sys.exit(1)

    def _init_claude(self) -> bool:
        """Initialize Anthropic Claude Sonnet API"""
        api_key = self.config.get("CLAUDE_API_KEY") or self.config.get("ANTHROPIC_API_KEY")
        if not CLAUDE_AVAILABLE:
            print("[Claude Init] anthropic package not available.")
            return False
        if not api_key:
            print("[Claude Init] No Claude API key found in config.")
            return False
        try:
            self.claude_client = anthropic.Anthropic(api_key=api_key)
            if self.config.get("VERBOSE_OUTPUT", True):
                print("✓ Claude Sonnet API initialized")
            return True
        except Exception as e:
            print(f"Failed to initialize Claude Sonnet: {e}")
            return False
    
    def _init_gemini(self) -> bool:
        """Initialize Gemini API"""
        api_key = self.config.get("GEMINI_API_KEY")
        if not GEMINI_AVAILABLE:
            print("[Gemini Init] google-generativeai package not available.")
            return False
        if not api_key:
            print("[Gemini Init] No Gemini API key found in config.")
            return False
        try:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            if self.config.get("VERBOSE_OUTPUT", True):
                print("✓ Gemini API initialized")
            return True
        except Exception as e:
            print(f"Failed to initialize Gemini: {e}")
            return False
    
    def _init_local_model(self, model_name: str) -> bool:
        """Initialize local transformers model"""
        if not TRANSFORMERS_AVAILABLE or model_name not in self.config.get("LOCAL_MODELS", {}):
            return False
        
        try:
            model_id = self.config.get("LOCAL_MODELS", {})[model_name]
            self.local_pipeline = pipeline(
                "text-generation", 
                model=model_id, 
                max_new_tokens=self.config.get("MAX_TOKENS", 100),
                temperature=self.config.get("TEMPERATURE", 0.7),
                max_length=2048
            )
            if self.config.get("VERBOSE_OUTPUT", True):
                print(f"✓ Local model initialized: {model_id}")
            return True
        except Exception as e:
            print(f"Failed to initialize local model {model_name}: {e}")
            return False
    
    def generate(self, prompt: str, max_tokens: int = None) -> str:
        """Generate text using the current model"""
        max_tokens = max_tokens or self.config.get("MAX_TOKENS", 100)
        if self.current_model == "gemini":
            return self._generate_gemini(prompt, max_tokens)
        elif self.current_model == "claude-sonnet":
            return self._generate_claude(prompt, max_tokens)
        else:
            return self._generate_local(prompt, max_tokens)

    def _generate_claude(self, prompt: str, max_tokens: int) -> str:
        """Generate using Claude Sonnet API"""
        if not hasattr(self, "claude_client"):
            return "Claude client not initialized"
        try:
            if self.config.get("LOG_API_CALLS", False):
                print(f"API Call: Claude Sonnet - {prompt[:50]}...")
            # Claude expects a system prompt and a user message
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=max_tokens,
                temperature=self.config.get("TEMPERATURE", 0.7),
                system="You are a Lean 4 theorem prover assistant. Output only valid Lean 4 code when asked.",
                messages=[{"role": "user", "content": prompt}]
            )
            # Claude API returns a list of content blocks; join them if needed
            if hasattr(response, "content"):
                if isinstance(response.content, list):
                    return "\n".join([c.text for c in response.content if hasattr(c, "text")])
                return str(response.content)
            return str(response)
        except Exception as e:
            print(f"Claude Sonnet API error: {e}")
            return "Error generating response"
    
    def _generate_gemini(self, prompt: str, max_tokens: int) -> str:
        """Generate using Gemini API with rate limiting"""
        if self.config.get("ENABLE_RATE_LIMITING", True):
            self.rate_limiters["gemini"].wait_if_needed()
        
        try:
            if self.config.get("LOG_API_CALLS", False):
                print(f"API Call: Gemini - {prompt[:50]}...")
            
            response = self.gemini_model.generate_content(prompt)
            
            if self.config.get("ENABLE_RATE_LIMITING", True):
                self.rate_limiters["gemini"].record_request()
            
            return response.text
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fallback to local model
            fallback_model = self.config.get("FALLBACK_LOCAL_MODEL", "gpt2")
            if self._init_local_model(fallback_model):
                self.current_model = fallback_model
                print(f"Falling back to local model: {fallback_model}")
                return self._generate_local(prompt, max_tokens)
            else:
                return "Error generating response"
    
    def _generate_local(self, prompt: str, max_tokens: int) -> str:
        """Generate using local transformers model"""
        if not self.local_pipeline:
            return "Local model not available"
        
        try:
            if self.config.get("LOG_API_CALLS", False):
                print(f"Local Call: {self.current_model} - {prompt[:50]}...")
            
            result = self.local_pipeline(prompt, max_new_tokens=max_tokens)
            text = result[0]["generated_text"]
            
            # Remove the prompt from the result
            if text.startswith(prompt):
                text = text[len(prompt):].strip()
            
            return text
            
        except Exception as e:
            print(f"Local model error: {e}")
            return "Error generating response"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        model_type = "api" if self.current_model in ["gemini", "claude-sonnet"] else "local"
        rate_limited = self.config.get("ENABLE_RATE_LIMITING", True) and self.current_model in ["gemini", "claude-sonnet"]
        return {
            "current_model": self.current_model,
            "preferred_model": self.preferred_model,
            "model_type": model_type,
            "rate_limited": rate_limited
        }
    
    def switch_model(self, model_name: str) -> bool:
        """Switch to a different model"""
        old_model = self.current_model
        self.preferred_model = model_name
        
        try:
            self._initialize_model()
            if self.config.get("VERBOSE_OUTPUT", True):
                print(f"Switched from {old_model} to {self.current_model}")
            return True
        except Exception as e:
            print(f"Failed to switch to {model_name}: {e}")
            # Restore previous model
            self.preferred_model = old_model
            self.current_model = old_model
            return False
