# Analiza Bezpieczeństwa LLM

**Autor:** Radosław Małek, nr indeksu: 263448

**Temat:** 12 — Prompt injection — testy bezpieczeństwa LLM

**Kurs:** Aspekty prawne, społeczne i etyczne w AI, PWr 2025/2026

> Lista tematów: [Zasady zaliczenia — Menu mini-projektów](https://github.com/laugustyniak/ai-ethics-law-course/blob/main/Zasady%20zaliczenia.md#menu-mini-projekt%C3%B3w)

---

## Quick Start

```bash
uv sync                        # zainstaluj zależności
cp .env.example .env           # skopiuj wzór zmiennych środowiskowych
# uzupełnij klucze API w .env (jeśli projekt łączy się zewnętrznie)

# Uruchom podstawowy test modeli (Ollama)
uv run python -m scripts.run_attacks

# Uruchom uodpornioną demonstrację działania z LLM-Guard
uv run python -m scripts.run_with_shield
```

---


## Cel projektu

Projekt analizuje zjawisko **luki semantycznej** w architekturze współczesnych dużych modeli językowych (LLM). Ponieważ modele nie odróżniają na poziomie wejściowym "instrukcji systemowych" od "danych" wprowadzonych przez użytkownika, pozwala to na nadpisanie polityk modelu (Jailbreak) lub wydobycie ukrytych w nim wewnątrz promptu danych uwierzytelniających (Data Exfiltration). Narzędzie to automatycznie testuje kilkanaście znanych wektorów Prompt Injection. 

## Opis projektu

Modele LLM nie odróżniają twardo „danych" od „instrukcji" — całość pojawia się w tym samym oknie kontekstowym jako tekst. To źródło tzw. **luki semantycznej**: złośliwie sformułowany prompt użytkownika może nadpisać politykę systemową modelu (jailbreak) lub wyciągnąć z niej sekrety (data exfiltration).

Projekt:
1. uruchamia **15 ataków Prompt Injection** przeciwko 3 modelom open-source w Ollama,
2. ocenia skuteczność każdego ataku (markery sukcesu),
3. porównuje wyniki **bez** i **z** warstwą obronną `LLM-Guard`,
4. dokumentuje konsekwencje **prawne** (EU AI Act, AI Liability Directive, RODO) — `docs/analiza_prawna.md`.

## Modele testowane

| Model        | Rola w eksperymencie                          |
| ------------ | ---------------------------------------------- |
| `llama2:7b`  | Baseline – starsza architektura Meta           |
| `gemma3:4b`  | Safety-first – najnowsza generacja Google      |
| `qwen3:4b`   | High-performance – najnowsza generacja Alibaba |

## Metodologia — 15 ataków

| ID  | Nazwa                          | Kategoria             | Cel                  | Mechanizm |
|-----|--------------------------------|-----------------------|----------------------|-----------|
| A01 | Direct Override                | Instruction Override  | secret_exfiltration  | Bezpośrednie „IGNORUJ poprzednie instrukcje". |
| A02 | Payload Splitting              | Obfuscation           | secret_exfiltration  | Złośliwy string sklejany ze zmiennych A+B+C. |
| A03 | Base64 Obfuscation             | Obfuscation           | jailbreak            | Polecenie zakodowane w Base64. |
| A04 | Typoglycemia                   | Obfuscation           | jailbreak            | Przestawione litery omijają filtry słownikowe. |
| A05 | DAN (Do Anything Now)          | Persona Hijack        | jailbreak            | Wymuszenie roli „bez zasad". |
| A06 | Command Injection (fake tag)   | Instruction Override  | secret_exfiltration  | Fałszywe znaczniki `<<SYSTEM OVERRIDE>>`. |
| A07 | Data Exfiltration via Roleplay | Roleplay              | secret_exfiltration  | „Audytor bezpieczeństwa" prosi o sekret. |
| A08 | Prompt Chaining                | Multi-step            | secret_exfiltration  | Łańcuch niewinnych kroków, ostatni = wyciek. |
| A09 | Context Manipulation           | Context Manipulation  | secret_exfiltration  | Sfałszowana historia rozmowy z „adminem". |
| A10 | Semantic Injection (translate) | Obfuscation           | jailbreak            | Atak ukryty w zadaniu tłumaczenia. |
| A11 | API Abuse (fake function)      | Tool Abuse            | secret_exfiltration  | Fikcyjne `system.dump_config(include_secrets=True)`. |
| A12 | Logic Flaw (negation trap)     | Logic Exploit         | secret_exfiltration  | Pułapka podwójnego przeczenia. |
| A13 | Race / Urgency Pressure        | Social Engineering    | jailbreak            | Presja czasu („ratuj życie"). |
| A14 | RAG Poisoning                  | RAG Poisoning         | secret_exfiltration  | Zatruty „dokument" z bazy wiedzy. |
| A15 | Feedback Loop Exploitation     | Multi-step            | jailbreak            | Iteracyjne „doszlifowanie" treści zakazanej. |

Pełne payloady: `data/payloads/attacks.json`. Opisy mechanizmów: `docs/opis_atakow.md`.

## Powiązanie z projektem grupowym

Mini-projekt wiąże się bezpośrednio z potrzebami zabezpieczenia generowanych embeddingów przed atakamim wywołanymi przez wrogich użytkowników platform społecznościowych z których zbierane były dane.

## Wymagania

Projekt korzysta z [uv](https://docs.astral.sh/uv/) — szybkiego menedżera pakietów Python.

```bash
# Instalacja uv (jeśli nie masz)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Instalacja zależności
uv sync

# Z notebookami Jupyter
uv sync --extra notebooks
```

**Zmienne środowiskowe** — skopiuj plik `.env.example` i uzupełnij klucze API:

```bash
cp .env.example .env
# Uzupełnij klucze w .env (OpenAI / Anthropic / Google — w zależności od projektu)
```

## Uruchomienie

| Skrypt / Polecenie  | Działanie  |
| ------------------- | ---------- |
| `uv run python -m scripts.run_attacks` | Środowisko sandboxowe wykonujące 15 ataków przeciwko modelom. Wyniki lączą do pliku w `data/results/`. |
| `uv run python -m scripts.run_with_shield` | Przelecenie pytań od użytkownika wraz z analizą bezpieczeństwa na wejściu w klasyfikatorze `LLM-Guard`. |
| `uv run jupyter notebook notebooks/analiza_wynikow.ipynb` | Odpalenie notatnika Jupiter do wykreślania metryk w pliku. |

## Wyniki

Projekt testował odporność na 15 złośliwych ataków sklasyfikowanych m.in jako *Instruction Override*, *Base64 Obfuscation*, czy *Multi-step (Prompt Chaining)*.
Kompletne wyniki oraz odniesienia do prawa zawiera wygenerowany plik `wyniki/raport.md`.

Skuteczność Obron:
* Odsetek ataków skutecznych bez warstwy obronnej (na Gemma): **11.1%** (w tym podanie klucza systemowego w 4 próbach)
* Ochrona `LLM-Guard` blokuje całkowicie wylistowanie pełnego klucza (*Secret Exfiltration* spada do 0%) 

## Wnioski merytoryczne

1. **Jailbreaki:** Ataki typu zmian ról (*Persona Hijack*, odgrywanie "DAN") lub wprowadzania w błąd tłumacza są bardzo słabymi typami ataków w nowszych iteracjach Llama i Qwen - zazwyczaj wyłapują je od razu. Najbardziej podatny był u nas lekki model *gemma3:4b*.
2. **Krytyczny wektor — Multi-step:** Atak wprowadzający w błąd model krok-po-kroku (np. nakazując napisanie książki o terroryzmie fikcyjnie, a z każdą iteracją zmuszając do dostraczania szczegółów konkretnej receptury). W ten sposób udało się obejść wejściowy *LLM-Guard*.
3. **Prawny obowiązek filtrowania:** Wdrażający (Deployer) bez wykorzystania silników warstwy ochronnej w otwartych API ryzykuje wyciekiem np. poświadczeń ukrytych w `Context`. Taki wyciek kwalifikuje się jednoznacznie jako złamanie zasady Poufności w świetle RODO.

## Ograniczenia

1. Analiza podatności odbywa się jedynie dla lekkich modeli `4B-7B`. Rozmiar powoduje spiętrzenie wyników (duże modele rzędu 70B posiadają mocniejsze ukształtowania logiczne RLHF).
2. Wynik skuteczności ataku oparty jest o wyszukiwanie zhardcodowanych znaczników ("secret phrase"). Brak detekcji sentymentu i odcieni odmowy używających synonimów. Dla rzetelnych wynków konieczna była ręczna weryfikacja wyników.
3. Warstwa `LLM-Guard` w środowisku działa z defaultowym obcięciem Threshold=0.5 dla klasyfikatorów i wyłapuje tylko prompt wejściowy (brakuje detektora na odpowiedź wychodzącą, co naprawiłoby ominięcie `Multi-step`).

## Źródła

- [Ollama.com](https://ollama.com/) — środowisko lokalne i pobieranie paczek GGUF.
- [HuggingFace: LLM-Guard](https://github.com/protectai/llm-guard) — Zabezpieczenia systemów sztucznej inteligencji.
- [AI Liability Directive / EU AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) — dokumentacje europejskiej ustawy i dyrektyw dotyczących odpowiedzialności systemów AI.
