import importlib
import os
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("GOOGLE_API_KEY", "test-key")


class StubLogger:
    def __init__(self):
        self.messages = []

    def info(self, message, *args):
        self.messages.append(message.format(*args))


class ExampleLoggingTest(unittest.TestCase):
    def _assert_logs_question_and_answer(
        self,
        module_name: str,
        function_name: str,
        expected_answer_label: str,
    ) -> None:
        module = importlib.import_module(module_name)
        logger = StubLogger()

        setattr(module, "logger", logger)
        setattr(module, function_name, lambda _: "odpowiedz-testowa")

        module.pokaz_przyklad()

        self.assertEqual(
            logger.messages,
            [
                f"Pytanie:\n{module.PYTANIE}",
                f"{expected_answer_label}odpowiedz-testowa",
            ],
        )

    def test_example_openai_uses_logger(self):
        self._assert_logs_question_and_answer(
            "example_openai",
            "zapytaj_openai",
            "Odpowiedź (OpenAI):\n",
        )

    def test_example_anthropic_uses_logger(self):
        self._assert_logs_question_and_answer(
            "example_anthropic",
            "zapytaj_claude",
            "Odpowiedź (Claude):\n",
        )

    def test_example_gemini_uses_logger(self):
        self._assert_logs_question_and_answer(
            "example_gemini",
            "zapytaj_gemini",
            "Odpowiedź (Gemini):\n",
        )


if __name__ == "__main__":
    unittest.main()
