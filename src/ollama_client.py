"""Minimalny klient HTTP do lokalnego API Ollama.

Wykorzystuje endpoint `POST /api/chat` (bez streamingu) i obsluguje:
  * konfigurowalny host (zmienna `OLLAMA_HOST`, domyslnie http://localhost:11434),
  * timeout i wyjatki sieciowe,
  * przekazanie odrebnego promptu systemowego (kluczowe dla testow Prompt Injection).

Kontekst prawno-etyczny:
    Komunikacja odbywa sie wylacznie z modelami uruchomionymi LOKALNIE,
    co minimalizuje ryzyko transferu danych do podmiotow trzecich (RODO art. 44+).
"""
from __future__ import annotations

import os
from typing import Any

import requests

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_TIMEOUT = float(os.environ.get("OLLAMA_TIMEOUT", "120"))


class OllamaError(RuntimeError):
    """Blad komunikacji z API Ollama."""


def chat(
    model: str,
    user_prompt: str,
    system_prompt: str | None = None,
    *,
    host: str = DEFAULT_HOST,
    timeout: float = DEFAULT_TIMEOUT,
    options: dict[str, Any] | None = None,
) -> str:
    """Wysyla pojedyncze zapytanie chat do Ollama i zwraca tresc odpowiedzi."""
    messages: list[dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": options or {"temperature": 0.2},
    }

    url = f"{host.rstrip('/')}/api/chat"
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
    except requests.Timeout as exc:
        raise OllamaError(f"Timeout po {timeout}s dla modelu {model}") from exc
    except requests.RequestException as exc:
        raise OllamaError(f"Blad HTTP do {url}: {exc}") from exc

    try:
        data = resp.json()
        return data["message"]["content"]
    except (ValueError, KeyError) as exc:
        raise OllamaError(f"Nieprawidlowa odpowiedz Ollama: {resp.text[:200]}") from exc


def is_server_alive(host: str = DEFAULT_HOST, timeout: float = 3.0) -> bool:
    """Szybkie sprawdzenie, czy serwer Ollama jest dostepny."""
    try:
        r = requests.get(f"{host.rstrip('/')}/api/tags", timeout=timeout)
        return r.ok
    except requests.RequestException:
        return False


if __name__ == "__main__":
    if not is_server_alive():
        print(f"Brak serwera Ollama pod {DEFAULT_HOST}. Uruchom: `ollama serve`.")
    else:
        print(chat("gemma3:4b", "Powiedz krotko: czym jest RODO?"))
