import unittest
import os
import json
from datetime import datetime
from src.memory import Memory
from src.pocketresearcher import extract_fact_idea, is_novel_idea

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

    def test_extract_fact_idea(self):
        text = "Fact: P != NP\nIdea: Try diagonalization."
        fact, idea = extract_fact_idea(text)
        self.assertEqual(fact, "P != NP")
        self.assertEqual(idea, "Try diagonalization.")

    def test_is_novel_idea(self):
        ideas = ["Try diagonalization.", "Use SAT reduction."]
        self.assertTrue(is_novel_idea("Explore quantum algorithms.", ideas))
        self.assertFalse(is_novel_idea("Try diagonalization.", ideas))

if __name__ == "__main__":
    unittest.main()
