#!/usr/bin/env python3
"""
Enhanced PocketResearcher with Unified Configuration System

Usage:
    python pocketresearcher_unified.py [problem] [llm]
    
Examples:
    python pocketresearcher_unified.py direct_proof gpt2-medium
    python pocketresearcher_unified.py p_vs_np gemini
    python pocketresearcher_unified.py                    # Uses defaults
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_unified import create_config, list_available_llms, list_available_problems

def main():
    # Parse command line arguments
    problem = "direct_proof"  # default
    llm = "gpt2-medium"       # default
    
    if len(sys.argv) >= 2:
        problem = sys.argv[1]
    if len(sys.argv) >= 3:
        llm = sys.argv[2]
    
    # Handle help
    if problem in ["-h", "--help", "help"]:
        print(__doc__)
        print(f"Available problems: {', '.join(list_available_problems())}")
        print(f"Available LLMs: {', '.join(list_available_llms())}")
        return
    
    # Create unified configuration
    try:
        config = create_config(llm, problem)
        print("🔧 Unified Configuration Loaded")
        print(config.summary())
        print()
        
        # Now run the research system with this configuration
        run_research_system(config)
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print(f"Available problems: {', '.join(list_available_problems())}")
        print(f"Available LLMs: {', '.join(list_available_llms())}")
        return 1

def run_research_system(config):
    """Run the research system with the given configuration"""
    
    # Import research modules with the unified config
    from src.memory import Memory
    from src.content_filter import ContentFilter
    from src.formal_proof_engine import FormalProofEngine
    from src.proof_assistant import MathProofAssistant
    from src.breakthrough_detector import BreakthroughDetector
    
    # This would replace the old pocketresearcher.py logic
    print("🚀 Starting PocketResearcher with unified configuration...")
    print(f"📁 Problem: {config.PROBLEM_NAME}")
    print(f"🤖 LLM: {config.llm_name} ({config.LLM_TYPE})")
    print(f"💾 Memory: {config.MEMORY_FILE}")
    print(f"🔧 Lean Translation: {'Enabled' if config.ENABLE_LEAN_TRANSLATION else 'Disabled'}")
    print()
    
    # Initialize components with unified config
    memory_config = {"file_path": config.MEMORY_FILE, "backend": "file"}
    memory_store = Memory(memory_config)
    memory = memory_store.load()  # Load the actual memory data as dict
    content_filter = ContentFilter(config=config.CONTENT_FILTER_CONFIG)
    
    # Initialize formal proof engine based on config
    api_key = config.GEMINI_API_KEY if config.ENABLE_LEAN_TRANSLATION else None
    formal_engine = FormalProofEngine(api_key=api_key)
    
    proof_assistant = MathProofAssistant()
    breakthrough_detector = BreakthroughDetector()
    
    # Initialize memory if empty
    if not memory.get("facts"):
        print("🔄 Initializing memory with problem-specific content...")
        memory.setdefault("facts", []).extend(config.INITIAL_FACTS)
        memory.setdefault("ideas", []).extend(config.INITIAL_IDEAS)
        memory_store.save(memory)  # Save the initialized memory
        print(f"✅ Initialized with {len(config.INITIAL_FACTS)} facts and {len(config.INITIAL_IDEAS)} ideas")
    
    # This is where the main research loop would go
    # For now, just show that everything is configured correctly
    
    print("✅ All components initialized successfully!")
    print("🔬 Ready to begin research...")
    
    # Import and run the actual research logic
    try:
        # Use the existing research logic but with our unified config
        print("🏃 Running research iteration...")
        
        # This is a simplified version - the full implementation would
        # integrate the existing research loop from pocketresearcher.py
        
        print("💡 Research system configured and ready!")
        print("ℹ️  To run actual research, integrate this with the existing pocketresearcher.py logic")
        
    except Exception as e:
        print(f"❌ Error during research: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    exit_code = main()
    if exit_code:
        sys.exit(exit_code)
