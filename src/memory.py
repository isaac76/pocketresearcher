"""
Memory System for Tracking Mathematical Proofs

Stores proof attempts, methods used, axioms applied, and success/failure status.
Uses JSON for persistent storage.
"""

import json
import os
from typing import List, Dict, Optional, Any
from datetime import datetime


class ProofMemory:
    """Manages storage and retrieval of proof attempts"""
    
    def __init__(self, memory_file: str = "proofs/proof_memory.json"):
        """
        Initialize the proof memory system
        
        Args:
            memory_file: Path to the JSON file for persistent storage
        """
        self.memory_file = memory_file
        
        # Ensure the proofs directory exists
        proofs_dir = os.path.dirname(memory_file)
        if proofs_dir and not os.path.exists(proofs_dir):
            os.makedirs(proofs_dir)
            print(f"✓ Created directory: {proofs_dir}")
        
        self.proofs = []
        self._next_proof_id = 1
        self.load()
    
    def load(self):
        """Load existing proofs from JSON file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.proofs = data.get('proofs', [])
                    self._next_proof_id = data.get('next_proof_id', 1)
                print(f"✓ Loaded {len(self.proofs)} proofs from {self.memory_file}")
            except Exception as e:
                print(f"⚠ Error loading memory: {e}")
                self.proofs = []
                self._next_proof_id = 1
        else:
            print(f"✓ Starting fresh - no existing memory file")
            self.proofs = []
    
    def save(self):
        """Save all proofs to JSON file"""
        try:
            data = {
                'proofs': self.proofs,
                'next_proof_id': self._next_proof_id,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Saved {len(self.proofs)} proofs to {self.memory_file}")
        except Exception as e:
            print(f"✗ Error saving memory: {e}")
    
    def create_proof(self, description: str, statement: str = None) -> int:
        """
        Create a new proof entry
        
        Args:
            description: Human-readable description of what to prove
            statement: Optional formal statement (e.g., "For all n in N, exists m > n")
        
        Returns:
            proof_id: Unique identifier for this proof
        """
        proof_id = self._next_proof_id
        self._next_proof_id += 1
        
        proof = {
            'proof_id': proof_id,
            'description': description,
            'statement': statement,
            'attempts': [],
            'lemma': None,
            'success': False,
            'created_at': datetime.now().isoformat()
        }
        
        self.proofs.append(proof)
        self.save()
        print(f"✓ Created proof #{proof_id}: {description}")
        return proof_id
    
    def add_attempt(self, 
                   proof_id: int,
                   proof_method: str,
                   axioms_used: List[str],
                   reasoning: str,
                   success: bool = False,
                   failure_analysis: str = None) -> bool:
        """
        Add an attempt to prove something
        
        Args:
            proof_id: ID of the proof to add attempt to
            proof_method: Name of proof method used (e.g., "contradiction", "induction")
            axioms_used: List of axioms/lemmas used in the attempt
            reasoning: The actual proof reasoning/text
            success: Whether this attempt succeeded
            failure_analysis: Optional analysis of why the attempt failed
        
        Returns:
            True if attempt was added successfully
        """
        proof = self._get_proof_by_id(proof_id)
        if not proof:
            print(f"✗ Proof #{proof_id} not found")
            return False
        
        attempt = {
            'attempt_number': len(proof['attempts']) + 1,
            'proof_method': proof_method,
            'axioms_used': axioms_used,
            'reasoning': reasoning,
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
        
        if failure_analysis:
            attempt['failure_analysis'] = failure_analysis
        
        proof['attempts'].append(attempt)
        
        # If this attempt succeeded, mark the whole proof as successful
        if success:
            proof['success'] = True
            print(f"🎉 Proof #{proof_id} marked as SUCCESSFUL!")
        else:
            print(f"⚠️  Proof #{proof_id} attempt failed")
        
        self.save()
        print(f"✓ Added attempt #{attempt['attempt_number']} to proof #{proof_id}")
        return True
    
    def mark_as_lemma(self, proof_id: int, lemma_statement: str):
        """
        Mark a successful proof as a lemma that can be used in future proofs
        
        Args:
            proof_id: ID of the proven statement
            lemma_statement: Concise statement of the lemma for reuse
        """
        proof = self._get_proof_by_id(proof_id)
        if not proof:
            print(f"✗ Proof #{proof_id} not found")
            return False
        
        if not proof['success']:
            print(f"⚠ Warning: Marking unproven statement as lemma")
        
        proof['lemma'] = lemma_statement
        self.save()
        print(f"✓ Proof #{proof_id} marked as lemma: {lemma_statement}")
        return True
    
    def get_proof(self, proof_id: int) -> Optional[Dict]:
        """Get a specific proof by ID"""
        return self._get_proof_by_id(proof_id)
    
    def get_all_proofs(self) -> List[Dict]:
        """Get all proofs"""
        return self.proofs
    
    def get_successful_proofs(self) -> List[Dict]:
        """Get all successful proofs"""
        return [p for p in self.proofs if p['success']]
    
    def get_failed_proofs(self) -> List[Dict]:
        """Get all proofs that haven't succeeded yet"""
        return [p for p in self.proofs if not p['success']]
    
    def get_available_lemmas(self) -> List[Dict]:
        """Get all proven statements that can be used as lemmas"""
        return [p for p in self.proofs if p['success'] and p['lemma']]
    
    def get_failed_attempts(self, proof_id: int) -> List[Dict]:
        """Get all failed attempts for a specific proof (to learn from mistakes)"""
        proof = self._get_proof_by_id(proof_id)
        if not proof:
            return []
        return [a for a in proof['attempts'] if not a['success']]
    
    def find_proofs_by_description(self, keyword: str) -> List[Dict]:
        """Search for proofs by keyword in description"""
        keyword_lower = keyword.lower()
        return [p for p in self.proofs if keyword_lower in p['description'].lower()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about proof attempts"""
        total_proofs = len(self.proofs)
        successful = len(self.get_successful_proofs())
        failed = total_proofs - successful
        total_attempts = sum(len(p['attempts']) for p in self.proofs)
        lemmas = len(self.get_available_lemmas())
        
        # Count proof methods used
        method_counts = {}
        for proof in self.proofs:
            for attempt in proof['attempts']:
                method = attempt['proof_method']
                method_counts[method] = method_counts.get(method, 0) + 1
        
        return {
            'total_proofs': total_proofs,
            'successful_proofs': successful,
            'failed_proofs': failed,
            'success_rate': f"{(successful/total_proofs*100):.1f}%" if total_proofs > 0 else "0%",
            'total_attempts': total_attempts,
            'available_lemmas': lemmas,
            'methods_used': method_counts
        }
    
    def print_statistics(self):
        """Print a summary of proof statistics"""
        stats = self.get_statistics()
        print("\n" + "="*50)
        print("PROOF MEMORY STATISTICS")
        print("="*50)
        print(f"Total Proofs: {stats['total_proofs']}")
        print(f"  ✓ Successful: {stats['successful_proofs']}")
        print(f"  ✗ Failed: {stats['failed_proofs']}")
        print(f"  Success Rate: {stats['success_rate']}")
        print(f"Total Attempts: {stats['total_attempts']}")
        print(f"Available Lemmas: {stats['available_lemmas']}")
        if stats['methods_used']:
            print("\nProof Methods Used:")
            for method, count in sorted(stats['methods_used'].items(), key=lambda x: x[1], reverse=True):
                print(f"  - {method}: {count}")
        print("="*50 + "\n")
    
    def print_proof(self, proof_id: int):
        """Print detailed information about a specific proof"""
        proof = self._get_proof_by_id(proof_id)
        if not proof:
            print(f"✗ Proof #{proof_id} not found")
            return
        
        print("\n" + "="*50)
        print(f"PROOF #{proof['proof_id']}")
        print("="*50)
        print(f"Description: {proof['description']}")
        if proof['statement']:
            print(f"Statement: {proof['statement']}")
        print(f"Status: {'✓ PROVEN' if proof['success'] else '✗ NOT YET PROVEN'}")
        if proof['lemma']:
            print(f"Lemma: {proof['lemma']}")
        print(f"\nAttempts: {len(proof['attempts'])}")
        
        for i, attempt in enumerate(proof['attempts'], 1):
            print(f"\n--- Attempt #{i} ---")
            print(f"Method: {attempt['proof_method']}")
            print(f"Axioms Used: {', '.join(attempt['axioms_used']) if attempt['axioms_used'] else 'None'}")
            print(f"Status: {'✓ SUCCESS' if attempt['success'] else '✗ FAILED'}")
            print(f"Reasoning:\n{attempt['reasoning'][:200]}{'...' if len(attempt['reasoning']) > 200 else ''}")
        
        print("="*50 + "\n")
    
    def _get_proof_by_id(self, proof_id: int) -> Optional[Dict]:
        """Internal method to find proof by ID"""
        for proof in self.proofs:
            if proof['proof_id'] == proof_id:
                return proof
        return None


if __name__ == "__main__":
    print("ProofMemory module - run tests with: python test/test_memory.py")
