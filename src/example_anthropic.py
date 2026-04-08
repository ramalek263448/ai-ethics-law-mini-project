"""
Przykład użycia Anthropic API (Claude) w mini-projekcie.

Pomysł na projekt (temat 9):
    Analiza Terms of Service / regulaminów API AI
    — porównaj regulaminy OpenAI, Anthropic, Google pod kątem
    praw do danych, własności outputu, wykorzystania danych treningowych.

Pomysł na projekt (temat 13):
    Generator polityki prywatności dla projektu AI
    — na podstawie ankiety o projekcie wygeneruj draft polityki
    prywatności zgodnej z RODO.

Uruchomienie:
    cp .env.example .env   # uzupełnij ANTHROPIC_API_KEY
    uv run src/example_anthropic.py
"""

from dotenv import load_dotenv
from anthropic import Anthropic
from loguru import logger

load_dotenv()  # wczytuje zmienne z pliku .env

client = Anthropic()  # automatycznie czyta ANTHROPIC_API_KEY z env

# --- Prompt bazowy ---
SYSTEM_PROMPT = """Jesteś ekspertem od prawa i etyki sztucznej inteligencji.
Odpowiadasz po polsku, zwięźle i merytorycznie.
Podajesz podstawę prawną (artykuł ustawy / rozporządzenia) gdy to możliwe."""

PYTANIE = (
    "Porównaj podejście do własności outputu (kto jest właścicielem "
    "tekstu wygenerowanego przez model) w regulaminach OpenAI, Anthropic "
    "i Google. Jakie ryzyka prawne niesie to dla użytkownika komercyjnego?"
)


def zapytaj_claude(pytanie: str, model: str = "claude-haiku-4-5-20251001") -> str:
    """Wysyła pytanie do Claude i zwraca odpowiedź."""
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": pytanie},
        ],
    )
    return message.content[0].text


def pokaz_przyklad() -> None:
    """Uruchamia przykładowe zapytanie i loguje wynik."""
    logger.info("Pytanie:\n{}", PYTANIE)
    odpowiedz = zapytaj_claude(PYTANIE)
    logger.info("Odpowiedź (Claude):\n{}", odpowiedz)


if __name__ == "__main__":
    pokaz_przyklad()
