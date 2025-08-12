#!/usr/bin/env python3
"""
Demonstration of Unified Configuration System Benefits
"""

from config_unified import create_config

def show_configuration_matrix():
    """Show how different LLM + Problem combinations auto-configure"""
    
    print("=" * 80)
    print("🔧 UNIFIED CONFIGURATION SYSTEM DEMONSTRATION")
    print("=" * 80)
    print()
    
    combinations = [
        ("gemini", "p_vs_np", "🔬 Complex AI research with API model"),
        ("gpt2-medium", "direct_proof", "🧮 Simple math with local model"),
        ("phi2", "p_vs_np", "🚀 Complex research with advanced local model"),
        ("gpt2", "direct_proof", "📚 Basic learning setup")
    ]
    
    for llm, problem, description in combinations:
        print(f"🎯 {description}")
        print(f"   Command: python pocketresearcher_unified.py {problem} {llm}")
        
        try:
            config = create_config(llm, problem)
            
            # Show key auto-configurations
            print(f"   🤖 LLM: {llm} ({config.LLM_TYPE})")
            print(f"   📁 Problem: {config.PROBLEM_NAME} ({config.PROBLEM_COMPLEXITY} complexity)")
            print(f"   🔧 Lean Translation: {'✅' if config.ENABLE_LEAN_TRANSLATION else '❌'}")
            print(f"   ⚡ Rate Limiting: {'✅' if config.ENABLE_RATE_LIMITING else '❌'}")
            print(f"   📊 Proof Frequency: Every {config.PROOF_GENERATION_FREQUENCY} iterations")
            print(f"   🎛️  Temperature: {config.TEMPERATURE}")
            print(f"   🧠 Content Filter: min_relevance={config.CONTENT_FILTER_CONFIG['min_mathematical_relevance']}")
            print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    print("✨ BENEFITS OF UNIFIED CONFIGURATION:")
    print("• 🎯 One command, automatic optimization")
    print("• 🔄 No manual sync between LLM and problem settings")
    print("• 🛡️  Automatic fallbacks and compatibility checks")
    print("• 📊 Problem-complexity-aware settings")
    print("• 🔧 LLM-capability-aware feature enablement")
    print("• 💾 Centralized configuration management")
    print()
    
    print("🔄 BEFORE (fragmented):")
    print("  config.py → DEFAULT_LLM + ENABLE_LEAN_TRANSLATION")
    print("  p_vs_np.py → CONTENT_FILTER_CONFIG + INITIAL_FACTS")
    print("  direct_proof.py → Different CONTENT_FILTER_CONFIG")
    print("  Manual coordination required!")
    print()
    
    print("✅ AFTER (unified):")
    print("  config_unified.py → Everything auto-configured")
    print("  Single source of truth")
    print("  Automatic optimization based on LLM + Problem")
    print()

if __name__ == "__main__":
    show_configuration_matrix()
