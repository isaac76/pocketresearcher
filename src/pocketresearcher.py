#!/usr/bin/python3

# pocketresearcher.py
import os
import sys
from datetime import datetime

# Add project root to path for config import
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    import config
except ImportError:
    print("Config file not found. Please copy config_template.py to config.py")
    sys.exit(1)

# Handle imports for both direct execution and module execution
try:
    # Try relative imports first (for python -m src.pocketresearcher)
    from .memory import Memory
    from .proof_assistant import MathProofAssistant
    from .formal_proof_engine import FormalProofEngine
    from .breakthrough_detector import BreakthroughDetector
    from .content_filter import ContentFilter
    from .llm_manager import LLMManager
except ImportError:
    # Fall back to direct imports (for running from src directory)
    from memory import Memory
    from proof_assistant import MathProofAssistant
    from formal_proof_engine import FormalProofEngine
    from breakthrough_detector import BreakthroughDetector
    from content_filter import ContentFilter
    from llm_manager import LLMManager

# ----------------------------
# Config
# ----------------------------
# Initialize LLM Manager with configured model
llm_manager = LLMManager(config.DEFAULT_LLM)

# Set research log path relative to the project root directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(current_dir, "research_log.md")

# API key for formal proof engine (if using Lean translation)
API_KEY = config.GEMINI_API_KEY

memory_store = Memory()
proof_assistant = MathProofAssistant()
formal_engine = FormalProofEngine(api_key=API_KEY if config.ENABLE_LEAN_TRANSLATION else None)
breakthrough_detector = BreakthroughDetector()
content_filter = ContentFilter()

# ----------------------------
# Append to research log
# ----------------------------
def log_research(step_text):
    with open(LOG_FILE, "a") as f:
        f.write(f"### {datetime.now().isoformat()}\n")
        f.write(step_text.strip() + "\n\n")

# ----------------------------
# Main research loop
# ----------------------------

def generate_and_prove_theorems(memory, generator):
    """
    Generate formal theorems based on current knowledge and attempt to prove them
    """
    print("=== FORMAL THEOREM GENERATION & PROVING ===")
    
    # Get suggestions based on what we've learned so far
    suggested_theorems = formal_engine.suggest_next_theorems(memory)
    
    # Also generate new theorem ideas based on recent facts and ideas
    recent_knowledge = memory["facts"][-5:] + memory["ideas"][-5:]
    
    theorem_prompt = f"""Based on this mathematical knowledge about P vs NP:
{' '.join(recent_knowledge)}

Generate a specific mathematical theorem or conjecture that could be formally proven. State it clearly and precisely:

Theorem: """

    theorem_result = generator(theorem_prompt, max_tokens=100)
    generated_theorem = theorem_result.replace(theorem_prompt, "").strip() if theorem_prompt in theorem_result else theorem_result.strip()
    
    # Clean up the generated theorem
    generated_theorem = generated_theorem.split('\n')[0].strip()
    if generated_theorem:
        suggested_theorems.insert(0, generated_theorem)
    
    print(f"Attempting to prove {len(suggested_theorems)} theorems...")
    
    proof_results = []
    for i, theorem_statement in enumerate(suggested_theorems[:3]):  # Try top 3 theorems
        print(f"\n--- Theorem {i+1}: {theorem_statement} ---")
        
        # Use new translation method for better Lean syntax
        proof_result = formal_engine.attempt_proof_with_translation(theorem_statement)
        proof_result["informal_statement"] = theorem_statement
        proof_result["timestamp"] = datetime.now().isoformat()
        
        # Print the generated Lean code
        if "lean_statement" in proof_result:
            print(f"Lean statement: {proof_result['lean_statement']}")
            print(f"Proof attempt: {proof_result['proof_attempt']}")
        
        if proof_result["success"]:
            print(f"✓ PROOF TRANSLATION SUCCESSFUL!")
            if "proof_steps" in proof_result:
                print(f"Proof steps: {proof_result['proof_steps']}")
            
            # BREAKTHROUGH DETECTION - Critical addition!
            significance_analysis = breakthrough_detector.analyze_proof_significance(proof_result)
            
            if significance_analysis["is_breakthrough"]:
                breakthrough_record = breakthrough_detector.record_breakthrough(proof_result, significance_analysis)
                alert = breakthrough_detector.generate_breakthrough_alert(breakthrough_record)
                print(alert)
                
                # Store breakthrough in memory
                memory.setdefault("breakthroughs", []).append(breakthrough_record)
                
                # Log breakthrough to research log
                log_research(f"🚨 BREAKTHROUGH DETECTED 🚨\n{alert}")
                
            else:
                print(f"⚠️  Proof quality issues: {significance_analysis.get('issues', [])}")
                print(f"Significance: {significance_analysis['significance_level']} (confidence: {significance_analysis['confidence']:.2f})")
            
            # Learn from successful proof
            formal_engine.learn_from_proof(proof_result, recent_knowledge)
            
            # Store successful proof in memory
            memory.setdefault("formal_proofs", []).append(proof_result)
            
        else:
            print(f"✗ Proof failed: {proof_result.get('error', 'Unknown error')}")
            print(f"Tactics tried: {proof_result['tactics_tried']}")
            
            # Store failed attempt for learning
            memory.setdefault("failed_proofs", []).append(proof_result)
        
        proof_results.append(proof_result)
    
    return proof_results

def enhance_research_with_proofs(memory, generator):
    """
    Enhanced research step that incorporates formal proof attempts
    """
    # Generate formal theorems and attempt proofs
    proof_results = generate_and_prove_theorems(memory, generator)
    
    # Analyze what we learned from proofs
    successful_proofs = [p for p in proof_results if p["success"]]
    failed_proofs = [p for p in proof_results if not p["success"]]
    
    proof_summary = f"""
FORMAL PROOF ANALYSIS:
- Attempted proofs: {len(proof_results)}
- Successful proofs: {len(successful_proofs)}
- Failed proofs: {len(failed_proofs)}
- Proof techniques learned: {len(formal_engine.learned_tactics)}
"""
    
    # Generate insights based on proof attempts
    if successful_proofs:
        insight_prompt = f"We successfully proved: {[p['informal_statement'] for p in successful_proofs]}. This suggests: "
        insight_result = generator(insight_prompt, max_tokens=50)
        insight = insight_result.replace(insight_prompt, "").strip() if insight_prompt in insight_result else insight_result.strip()
        
        if insight and len(insight) > 10:
            memory["ideas"].append(f"Proof insight: {insight}")
    
    if failed_proofs:
        # Learn from failures
        failure_prompt = f"Failed to prove: {[p['informal_statement'] for p in failed_proofs[:2]]}. Alternative approach: "
        alternative_result = generator(failure_prompt, max_tokens=50)
        alternative = alternative_result.replace(failure_prompt, "").strip() if failure_prompt in alternative_result else alternative_result.strip()
        
        if alternative and len(alternative) > 10:
            memory["ideas"].append(f"Alternative approach: {alternative}")
    
    return proof_summary


def is_novel_fact(fact, facts):
    """Check if the fact is novel compared to previous facts."""
    if not fact:
        return False
    
    fact_lower = fact.lower()
    # Check for exact duplicates
    for prev_fact in facts:
        if fact_lower == prev_fact.lower():
            return False
        
        # Check for substantial overlap (simple similarity check)
        fact_words = set(fact_lower.split())
        prev_words = set(prev_fact.lower().split())
        overlap = len(fact_words.intersection(prev_words))
        total_words = len(fact_words.union(prev_words))
        
        # If more than 70% overlap, consider it a repeat
        if total_words > 0 and overlap / total_words > 0.7:
            return False
    
    return True

def is_novel_idea(idea, ideas):
    """Check if the idea is novel compared to previous ideas."""
    if not idea:
        return False
    
    idea_lower = idea.lower()
    # Check for exact duplicates
    for prev_idea in ideas:
        if idea_lower == prev_idea.lower():
            return False
        
        # Check for substantial overlap (simple similarity check)
        idea_words = set(idea_lower.split())
        prev_words = set(prev_idea.lower().split())
        overlap = len(idea_words.intersection(prev_words))
        total_words = len(idea_words.union(prev_words))
        
        # If more than 70% overlap, consider it a repeat
        if total_words > 0 and overlap / total_words > 0.7:
            return False
    
    return True

def truncate_for_context(items, max_chars=1000):
    """Truncate a list of items to fit within character limit, keeping most recent items."""
    if not items:
        return []
    
    # Start with most recent items and work backwards
    truncated = []
    total_chars = 0
    
    for item in reversed(items):
        item_chars = len(str(item)) + 2  # +2 for separator
        if total_chars + item_chars > max_chars:
            break
        truncated.insert(0, item)  # Insert at beginning to maintain order
        total_chars += item_chars
    
    return truncated

def estimate_token_count(text):
    """Rough estimate of token count (approximately 4 chars per token)."""
    return len(text) // 4

def run_research():
    # Use unified LLM manager
    generator = llm_manager.generate
    
    # Print model info
    model_info = llm_manager.get_model_info()
    print(f"Using LLM: {model_info['current_model']} ({model_info['model_type']})")
    if model_info['rate_limited']:
        print(f"Rate limiting enabled: {config.GEMINI_RATE_LIMIT} requests/minute")

    # Load existing memory
    memory = memory_store.load()

    # Build prompt from memory, with aggressive truncation to stay within token limits
    # Only use the most recent and concise reflections
    recent_reflections = []
    if memory.get("reflections"):
        for reflection in memory["reflections"][-2:]:
            # Handle both old string reflections and new structured reflections
            if isinstance(reflection, dict):
                insight_text = f"{reflection.get('type', 'insight')}: {reflection.get('insight', '')}"
                if len(insight_text) < 200:
                    recent_reflections.append(insight_text)
            elif isinstance(reflection, str) and len(reflection) < 200:
                recent_reflections.append(reflection)
    reflections_text = "\n".join(recent_reflections[:1])  # Only 1 reflection max
    
    # Truncate facts and ideas to keep most recent and important ones
    recent_facts = truncate_for_context(memory["facts"], max_chars=400)  # Reduced
    recent_ideas = truncate_for_context(memory["ideas"], max_chars=300)  # Reduced
    
    # Use variables to avoid potential issues with string concatenation
    facts_str = "; ".join(recent_facts[-4:]) if recent_facts else ""  # Only last 4 facts
    ideas_str = "; ".join(recent_ideas[-3:]) if recent_ideas else ""  # Only last 3 ideas
    
    # Build prompt using f-strings with proper newlines
    newline = "\n"
    reflections_part = f"Recent insight: {reflections_text}{newline}" if reflections_text else ""
    
    # Add learning context from experiments (keep recent techniques only)
    experiments_summary = ""
    if memory.get("experiments"):
        recent_techniques = [exp["technique"] for exp in memory["experiments"][-3:]]  # Last 3 techniques
        experiments_summary = f"Analyzed: {', '.join(recent_techniques)}{newline}"
    
    # If we have no facts yet, provide some starter context
    if not memory["facts"]:
        context = "P vs NP is a fundamental problem in computer science. P contains problems solvable in polynomial time, NP contains problems verifiable in polynomial time."
    else:
        # Use truncated facts to stay within token limits
        if len(facts_str) > 500:  # If still too long, use just the core facts
            core_facts = [
                "P = NP is one of the seven Millennium Prize Problems in mathematics.",
                "P is the class of problems solvable in polynomial time by a deterministic Turing machine.",
                "NP is the class of problems for which a solution can be verified in polynomial time by a deterministic Turing machine.",
                "It is unknown whether P = NP or P != NP; neither has been proven."
            ]
            context = f"Core facts: {'; '.join(core_facts)}"
        else:
            context = f"Known facts: {facts_str}"
    
    # Create effective prompts based on testing
    fact_prompt = f"P vs NP complexity theory. Recent research: {recent_facts[-1] if recent_facts else 'P and NP are complexity classes'}. New fact: "
    
    idea_prompt = f"Complexity theory research ideas. Previous approaches: {recent_ideas[-1] if recent_ideas else 'algorithmic methods'}. New research idea: "

    # Generate fact first
    fact_result = generator(fact_prompt, max_tokens=80)
    fact_generated = fact_result.replace(fact_prompt, "").strip() if fact_prompt in fact_result else fact_result.strip()
    
    # Generate idea second  
    idea_result = generator(idea_prompt, max_tokens=80)
    idea_generated = idea_result.replace(idea_prompt, "").strip() if idea_prompt in idea_result else idea_result.strip()
    
    # Clean up the generated content
    fact = fact_generated.split('\n')[0].strip() if fact_generated else None
    idea = idea_generated.split('\n')[0].strip() if idea_generated else None
    
    # Create a combined result for logging
    result = f"Generated Research Step:{newline}Fact: {fact}{newline}Idea: {idea}"
    novelty = is_novel_idea(idea, memory["ideas"])
    
    # Add formal proof attempts every few iterations
    formal_proof_summary = ""
    if len(memory["facts"]) % 3 == 0:  # Every 3rd iteration, attempt formal proofs
        formal_proof_summary = enhance_research_with_proofs(memory, generator)
        result += f"{newline}{formal_proof_summary}"
    
    # Analyze mathematical content in the generated result
    math_content = proof_assistant.parse_mathematical_content(result)
    
    # Store extracted information with content filtering
    # Store fact and idea if they are novel AND high quality
    if fact:
        should_keep_fact, fact_reason = content_filter.should_keep_content(fact, "fact")
        if should_keep_fact and is_novel_fact(fact, memory["facts"]):
            memory["facts"].append(fact)
            print(f"✅ Added fact: {fact_reason}")
        else:
            reason = fact_reason if not should_keep_fact else "Not novel"
            print(f"❌ Rejected fact: {reason}")
    
    if idea:
        should_keep_idea, idea_reason = content_filter.should_keep_content(idea, "idea")
        if should_keep_idea and is_novel_idea(idea, memory["ideas"]):
            memory["ideas"].append(idea)
            print(f"✅ Added idea: {idea_reason}")
        else:
            reason = idea_reason if not should_keep_idea else "Not novel"
            print(f"❌ Rejected idea: {reason}")
    
    # Store mathematical content if found
    if math_content["proof_steps"]:
        memory.setdefault("proofs", []).extend(math_content["proof_steps"])
    if math_content["assumptions"]:
        memory.setdefault("techniques", []).extend(math_content["assumptions"])
    
    # Analyze any mentioned proof techniques in the generated content AND stored memory
    technique_keywords = ["diagonalization", "reduction", "induction", "contradiction", "algebraic", "geometric", "probabilistic", "quantum"]
    existing_techniques = [exp["technique"] for exp in memory.get("experiments", [])]
    
    # Check both the current generation and recent memory for technique mentions
    content_to_check = result.lower()
    if fact:
        content_to_check += " " + fact.lower()
    if idea:
        content_to_check += " " + idea.lower()
    
    # Also check recent facts and ideas for technique keywords
    recent_facts = memory["facts"][-5:] if len(memory["facts"]) > 5 else memory["facts"]
    recent_ideas = memory["ideas"][-5:] if len(memory["ideas"]) > 5 else memory["ideas"]
    content_to_check += " " + " ".join(recent_facts).lower()
    content_to_check += " " + " ".join(recent_ideas).lower()
    
    for keyword in technique_keywords:
        if keyword in content_to_check and keyword not in existing_techniques:
            technique_analysis = proof_assistant.analyze_proof_technique(keyword)
            memory.setdefault("experiments", []).append({
                "technique": keyword,
                "analysis": technique_analysis["description"],
                "limitations": technique_analysis["limitations"],
                "timestamp": datetime.now().isoformat()
            })
            print(f"New technique analysis added: {keyword}")

    # Progress summary with breakthrough tracking
    breakthrough_summary = breakthrough_detector.get_breakthrough_summary()
    summary = (
        f"Progress Summary ({datetime.now().isoformat()}):{newline}"
        f"Total facts: {len(memory['facts'])}{newline}"
        f"Total ideas: {len(memory['ideas'])}{newline}"
        f"Total proof steps: {len(memory.get('proofs', []))}{newline}"
        f"Formal proofs: {len(memory.get('formal_proofs', []))}{newline}"
        f"Techniques analyzed: {len(memory.get('experiments', []))}{newline}"
        f"Breakthrough attempts: {breakthrough_summary['total_breakthroughs_detected']}{newline}"
        f"Highest confidence: {breakthrough_summary['highest_confidence']:.2f}{newline}"
        f"Novelty of latest idea: {'Novel' if novelty else 'Repeat'}{newline}"
    )

    # Reflection step - generate structured insights instead of recursive reflections
    def parse_structured_reflection(reflection_text):
        """Parse reflection output into structured insights."""
        insights = []
        lines = reflection_text.split('\n')
        for line in lines:
            line = line.strip()
            if ':' in line:
                for keyword in ['Pattern:', 'Limitation:', 'Opportunity:', 'Next Step:', 'Mistake:']:
                    if line.startswith(keyword):
                        insight_text = line[len(keyword):].strip()
                        if insight_text and len(insight_text) > 10:  # Avoid trivial insights
                            insights.append({
                                "type": keyword.replace(':', '').lower().replace(' ', '_'),
                                "insight": insight_text[:200],  # Limit length
                                "timestamp": datetime.now().isoformat()
                            })
                        break
        return insights

    # Generate simpler, more effective reflection
    reflection_prompt = f"P vs NP research analysis. Recent progress: {len(memory['facts'])} facts, {len(memory['ideas'])} ideas. Key research pattern observed: "
    
    reflection_result = generator(reflection_prompt, max_tokens=100)
    reflection_generated = reflection_result.replace(reflection_prompt, "").strip() if reflection_prompt in reflection_result else reflection_result.strip()
    
    # Create a structured insight from the generated reflection
    pattern_text = reflection_generated.split('\n')[0].strip() if reflection_generated else "Research is expanding in multiple directions"
    
    structured_insights = [{
        "type": "pattern",
        "insight": pattern_text[:200],  # Limit length
        "timestamp": datetime.now().isoformat()
    }]
    if structured_insights:
        # Limit total reflections to prevent bloat
        if len(memory.get("reflections", [])) > 10:
            memory["reflections"] = memory["reflections"][-5:]  # Keep only 5 most recent
        
        memory.setdefault("reflections", []).extend(structured_insights)

    # Save updates
    memory_store.save(memory)
    
    # Format reflection summary for logging
    reflection_summary = "Structured Insights:\n"
    for insight in structured_insights[-3:]:  # Only show recent insights
        reflection_summary += f"- {insight['type'].replace('_', ' ').title()}: {insight['insight']}\n"
    
    log_research(result + "\n" + summary + "\n" + reflection_summary)

    print(f"--- New step logged at {datetime.now().isoformat()} ---")
    print(result)
    print(summary)
    print(reflection_summary)

# ----------------------------
if __name__ == "__main__":
    run_research()

