"""
Problem definition and logic for P = NP
"""

# Problem metadata
PROBLEM_NAME = "P vs NP"
MEMORY_FILE = "memory-pvnp.json"

# Initial facts, ideas, and prompts
INITIAL_FACTS = [
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
]

INITIAL_IDEAS = [
    "Try to find a polynomial-time algorithm for SAT or 3-SAT.",
    "Investigate circuit complexity lower bounds for NP-complete problems.",
    "Explore diagonalization arguments to separate P from NP.",
    "Consider the role of oracles and relativization in previous proofs.",
    "Analyze the limitations of current proof techniques and seek new approaches."
]

# Prompts and heuristics
FACT_PROMPT = "P vs NP complexity theory. Recent research: {recent_fact}. New fact: "
IDEA_PROMPT = "Complexity theory research ideas. Previous approaches: {recent_idea}. New research idea: "

# Content filtering configuration (strict for complex problems)
CONTENT_FILTER_CONFIG = {
    "min_mathematical_relevance": 0.3,  # Higher threshold for complexity theory
    "min_length": 15,
    "max_length": 1000,
    "allow_simple_statements": False,
    "domain_keywords": ["complexity", "polynomial", "NP", "algorithm", "proof", "class", "reduction", "SAT"]
}

# Any other problem-specific logic can go here
