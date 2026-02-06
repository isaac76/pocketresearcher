"""
Simple LLM Manager for Local Models

Handles local transformer models (gpt2, gpt2-medium, phi2) without API dependencies.
"""

import sys
import os
import glob

try:
    from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠ Warning: transformers not available. Install with: pip install transformers torch")


class LocalLLM:
    """Manager for local transformer models"""
    
    # Available local models
    MODELS = {
        "gpt2": "gpt2",
        "gpt2-medium": "gpt2-medium",
        "gpt2-large": "gpt2-large",
        "phi2": "microsoft/phi-2"
    }
    
    def __init__(self, model_name: str = "gpt2-medium", max_tokens: int = 150, temperature: float = 0.7):
        """
        Initialize local LLM
        
        Args:
            model_name: Name of the model to use (gpt2, gpt2-medium, gpt2-large, phi2)
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
        """
        if not TRANSFORMERS_AVAILABLE:
            print("✗ Transformers library not available!")
            sys.exit(1)
        
        if model_name not in self.MODELS:
            print(f"✗ Unknown model: {model_name}")
            print(f"Available models: {', '.join(self.MODELS.keys())}")
            sys.exit(1)
        
        self.model_name = model_name
        self.model_id = self.MODELS[model_name]
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.pipeline = None
        
        self._initialize()
    
    def _initialize(self):
        """Initialize the transformer pipeline"""
        print(f"🤖 Initializing {self.model_name}...")
        
        # For phi-2, try to find the cached snapshot directly
        if self.model_name == "phi2":
            try:
                # Find the snapshot directory
                cache_dir = os.path.expanduser("~/.cache/huggingface/hub/models--microsoft--phi-2/snapshots")
                snapshots = glob.glob(os.path.join(cache_dir, "*"))
                
                if snapshots:
                    snapshot_path = snapshots[0]  # Use the first (should be only) snapshot
                    print(f"   Found cached model at: {snapshot_path}")
                    
                    # Load with trust_remote_code to get custom tokenizer
                    tokenizer = AutoTokenizer.from_pretrained(
                        snapshot_path,
                        trust_remote_code=True,
                        local_files_only=True
                    )
                    model = AutoModelForCausalLM.from_pretrained(
                        snapshot_path,
                        trust_remote_code=True,
                        local_files_only=True,
                        torch_dtype="auto"
                    )
                    
                    self.pipeline = pipeline(
                        "text-generation",
                        model=model,
                        tokenizer=tokenizer,
                        max_new_tokens=self.max_tokens,
                        temperature=self.temperature,
                        device=-1
                    )
                    print(f"✓ {self.model_name} ready (from local cache)")
                    return
                else:
                    raise Exception("Cached model not found")
                    
            except Exception as e:
                print(f"✗ Failed to load phi2 from cache: {e}")
                print("   Phi2 may need additional dependencies or config files")
                print("   Try using gpt2-medium instead: python3 src/pocketresearcher.py gpt2-medium")
                sys.exit(1)
        
        # For other models, use standard pipeline
        try:
            self.pipeline = pipeline(
                "text-generation",
                model=self.model_id,
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                device=-1,
                trust_remote_code=True
            )
            print(f"✓ {self.model_name} ready")
        except Exception as e:
            print(f"✗ Failed to initialize {self.model_name}: {e}")
            sys.exit(1)
    
    def generate(self, prompt: str, max_tokens: int = None) -> str:
        """
        Generate text from a prompt
        
        Args:
            prompt: Input prompt for the model
            max_tokens: Override default max_tokens if provided
        
        Returns:
            Generated text (with prompt removed)
        """
        if not self.pipeline:
            return "Error: Model not initialized"
        
        tokens = max_tokens or self.max_tokens
        
        try:
            result = self.pipeline(
                prompt,
                max_new_tokens=tokens,
                do_sample=True,
                temperature=self.temperature,
                pad_token_id=self.pipeline.tokenizer.eos_token_id
            )
            
            # Extract generated text
            generated = result[0]["generated_text"]
            
            # Remove the prompt from the result
            if generated.startswith(prompt):
                generated = generated[len(prompt):].strip()
            
            return generated
            
        except Exception as e:
            print(f"✗ Error generating text: {e}")
            return ""
    
    def get_info(self) -> dict:
        """Get information about the current model"""
        return {
            "model_name": self.model_name,
            "model_id": self.model_id,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }


# Simple test
if __name__ == "__main__":
    print("Testing LocalLLM\n")
    
    # Initialize model
    llm = LocalLLM("gpt2-medium", max_tokens=50)
    
    # Test generation
    prompt = "The proof that there is no largest natural number:"
    print(f"Prompt: {prompt}")
    print(f"Generating...\n")
    
    response = llm.generate(prompt)
    print(f"Response: {response}")
    
    # Show model info
    print(f"\nModel Info: {llm.get_info()}")
