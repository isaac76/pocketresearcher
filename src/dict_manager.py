#!/usr/bin/env python3
"""
Dictionary Manager for PocketResearcher

Utility to manage the unified dictionary.json file that stores all experiments
organized by category.

Usage:
    python dict_manager.py list                    # List all categories
    python dict_manager.py status                  # Show status of all problems
    python dict_manager.py show <category>         # Show detailed info for category
    python dict_manager.py solved                  # List solved problems
    python dict_manager.py theorems               # List reusable theorems
    python dict_manager.py migrate <old_file>     # Migrate old memory file to dictionary
"""

import sys
import json
import os
from datetime import datetime

class DictionaryManager:
    def __init__(self, dict_path="dictionary.json"):
        self.dict_path = dict_path
        
    def load_dictionary(self):
        """Load the dictionary file"""
        if os.path.exists(self.dict_path):
            with open(self.dict_path, 'r') as f:
                return json.load(f)
        return {"categories": {}}
    
    def save_dictionary(self, data):
        """Save the dictionary file"""
        with open(self.dict_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def list_categories(self):
        """List all categories in the dictionary"""
        data = self.load_dictionary()
        categories = data.get("categories", {})
        
        print("📚 Dictionary Categories:")
        print("=" * 40)
        
        if not categories:
            print("No categories found.")
            return
            
        for category, info in categories.items():
            facts_count = len(info.get("facts", []))
            ideas_count = len(info.get("ideas", []))
            proofs_count = len(info.get("formal_proofs", []))
            solved = "✅ SOLVED" if info.get("solved", False) else "🔬 Active"
            
            print(f"{category:20} | {solved:10} | Facts: {facts_count:3} | Ideas: {ideas_count:3} | Proofs: {proofs_count:3}")
    
    def show_status(self):
        """Show overall status"""
        data = self.load_dictionary()
        categories = data.get("categories", {})
        
        total_categories = len(categories)
        solved_count = sum(1 for cat in categories.values() if cat.get("solved", False))
        active_count = total_categories - solved_count
        
        total_facts = sum(len(cat.get("facts", [])) for cat in categories.values())
        total_ideas = sum(len(cat.get("ideas", [])) for cat in categories.values())
        total_proofs = sum(len(cat.get("formal_proofs", [])) for cat in categories.values())
        
        print("📊 Dictionary Status:")
        print("=" * 40)
        print(f"Total Categories: {total_categories}")
        print(f"Solved Problems: {solved_count}")
        print(f"Active Problems: {active_count}")
        print(f"Total Facts: {total_facts}")
        print(f"Total Ideas: {total_ideas}")
        print(f"Total Formal Proofs: {total_proofs}")
    
    def show_category(self, category):
        """Show detailed information for a specific category"""
        data = self.load_dictionary()
        categories = data.get("categories", {})
        
        if category not in categories:
            print(f"❌ Category '{category}' not found.")
            return
        
        cat_data = categories[category]
        
        print(f"📖 Category: {category}")
        print("=" * 50)
        
        if cat_data.get("solved", False):
            print("✅ Status: SOLVED")
            if "solved_timestamp" in cat_data:
                print(f"🕒 Solved at: {cat_data['solved_timestamp']}")
        else:
            print("🔬 Status: Active")
        
        print(f"\n📝 Facts ({len(cat_data.get('facts', []))}):")
        for i, fact in enumerate(cat_data.get("facts", [])[:5], 1):
            print(f"  {i}. {fact[:100]}{'...' if len(fact) > 100 else ''}")
        if len(cat_data.get("facts", [])) > 5:
            print(f"  ... and {len(cat_data.get('facts', [])) - 5} more")
        
        print(f"\n💡 Ideas ({len(cat_data.get('ideas', []))}):")
        for i, idea in enumerate(cat_data.get("ideas", [])[:3], 1):
            print(f"  {i}. {idea[:100]}{'...' if len(idea) > 100 else ''}")
        if len(cat_data.get("ideas", [])) > 3:
            print(f"  ... and {len(cat_data.get('ideas', [])) - 3} more")
        
        print(f"\n🔬 Formal Proofs ({len(cat_data.get('formal_proofs', []))}):")
        for i, proof in enumerate(cat_data.get("formal_proofs", []), 1):
            theorem_name = proof.get("theorem_name", "Unknown")
            success = "✅" if proof.get("success", False) else "❌"
            print(f"  {i}. {success} {theorem_name}")
    
    def list_solved(self):
        """List all solved problems"""
        data = self.load_dictionary()
        categories = data.get("categories", {})
        
        solved_problems = {cat: info for cat, info in categories.items() if info.get("solved", False)}
        
        print("✅ Solved Problems:")
        print("=" * 40)
        
        if not solved_problems:
            print("No solved problems yet.")
            return
        
        for category, info in solved_problems.items():
            proofs_count = len(info.get("formal_proofs", []))
            timestamp = info.get("solved_timestamp", "Unknown time")
            print(f"{category:20} | Proofs: {proofs_count:2} | Solved: {timestamp}")
    
    def list_theorems(self):
        """List all reusable theorems from solved problems"""
        data = self.load_dictionary()
        categories = data.get("categories", {})
        
        print("📚 Reusable Theorems:")
        print("=" * 50)
        
        theorem_count = 0
        for category, info in categories.items():
            if info.get("solved", False):
                for proof in info.get("formal_proofs", []):
                    if proof.get("success", False) and proof.get("verification_status") == "verified":
                        theorem_count += 1
                        theorem_name = proof.get("theorem_name", "Unknown")
                        print(f"{theorem_count:2}. {theorem_name} (from {category})")
                        print(f"    {proof.get('informal_statement', 'No description')[:80]}...")
        
        if theorem_count == 0:
            print("No verified reusable theorems found.")
        else:
            print(f"\nTotal: {theorem_count} reusable theorems")
    
    def migrate_old_file(self, old_file_path, target_category):
        """Migrate an old memory file to the dictionary"""
        if not os.path.exists(old_file_path):
            print(f"❌ File '{old_file_path}' not found.")
            return
        
        # Load old memory file
        with open(old_file_path, 'r') as f:
            old_data = json.load(f)
        
        # Load current dictionary
        dict_data = self.load_dictionary()
        
        # Ensure categories structure
        if "categories" not in dict_data:
            dict_data["categories"] = {}
        
        # Add migrated data
        dict_data["categories"][target_category] = old_data
        
        # Save updated dictionary
        self.save_dictionary(dict_data)
        
        print(f"✅ Migrated {old_file_path} to dictionary.json under category '{target_category}'")
        
        # Show stats
        facts_count = len(old_data.get("facts", []))
        ideas_count = len(old_data.get("ideas", []))
        proofs_count = len(old_data.get("formal_proofs", []))
        print(f"   Migrated: {facts_count} facts, {ideas_count} ideas, {proofs_count} formal proofs")

    def ensure_axioms_category(self, axioms: dict, category: str = "axioms"):
        """Ensure a dedicated 'axioms' category exists in the dictionary and
        populate its facts from the provided axioms mapping (concatenate all
        lists). This is idempotent and will overwrite the facts list for the
        axioms category so it matches the provided axioms.
        """
        dict_data = self.load_dictionary()
        if "categories" not in dict_data:
            dict_data["categories"] = {}

        # Build flattened list of axiom strings preserving order
        flattened = []
        seen = set()
        for v in axioms.values():
            if isinstance(v, list):
                for item in v:
                    if not isinstance(item, str):
                        continue
                    if item in seen:
                        continue
                    seen.add(item)
                    flattened.append(item)

        # Ensure category structure
        cat = dict_data["categories"].get(category, {})
        # Primary storage: facts is a flattened list of canonical axioms
        cat["facts"] = flattened
        # If the provided axioms include specialized strategy templates,
        # persist them under a dedicated key so callers can include them
        # separately (e.g. as "Strategy: ..." in prompts).
        proof_strats = []
        seen_strat = set()
        for s in axioms.get("proof_strategies", []):
            if isinstance(s, str) and s not in seen_strat:
                seen_strat.add(s)
                proof_strats.append(s)
        if proof_strats:
            cat["proof_strategies"] = proof_strats
        else:
            # Ensure the key exists for consumers
            cat.setdefault("proof_strategies", [])
        # Ensure required arrays exist
        cat.setdefault("ideas", [])
        cat.setdefault("reflections", [])
        cat.setdefault("proofs", [])
        cat.setdefault("techniques", [])
        cat.setdefault("experiments", [])
        cat.setdefault("formal_proofs", [])

        dict_data["categories"][category] = cat
        self.save_dictionary(dict_data)
        print(f"\u2705 Ensured axioms category '{category}' with {len(flattened)} facts in {self.dict_path}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    manager = DictionaryManager()
    command = sys.argv[1]
    
    if command == "list":
        manager.list_categories()
    elif command == "status":
        manager.show_status()
    elif command == "show" and len(sys.argv) > 2:
        manager.show_category(sys.argv[2])
    elif command == "solved":
        manager.list_solved()
    elif command == "theorems":
        manager.list_theorems()
    elif command == "migrate" and len(sys.argv) > 3:
        old_file = sys.argv[2]
        category = sys.argv[3]
        manager.migrate_old_file(old_file, category)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
