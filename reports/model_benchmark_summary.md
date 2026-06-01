# Model Benchmark Summary

## 2026-05-31

### Umgebung

- Ollama: 0.24.0
- RAM: ca. 32 GB
- GPU: Radeon RX 580 Series, ca. 4 GB VRAM
- Freier Speicher auf `G:` vor Installation: ca. 600 GB

### Installierte Modelle

| Modell | Status | Ergebnis |
|---|---|---|
| `gpt-oss:20b` | installiert, blockiert | nach Neu-Pull wieder lauffaehig; Minimaltest braucht ca. 81 Sekunden, Review-Benchmark laeuft nicht in 300 Sekunden fertig |
| `qwen2.5:7b` | installiert, lauffaehig | Minimaltest gibt `OK` zurueck; bleibt fuer Review-Aufgaben gesperrt |
| `qwen3:14b` | installiert, blockiert | einfacher JSON-Smoke-Test funktioniert nach Modell-Ladezeit, aber Review-Benchmark laeuft nicht in 120/180 Sekunden fertig |
| `mistral-small3.2:24b` | installiert, blockiert | 24B, 128K Kontext, 15 GB; Minimalaufruf laeuft auf CPU nicht in 180 Sekunden fertig |

### Benchmark-Ergebnisse

- `reports/reading_sample_benchmark.json`: fuenf Review-Foki mit `gpt-oss:20b`, alle blockiert.
- `reports/reading_sample_benchmark_qwen3_single.json`: einzelner Fokus `fehlerkorrektur` mit `qwen3:14b`, blockiert durch Timeout.
- `reports/reading_sample_benchmark_gptoss_single.json`: einzelner Fokus `fehlerkorrektur` mit neu gezogenem `gpt-oss:20b`, blockiert durch 300-Sekunden-Timeout.

### Entscheidung

Aktuell ist kein lokales Modell fuer produktive Kapitel-Leseproben freigegeben.

Naechste Optionen:

1. Kleineres Reviewmodell mit mindestens 32K Kontext testen.
2. Prompt fuer Benchmark-Ausgaben weiter reduzieren und mit hartem Output-Limit testen.
3. Externes Reviewmodell nur mit Kostenprofil und Tokenmonitoring freigeben.

## 2026-06-01

### Kompakter Reading-Sample-Prompt

Der Prompt `reading_sample_review_prompt.md` wurde auf kompakte Befundausgabe umgestellt:

- keine vollstaendige Kapitel-Neufassung
- maximal 8 erkannte Probleme
- maximal 5 Aenderungsvorschlaege
- hartes Output-Limit: `max_output_tokens = 768`
- Qwen3-Kurzreview-Grenze: `secondary_review_max_input_tokens = 12000`

Gemessene Promptgroesse fuer den Benchmarkfall `consulting_practical_guide_chapter_1`:

- kompletter Auftrag inklusive Prompt, JSON und Testkapitel: ca. 1.913 Tokens
- Kapitelrohfassung allein: ca. 357 Tokens

### Benchmark-Ergebnisse

- `qwen3:14b` mit kompaktem Prompt, Fokus `fehlerkorrektur`, Health-Gate nur fuer den Benchmarkprozess deaktiviert: Timeout nach 240 Sekunden.
- `qwen3:14b` mit direktem Ollama-Chat-Aufruf und `think: false`: Timeout nach 240 Sekunden.
- `qwen2.5:7b` als direkte Baseline fuer denselben kompakten Reviewauftrag: Timeout nach 120 Sekunden.
- `qwen2.5:7b` Minimaltest `Gib nur OK aus.`: ca. 71 Sekunden.

### Bewertung

Die aktuelle lokale Ausfuehrung ist fuer interaktive Kapitelreviews nicht tragbar. Der kompakte Prompt ist nicht mehr der Hauptengpass; selbst kurze lokale Modellaufrufe sind auf CPU zu langsam.

### Entscheidung

Lokale Review-Modelle bleiben fuer produktive Leseproben blockiert. Der naechste sinnvolle Schritt ist ein externer Review-Runtime-Pfad mit Tokenmonitoring und Kostenprofil oder ein deutlich kleineres lokales Modell nur als Vorfilter, nicht als finale fachliche Reviewinstanz.
