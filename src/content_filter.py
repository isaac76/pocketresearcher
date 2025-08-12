#!/usr/bin/python3

"""
Content Filter - Removes low-quality, irrelevant, or corrupted content from memory
"""

import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class ContentFilter:
    """
    Advanced content filtering system to maintain high-quality mathematical knowledge
    """
    
    def __init__(self, config=None):
        # Default configuration
        default_config = {
            "min_mathematical_relevance": 0.3,
            "min_length": 15,
            "max_length": 500,
            "allow_simple_statements": False,
            "domain_keywords": []
        }
        
        # Merge with provided config
        if config:
            default_config.update(config)
        self.config = default_config
        
        self.quality_thresholds = {
            "min_fact_length": self.config["min_length"],
            "max_fact_length": self.config["max_length"],
            "min_idea_length": self.config["min_length"],
            "max_idea_length": 1000,
            "min_mathematical_relevance": 0.3
        }
        
        # Patterns for low-quality content
        self.noise_patterns = [
            # Placeholder text
            r"_{10,}",  # Long underscores
            r"\([0-9]+\)\.\s*[A-Z][a-z]+\s+(asked|wanted|implemented)",  # Conversational fragments
            r"Mark asked Sarah",
            r"Emily.*David.*Sarah",
            r"Once upon a time",
            
            # Technical noise  
            r"database.*MySQL",
            r"caching mechanism",
            r"memory leak",
            r"system.*operating system",
            r"gene regulatory network",
            
            # Repetitive patterns
            r"I believe.*relevant.*because.*relevant.*because",
            r"Question:.*False\.$",
            r"True\.$",
            
            # Corrupted/incomplete content
            r"\.{3,}",  # Multiple dots
            r"New fact:$",
            r"^\([0-9]+\)\.$",  # Just numbered items
        ]
        
        # Mathematical relevance keywords (use config-specific keywords if provided)
        default_math_keywords = [
            "polynomial", "exponential", "algorithm", "complexity", "NP", "P=NP", 
            "SAT", "reduction", "proof", "theorem", "diagonalization", "circuit",
            "quantum", "probabilistic", "geometric", "algebraic", "computational",
            "turing machine", "decidable", "completeness", "hierarchy", "oracle",
            "lower bound", "upper bound", "verification", "satisfiability"
        ]
        self.math_keywords = self.config.get("math_keywords", default_math_keywords)
        
        # Content categories for filtering
        self.content_categories = {
            "mathematical": 1.0,
            "technical_cs": 0.8,
            "general_programming": 0.3,
            "conversational": 0.1,
            "noise": 0.0
        }
        
        self.filter_stats = {
            "facts_removed": 0,
            "ideas_removed": 0,
            "proofs_cleaned": 0,
            "reflections_filtered": 0,
            "total_content_before": 0,
            "total_content_after": 0
        }
    
    def calculate_mathematical_relevance(self, text: str) -> float:
        """Calculate how mathematically relevant content is (0.0 to 1.0)"""
        text_lower = text.lower()
        
        # Count mathematical keywords
        math_score = sum(1 for keyword in self.math_keywords if keyword in text_lower)
        max_possible = len(self.math_keywords)
        keyword_ratio = min(math_score / 5.0, 1.0)  # Normalize to max 5 keywords
        
        # Length penalty for very short or very long content
        length_score = 1.0
        if len(text) < 20:
            length_score = 0.5
        elif len(text) > 800:
            length_score = 0.7
            
        # Complexity penalty for simple statements
        complexity_score = 1.0
        if text.count(' ') < 5:  # Very short statements
            complexity_score = 0.6
            
        return keyword_ratio * length_score * complexity_score
    
    def is_noise_content(self, text: str) -> Tuple[bool, str]:
        """Check if content matches noise patterns"""
        for pattern in self.noise_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True, f"Matches noise pattern: {pattern}"
        return False, ""
    
    def categorize_content(self, text: str) -> str:
        """Categorize content type"""
        text_lower = text.lower()
        
        # Check for mathematical content
        math_keywords_found = sum(1 for kw in self.math_keywords if kw in text_lower)
        if math_keywords_found >= 2:
            return "mathematical"
        
        # Check for noise patterns
        is_noise, _ = self.is_noise_content(text)
        if is_noise:
            return "noise"
            
        # Check for conversational content
        conversational_indicators = ["asked", "said", "wanted", "implemented", "emily", "mark", "sarah"]
        if any(indicator in text_lower for indicator in conversational_indicators):
            return "conversational"
            
        # Check for general programming
        programming_keywords = ["algorithm", "database", "performance", "optimization", "function"]
        if any(kw in text_lower for kw in programming_keywords):
            return "technical_cs"
            
        return "general_programming"
    
    def should_keep_content(self, text: str, content_type: str) -> Tuple[bool, str]:
        """Determine if content should be kept"""
        if not text or not text.strip():
            return False, "Empty content"
            
        # Check noise patterns first
        is_noise, noise_reason = self.is_noise_content(text)
        if is_noise:
            return False, noise_reason
            
        # Check length constraints
        if content_type == "fact":
            if len(text) < self.quality_thresholds["min_fact_length"]:
                return False, f"Fact too short: {len(text)} chars"
            if len(text) > self.quality_thresholds["max_fact_length"]:
                return False, f"Fact too long: {len(text)} chars"
        elif content_type == "idea":
            if len(text) < self.quality_thresholds["min_idea_length"]:
                return False, f"Idea too short: {len(text)} chars"
            if len(text) > self.quality_thresholds["max_idea_length"]:
                return False, f"Idea too long: {len(text)} chars"
        
        # Check mathematical relevance
        relevance = self.calculate_mathematical_relevance(text)
        if relevance < self.config["min_mathematical_relevance"]:
            return False, f"Low mathematical relevance: {relevance:.2f}"
            
        return True, f"Quality content (relevance: {relevance:.2f})"
    
    def filter_facts(self, facts: List[str]) -> Tuple[List[str], List[Dict]]:
        """Filter fact list and return cleaned facts + removal log"""
        cleaned_facts = []
        removal_log = []
        
        for i, fact in enumerate(facts):
            should_keep, reason = self.should_keep_content(fact, "fact")
            
            if should_keep:
                cleaned_facts.append(fact)
            else:
                removal_log.append({
                    "index": i,
                    "content": fact[:100] + "..." if len(fact) > 100 else fact,
                    "reason": reason,
                    "type": "fact"
                })
                self.filter_stats["facts_removed"] += 1
        
        return cleaned_facts, removal_log
    
    def filter_ideas(self, ideas: List[str]) -> Tuple[List[str], List[Dict]]:
        """Filter idea list and return cleaned ideas + removal log"""
        cleaned_ideas = []
        removal_log = []
        
        for i, idea in enumerate(ideas):
            should_keep, reason = self.should_keep_content(idea, "idea")
            
            if should_keep:
                cleaned_ideas.append(idea)
            else:
                removal_log.append({
                    "index": i,
                    "content": idea[:100] + "..." if len(idea) > 100 else idea,
                    "reason": reason,
                    "type": "idea"
                })
                self.filter_stats["ideas_removed"] += 1
        
        return cleaned_ideas, removal_log
    
    def filter_proofs(self, proofs: List[str]) -> Tuple[List[str], List[Dict]]:
        """Filter proof list, removing analysis summaries and keeping actual proofs"""
        cleaned_proofs = []
        removal_log = []
        
        for i, proof in enumerate(proofs):
            # Remove formal proof analysis summaries
            if "FORMAL PROOF ANALYSIS:" in proof or "Generated Research Step:" in proof:
                removal_log.append({
                    "index": i,
                    "content": proof[:100] + "..." if len(proof) > 100 else proof,
                    "reason": "Analysis summary, not actual proof",
                    "type": "proof"
                })
                self.filter_stats["proofs_cleaned"] += 1
                continue
                
            # Keep only substantial mathematical proofs
            if len(proof) > 50 and any(kw in proof.lower() for kw in ["proof:", "theorem", "complexity", "algorithm"]):
                cleaned_proofs.append(proof)
            else:
                removal_log.append({
                    "index": i,
                    "content": proof[:100] + "..." if len(proof) > 100 else proof,
                    "reason": "Not a substantial mathematical proof",
                    "type": "proof"
                })
                self.filter_stats["proofs_cleaned"] += 1
        
        return cleaned_proofs, removal_log
    
    def filter_reflections(self, reflections: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """Filter reflections to keep only meaningful mathematical insights"""
        cleaned_reflections = []
        removal_log = []
        
        for i, reflection in enumerate(reflections):
            if isinstance(reflection, dict) and "insight" in reflection:
                insight = reflection["insight"]
                
                # Remove very short or nonsensical insights
                if len(insight) < 20 or insight.startswith("#") or "neural networks" in insight.lower():
                    removal_log.append({
                        "index": i,
                        "content": insight,
                        "reason": "Non-mathematical or trivial insight",
                        "type": "reflection"
                    })
                    self.filter_stats["reflections_filtered"] += 1
                    continue
                
                # Keep mathematical insights
                if any(kw in insight.lower() for kw in self.math_keywords[:10]):  # Top 10 math keywords
                    cleaned_reflections.append(reflection)
                else:
                    removal_log.append({
                        "index": i,
                        "content": insight,
                        "reason": "Low mathematical content",
                        "type": "reflection"
                    })
                    self.filter_stats["reflections_filtered"] += 1
            else:
                # Handle old string-based reflections
                removal_log.append({
                    "index": i,
                    "content": str(reflection)[:100],
                    "reason": "Old format reflection",
                    "type": "reflection"
                })
                self.filter_stats["reflections_filtered"] += 1
        
        return cleaned_reflections, removal_log
    
    def filter_memory(self, memory: Dict) -> Tuple[Dict, Dict]:
        """Filter entire memory structure and return cleaned memory + comprehensive log"""
        
        # Store original counts
        self.filter_stats["total_content_before"] = (
            len(memory.get("facts", [])) + 
            len(memory.get("ideas", [])) + 
            len(memory.get("proofs", [])) + 
            len(memory.get("reflections", []))
        )
        
        # Create cleaned memory copy
        cleaned_memory = memory.copy()
        comprehensive_log = {
            "timestamp": datetime.now().isoformat(),
            "filtering_summary": {},
            "removed_content": [],
            "statistics": {}
        }
        
        # Filter each content type
        if "facts" in memory:
            cleaned_facts, fact_log = self.filter_facts(memory["facts"])
            cleaned_memory["facts"] = cleaned_facts
            comprehensive_log["removed_content"].extend(fact_log)
        
        if "ideas" in memory:
            cleaned_ideas, idea_log = self.filter_ideas(memory["ideas"])
            cleaned_memory["ideas"] = cleaned_ideas
            comprehensive_log["removed_content"].extend(idea_log)
        
        if "proofs" in memory:
            cleaned_proofs, proof_log = self.filter_proofs(memory["proofs"])
            cleaned_memory["proofs"] = cleaned_proofs
            comprehensive_log["removed_content"].extend(proof_log)
            
        if "reflections" in memory:
            cleaned_reflections, reflection_log = self.filter_reflections(memory["reflections"])
            cleaned_memory["reflections"] = cleaned_reflections
            comprehensive_log["removed_content"].extend(reflection_log)
        
        # Update statistics
        self.filter_stats["total_content_after"] = (
            len(cleaned_memory.get("facts", [])) + 
            len(cleaned_memory.get("ideas", [])) + 
            len(cleaned_memory.get("proofs", [])) + 
            len(cleaned_memory.get("reflections", []))
        )
        
        comprehensive_log["statistics"] = self.filter_stats.copy()
        comprehensive_log["filtering_summary"] = {
            "content_removed": len(comprehensive_log["removed_content"]),
            "size_reduction": self.filter_stats["total_content_before"] - self.filter_stats["total_content_after"],
            "compression_ratio": (
                (self.filter_stats["total_content_before"] - self.filter_stats["total_content_after"]) / 
                max(self.filter_stats["total_content_before"], 1)
            )
        }
        
        return cleaned_memory, comprehensive_log
    
    def generate_filter_report(self, filter_log: Dict) -> str:
        """Generate human-readable filtering report"""
        stats = filter_log["statistics"]
        summary = filter_log["filtering_summary"]
        
        report = f"""
🧹 CONTENT FILTERING REPORT
==========================

SUMMARY:
- Total items before: {stats['total_content_before']}
- Total items after: {stats['total_content_after']}
- Items removed: {summary['content_removed']}
- Size reduction: {summary['size_reduction']} items ({summary['compression_ratio']:.1%})

BREAKDOWN:
- Facts removed: {stats['facts_removed']}
- Ideas removed: {stats['ideas_removed']}
- Proofs cleaned: {stats['proofs_cleaned']}
- Reflections filtered: {stats['reflections_filtered']}

QUALITY IMPROVEMENTS:
✅ Removed conversational noise (Mark/Sarah/Emily stories)
✅ Filtered placeholder text and incomplete thoughts
✅ Eliminated low mathematical relevance content
✅ Cleaned analysis summaries from proofs
✅ Kept only substantial mathematical insights

The knowledge base is now more focused on mathematical content!
"""
        return report
