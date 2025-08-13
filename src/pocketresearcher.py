#!/usr/bin/env python3
"""
PocketResearcher with Integrated Unified Configuration System

This version automatically configures all settings based on LLM and problem choice,
preventing configuration errors and memory file contamination.

Usage:
    python src/pocketresearcher.py [problem] [llm]
    
Examples:
    python src/pocketresearcher.py direct_proof gpt2-medium
    python src/pocketresearcher.py p_vs_np gemini
"""

import sys
import os
import datetime
import json
from datetime import datetime

# Add project root to path (since we're now in src/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config_unified import create_config, list_available_llms, list_available_problems

def main():
    """Main entry point with unified configuration"""
    
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
        print("🔧 Unified Configuration Active")
        print(config.summary())
        print()
        
        # Run research with unified config
        run_research_loop(config)
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print(f"Available problems: {', '.join(list_available_problems())}")
        print(f"Available LLMs: {', '.join(list_available_llms())}")
        return 1

def run_research_loop(config):
    """Run the main research loop with unified configuration"""
    
    # Import all required modules
    from memory import Memory
    from content_filter import ContentFilter
    from formal_proof_engine import FormalProofEngine
    from proof_assistant import MathProofAssistant
    from breakthrough_detector import BreakthroughDetector
    from quality_assessor import ProofQualityAssessor
    from llm_manager import LLMManager
    
    print("🚀 Starting PocketResearcher v2 with Unified Configuration")
    print(f"📁 Problem: {config.PROBLEM_NAME}")
    print(f"🤖 LLM: {config.llm_name} ({config.LLM_TYPE})")
    print(f"💾 Memory: {config.MEMORY_FILE}")
    print(f"🔧 Lean Translation: {'Enabled' if config.ENABLE_LEAN_TRANSLATION else 'Disabled'}")
    print()
    
    # Initialize all components with unified config
    memory_store = Memory({"file_path": config.MEMORY_FILE, "backend": "file"})
    memory = memory_store.load()

    # Validate memory file matches problem (CRITICAL FIX!)
    validate_memory_consistency(memory, config)

    content_filter = ContentFilter(config=config.CONTENT_FILTER_CONFIG)
    print(f"⚙️  Content filter configured for {config.PROBLEM_DOMAIN}")
    print(f"   - Min relevance: {config.CONTENT_FILTER_CONFIG['min_mathematical_relevance']}")

    # Initialize LLM with unified config and pass all relevant settings
    llm_manager = LLMManager(
        config.DEFAULT_LLM,
        config={
            "GEMINI_API_KEY": config.GEMINI_API_KEY,
            "GEMINI_RATE_LIMIT": config.RATE_LIMIT,
            "LOCAL_MODELS": {
                "phi2": "microsoft/phi-2",
                "gpt2": "gpt2",
                "gpt2-medium": "gpt2-medium",
                "gpt2-large": "gpt2-large"
            },
            "FALLBACK_LOCAL_MODEL": config.FALLBACK_LOCAL_MODEL,
            "MAX_TOKENS": config.MAX_TOKENS,
            "TEMPERATURE": config.TEMPERATURE,
            "VERBOSE_OUTPUT": config.VERBOSE_OUTPUT,
            "ENABLE_RATE_LIMITING": config.ENABLE_RATE_LIMITING,
            "LOG_API_CALLS": config.LOG_API_CALLS
        }
    )

    # Initialize formal proof engine
    api_key = config.GEMINI_API_KEY if config.ENABLE_LEAN_TRANSLATION else None
    formal_engine = FormalProofEngine(api_key=api_key)

    proof_assistant = MathProofAssistant()
    breakthrough_detector = BreakthroughDetector()
    quality_assessor = ProofQualityAssessor()

    # Special debug mode for phi2: do not update memory file, only log to console
    phi2_debug = getattr(config.llm_profile, 'debug_only', False) or config.llm_name == 'phi2' or config.llm_profile.get('disable_memory_update', False)

    # Prevent any modifications if memory is marked complete
    if memory.get("complete", False):
        print("🚩 Problem is marked as complete. No further changes will be made to the database.")
        return
    
    # Initialize memory if empty or contaminated
    if not memory.get("facts") or len(memory.get("facts", [])) == 0:
        print("🔄 Initializing memory with problem-specific content...")
        memory["facts"] = config.INITIAL_FACTS.copy()
        memory["ideas"] = config.INITIAL_IDEAS.copy()
        memory_store.save(memory)
        print(f"✅ Initialized with {len(config.INITIAL_FACTS)} facts and {len(config.INITIAL_IDEAS)} ideas")
    
    print(f"🗂️  Loaded memory: {len(memory.get('facts', []))} facts, {len(memory.get('ideas', []))} ideas")
    print()
    
    # Main research iteration
    try:
        print("🔬 Running research iteration...")
        result = run_single_research_step(memory, config, llm_manager, content_filter, 
                                        formal_engine, proof_assistant, breakthrough_detector, quality_assessor)

        # Check if research step failed due to LLM quota errors
        if "LLM quota/API error" in result:
            print("❌ Research iteration failed due to LLM quota/API errors.")
            return

        if phi2_debug:
            print("[phi2 debug mode] Results (not saved to memory file):")
            print(result)
            print(f"[phi2 debug mode] Would have saved: {len(memory.get('facts', []))} facts, {len(memory.get('ideas', []))} ideas")
        else:
            # Save updated memory
            memory_store.save(memory)
            print(f"💾 Memory saved: {len(memory.get('facts', []))} facts, {len(memory.get('ideas', []))} ideas")
            # Log the result
            log_research_step(result, config)
            print("✅ Research iteration completed successfully!")

    except Exception as e:
        print(f"❌ Error during research: {e}")
        import traceback
        traceback.print_exc()

def validate_memory_consistency(memory, config):
    """Validate that memory content matches the expected problem domain"""
    
    print("🔍 Validating memory consistency...")
    
    # Check for cross-contamination
    domain_keywords = config.CONTENT_FILTER_CONFIG.get('domain_keywords', [])
    wrong_domain_content = []
    
    # Check facts for wrong domain content
    for fact in memory.get('facts', []):
        fact_lower = fact.lower()
        
        # Look for P vs NP content in non-P-vs-NP problems
        if config.problem_name == 'direct_proof':
            pnp_indicators = ['np-complete', 'polynomial time', 'sat', 'complexity theory', 'p vs np', 'p = np']
            if any(indicator in fact_lower for indicator in pnp_indicators):
                wrong_domain_content.append(f"Fact: {fact[:50]}...")
        
        # Look for number theory content in P vs NP problems
        elif config.problem_name == 'p_vs_np':
            number_theory_indicators = ['even number', 'odd number', '2k where k', 'divisible by 2']
            if any(indicator in fact_lower for indicator in number_theory_indicators):
                wrong_domain_content.append(f"Fact: {fact[:50]}...")
    
    # Check ideas for wrong domain content
    for idea in memory.get('ideas', []):
        idea_lower = idea.lower()
        
        if config.problem_name == 'direct_proof':
            pnp_indicators = ['np-complete', 'polynomial time', 'sat', 'complexity theory']
            if any(indicator in idea_lower for indicator in pnp_indicators):
                wrong_domain_content.append(f"Idea: {idea[:50]}...")
    
    # Check formal proofs for wrong domain content
    for i, proof in enumerate(memory.get('formal_proofs', [])):
        proof_text = str(proof).lower()
        
        if config.problem_name == 'direct_proof':
            pnp_indicators = ['np-complete', 'polynomial time', 'sat', 'complexity theory', 'p vs np', 'p = np', 'p ⊆ np', 'p \\u2286 np', 'p_subset_np']
            if any(indicator in proof_text for indicator in pnp_indicators):
                proof_name = proof.get('theorem_name', f'Proof {i}')
                wrong_domain_content.append(f"Formal Proof: {proof_name}...")
        
        elif config.problem_name == 'p_vs_np':
            number_theory_indicators = ['even number', 'odd number', '2k where k', 'divisible by 2']
            if any(indicator in proof_text for indicator in number_theory_indicators):
                proof_name = proof.get('theorem_name', f'Proof {i}')
                wrong_domain_content.append(f"Formal Proof: {proof_name}...")
    
    if wrong_domain_content:
        print(f"⚠️  WARNING: Memory contamination detected!")
        print(f"   Problem: {config.PROBLEM_NAME}")
        print(f"   Memory file: {config.MEMORY_FILE}")
        print("   Contaminated content:")
        for content in wrong_domain_content[:3]:  # Show first 3
            print(f"     - {content}")
        
        response = input("🧹 Clean memory file? (y/N): ")
        if response.lower() == 'y':
            clean_memory_file(memory, config)
            print("✅ Memory cleaned!")
        else:
            print("⚠️  Continuing with contaminated memory...")
    else:
        print("✅ Memory content matches expected problem domain")

def clean_memory_file(memory, config):
    """Clean memory file and reinitialize with correct content"""
    
    # Keep only domain-appropriate content
    clean_memory = {
        "facts": config.INITIAL_FACTS.copy(),
        "ideas": config.INITIAL_IDEAS.copy(),
        "reflections": [],
        "proofs": [],
        "techniques": [],
        "experiments": [],
        "formal_proofs": []
    }
    
    # Update the memory dict in place
    memory.clear()
    memory.update(clean_memory)

def extract_meaningful_content(generated_text: str, content_type: str) -> str:
    """
    Extract meaningful mathematical content from LLM output.
    Handles various formats like "Solution 0:", "Problem:", etc.
    """
    if not generated_text:
        return ""
    
    lines = generated_text.strip().split('\n')
    
    # Filter out common prefixes that aren't useful
    skip_patterns = [
        "solution", "problem", "answer", "step", "example", "note", 
        "possible rewrite", "rewrite", "question", "hint"
    ]
    
    # Look for lines that contain mathematical content
    mathematical_keywords = [
        "even", "odd", "number", "integer", "sum", "addition", "proof", 
        "algebra", "divisible", "remainder", "theorem", "property"
    ]
    
    best_line = ""
    best_score = 0
    
    for line in lines:
        line = line.strip()
        if len(line) < 10:  # Too short
            continue
            
        line_lower = line.lower()
        
        # Skip lines that start with common prefixes
        if any(line_lower.startswith(pattern) for pattern in skip_patterns):
            continue
        
        # Score based on mathematical content
        score = sum(1 for keyword in mathematical_keywords if keyword in line_lower)
        score += len(line) / 50  # Slight preference for longer lines
        
        if score > best_score:
            best_score = score
            best_line = line
    
    # If no good line found, return the first substantial line
    if not best_line:
        for line in lines:
            line = line.strip()
            if len(line) >= 15:  # At least some substance
                return line
    
    return best_line

def run_single_research_step(memory, config, llm_manager, content_filter, 
                           formal_engine, proof_assistant, breakthrough_detector, quality_assessor):
    """Run a single research step using unified configuration"""
    
    # Generate fact using problem-specific prompt
    recent_facts = memory.get("facts", [])[-3:] if memory.get("facts") else []
    recent_fact = recent_facts[-1] if recent_facts else "No previous facts"
    
    fact_prompt = config.FACT_PROMPT.format(recent_fact=recent_fact)
    fact_result = llm_manager.generate(fact_prompt, max_tokens=config.MAX_TOKENS)
    fact = extract_meaningful_content(fact_result, "fact") if fact_result else None
    
    # Generate idea using problem-specific prompt  
    recent_ideas = memory.get("ideas", [])[-3:] if memory.get("ideas") else []
    recent_idea = recent_ideas[-1] if recent_ideas else "No previous ideas"
    
    idea_prompt = config.IDEA_PROMPT.format(recent_idea=recent_idea)
    idea_result = llm_manager.generate(idea_prompt, max_tokens=config.MAX_TOKENS)
    idea = extract_meaningful_content(idea_result, "idea") if idea_result else None
    
    result = f"Generated Research Step:\nFact: {fact}\nIdea: {idea}"
    
    # Content filtering with problem-specific config
    if fact:
        should_keep_fact, fact_reason = content_filter.should_keep_content(fact, "fact")
        if should_keep_fact and is_novel_content(fact, memory.get("facts", [])):
            memory.setdefault("facts", []).append(fact)
            print(f"✅ Added fact: {fact_reason}")
        else:
            print(f"❌ Rejected fact: {fact_reason}")
    
    if idea:
        should_keep_idea, idea_reason = content_filter.should_keep_content(idea, "idea")
        if should_keep_idea and is_novel_content(idea, memory.get("ideas", [])):
            memory.setdefault("ideas", []).append(idea)
            print(f"✅ Added idea: {idea_reason}")
        else:
            print(f"❌ Rejected idea: {idea_reason}")
    
    # Formal proof generation based on unified config
    should_generate_proofs = (
        config.ENABLE_FORMAL_PROOFS and (
            # Always generate for direct_proof (even sum experiment)
            config.problem_name == "direct_proof" or
            # Or based on frequency for other problems
            len(memory.get("facts", [])) % config.PROOF_GENERATION_FREQUENCY == 0
        )
    )
    
    if should_generate_proofs:
        print("\n=== FORMAL THEOREM GENERATION & PROVING with Quality Assessment ===")
        proof_results = generate_formal_proofs(memory, llm_manager, formal_engine, quality_assessor, config)
        
        # Check if proof generation failed due to LLM errors
        if isinstance(proof_results, str) and "LLM quota/API error" in proof_results:
            return proof_results  # Pass the error signal up to main loop
        
        memory.setdefault("formal_proofs", []).extend(proof_results)
    
    return result

def generate_formal_proofs(memory, llm_manager, formal_engine, quality_assessor, config):
    """Generate formal proofs using unified configuration with quality assessment"""
    
    # Generate problem-appropriate theorem statements
    facts = memory.get("facts", [])
    ideas = memory.get("ideas", [])
    
    if config.problem_name == "direct_proof":
        # For direct_proof, focus on even number theorems
        theorem_templates = [
            "The sum of two even numbers is even",
            "Even numbers have the form 2k where k is an integer",
            "If n is even and m is even, then n+m is even"
        ]
    else:
        # For p_vs_np, focus on complexity theory
        theorem_templates = [
            "P ⊆ NP by definition",
            "SAT is NP-complete",
            "If P = NP then all NP problems are in P"
        ]
    
    # Use recent content to generate new theorems or Lean code
    if facts:
        recent_context = f"Recent research: {facts[-1]}"
        if config.ENABLE_LEAN_TRANSLATION:
            # Prompt for Lean code directly
            if config.problem_name == "direct_proof":
                lean_prompt = f"{recent_context}. Write a Lean theorem and proof about even numbers, odd numbers, or their arithmetic properties. Avoid trivial proofs."
            else:
                lean_prompt = f"{recent_context}. Write a Lean theorem and proof about computational complexity theory or P vs NP. Avoid trivial proofs."
            generated_lean = llm_manager.generate(lean_prompt, max_tokens=200)
            if generated_lean:
                theorem_templates.insert(0, generated_lean.strip())
        else:
            # Prompt for plain-text theorem, then translate
            if config.problem_name == "direct_proof":
                theorem_prompt = f"{recent_context}. State a new theorem specifically about even numbers, odd numbers, or their arithmetic properties: "
            else:
                theorem_prompt = f"{recent_context}. State a new theorem about computational complexity theory or P vs NP: "
            generated_theorem = llm_manager.generate(theorem_prompt, max_tokens=50)
            if generated_theorem:
                theorem_clean = generated_theorem.strip()
                if config.problem_name == "direct_proof":
                    pnp_indicators = ['polynomial time', 'np-complete', 'complexity theory', 'p vs np', 'p = np', 'reduction', 'sat problem']
                    if any(indicator in theorem_clean.lower() for indicator in pnp_indicators):
                        print(f"🚫 Rejected contaminated theorem: {theorem_clean[:50]}...")
                    else:
                        theorem_templates.insert(0, theorem_clean)
                else:
                    number_theory_indicators = ['even number', 'odd number', '2k where k', 'divisible by 2']
                    if any(indicator in theorem_clean.lower() for indicator in number_theory_indicators):
                        print(f"🚫 Rejected contaminated theorem: {theorem_clean[:50]}...")
                    else:
                        theorem_templates.insert(0, theorem_clean)
    
    proof_results = []
    from src.lean_feedback_parser import LeanFeedbackParser
    for theorem in theorem_templates[:2]:  # Try 2 theorems
        print(f"\n--- Attempting: {theorem} ---")
        proof_result = formal_engine.attempt_proof_with_translation(theorem)
        proof_result["timestamp"] = datetime.now().isoformat()

        # Check for LLM quota/API error and stop further logging if so
        err = proof_result.get('error', '')
        is_llm_error = (
            isinstance(err, str) and (
                'quota' in err.lower() or 'rate limit' in err.lower() or '429' in err or 'api error' in err.lower()
            )
        )
        if is_llm_error:
            print(f"❌ LLM quota/API error: {err}\n⚠️  Stopping proof session. No further proof or quality logs will be shown.")
            # Signal to main loop that we had LLM errors
            return "LLM quota/API error detected"

        if proof_result["success"]:
            print(f"✅ Lean validation: SUCCESS")

            # 🎯 NEW: Quality Assessment
            lean_code = proof_result.get("lean_code", "")
            if lean_code:
                quality_info = quality_assessor.assess_proof_quality(
                    lean_code, theorem, config.problem_name
                )
                proof_result["quality_assessment"] = quality_info

                print(f"🎯 Proof Quality: {quality_info['quality_score']:.1f}/1.0")
                print(f"💡 Assessment: {quality_info['explanation']}")
                print(f"🔬 Mathematical Type: {quality_info['mathematical_substance']}")

                if quality_info["is_meaningful"]:
                    print("🏆 HIGH QUALITY: Proof shows meaningful mathematical reasoning!")
                    # Mark database as complete if not already
                    if not memory.get("complete", False):
                        print("🚩 Marking problem as complete: high-quality proof found.")
                        memory["complete"] = True
                elif quality_info["is_placeholder"]:
                    print("⚠️  LOW QUALITY: Proof relies on placeholders or trivial tactics")
                else:
                    print("📝 MEDIUM QUALITY: Valid proof with basic techniques")
            else:
                print("⚠️  No Lean code generated for quality assessment")
        else:
            print(f"❌ Lean validation: FAILED")
            print(f"Error: {proof_result.get('error', 'Unknown')}")

            # Parse Lean error and add recommendations to ideas
            lean_error = proof_result.get('error', '')
            if lean_error:
                parser = LeanFeedbackParser(lean_error)
                recommendations = parser.parse()
                actionable = [rec for rec in recommendations if rec != "No actionable feedback detected."]
                if actionable:
                    memory.setdefault('ideas', []).extend(actionable)
                    print(f"💡 Added Lean feedback to ideas: {actionable}")

        proof_results.append(proof_result)

        # 🎯 LEARN FROM THIS PROOF ATTEMPT
        context = facts[-3:] if len(facts) >= 3 else facts  # Use recent facts as context
        formal_engine.learn_from_proof(proof_result, context)

        # Add successful proofs to memory for cross-validation
        memory.setdefault('formal_proofs', []).append(proof_result)

    # 📊 Generate Quality Report
    if proof_results:
        print("\n📊 PROOF SESSION QUALITY REPORT")
        print("=" * 40)
        quality_report = quality_assessor.generate_quality_report(proof_results)
        print(f"📈 {quality_report['summary']}")
        
        if quality_report["status"] == "complete":
            print(f"🎯 Average Quality: {quality_report['average_quality']:.1f}/1.0")
            print(f"🏆 Best Quality: {quality_report['max_quality']:.1f}/1.0")
            print(f"✨ Meaningful Proofs: {quality_report['meaningful_proofs']}/{quality_report['total_attempts']}")
            
            # Show substance distribution
            if quality_report['substance_distribution']:
                print("🔬 Mathematical Reasoning Types:")
                for substance, count in quality_report['substance_distribution'].items():
                    print(f"   • {substance.replace('_', ' ').title()}: {count}")
    return proof_results

def is_novel_content(content, existing_list):
    """Check if content is novel (simple similarity check)"""
    content_lower = content.lower()
    for existing in existing_list:
        if content_lower in existing.lower() or existing.lower() in content_lower:
            return False
    return True

def log_research_step(result, config):
    """Log research step with timestamp"""
    timestamp = datetime.now().isoformat()
    log_entry = f"\n--- Research Step logged at {timestamp} ---\n{result}\n"
    
    log_file = f"research_log_{config.problem_name}.md"
    with open(log_file, "a") as f:
        f.write(log_entry)

if __name__ == "__main__":
    exit_code = main()
    if exit_code:
        sys.exit(exit_code)
