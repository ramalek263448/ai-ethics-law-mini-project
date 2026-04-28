# Dokumentacja Procesu Pracy z AI

## Wprowadzenie
Dokument ten ma na celu udokumentowanie procesu pracy nad projektem "LLM Security Sandbox". Zawiera on kluczowe informacje dotyczące używanych promptów, podjętych decyzji oraz iteracji w trakcie realizacji projektu.

## Prompty
### 1. Automatyzacja Testów Penetracyjnych
- **Cel:** Wygenerowanie skryptu do masowego testowania 15 ataków na modelach.
- **Treść promptu:** "Działaj jako Python Developer. Napisz skrypt korzystający z API HTTP (np. `requests`), który automatyzuje testowanie 15 różnych ataków Prompt Injection na modelach obsługiwanych przez Ollama. Skrypt ma ładować payloady z pliku JSON i iteracyjnie przepytywać wybrane modele, a uzyskane odpowiedzi wraz z metadanymi i czasem wykonania zapisywać do pliku `results.csv`."

### 2. Implementacja Warstwy Obronnej
- **Cel:** Stworzenie mechanizmu sterylizacji wejścia.
- **Treść promptu:** "Napisz moduł `security_shield.py` w Pythonie, który wykorzystuje nakładkę sprawdzającą z biblioteki `llm-guard` do sterylizacji i analizy promptów wejściowych od użytkownika pod kątem Prompt Injection. Funkcja powinna posiadać proste sterowanie logiczne – jeśli zostanie wykryte zagrożenie, zwróć akcję 'BLOCKED' jako log z odmową, w przeciwnym razie zwróć przeprocesowany czysty prompt."

### 3. Generowanie Dokumentacji README.md
- **Cel:** Stworzenie profesjonalnego opisu projektu.
- **Treść promptu:** "Stwórz plik README.md dla projektu 'LLM Security Sandbox'. Dokument musi zawierać sekcje takie jak: Cel projektu, Wymagania (w tym instrukcję pobierania menedżera pakietów `uv`), Tabela z 15 kategoriami ataków testowanymi w eksperymencie, Architektura przepływu danych jako ASCII oraz Wnioski merytoryczne i prawne z przeprowadzonych testów."

### 4. Analiza Prawna i Etyczna
- **Cel:** Dokumentacja odpowiedzialności za zmanipulowany output modelu.
- **Treść promptu:** "Działaj jako ekspert ds. prawa nowych technologii i AI. Opracuj dogłębną odpowiedź zawierającą wnioski prawno-etyczne dla naszego wyniku z LLM, uwzględniając postanowienia RODO (art. 5 w kontekście wycieku systemowego sekretu)
### 5. Struktura Katalogów Projektu
- **Cel:** Uporządkowanie plików w repozytorium.
- **Treść promptu:** "Przedstaw logiczną i poukładaną strukturę drzewa katalogów formatowaną tekstowo (ASCII) dla profesjonalnego projektu badawczego LLM Security Sandbox. Powinna zawierać podział m.in. na skrypty inicjujące, oddzielny moduł dla guardrails, sekcję dokumentacji (docs/), wyjścia dla notatników w Jupyterze (notebooks/) oraz wyodrębnione pliki z konfigami czy wynikami końcowymi (data/ i wyniki/)."

## Decyzje
- Wybór modeli do testów: `llama2:7b`, `gemma3:4b`, `qwen3:4b`.
- Użycie biblioteki `llm-guard` do implementacji warstwy obronnej.
- Zastosowanie formatu CSV do przechowywania wyników testów.

## Iteracje
- Iteracja 1: Wstępne testy z użyciem modelu `llama2:7b` i podstawowych payloadów.
- Iteracja 2: Rozszerzenie testów o modele `gemma3:4b` i `qwen3:4b`.
- Iteracja 3: Analiza wyników i dostosowanie payloadów na podstawie uzyskanych odpowiedzi.

## Podsumowanie
Dokumentacja procesu pracy z AI jest kluczowym elementem projektu, umożliwiającym śledzenie postępów oraz podejmowanych decyzji. Wszelkie zmiany i aktualizacje będą na bieżąco wprowadzane do tego dokumentu.