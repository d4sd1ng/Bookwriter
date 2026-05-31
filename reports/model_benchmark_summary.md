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
| `gpt-oss:20b` | installiert, blockiert | `ollama run gpt-oss:20b` endet mit `EOF`; API meldet unsupported chat/generate |
| `qwen2.5:7b` | installiert, lauffaehig | Minimaltest gibt `OK` zurueck; bleibt fuer Review-Aufgaben gesperrt |
| `qwen3:14b` | installiert, blockiert | einfacher JSON-Smoke-Test funktioniert nach Modell-Ladezeit, aber Review-Benchmark laeuft nicht in 120/180 Sekunden fertig |
| `mistral-small3.2:24b` | installiert, blockiert | 24B, 128K Kontext, 15 GB; Minimalaufruf laeuft auf CPU nicht in 180 Sekunden fertig |

### Benchmark-Ergebnisse

- `reports/reading_sample_benchmark.json`: fuenf Review-Foki mit `gpt-oss:20b`, alle blockiert.
- `reports/reading_sample_benchmark_qwen3_single.json`: einzelner Fokus `fehlerkorrektur` mit `qwen3:14b`, blockiert durch Timeout.

### Entscheidung

Aktuell ist kein lokales Modell fuer produktive Kapitel-Leseproben freigegeben.

Naechste Optionen:

1. `gpt-oss:20b` neu ziehen oder reparieren und danach Health-Check wiederholen.
2. Kleineres Reviewmodell mit mindestens 32K Kontext testen.
3. Externes Reviewmodell nur mit Kostenprofil und Tokenmonitoring freigeben.
