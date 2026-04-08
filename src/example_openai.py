"""
Przykład użycia OpenAI API w mini-projekcie.

Pomysł na projekt (temat 6):
    Porównanie LLM-ów na pytaniach prawnych / etycznych
    — zadaj kilku modelom te same pytania o RODO, AI Act, IP
    i porównaj jakość odpowiedzi.

Pomysł na projekt (temat 25):
    Automated fact-checking — weryfikacja outputu LLM
    — wygeneruj odpowiedzi na pytania prawne, wyciągnij twierdzenia,
    zweryfikuj z wiarygodnym źródłem (np. tekst ustawy).

Uruchomienie:
    cp .env.example .env   # uzupełnij OPENAI_API_KEY
    uv run src/example_openai.py
"""

from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI

load_dotenv()  # wczytuje zmienne z pliku .env

client = OpenAI()  # automatycznie czyta OPENAI_API_KEY z env

# --- Prompt bazowy ---
SYSTEM_PROMPT = """Jesteś ekspertem od prawa i etyki sztucznej inteligencji.
Odpowiadasz po polsku, zwięźle i merytorycznie.
Podajesz podstawę prawną (artykuł ustawy / rozporządzenia) gdy to możliwe."""

PYTANIE = (
    "Czy system rekomendacji produktów w sklepie internetowym "
    "podlega obowiązkom z AI Act? Jeśli tak — jaka to kategoria ryzyka "
    "i jakie obowiązki ma dostawca?"
)


def zapytaj_openai(pytanie: str, model: str = "gpt-4.1-nano") -> str:
    """Wysyła pytanie do OpenAI i zwraca odpowiedź."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": pytanie},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def pokaz_przyklad() -> None:
    """Uruchamia przykładowe zapytanie i loguje wynik."""
    logger.info("Pytanie:\n{}", PYTANIE)
    odpowiedz = zapytaj_openai(PYTANIE)
    logger.info("Odpowiedź (OpenAI):\n{}", odpowiedz)


if __name__ == "__main__":
    pokaz_przyklad()
