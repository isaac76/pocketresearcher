"""
Problem definition and logic for direct proof that the sum of any two even numbers is also even
"""

# Problem metadata
PROBLEM_NAME = "Even Sum"
MEMORY_FILE = "memory-even-proof.json"

# Initial facts, ideas, and prompts
INITIAL_FACTS = [
    "An even number is defined as an integer that is divisible by 2.",
    "Even numbers can be written in the form 2k, where k is an integer.",
    "Addition is a binary operation on integers.",
    "The sum of two integers is also an integer.",
    "Odd numbers are integers not divisible by 2."
]

INITIAL_IDEAS = [
    "To prove that the sum of two even numbers is even we can try to form an algebraic expression."
]

# Prompts and heuristics
FACT_PROMPT = "Number theory. Recent fact: {recent_fact}. State a new fact about even numbers or their sums:"
IDEA_PROMPT = "Number theory research ideas. Previous approach: {recent_idea}. Suggest a new idea for proving properties of even numbers:"

# Content filtering configuration (more lenient for simpler problems)
CONTENT_FILTER_CONFIG = {
    "min_mathematical_relevance": 0.1,  # Lower threshold for basic number theory
    "min_length": 10,
    "max_length": 500,
    "math_keywords": [
        "even", "odd", "integer", "sum", "add", "addition", "divisible", "divisibility",
        "arithmetic", "number", "proof", "theorem", "algebra", "algebraic", "expression",
        "form", "2k", "binary", "operation", "property", "mathematical", "define", "definition"
    ],
    "allow_simple_statements": True,
    "domain_keywords": ["even", "odd", "number", "integer", "sum", "addition", "proof", "algebra"]
}

# Any other problem-specific logic can go here
