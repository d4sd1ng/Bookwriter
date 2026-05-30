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
12. Kapitel prüfen
13. Kapitel überarbeiten
14. Konsistenzprüfung über mehrere Kapitel
15. Gesamtredaktion
16. Quellenprüfung
17. Exportvorbereitung
18. finale Freigabe

## Pflichtprozess Kapitel

1. Kapitelziel prüfen
2. Kapitelbriefing erstellen
3. Briefing prüfen
4. Quellen prüfen
5. Rohfassung schreiben
6. Rohfassung prüfen
7. Redaktion
8. Konsistenzprüfung
9. Freigabe

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
