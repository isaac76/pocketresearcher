import unittest
from unittest.mock import patch, MagicMock

from src.pocketresearcher import run_single_research_step
from src.pocketresearcher import extract_meaningful_content
from src.pocketresearcher import is_novel_content

class TestPromptsIncludeAxiomsAndStrategies(unittest.TestCase):
    def setUp(self):
        # Minimal memory and config stubs
        import unittest
        from unittest.mock import MagicMock

        import sys
        import types

        from src.pocketresearcher import run_single_research_step


        class TestPromptsIncludeAxiomsAndStrategies(unittest.TestCase):
            def setUp(self):
                # Minimal memory and config stubs
                self.memory = {
                    "facts": ["Existing fact"],
                    "ideas": ["Existing idea"],
                    "formal_proofs": []
                }

                class Cfg:
                    FACT_PROMPT = "Recent fact: {recent_fact}. New fact:"
                    IDEA_PROMPT = "Previous approach: {recent_idea}. New idea:"
                    MAX_TOKENS = 10
                    ENABLE_FORMAL_PROOFS = False
                    PROOF_GENERATION_FREQUENCY = 1
                    problem_name = "test_problem"
                    INITIAL_FACTS = []
                    INITIAL_IDEAS = []
                    CONTENT_FILTER_CONFIG = {"min_mathematical_relevance": 0.0, "domain_keywords": []}
                    ENABLE_LEAN_TRANSLATION = False

                self.cfg = Cfg()

            def test_prompt_contains_axioms_and_strategies(self):
                # Prepare the mock DictionaryManager to return axioms and strategies
                mock_dm = MagicMock()
                mock_dm.load_dictionary.return_value = {
                    "categories": {
                        "axioms": {
                            "facts": ["Addition identity: For all n, n + 0 = n."],
                            "proof_strategies": ["Induction on first variable: show base and inductive step."]
                        }
                    }
                }

                # Mock LLM manager to capture the prompt passed
                class FakeLLM:
                    def __init__(self):
                        self.last_prompt = None

                    def generate(self, prompt, max_tokens=None):
                        self.last_prompt = prompt
                        return "A plausible fact: 0 is additive identity."

                fake_llm = FakeLLM()

                # Content filter stub that accepts everything
                class FakeFilter:
                    def should_keep_content(self, content, ctype):
                        return True, "Quality content (relevance: 0.9)"

                # Inject a fake dict_manager module so runtime import resolves inside the function under test
                fake_module = types.SimpleNamespace(DictionaryManager=lambda: mock_dm)
                sys.modules['dict_manager'] = fake_module
                sys.modules['src.dict_manager'] = fake_module

                try:
                    # Call the function under test. Pass MagicMock for engines not used in this test.
                    result = run_single_research_step(self.memory, self.cfg, fake_llm, FakeFilter(),
                                                      MagicMock(), MagicMock(), MagicMock(), MagicMock())
                finally:
                    # Clean up sys.modules entries we injected
                    del sys.modules['dict_manager']
                    del sys.modules['src.dict_manager']

                # Assert LLM saw both an Axiom: and a Strategy: line
                self.assertIsNotNone(fake_llm.last_prompt)
                prompt_text = fake_llm.last_prompt
                self.assertIn("Axiom: Addition identity", prompt_text)
                self.assertIn("Strategy: Induction on first variable", prompt_text)


        if __name__ == '__main__':
            unittest.main()
    # Clean up sys.modules entries we injected
