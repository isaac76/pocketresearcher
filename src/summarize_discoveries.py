"""
Summarize discoveries from memory.json for PocketResearcher
"""
import json
import os

MEMORY_PATH = os.path.join(os.path.dirname(__file__), "../memory.json")

def load_memory(path):
    with open(path, "r") as f:
        return json.load(f)

def summarize_memory(memory):
    summary = []
    facts = memory.get("facts", [])
    ideas = memory.get("ideas", [])
    proofs = memory.get("proofs", [])
    breakthroughs = memory.get("breakthroughs", [])

    summary.append(f"Facts discovered: {len(facts)}")
    if facts:
        summary.append("Sample facts:")
        for fact in facts[:3]:
            summary.append(f"- {fact}")

    summary.append(f"Ideas generated: {len(ideas)}")
    if ideas:
        summary.append("Sample ideas:")
        for idea in ideas[:3]:
            summary.append(f"- {idea}")

    summary.append(f"Proofs attempted: {len(proofs)}")
    successful = [p for p in proofs if isinstance(p, dict) and p.get("success")]
    summary.append(f"Successful proofs: {len(successful)}")
    if successful:
        summary.append("Sample successful proofs:")
        for proof in successful[:2]:
            summary.append(f"- {proof.get('informal_statement', str(proof)[:60])}")

    summary.append(f"Breakthroughs recorded: {len(breakthroughs)}")
    if breakthroughs:
        summary.append("Sample breakthroughs:")
        for br in breakthroughs[:2]:
            summary.append(f"- {str(br)[:80]}")

    return "\n".join(summary)

def main():
    try:
        memory = load_memory(MEMORY_PATH)
        print("PocketResearcher Discovery Summary:")
        print("="*40)
        print(summarize_memory(memory))
    except Exception as e:
        print(f"Error reading memory.json: {e}")

if __name__ == "__main__":
    main()
