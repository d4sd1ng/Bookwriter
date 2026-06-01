# Project Status Report: Bookwriter

## Status

Eigenständige Bookwriter-Projektstruktur erstellt.

## Enthalten

- 7 Kern-Dateien
- Agentenübersicht
- Agenten-Verantwortungsmatrix
- Orchestrator-Regeln
- Freigabekette
- Modellstrategie
- Interview-Fragenkatalog als Abstimmungsentwurf
- fuenf kapitelweise Leseproben nach jeder Kapitelrohfassung
- Entwicklungsfundament mit Startmodus, Buchart, Altersgruppe, Erzaehlform, Ausgabeform und Figurenstatus
- 5-3-1-Brainstorming fuer fehlende Grundideen
- Kapitelpipeline mit Briefing, Draft, fuenf Review-Runs und Kapitel-Freigabe
- optionale Ollama-Ausfuehrung fuer kapitelweise Leseproben mit Modellrouting und Tokenledger
- reproduzierbarer Leseproben-Benchmark mit Testkapitel und Modell-Health-Blockern
- Buchprojekt-Workflow
- Kapitel-Workflow
- Redaktions-Workflow
- Export-Workflow
- Templates
- Prompt-Dateien
- Externer OpenAI-kompatibler Review-Runtime-Adapter mit Token- und Kostenlogging
- Projektberichte

## Nicht enthalten

- YouTube
- LinkedIn
- Shorts
- Social Media
- Videoproduktion

## Offene Punkte

1. Fragenkatalog gemeinsam abstimmen und freigeben.
2. Prompt-Optimierungen pruefen und freigeben.
3. Entscheiden, ob jede kapitelweise Leseprobe manuelle Freigabe braucht.
4. Konkreten Buchtyp festlegen.
5. Zielgruppe definieren.
6. Umfangsziel festlegen.
7. Exportformat bestimmen.
8. Stilvorgaben definieren.
9. Quellenregeln konkretisieren.
10. Kapitelstandard testen.
11. Designvorgaben ergänzen.
12. Weitere Bookwriter-Adapter fuer die importierten Shared Agents aus Agenten-Standards erstellen.
13. Modellausgaben fuer Kapitelreviews anhand echter Buchkapitel benchmarken und Qualitaetsgates schaerfen.
14. Prompt fuer `reading_sample_review` mit echten Kapitelrohfassungen benchmarken: Minimal-Smoke-Test ueber Ollama-Chat liefert valides JSON, aber der produktive Review-Prompt bleibt `needs_revision`.
15. Externen Reviewpfad fuer kapitelweise Leseproben implementieren und mit Kostenprofil absichern.
15. Review-Modell reparieren oder ersetzen: lokal ist aktuell kein Review-Modell freigegeben (`gpt-oss:20b` EOF, `qwen3:14b` Timeout, `mistral-small3.2:24b` CPU-Timeout).
