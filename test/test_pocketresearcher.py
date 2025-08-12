import unittest
import os
import json
from datetime import datetime
from src.memory import Memory
from src.pocketresearcher import is_novel_idea, is_novel_fact
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

    def test_is_novel_idea(self):
        ideas = ["Try diagonalization.", "Use SAT reduction."]
        self.assertTrue(is_novel_idea("Explore quantum algorithms.", ideas))
        self.assertFalse(is_novel_idea("Try diagonalization.", ideas))

    def test_is_novel_fact(self):
        facts = ["P != NP", "NP is a complexity class"]
        self.assertTrue(is_novel_fact("P contains polynomial time problems", facts))
        self.assertFalse(is_novel_fact("P != NP", facts))

    def test_llm_manager_initialization(self):
        """Test that LLM manager can be initialized"""
        try:
            llm_manager = LLMManager()
            self.assertIsNotNone(llm_manager)
            self.assertIn(llm_manager.current_model, ["gemini", "phi2", "gpt2"])
        except Exception as e:
            # It's OK if initialization fails due to missing dependencies
            self.assertIsInstance(e, (ImportError, OSError, ValueError))

if __name__ == "__main__":
    unittest.main()
