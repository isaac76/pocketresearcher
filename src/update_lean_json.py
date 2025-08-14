"""
update_lean_json.py

Script to update Lean code snippets in .json memory files to use Lean 4 Mathlib imports and idioms.
- Replaces old Lean 3 imports (e.g., 'import data.nat.parity') with 'import Mathlib.Algebra.Ring.Parity'.
- Ensures theorem statements use 'Even'/'Odd' (capitalized).
- Prepends imports if missing.
- Optionally, can be extended to fix other Lean 3 to Lean 4 issues.

Usage:
    python update_lean_json.py memory-even-proof.json
"""
import sys
import json
import re
from pathlib import Path

LEAN4_IMPORTS = "import Mathlib.Algebra.Ring.Parity\n\n"

# Patterns for Lean 3 imports and lowercase even/odd
LEAN3_IMPORTS = [
    r"import data.nat.parity",
    r"import data.nat.basic",
    r"import tactic"
]

# Fix theorem statements and proof attempts
THEOREM_PATTERN = re.compile(r"theorem ([^(]+)\(([^)]*)\) *: *([^{:=]+) *:?=?.*")

# Fix Even/Odd capitalization
EVEN_ODD_FIX = [
    (re.compile(r"\beven\b"), "Even"),
    (re.compile(r"\bodd\b"), "Odd")
]


def fix_imports(lean_code: str) -> str:
    # Remove old imports
    for pat in LEAN3_IMPORTS:
        lean_code = re.sub(pat, "", lean_code, flags=re.IGNORECASE)
    # Remove duplicate new imports
    lean_code = re.sub(r"import Mathlib.Data.Nat.Parity", "import Mathlib.Algebra.Ring.Parity", lean_code)
    lean_code = re.sub(r"import Mathlib.Tactic", "", lean_code)
    # Prepend correct imports
    lean_code = LEAN4_IMPORTS + lean_code.lstrip()
    return lean_code

def fix_even_odd(lean_code: str) -> str:
    for pat, repl in EVEN_ODD_FIX:
        lean_code = pat.sub(repl, lean_code)
    return lean_code

def update_lean_code(lean_code: str) -> str:
    code = fix_imports(lean_code)
    code = fix_even_odd(code)
    return code

def update_json_file(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    changed = False
    for section in ["formal_proofs", "proofs"]:
        if section in data:
            for entry in data[section]:
                for key in ["lean_statement", "proof_attempt"]:
                    if key in entry and isinstance(entry[key], str):
                        orig = entry[key]
                        updated = update_lean_code(orig)
                        if updated != orig:
                            entry[key] = updated
                            changed = True
    if changed:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Updated: {json_path}")
    else:
        print(f"No changes needed: {json_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_lean_json.py <json_file>")
        sys.exit(1)
    update_json_file(Path(sys.argv[1]))
