# Analiza Zgodności i Odpowiedzialności

> Analiza prawno-etyczna projektu „LLM Security Sandbox" w kontekście prawa UE.
> Materiał dydaktyczny — nie stanowi porady prawnej.

## 1. Rola Wdrażającego (Deployer) wg EU AI Act

Rozporządzenie 2024/1689 (**EU AI Act**, dalej „AI Act") wprowadza rozróżnienie między:
- **Providerem** — twórcą modelu lub systemu AI (np. Meta dla `llama2`, Google dla `gemma3`, Alibaba dla `qwen3`),
- **Deployerem** (Wdrażającym) — podmiotem wykorzystującym system AI w ramach swojej działalności (np. uczelnia, firma, instytucja publiczna, która stawia chatbota na bazie tych modeli).

W przypadku korzystania z **modeli open-source** wdrażanych lokalnie (Ollama):
- Provider udostępnia tzw. *general-purpose AI model* (GPAI). Jeżeli nie jest to model „with systemic risk" (próg 10²⁵ FLOP), obowiązki Providera są ograniczone — w szczególności wdrażając model open-source pod licencją wolną, Provider korzysta z wyłączeń (motyw 102, art. 53 ust. 2 AI Act).
- **Cały ciężar zgodności przesuwa się na Deployera.** To on:
  - decyduje o **celu** zastosowania (ten cel determinuje klasyfikację ryzyka — art. 6),
  - musi przeprowadzić **ocenę wpływu na prawa podstawowe** (FRIA — art. 27) dla zastosowań wysokiego ryzyka,
  - musi zapewnić **nadzór człowieka** (art. 14) oraz **prowadzenie logów** (art. 12, 26 ust. 6),
  - odpowiada za **dokładność, solidność i cyberbezpieczeństwo** systemu (art. 15) — w tym za odporność na *prompt injection*, *data poisoning*, *adversarial examples*.

**Wniosek:** uruchamiając lokalnie `llama2:7b`, `gemma3:4b` lub `qwen3:4b` w produkcyjnym chatbocie, podmiot wdrażający staje się głównym adresatem obowiązków AI Act — niezależnie od tego, że nie wytrenował modelu samodzielnie.


## 2. RAG Poisoning, wyciek danych i odpowiedzialność cywilna

Atak **A14 (RAG Poisoning)** ilustruje scenariusz krytyczny dla aplikacji biznesowych:

- Złośliwy dokument trafia do bazy wiedzy (np. wewnętrzna Confluence, SharePoint, baza wektorowa).
- Podczas zapytania użytkownika dokument zostaje wciągnięty do kontekstu.
- Model interpretuje treść dokumentu jako instrukcję — i np. **ujawnia dane osobowe** innych użytkowników, **wykonuje wywołania narzędzi** (jeśli są podpięte tool-use) lub **eksfiltruje sekrety** ze swojego promptu systemowego.

Konsekwencje prawne:

- **RODO** (rozp. 2016/679):
  - art. 5 ust. 1 lit. f — naruszenie zasady **integralności i poufności**,
  - art. 32 — brak adekwatnych środków technicznych i organizacyjnych,
  - art. 33–34 — obowiązek **notyfikacji naruszenia** w 72 h i powiadomienia osób, których dane dotyczą,
  - art. 82 — **odpowiedzialność cywilna** administratora (i podmiotu przetwarzającego) za szkodę.
- **PLD 2024/2853** — uznanie oprogramowania (w tym systemów AI) za „produkt"; producent / Deployer odpowiada za szkody bez konieczności wykazywania winy, jeśli produkt nie zapewnia bezpieczeństwa, jakiego można rozsądnie oczekiwać.


**Wniosek**: w architekturze RAG warstwa typu `LLM-Guard` (lub równoważna walidacja kontekstu pobieranego z bazy) jest dziś **standardem należytej staranności**. Jej brak naraża Deployera nie tylko na sankcje administracyjne (DPA — do 20 mln EUR / 4 % obrotu), lecz także na masowe roszczenia cywilne.

## 3. Etyka i licencje modeli open-source

Korzystając z modeli takich jak `llama2`, należy pamiętać, że nie są to klasyczne licencje OSI (Open Source Initiative):

- **Llama 2 Community License** — ogranicza komercyjne użycie powyżej 700 mln MAU, zawiera „Acceptable Use Policy" zakazujący m.in. generowania broni, dezinformacji wyborczej, materiałów CSAM. Skuteczny **prompt injection** może doprowadzić do naruszenia AUP — odpowiedzialność spada na Deployera.
- **Gemma Terms of Use** — analogicznie: wyłącza odpowiedzialność Google i nakłada na użytkownika obowiązek wdrożenia odpowiednich filtrów.
- **Qwen License** — własna licencja Alibaba z klauzulami compliance.

Etycznie: brak pen-testów i warstwy obronnej w produkcyjnym wdrożeniu LLM jest **przerzucaniem ryzyka na użytkownika końcowego**, sprzeczne z zasadą odpowiedzialnej AI (HLEG „Ethics Guidelines for Trustworthy AI" — *human agency*, *technical robustness*, *accountability*).

## 4. Rekomendacje dla Deployera

1. **Klasyfikuj** zastosowanie wg AI Act (Annex III). Dla wysokiego ryzyka — pełen QMS i FRIA.
2. **Loguj** wejścia/wyjścia (art. 12 AI Act, art. 26 ust. 6) — sandbox robi to w `results.csv`.
3. **Wdrażaj filtry** (`llm-guard` lub równoważne) — udokumentuj próg detekcji i metryki.
4. **Pen-testuj** regularnie — co najmniej katalog 15 ataków z `attacks.json` + ataki celowane.
5. **Aktualizuj** politykę systemową i markery sekretów po każdym potwierdzonym wycieku.
6. **Szkól** użytkowników — zgodnie z art. 4 AI Act (AI literacy).
7. **Dokumentuj** decyzje (FRIA, DPIA) — to dowód staranności w ewentualnym postępowaniu.

---

### Podstawa normatywna (skrócona)
- Rozp. 2024/1689 (EU AI Act).
- Dyr. 2024/2853 (Product Liability Directive).
- Rozp. 2016/679 (RODO).
- OWASP Top 10 for LLM Applications, wersja 2025.
