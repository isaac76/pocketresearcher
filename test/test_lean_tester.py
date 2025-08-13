import subprocess
import tempfile
import os
import sys
import json

def run_lean_code(lean_code: str):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lean', delete=False) as f:
        f.write(lean_code)
        temp_path = f.name
    try:
        print(f"Running Lean on: {temp_path}\n---")
        result = subprocess.run(['lean', temp_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print("Lean stdout:\n", result.stdout)
        print("Lean stderr:\n", result.stderr)
    finally:
        os.remove(temp_path)

def run_lean_from_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    formal_proofs = data.get('formal_proofs', [])
    found = False
    for i, proof in enumerate(formal_proofs):
        lean_code = proof.get('lean_code', '')
        if lean_code:
            found = True
            print(f"\n=== Proof {i+1} ===")
            print(lean_code)
            run_lean_code(lean_code)
    if not found:
        print("No Lean code found in formal_proofs section.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test_lean_tester.py <lean_code or json_file>")
        print("Or paste Lean code below. End with Ctrl+D (Linux/Mac) or Ctrl+Z (Windows).\n")
        print("Paste Lean code:")
        lean_code = sys.stdin.read()
        run_lean_code(lean_code)
    else:
        arg = sys.argv[1]
        if arg.endswith('.json'):
            run_lean_from_json(arg)
        else:
            run_lean_code(arg)

if __name__ == "__main__":
    main()
