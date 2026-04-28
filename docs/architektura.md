# Architektura projektu LLM Security Sandbox

## Komponenty

| Warstwa     | Plik                                | Odpowiedzialność |
| ----------- | ----------------------------------- | ---------------- |
| Dane        | `data/payloads/attacks.json`        | 15 payloadów + meta (system prompt, markery oceny). |
| Loader      | `scripts/attacks_payloads.py`       | Ładowanie i walidacja JSON-a. |
| Klient LLM  | `src/ollama_client.py`              | HTTP do `POST /api/chat` (Ollama), timeout, błędy. |
| Orkiestrator| `scripts/run_attacks.py`            | Sweep modele × ataki, ewaluacja, zapis CSV. |
| Obrona      | `guardrails/security_shield.py`     | `scan_input()` — `llm-guard` + fallback heurystyczny. |
| Demo E2E    | `scripts/run_with_shield.py`        | User → LLM-Guard → Ollama (`gemma3:4b`). |
| Analiza     | `notebooks/analiza_wynikow.ipynb`   | Tabele i wykresy podatności. |
| Raport      | `wyniki/raport.md`                  | Wnioski merytoryczne i prawne. |
| Dokumentacja| `docs/`                             | Opis ataków, analiza prawna, architektura. |

## Przepływ danych (sweep ataków)

```
attacks.json ─► attacks_payloads.get_attack_payloads()
                 │
                 ▼
   ┌───────────────────────────────────────────────────┐
   │ run_attacks.py:                                   │
   │   for model in [llama2:7b, gemma3:4b, qwen3:4b]:  │
   │     for atk in attacks:                           │
   │       resp = ollama_client.chat(model, atk.payload│
   │                              , system=meta.system)│
   │       success = evaluate(resp, atk.goal, meta)    │
   │       row = {Model, Attack_ID, ..., Success}      │
   └───────────────────────────────────────────────────┘
                 │
                 ▼
        data/results/results.csv ──► notebooks/analiza_wynikow.ipynb
```

## Przepływ danych (z warstwą obronną)

```
        user_input
            │
            ▼
   security_shield.scan_input()
            │
   ┌────────┴─────────┐
   │ BLOCKED          │ SAFE
   ▼                  ▼
log + odmowa     ollama_client.chat(gemma3:4b, sanitized, system=...)
                       │
                       ▼
               data/results/results_shielded.csv
```

## Decyzje projektowe

1. **Lokalna inferencja (Ollama)** — żadne dane nie opuszczają maszyny (RODO art. 44+, minimalizacja danych).
2. **Heurystyczny fallback** dla `llm-guard` — projekt działa offline, na słabszym sprzęcie.
3. **Zewnętrzna baza payloadów (JSON)** — łatwa rozbudowa katalogu ataków bez modyfikacji kodu.
4. **Markery sukcesu w `_meta`** — kryteria oceny są jawne i powtarzalne (replikowalność wymagana przez art. 12 EU AI Act — logging).
