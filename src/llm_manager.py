"""
LLM Manager - Unified interface for multiple language models with rate limiting
"""
import time
from collections import deque
from typing import Optional, Dict, Any
import sys
import os

# Import config
try:
    import config
except ImportError:
    print("Config file not found. Please copy config_template.py to config.py")
    sys.exit(1)

# Conditional imports based on availability
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not available. Install with: pip install google-generativeai")

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
                if config.VERBOSE_OUTPUT:
                    print(f"Rate limit reached. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time + 0.1)  # Add small buffer

class LLMManager:
    """Unified manager for multiple LLM backends"""
    
    def __init__(self, preferred_model: str = None):
        self.preferred_model = preferred_model or config.DEFAULT_LLM
        self.current_model = None
        self.local_pipeline = None
        
        # Rate limiters for different APIs
        self.rate_limiters = {
            "gemini": RateLimiter(config.GEMINI_RATE_LIMIT),
            "openai": RateLimiter(config.OPENAI_RATE_LIMIT)
        }
        
        # Initialize the preferred model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the preferred model or fallback to available ones"""
        if self.preferred_model == "gemini" and self._init_gemini():
            self.current_model = "gemini"
        elif self.preferred_model in config.LOCAL_MODELS and self._init_local_model(self.preferred_model):
            self.current_model = self.preferred_model
        else:
            # Try fallback options
            if self._init_local_model(config.FALLBACK_LOCAL_MODEL):
                self.current_model = config.FALLBACK_LOCAL_MODEL
                print(f"Falling back to local model: {config.FALLBACK_LOCAL_MODEL}")
            else:
                raise RuntimeError("No LLM backend available")
    
    def _init_gemini(self) -> bool:
        """Initialize Gemini API"""
        if not GEMINI_AVAILABLE or not config.GEMINI_API_KEY:
            return False
        
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            if config.VERBOSE_OUTPUT:
                print("✓ Gemini API initialized")
            return True
        except Exception as e:
            print(f"Failed to initialize Gemini: {e}")
            return False
    
    def _init_local_model(self, model_name: str) -> bool:
        """Initialize local transformers model"""
        if not TRANSFORMERS_AVAILABLE or model_name not in config.LOCAL_MODELS:
            return False
        
        try:
            model_id = config.LOCAL_MODELS[model_name]
            self.local_pipeline = pipeline(
                "text-generation", 
                model=model_id, 
                max_new_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE,
                max_length=2048
            )
            if config.VERBOSE_OUTPUT:
                print(f"✓ Local model initialized: {model_id}")
            return True
        except Exception as e:
            print(f"Failed to initialize local model {model_name}: {e}")
            return False
    
    def generate(self, prompt: str, max_tokens: int = None) -> str:
        """Generate text using the current model"""
        max_tokens = max_tokens or config.MAX_TOKENS
        
        if self.current_model == "gemini":
            return self._generate_gemini(prompt, max_tokens)
        else:
            return self._generate_local(prompt, max_tokens)
    
    def _generate_gemini(self, prompt: str, max_tokens: int) -> str:
        """Generate using Gemini API with rate limiting"""
        if config.ENABLE_RATE_LIMITING:
            self.rate_limiters["gemini"].wait_if_needed()
        
        try:
            if config.LOG_API_CALLS:
                print(f"API Call: Gemini - {prompt[:50]}...")
            
            response = self.gemini_model.generate_content(prompt)
            
            if config.ENABLE_RATE_LIMITING:
                self.rate_limiters["gemini"].record_request()
            
            return response.text
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fallback to local model
            if self._init_local_model(config.FALLBACK_LOCAL_MODEL):
                self.current_model = config.FALLBACK_LOCAL_MODEL
                print(f"Falling back to local model: {config.FALLBACK_LOCAL_MODEL}")
                return self._generate_local(prompt, max_tokens)
            else:
                return "Error generating response"
    
    def _generate_local(self, prompt: str, max_tokens: int) -> str:
        """Generate using local transformers model"""
        if not self.local_pipeline:
            return "Local model not available"
        
        try:
            if config.LOG_API_CALLS:
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
        return {
            "current_model": self.current_model,
            "preferred_model": self.preferred_model,
            "model_type": "api" if self.current_model == "gemini" else "local",
            "rate_limited": config.ENABLE_RATE_LIMITING and self.current_model == "gemini"
        }
    
    def switch_model(self, model_name: str) -> bool:
        """Switch to a different model"""
        old_model = self.current_model
        self.preferred_model = model_name
        
        try:
            self._initialize_model()
            if config.VERBOSE_OUTPUT:
                print(f"Switched from {old_model} to {self.current_model}")
            return True
        except Exception as e:
            print(f"Failed to switch to {model_name}: {e}")
            # Restore previous model
            self.preferred_model = old_model
            self.current_model = old_model
            return False
