"""Demonstracja end-to-end: User -> LLM-Guard -> Ollama (gemma3:4b).

Pokazuje różnicę między uruchomieniem ataku BEZ warstwy obronnej (bezpośrednie
wywołanie modelu) i Z warstwą obronną (`security_shield.scan_input`). Wynik
zapisywany jest do `data/results/results_shielded.csv`.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tqdm import tqdm  # noqa: E402

from guardrails.security_shield import scan_input  # noqa: E402
from scripts.attacks_payloads import get_attack_payloads, get_meta  # noqa: E402
from src.ollama_client import OllamaError, chat, is_server_alive  # noqa: E402

OUTPUT = _ROOT / "data" / "results" / "results_shielded.csv"
MODEL = "gemma3:4b"
FIELDS = ["Attack_ID", "Category", "Shield_Status", "Risk_Score",
          "Shield_Reason", "Model_Response"]


def main() -> None:
    if not is_server_alive():
        raise SystemExit("Brak serwera Ollama. Uruchom `ollama serve`.")

    attacks = get_attack_payloads()
    system_prompt = get_meta()["system_prompt"]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    blocked = 0
    for atk in tqdm(attacks, desc=f"Shielded sweep [{MODEL}]"):
        scan = scan_input(atk["payload"])
        if scan.is_blocked:
            blocked += 1
            response = "[BLOCKED przez LLM-Guard – nie wysłano do modelu]"
        else:
            try:
                response = chat(MODEL, scan.sanitized, system_prompt=system_prompt)
            except OllamaError as exc:
                response = f"[ERROR Ollama] {exc}"
        rows.append({
            "Attack_ID": atk["id"],
            "Category": atk["category"],
            "Shield_Status": scan.status,
            "Risk_Score": round(scan.risk_score, 3),
            "Shield_Reason": scan.reason,
            "Model_Response": response,
        })

    with OUTPUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nZablokowane przez LLM-Guard: {blocked}/{len(attacks)}")
    print(f"Wyniki: {OUTPUT}")


if __name__ == "__main__":
    main()
