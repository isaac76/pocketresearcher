"""
Unit tests for ProofMemory system
"""

import sys
import os
import unittest
import json
from datetime import datetime

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.memory import ProofMemory


class TestProofMemory(unittest.TestCase):
    """Test cases for ProofMemory class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = "test/test_proof_memory.json"
        # Remove test file if it exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.memory = ProofMemory(self.test_file)
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_create_proof(self):
        """Test creating a new proof"""
        proof_id = self.memory.create_proof(
            description="Test proof",
            statement="Test statement"
        )
        self.assertEqual(proof_id, 1)
        self.assertEqual(len(self.memory.proofs), 1)
        
        proof = self.memory.get_proof(proof_id)
        self.assertIsNotNone(proof)
        self.assertEqual(proof['description'], "Test proof")
        self.assertEqual(proof['statement'], "Test statement")
        self.assertFalse(proof['success'])
    
    def test_add_attempt(self):
        """Test adding an attempt to a proof"""
        proof_id = self.memory.create_proof("Test proof")
        
        success = self.memory.add_attempt(
            proof_id=proof_id,
            proof_method="contradiction",
            axioms_used=["Axiom 1", "Axiom 2"],
            reasoning="Test reasoning",
            success=False
        )
        
        self.assertTrue(success)
        proof = self.memory.get_proof(proof_id)
        self.assertEqual(len(proof['attempts']), 1)
        
        attempt = proof['attempts'][0]
        self.assertEqual(attempt['proof_method'], "contradiction")
        self.assertEqual(attempt['axioms_used'], ["Axiom 1", "Axiom 2"])
        self.assertEqual(attempt['reasoning'], "Test reasoning")
        self.assertFalse(attempt['success'])
    
    def test_successful_attempt_marks_proof(self):
        """Test that a successful attempt marks the proof as successful"""
        proof_id = self.memory.create_proof("Test proof")
        
        # Add failed attempt
        self.memory.add_attempt(
            proof_id=proof_id,
            proof_method="direct",
            axioms_used=["Axiom 1"],
            reasoning="Failed reasoning",
            success=False
        )
        
        proof = self.memory.get_proof(proof_id)
        self.assertFalse(proof['success'])
        
        # Add successful attempt
        self.memory.add_attempt(
            proof_id=proof_id,
            proof_method="contradiction",
            axioms_used=["Axiom 2"],
            reasoning="Successful reasoning",
            success=True
        )
        
        proof = self.memory.get_proof(proof_id)
        self.assertTrue(proof['success'])
    
    def test_mark_as_lemma(self):
        """Test marking a proof as a lemma"""
        proof_id = self.memory.create_proof("Test proof")
        self.memory.add_attempt(
            proof_id=proof_id,
            proof_method="direct",
            axioms_used=["Axiom 1"],
            reasoning="Proof reasoning",
            success=True
        )
        
        self.memory.mark_as_lemma(proof_id, "Test Lemma Statement")
        
        proof = self.memory.get_proof(proof_id)
        self.assertEqual(proof['lemma'], "Test Lemma Statement")
        
        lemmas = self.memory.get_available_lemmas()
        self.assertEqual(len(lemmas), 1)
        self.assertEqual(lemmas[0]['lemma'], "Test Lemma Statement")
    
    def test_get_successful_and_failed_proofs(self):
        """Test filtering proofs by success status"""
        # Create successful proof
        proof_id1 = self.memory.create_proof("Successful proof")
        self.memory.add_attempt(proof_id1, "direct", ["A1"], "Success", success=True)
        
        # Create failed proof
        proof_id2 = self.memory.create_proof("Failed proof")
        self.memory.add_attempt(proof_id2, "direct", ["A1"], "Failed", success=False)
        
        successful = self.memory.get_successful_proofs()
        failed = self.memory.get_failed_proofs()
        
        self.assertEqual(len(successful), 1)
        self.assertEqual(len(failed), 1)
        self.assertEqual(successful[0]['proof_id'], proof_id1)
        self.assertEqual(failed[0]['proof_id'], proof_id2)
    
    def test_persistence(self):
        """Test that data persists across memory instances"""
        # Create proof and save
        proof_id = self.memory.create_proof("Persistent proof")
        self.memory.add_attempt(proof_id, "direct", ["A1"], "Test", success=True)
        
        # Create new memory instance with same file
        memory2 = ProofMemory(self.test_file)
        
        # Check data was loaded
        self.assertEqual(len(memory2.proofs), 1)
        proof = memory2.get_proof(proof_id)
        self.assertIsNotNone(proof)
        self.assertEqual(proof['description'], "Persistent proof")
        self.assertTrue(proof['success'])
    
    def test_statistics(self):
        """Test statistics calculation"""
        # Create multiple proofs
        proof_id1 = self.memory.create_proof("Proof 1")
        self.memory.add_attempt(proof_id1, "contradiction", ["A1"], "Test", success=True)
        
        proof_id2 = self.memory.create_proof("Proof 2")
        self.memory.add_attempt(proof_id2, "induction", ["A2"], "Test", success=False)
        self.memory.add_attempt(proof_id2, "direct", ["A3"], "Test", success=False)
        
        stats = self.memory.get_statistics()
        
        self.assertEqual(stats['total_proofs'], 2)
        self.assertEqual(stats['successful_proofs'], 1)
        self.assertEqual(stats['failed_proofs'], 1)
        self.assertEqual(stats['total_attempts'], 3)
        self.assertEqual(stats['methods_used']['contradiction'], 1)
        self.assertEqual(stats['methods_used']['induction'], 1)
        self.assertEqual(stats['methods_used']['direct'], 1)
    
    def test_find_proofs_by_description(self):
        """Test searching proofs by keyword"""
        self.memory.create_proof("Prove that sum of evens is even")
        self.memory.create_proof("Prove there is no largest prime")
        self.memory.create_proof("Prove Pythagorean theorem")
        
        results = self.memory.find_proofs_by_description("even")
        self.assertEqual(len(results), 1)
        self.assertIn("even", results[0]['description'].lower())
        
        results = self.memory.find_proofs_by_description("prove")
        self.assertEqual(len(results), 3)


class TestProofMemoryIntegration(unittest.TestCase):
    """Integration test with realistic proof example"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = "test/test_integration_memory.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.memory = ProofMemory(self.test_file)
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_realistic_proof_workflow(self):
        """Test a realistic proof workflow: no largest natural number"""
        # Create the proof
        proof_id = self.memory.create_proof(
            description="Prove there is no largest natural number",
            statement="For all n in N, there exists m in N such that m > n"
        )
        
        # First attempt: Try contradiction but make a mistake
        self.memory.add_attempt(
            proof_id=proof_id,
            proof_method="contradiction",
            axioms_used=["Peano axiom - successor"],
            reasoning="Assume there is a largest natural number N. But then N+1 > N, which contradicts our assumption. However, I didn't properly establish that N+1 is a natural number.",
            success=False
        )
        
        # Second attempt: Constructive proof (successful)
        self.memory.add_attempt(
            proof_id=proof_id,
            proof_method="constructive",
            axioms_used=["Peano axiom - successor", "Peano axiom - zero"],
            reasoning="""
For any natural number n, we can construct m = S(n) (the successor of n).
By the Peano axioms:
1. S(n) is a natural number (successor of a natural number is a natural number)
2. By definition of successor, S(n) > n
Therefore, for any n, there exists m = S(n) where m > n.
This proves there is no largest natural number.
            """.strip(),
            success=True
        )
        
        # Mark as lemma for future use
        self.memory.mark_as_lemma(
            proof_id,
            "For any natural number n, there exists a natural number m such that m > n"
        )
        
        # Verify the proof state
        proof = self.memory.get_proof(proof_id)
        self.assertTrue(proof['success'])
        self.assertEqual(len(proof['attempts']), 2)
        self.assertIsNotNone(proof['lemma'])
        
        # Verify we can retrieve this as a lemma
        lemmas = self.memory.get_available_lemmas()
        self.assertEqual(len(lemmas), 1)
        
        # Print for manual verification
        print("\n" + "="*60)
        print("INTEGRATION TEST: Realistic Proof Workflow")
        print("="*60)
        self.memory.print_proof(proof_id)
        self.memory.print_statistics()


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
