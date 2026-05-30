# Architecture Rules: Bookwriter

## Projektgrenzen

Dieses Projekt enthält nur den Bookwriter.

Ausgeschlossen:

- YouTube Automation
- LinkedIn
- Shorts
- Social Media
- Videoproduktion
- tägliche Plattform-Ausspielung

## Agentenarchitektur

Alle Aufgaben werden von spezialisierten Agenten erledigt.

Der Orchestrator Agent:

- ist die einzige Kommunikationsstelle
- delegiert Aufgaben
- sammelt Ergebnisse
- prüft Freigabestatus
- übergibt geprüfte Ergebnisse an den nächsten Agenten

Der Orchestrator Agent erstellt nicht selbst:

- Buchkonzepte
- Inhaltsverzeichnisse
- Kapitel
- Redaktionen
- Exporte
- Quellenprüfungen

## Agentenkommunikation

Verboten:

- Agent kommuniziert direkt mit Agent
- Agent gibt Aufgabe direkt an anderen Agent weiter
- Agent nutzt Ergebnis eines anderen Agenten ohne Orchestrator-Freigabe
- Agent startet mit Datenbankinhalt ohne Freigabe
- Agent startet mit vorhandenen Texten ohne Freigabe
- Agent startet mit Quellen ohne Freigabe
- Agent startet mit Vorlage ohne Freigabe

Erlaubt:

- Orchestrator delegiert an Agent
- Agent liefert Ergebnis an Orchestrator
- Orchestrator übergibt Ergebnis nach Freigabe an nächsten Agenten
- Prüf-Agent gibt Freigabe, Blocker oder Änderungsanforderung zurück

## Freigabezustände

Jedes Objekt hat einen Status:

- draft
- pending_review
- approved
- blocked
- needs_revision
- ready_for_writing
- ready_for_editing
- ready_for_export
- exported
- archived

## Pflichtprozess Buchprojekt

1. Projektziel klären
2. Buchtyp festlegen
3. Zielgruppe definieren
4. Nutzenversprechen erstellen
5. Buchkonzept prüfen
6. Inhaltsverzeichnis erstellen
7. Inhaltsverzeichnis prüfen
8. Kapitelziele definieren
9. Kapitelbriefings erstellen
10. Kapitelbriefings prüfen
11. Rohfassung schreiben
12. Kapitel-Leseprobe Fehlerkorrektur
13. Kapitel-Leseprobe Logikfehler
14. Kapitel-Leseprobe Spannungsbogen
15. Kapitel-Leseprobe Schreibstil
16. Kapitel-Leseprobe Grammatik
17. Kapitel überarbeiten
18. Kapitel freigeben
19. First Draft aus freigegebenen Kapiteln zusammenstellen
20. Konsistenzprüfung über mehrere Kapitel
21. Gesamtredaktion
22. Quellenprüfung
23. Exportvorbereitung
24. finale Freigabe

## Pflichtprozess Kapitel

1. Kapitelziel prüfen
2. Kapitelbriefing erstellen
3. Briefing prüfen
4. Quellen prüfen
5. Rohfassung schreiben
6. Leseprobe Fehlerkorrektur
7. Leseprobe Logikfehler
8. Leseprobe Spannungsbogen
9. Leseprobe Schreibstil
10. Leseprobe Grammatik
11. Redaktion
12. Konsistenzprüfung
13. Freigabe

## Abbruchregeln

Ein Prozess stoppt, wenn:

- Zielgruppe fehlt
- Nutzenversprechen fehlt
- Kapitelziel fehlt
- Quellen fehlen
- Freigabe fehlt
- Briefing unvollständig ist
- Kapitel doppelt zum vorherigen Kapitel ist
- Stilvorgaben fehlen
- Orchestrator keine Freigabe hat
- eine der fuenf Leseproben des aktuellen Kapitels fehlt

## Kapitelweise Leseproben-Architektur

Die fuenf Leseproben nach jeder Kapitelrohfassung sind feste Pipeline-Schritte.

Reihenfolge:

1. Fehlerkorrektur
2. Logikfehler
3. Spannungsbogen
4. Schreibstil
5. Grammatik

Regeln:

- Jeder Prueflauf wird als eigener Auftrag dokumentiert.
- Jeder Prueflauf nutzt genau einen Fokus.
- Ergebnisse gehen an den Orchestrator zurueck.
- Der Orchestrator startet den naechsten Prueflauf erst nach dokumentiertem Abschluss des vorherigen.
- Das naechste Kapitel startet erst nach Abschluss der fuenf Prueflaeufe des aktuellen Kapitels.
- Exportvorbereitung darf erst starten, wenn alle Kapitel ihre fuenf Prueflaeufe und die Gesamtpruefung abgeschlossen haben.

## Modellarchitektur

Der Bookwriter nutzt Ollama-Modelle taskbasiert.

Primaermodell:

- gpt-oss:20b

Sekundaermodell:

- qwen2.5:7b

Regeln:

- Der Orchestrator waehlt das Modell anhand des freigegebenen Taskprofils.
- Modellprofile werden in config/model_profiles.toml dokumentiert.
- gpt-oss:20b wird fuer Orchestrierung, Struktur, Bewertung, Redaktion und Pruefung genutzt.
- qwen2.5:7b wird nur fuer kurze Rohtextvarianten, Stilvarianten und einfache Umformulierungen genutzt.
- qwen2.5:7b wird nicht fuer Leseproben, Redaktion oder Konsistenzpruefung genutzt.
- gpt-oss:20b ist das verpflichtende Review-Modell fuer Pruefungen.
- Pruefungen muessen mit ausreichend Kontext fuer den vollstaendigen Pruefabschnitt laufen.
- Wenn der Kontext nicht reicht, wird blockiert oder nach Freigabe segmentiert.
- Quellenpruefung, Marktanalyse und Publishing-Entscheidungen duerfen nicht allein auf Modellwissen beruhen.
- Kein Modell darf Freigaben selbst setzen.
- Modellwechsel muessen im Projektstatus dokumentiert werden.

## Shared-Agent-Architektur

Primaere Quelle fuer wiederverwendbare Agenten ist `G:/Projects/youtube_automations`.

Bookwriter kopiert generische Agentenlogik nicht, sondern nutzt Adapter.

Jeder Shared Agent muss:

- in `config/reusable_agents.toml` registriert sein
- vom Orchestrator beauftragt werden
- Bookwriter-Statuswerte abbilden
- nicht relevante YouTube-, Social-Media- und Video-Funktionen deaktivieren
- Tokenverbrauch melden, wenn ein Modelllauf stattfindet

Andere Projektordner gelten nur als Fallback oder Altbestand.

## Token Monitoring

Token- und Kostenmonitoring ist ein Pflichtbestandteil der Architektur.

Jeder Modelllauf schreibt einen Usage-Eintrag mit:

- Projekt-ID
- Auftrag/Task
- Agent
- Modell
- Kapitelnummer, falls zutreffend
- Leseprobenfokus, falls zutreffend
- Input-Tokens
- Output-Tokens
- Gesamt-Tokens
- geschaetzte Kosten

Der Orchestrator darf einen Modelllauf nur als abgeschlossen betrachten, wenn der Usage-Eintrag vorhanden ist.

Kostenprofile stehen in `config/token_costs.toml`.

Lokale Ollama-Modelle werden mit API-Kosten `0` gefuehrt. Externe Modelle ohne Kostenprofil sind blockiert.

## Qualitaetssteuerung

Modellfreigaben werden anhand realer Ausgabequalitaet gepflegt.

Ein Modell darf fuer einen Task enger freigegeben, eingeschraenkt oder gesperrt werden, wenn Benchmark oder produktiver Lauf zeigt, dass:

- strukturierte Ausgaben unzuverlaessig sind
- Prueffokus vermischt wird
- lange Kapitel nicht sauber verarbeitet werden
- Befunde erfunden oder zu allgemein sind
- Sprache, Stil oder Grammatik nicht genuegen

Qualitaetsgates stehen in `config/quality_gates.toml`.
