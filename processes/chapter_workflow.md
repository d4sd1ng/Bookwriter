# Chapter Workflow

## Ablauf

1. Kapitelnummer festlegen
2. Kapitelziel prüfen
3. Kapitelkontext prüfen
4. Abschnittsstruktur erstellen
5. Beispiele definieren
6. Quellenbedarf markieren
7. Kapitelbriefing prüfen
8. Rohfassung schreiben
9. Leseprobe Fehlerkorrektur
10. Leseprobe Logikfehler
11. Leseprobe Spannungsbogen
12. Leseprobe Schreibstil
13. Leseprobe Grammatik
14. Kapitelredaktion
15. Übergänge prüfen
16. Dopplungen prüfen
17. Kapitel freigeben

## Pflicht-Leseproben je Kapitel

Nach jeder Kapitelrohfassung muessen fuenf getrennte Leseproben laufen.

Jede Leseprobe prueft genau einen Fokus:

1. Fehlerkorrektur
2. Logikfehler
3. Spannungsbogen
4. Schreibstil
5. Grammatik

Das naechste Kapitel darf erst begonnen werden, wenn die fuenf Leseproben des aktuellen Kapitels abgeschlossen, freigegeben oder blockiert dokumentiert sind.

## Modellgestuetzte Leseproben

`bookwriter review-chapter` kann mit `--use-ollama` die lokale Ollama-Laufzeit aktivieren.

Regeln:

- Taskprofil ist `reading_sample_review`.
- Standardmodell ist `gpt-oss:20b`.
- `qwen2.5:7b` ist fuer Review-Laeufe blockiert.
- Die Antwort muss als JSON auswertbar sein.
- Gemessene Input- und Output-Tokens werden im Tokenledger gespeichert.

## Kapitelbriefing muss enthalten

- Kapitelnummer
- Kapiteltitel
- Kapitelziel
- Einordnung im Buch
- Kernpunkte
- Abschnittsstruktur
- Beispiele
- Quellenbedarf
- gewünschte Länge
- Tonalität
- offene Punkte
