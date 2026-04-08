"""
Przykład użycia Google Gemini API w mini-projekcie.

Pomysł na projekt (temat 7):
    Klasyfikator ryzyka AI Act
    — narzędzie klasyfikujące system AI według kategorii ryzyka AI Act
    na podstawie opisu projektu.

Pomysł na projekt (temat 26):
    DPIA — Data Protection Impact Assessment
    — narzędzie przeprowadzające ocenę skutków przetwarzania danych
    z automatycznym generowaniem raportu.

Uruchomienie:
    cp .env.example .env   # uzupełnij GOOGLE_API_KEY
    uv run src/example_gemini.py
"""

from dotenv import load_dotenv
from google import genai
from loguru import logger

load_dotenv()  # wczytuje zmienne z pliku .env

client = genai.Client()  # automatycznie czyta GOOGLE_API_KEY z env

# --- Prompt bazowy ---
SYSTEM_PROMPT = """Jesteś ekspertem od prawa i etyki sztucznej inteligencji.
Odpowiadasz po polsku, zwięźle i merytorycznie.
Podajesz podstawę prawną (artykuł ustawy / rozporządzenia) gdy to możliwe."""

OPIS_SYSTEMU = (
    "Nasz system AI analizuje zdjęcia CV kandydatów do pracy "
    "i automatycznie przyznaje scoring (0-100) dopasowania do stanowiska. "
    "Wykorzystuje model rozpoznawania obrazów i NLP do analizy tekstu CV."
)

PYTANIE = f"""Na podstawie poniższego opisu systemu AI, zaklasyfikuj go
według kategorii ryzyka AI Act (niedopuszczalne / wysokie / ograniczone / minimalne).
Uzasadnij klasyfikację i wymień kluczowe obowiązki dostawcy.

Opis systemu:
{OPIS_SYSTEMU}"""


def zapytaj_gemini(pytanie: str, model: str = "gemini-2.5-flash") -> str:
    """Wysyła pytanie do Gemini i zwraca odpowiedź."""
    response = client.models.generate_content(
        model=model,
        contents=pytanie,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "temperature": 0.3,
            "max_output_tokens": 1024,
        },
    )
    return response.text


def pokaz_przyklad() -> None:
    """Uruchamia przykładowe zapytanie i loguje wynik."""
    logger.info("Pytanie:\n{}", PYTANIE)
    odpowiedz = zapytaj_gemini(PYTANIE)
    logger.info("Odpowiedź (Gemini):\n{}", odpowiedz)


if __name__ == "__main__":
    pokaz_przyklad()
