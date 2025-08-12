#!/usr/bin/env python3
"""
Proof Quality Assessor - Evaluates the mathematical substance of generated proofs

Integrates with the main PocketResearcher system to distinguish between:
- Meaningful mathematical proofs (high quality)
- Valid but trivial proofs (medium quality) 
- Placeholder proofs with 'sorry' (low quality)
- Failed proofs (no quality)
"""

import re
from typing import Dict, List, Tuple

class ProofQualityAssessor:
    """Assesses the quality and mathematical substance of formal proofs"""
    
    def __init__(self):
        # Patterns that indicate placeholder/trivial content
        self.placeholder_patterns = [
            "sorry", "trivial", "True :=", "rfl"
        ]
        
        # Patterns that indicate meaningful mathematical content
        self.meaningful_patterns = [
            r"induction",
            r"cases",
            r"ring",
            r"norm_num",
            r"simp.*\[.*\]",  # simp with specific tactics
            r"rw\s*\[",       # rewrite with terms
            r"have.*:",       # intermediate steps
            r"show.*:",       # explicit goal statements
            r"calc",          # calculation proofs
            r"apply.*theorem", # applying named theorems
            r"by_cases",      # case analysis
            r"obtain.*:=",    # existential unpacking
            r"use\s+",        # existential construction
            r"left|right",    # disjunction selection
            r"exact\s+h",     # hypothesis application
        ]
    
    def assess_proof_quality(self, proof_code: str, theorem_statement: str, 
                           problem_context: str = "") -> Dict:
        """Assess the quality of a proof attempt"""
        
        # Basic quality indicators
        has_placeholders = any(pattern in proof_code.lower() 
                             for pattern in self.placeholder_patterns)
        
        meaningful_content = sum(1 for pattern in self.meaningful_patterns 
                               if re.search(pattern, proof_code, re.IGNORECASE))
        
        # Specific quality checks
        assessment = {
            "has_placeholders": has_placeholders,
            "meaningful_tactics": meaningful_content,
            "line_count": len(proof_code.split('\n')),
            "is_trivial_only": proof_code.strip().endswith("by trivial"),
            "is_sorry_proof": "sorry" in proof_code.lower(),
            "is_computational": "norm_num" in proof_code.lower(),
            "is_algebraic": "ring" in proof_code.lower(),
            "has_case_analysis": "by_cases" in proof_code.lower(),
            "has_existential_reasoning": any(pattern in proof_code.lower() 
                                           for pattern in ["obtain", "use", "exists"]),
            "proof_length": len(proof_code.strip())
        }
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(assessment, theorem_statement, problem_context)
        
        return {
            "quality_score": quality_score,
            "assessment": assessment,
            "is_meaningful": quality_score > 0.5,
            "is_placeholder": has_placeholders or quality_score < 0.3,
            "explanation": self._explain_quality(assessment, quality_score),
            "mathematical_substance": self._assess_mathematical_substance(assessment)
        }
    
    def _calculate_quality_score(self, assessment: Dict, theorem_statement: str, 
                               problem_context: str) -> float:
        """Calculate numerical quality score from 0.0 to 1.0"""
        
        # Start with base score
        score = 0.0
        
        # Penalize placeholders heavily
        if assessment["is_sorry_proof"]:
            return 0.0  # Sorry is never a real solution
        
        if assessment["is_trivial_only"]:
            # Check if trivial is appropriate for the statement
            if self._is_trivial_appropriate(theorem_statement):
                score = 0.4  # Valid but not sophisticated
            else:
                score = 0.2  # Too simple for complex statement
        else:
            score = 0.3  # At least not trivial
        
        # Reward meaningful mathematical content
        score += 0.15 * assessment["meaningful_tactics"]
        
        # Specific technique bonuses
        if assessment["is_computational"]:
            score += 0.2  # norm_num is valid for arithmetic
        if assessment["is_algebraic"]:
            score += 0.2  # ring is sophisticated
        if assessment["has_case_analysis"]:
            score += 0.3  # by_cases shows logical reasoning
        if assessment["has_existential_reasoning"]:
            score += 0.25  # obtain/use shows proof construction
        
        # Length bonus for substantial proofs
        if assessment["line_count"] > 3:
            score += 0.1
        if assessment["line_count"] > 6:
            score += 0.1
        
        # Problem context adjustments
        if "even number" in theorem_statement.lower():
            # For even number proofs, computational is fine
            if assessment["is_computational"]:
                score += 0.1
        elif "p vs np" in theorem_statement.lower() or "complexity" in problem_context.lower():
            # For complexity theory, need more sophisticated reasoning
            if assessment["has_case_analysis"]:
                score += 0.2
            elif assessment["is_trivial_only"]:
                score = max(score - 0.3, 0.1)  # Penalize trivial for hard problems
        
        return min(score, 1.0)
    
    def _is_trivial_appropriate(self, theorem_statement: str) -> bool:
        """Check if 'trivial' is an appropriate proof technique for this statement"""
        trivial_appropriate = [
            "true", "1 = 1", "2 + 2 = 4", "basic arithmetic"
        ]
        return any(pattern in theorem_statement.lower() for pattern in trivial_appropriate)
    
    def _explain_quality(self, assessment: Dict, score: float) -> str:
        """Generate human-readable explanation of quality assessment"""
        if assessment["is_sorry_proof"]:
            return "Contains 'sorry' - not a real proof, just a placeholder"
        elif score >= 0.8:
            return "High-quality proof with sophisticated mathematical reasoning"
        elif score >= 0.6:
            return "Good proof with meaningful mathematical content"
        elif score >= 0.4:
            return "Valid proof but relatively simple techniques"
        elif assessment["is_trivial_only"]:
            return "Uses only 'trivial' tactic - may be too simple for this statement"
        elif assessment["is_computational"]:
            return "Computational verification (norm_num) - valid for arithmetic"
        else:
            return "Low mathematical substance - mostly placeholder content"
    
    def _assess_mathematical_substance(self, assessment: Dict) -> str:
        """Categorize the type of mathematical reasoning used"""
        if assessment["is_sorry_proof"]:
            return "placeholder"
        elif assessment["has_case_analysis"]:
            return "logical_reasoning"
        elif assessment["has_existential_reasoning"]:
            return "proof_construction"
        elif assessment["is_algebraic"]:
            return "algebraic_manipulation"
        elif assessment["is_computational"]:
            return "computational_verification"
        elif assessment["is_trivial_only"]:
            return "trivial_proof"
        else:
            return "minimal_reasoning"
    
    def generate_quality_report(self, proof_results: List[Dict]) -> Dict:
        """Generate a summary report of proof quality across multiple attempts"""
        if not proof_results:
            return {"status": "no_proofs", "summary": "No proof attempts found"}
        
        total_attempts = len(proof_results)
        successful_attempts = sum(1 for result in proof_results if result.get("success", False))
        
        quality_scores = []
        substance_types = []
        
        for result in proof_results:
            if result.get("success") and "quality_assessment" in result:
                quality = result["quality_assessment"]
                quality_scores.append(quality["quality_score"])
                substance_types.append(quality["mathematical_substance"])
        
        if not quality_scores:
            return {
                "status": "no_quality_data",
                "summary": f"{successful_attempts}/{total_attempts} proofs succeeded but no quality assessment available"
            }
        
        avg_quality = sum(quality_scores) / len(quality_scores)
        max_quality = max(quality_scores)
        meaningful_count = sum(1 for score in quality_scores if score > 0.5)
        
        return {
            "status": "complete",
            "total_attempts": total_attempts,
            "successful_attempts": successful_attempts,
            "average_quality": avg_quality,
            "max_quality": max_quality,
            "meaningful_proofs": meaningful_count,
            "substance_distribution": {subst: substance_types.count(subst) 
                                     for subst in set(substance_types)},
            "summary": self._generate_summary_text(avg_quality, meaningful_count, total_attempts)
        }
    
    def _generate_summary_text(self, avg_quality: float, meaningful_count: int, 
                             total_attempts: int) -> str:
        """Generate human-readable summary of proof session"""
        if avg_quality >= 0.7:
            quality_desc = "high-quality"
        elif avg_quality >= 0.5:
            quality_desc = "moderate-quality"
        elif avg_quality >= 0.3:
            quality_desc = "basic-quality"
        else:
            quality_desc = "low-quality"
        
        meaningful_ratio = meaningful_count / total_attempts if total_attempts > 0 else 0
        
        if meaningful_ratio >= 0.5:
            meaning_desc = "Most proofs show meaningful mathematical reasoning"
        elif meaningful_ratio >= 0.3:
            meaning_desc = "Some proofs demonstrate mathematical substance"
        else:
            meaning_desc = "Few proofs achieve meaningful mathematical content"
        
        return f"Generated {quality_desc} proofs (avg: {avg_quality:.1f}). {meaning_desc}."
