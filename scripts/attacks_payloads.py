"""Loader payloadow atakow Prompt Injection.

Wczytuje 15 atakow zdefiniowanych w `data/payloads/attacks.json` i udostepnia
je w formie listy slownikow gotowych do uzycia przez `run_attacks.py`.

Kontekst prawno-etyczny:
    Material wylacznie edukacyjny. Payloady maja sluzyc do oceny odpornosci
    modeli LLM na manipulacje (Prompt Injection), zgodnie z wymogami art. 9
    i 15 EU AI Act (zarzadzanie ryzykiem, dokladnosc i odpornosc systemow AI).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
_ATTACKS_FILE = _ROOT / "data" / "payloads" / "attacks.json"


def load_attacks_file(path: Path | None = None) -> dict[str, Any]:
    """Zwraca caly dokument JSON z payloadami (lacznie z meta-danymi)."""
    path = path or _ATTACKS_FILE
    if not path.exists():
        raise FileNotFoundError(
            f"Nie znaleziono pliku z payloadami: {path}. "
            "Wygeneruj go lub przywroc z repozytorium."
        )
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def get_attack_payloads(path: Path | None = None) -> list[dict[str, Any]]:
    """Zwraca liste 15 atakow (id, name, category, goal, description, payload)."""
    doc = load_attacks_file(path)
    attacks = doc.get("attacks", [])
    if len(attacks) != 15:
        raise ValueError(
            f"Oczekiwano 15 atakow, znaleziono {len(attacks)}. "
            "Sprawdz integralnosc pliku attacks.json."
        )
    return attacks


def get_meta(path: Path | None = None) -> dict[str, Any]:
    """Zwraca sekcje `_meta` (system prompt, markery oceny sukcesu ataku)."""
    return load_attacks_file(path).get("_meta", {})


if __name__ == "__main__":
    attacks = get_attack_payloads()
    print(f"Zaladowano {len(attacks)} atakow:")
    for a in attacks:
        print(f"  [{a['id']}] {a['name']:35s}  cel={a['goal']:22s}  kat.={a['category']}")
