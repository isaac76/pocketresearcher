import unittest
import os
import json
from datetime import datetime
from src.memory import Memory
from src.pocketresearcher import is_novel_content
from src.llm_manager import LLMManager

class TestPocketResearcher(unittest.TestCase):
    def setUp(self):
        self.test_memory_file = "test_memory.json"
        self.memory = {
            "facts": ["Fact 1", "Fact 2"],
            "ideas": ["Idea 1", "Idea 2"],
            "reflections": ["Reflection 1"]
        }
        self.memory_store = Memory({"file_path": self.test_memory_file, "backend": "file"})
        self.memory_store.save(self.memory)

    def tearDown(self):
        if os.path.exists(self.test_memory_file):
            os.remove(self.test_memory_file)

    def test_load_and_save_memory(self):
        loaded = self.memory_store.load()
        self.assertEqual(loaded, self.memory)

    def test_novelty_detection(self):
        ideas = ["Try diagonalization.", "Use reduction techniques."]
        facts = ["P != NP", "NP contains non-deterministic polynomial problems"]
        
        # Test novel content detection for ideas
        self.assertTrue(is_novel_content("Explore quantum algorithms.", ideas))
        self.assertFalse(is_novel_content("Try diagonalization.", ideas))
        
        # Test novel content detection for facts
        self.assertTrue(is_novel_content("P contains polynomial time problems", facts))
        self.assertFalse(is_novel_content("P != NP", facts))

    def test_llm_manager_initialization(self):
        """Test that LLM manager can be initialized"""
        try:
            llm_manager = LLMManager()
            self.assertIsNotNone(llm_manager)
            self.assertIn(llm_manager.current_model, ["gemini", "phi2", "gpt2", "gpt2-medium", "gpt2-large"])
        except Exception as e:
            # It's OK if initialization fails due to missing dependencies
            self.assertIsInstance(e, (ImportError, OSError, ValueError))

if __name__ == "__main__":
    unittest.main()
