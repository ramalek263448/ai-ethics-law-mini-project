#!/usr/bin/env python3
"""Walidacja kompletności mini-projektu przed oddaniem."""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # .claude/skills/submit-solution/scripts -> root

ERRORS: list[str] = []
WARNINGS: list[str] = []
INFO: dict[str, str] = {}


def check_readme():
    readme = ROOT / "README.md"
    if not readme.exists():
        ERRORS.append("README.md nie istnieje")
        return

    text = readme.read_text(encoding="utf-8")

    # Placeholdery, które powinny być zastąpione
    placeholders = {
        "[Tytuł mini-projektu]": "tytuł projektu",
        "[Imię Nazwisko]": "imię i nazwisko",
        "[XXXXXX]": "numer indeksu",
        "[Numer z menu": "temat mini-projektu",
        "[2-3 zdania": "cel projektu",
    }
    for placeholder, desc in placeholders.items():
        if placeholder in text:
            ERRORS.append(f"README.md: nie uzupełniono pola — {desc} (zostało: '{placeholder}')")

    # Numer indeksu — 6 cyfr
    index_match = re.search(r"nr indeksu:\s*(\d{6})", text, re.IGNORECASE)
    if not index_match:
        # Szukaj luźniej
        index_match = re.search(r"\b(\d{6})\b", text)
        if not index_match:
            ERRORS.append("README.md: brak numeru indeksu (6 cyfr)")
        else:
            INFO["nr_indeksu"] = index_match.group(1)
            WARNINGS.append(
                f"README.md: znaleziono potencjalny numer indeksu ({index_match.group(1)}), "
                "ale nie w standardowym formacie 'nr indeksu: XXXXXX'"
            )
    else:
        INFO["nr_indeksu"] = index_match.group(1)

    # Wyciągnij dane do podsumowania
    name_match = re.search(r"\*\*Autor:\*\*\s*(.+?)(?:,|\n)", text)
    if name_match:
        name = name_match.group(1).strip()
        if name and "[" not in name:
            INFO["student"] = name

    topic_match = re.search(r"\*\*Temat:\*\*\s*(.+?)(?:\n)", text)
    if topic_match:
        topic = topic_match.group(1).strip()
        if topic and "[" not in topic:
            INFO["temat"] = topic

    # Sekcja wnioski — nie powinna być pusta
    wnioski_match = re.search(r"## Wnioski merytoryczne\s*\n(.*?)(?:\n##|\Z)", text, re.DOTALL)
    if wnioski_match:
        content = wnioski_match.group(1).strip()
        if not content or content.startswith("["):
            WARNINGS.append("README.md: sekcja 'Wnioski merytoryczne' wygląda na nieuzupełnioną")
    else:
        WARNINGS.append("README.md: brak sekcji 'Wnioski merytoryczne'")


def check_process():
    process = ROOT / "PROCESS.md"
    if not process.exists():
        ERRORS.append("PROCESS.md nie istnieje")
        return

    text = process.read_text(encoding="utf-8")

    required_sections = {
        "Narzędzia AI": r"## Narzędzia AI\s*\n(.*?)(?:\n##|\Z)",
        "Prompty": r"## Prompty\s*\n(.*?)(?:\n##|\Z)",
        "Decyzje": r"## Decyzje\s*\n(.*?)(?:\n##|\Z)",
        "Co nie zadziałało": r"## Co nie zadziałało\s*\n(.*?)(?:\n##|\Z)",
    }

    for section_name, pattern in required_sections.items():
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            ERRORS.append(f"PROCESS.md: brak sekcji '{section_name}'")
            continue

        content = match.group(1).strip()
        # Sprawdź czy sekcja ma treść (nie tylko szablonowe placeholdery)
        lines = [
            line.strip()
            for line in content.split("\n")
            if line.strip()
            and not line.strip().startswith(">")  # cytaty/instrukcje
            and not line.strip().startswith("[")  # placeholdery
            and line.strip() not in ("|", "---", "```")
        ]

        # Odfiltruj wiersze będące wyłącznie nagłówkami tabeli lub pustymi komórkami
        meaningful = [
            l
            for l in lines
            if not re.match(r"^\|[\s\-|]+\|$", l)  # separatory tabeli
            and not re.match(r"^\|.*np\..*\|$", l)  # przykładowe wiersze z "np."
            and "Kategoria" not in l
            and "[Wklej" not in l
            and "[Problem]" not in l
            and "[Decyzja]" not in l
            and "[Opis" not in l
        ]

        if len(meaningful) < 2:
            ERRORS.append(
                f"PROCESS.md: sekcja '{section_name}' wygląda na nieuzupełnioną "
                f"(znaleziono {len(meaningful)} merytorycznych linii)"
            )


def check_wyniki():
    wyniki = ROOT / "wyniki"
    if not wyniki.exists():
        ERRORS.append("Katalog wyniki/ nie istnieje")
        return

    files = [f for f in wyniki.iterdir() if f.name != ".gitkeep"]
    INFO["wyniki_count"] = str(len(files))

    if not files:
        ERRORS.append("wyniki/: katalog jest pusty — dodaj wykresy, tabelki lub raporty z wynikami")


def check_code():
    """Sprawdza czy student dodał własny kod w src/ lub notebooks/."""
    src = ROOT / "src"
    notebooks = ROOT / "notebooks"

    src_files = []
    if src.exists():
        src_files = [
            f for f in src.iterdir()
            if f.suffix in (".py", ".js", ".ts", ".sh")
            and not f.name.startswith("example_")  # pomijamy pliki startowe z szablonu
        ]

    nb_files = []
    if notebooks.exists():
        nb_files = [
            f for f in notebooks.iterdir()
            if f.suffix == ".ipynb"
        ]

    INFO["src_count"] = str(len(src_files))
    INFO["notebooks_count"] = str(len(nb_files))

    if not src_files and not nb_files:
        ERRORS.append(
            "Brak własnego kodu — dodaj skrypty do src/ lub notebooki do notebooks/. "
            "Pliki example_*.py z szablonu nie są liczone jako Twoja praca."
        )


def main():
    check_readme()
    check_process()
    check_wyniki()
    check_code()

    print("=" * 50)
    print("WALIDACJA MINI-PROJEKTU")
    print("=" * 50)

    if INFO:
        print("\nInformacje:")
        for key, val in INFO.items():
            print(f"  {key}: {val}")

    if WARNINGS:
        print(f"\nOSTRZEŻENIA ({len(WARNINGS)}):")
        for w in WARNINGS:
            print(f"  ⚠ {w}")

    if ERRORS:
        print(f"\nBŁĘDY ({len(ERRORS)}):")
        for e in ERRORS:
            print(f"  ✗ {e}")
        print(f"\nStatus: NIE GOTOWE — popraw {len(ERRORS)} błędów przed oddaniem")
        sys.exit(1)
    else:
        print("\nStatus: WALIDACJA OK — wszystkie sprawdzenia przeszły pomyślnie")
        sys.exit(0)


if __name__ == "__main__":
    main()
