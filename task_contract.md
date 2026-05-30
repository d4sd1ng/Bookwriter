# Task Contract: Bookwriter

## Gültigkeit

Gilt nur für Bookwriter-Aufgaben.

Nicht gültig für:

- YouTube
- LinkedIn
- Shorts
- Social Media
- Videoproduktion

## Oberste Regeln

1. Kein Buch ohne Zielgruppe.
2. Kein Inhaltsverzeichnis ohne Nutzenversprechen.
3. Kein Kapitel ohne Kapitelziel.
4. Keine Rohfassung ohne freigegebenes Kapitelbriefing.
5. Keine Quellenbehauptung ohne Quellenprüfung.
6. Keine Strukturänderung ohne Dokumentation.
7. Keine Stiländerung ohne Freigabe.
8. Keine Dopplungen zwischen Kapiteln.
9. Keine Exportarbeit vor stabiler Struktur.
10. Kein Agent nutzt vorhandene Inhalte, Datenbankinhalte oder Vorlagen ohne Freigabe.
11. Der Orchestrator Agent ist die einzige Kommunikationsstelle.
12. Agenten kommunizieren nicht untereinander.
13. Der Orchestrator Agent delegiert nur.
14. Prüf-Agenten prüfen.
15. Kein produktives Interview ohne freigegebenen Fragenkatalog.
16. Kein Kapitelabschluss ohne fuenf getrennte Leseproben nach der Kapitelrohfassung.
17. Jede Leseprobe hat genau einen Fokus: Fehlerkorrektur, Logikfehler, Spannungsbogen, Schreibstil oder Grammatik.
18. Kein Plotting ohne vollstaendiges Entwicklungsfundament.
19. Kein Scraping ohne freigegebene Quellen.
20. Wenn keine Grundidee vorhanden ist, muss ein 5-3-1-Brainstorming abgeschlossen sein.

## Auftragstyp: Buchkonzept

### Input

- Thema
- Zielgruppe
- Buchtyp
- gewünschtes Ergebnis
- Tonalität
- Umfangsziel

### Output

- Arbeitstitel
- Untertitel
- Zielgruppe
- Leserproblem
- Nutzenversprechen
- Abgrenzung
- Tonalität
- offene Fragen
- Freigabestatus

## Auftragstyp: Inhaltsverzeichnis

### Input

- freigegebenes Buchkonzept
- freigegebenes Plotting
- freigegebenes Treatment
- Zielgruppe
- Nutzenversprechen
- Buchtyp
- Umfangsziel

### Output

- Hauptteile
- Kapitel
- Unterkapitel
- Kapitelziele
- Leserführung
- mögliche Dopplungen
- offene Strukturfragen
- Freigabestatus

## Auftragstyp: Entwicklungsfundament

### Input

- Startmodus
- eigene Idee, vorhandener Text oder konkrete Vorgabe
- Buchart
- Alters- und Zielgruppe
- Erzaehlfokus
- Perspektive
- Anzahl Perspektiven
- Ende-Typ
- Ausgabeform
- Figurenstatus
- Recherchemodus

### Output

- ausgewaehlte Grundidee
- Buchart
- Zielalter und Zielgruppe
- Erzaehlparameter
- Ausgabeform
- Figurenbasis
- Recherchefreigabe
- Blocker
- Freigabestatus

### Regeln

- Wenn keine eigene Grundidee vorhanden ist, startet Brainstorming mit 5 Vorschlaegen, dann 3, dann 1.
- Kein Plotting, kein Treatment und kein Kapitelbriefing ohne vollstaendiges Entwicklungsfundament.
- Vorhandene Texte duerfen nur nach Freigabe genutzt werden.
- Scraping darf nur mit freigegebenen Quellen und Rate-Limit-Regeln laufen.

## Auftragstyp: Plotting

### Input

- freigegebenes Buchkonzept
- vollstaendiges Entwicklungsfundament
- Figurenbasis oder Sachbuchstruktur

### Output

- Plotstruktur
- Wendepunkte
- Spannungsbogen
- offene Logikfragen
- Freigabestatus

## Auftragstyp: Treatment

### Input

- freigegebenes Plotting
- vollstaendiges Entwicklungsfundament
- Stilvorgaben

### Output

- Treatment
- Kapitel- oder Szenenfolge
- offene Fragen
- Freigabestatus

## Auftragstyp: Kapitelbriefing

### Input

- freigegebenes Inhaltsverzeichnis
- Kapitelnummer
- Kapitelziel
- Zielgruppe
- Buchkontext

### Output

- Kapitelziel
- Kernpunkte
- Abschnittsstruktur
- Beispiele
- Quellenbedarf
- Übergang vom vorherigen Kapitel
- Übergang zum nächsten Kapitel
- Freigabestatus

## Auftragstyp: Kapitelrohfassung

### Input

- freigegebenes Kapitelbriefing
- freigegebene Quellen
- Stilvorgaben

### Output

- vollständiger Kapiteltext
- Zwischenüberschriften
- Beispiele
- Zusammenfassung
- Übergang
- offene Punkte

## Auftragstyp: Redaktion

### Input

- Kapiteltext oder Gesamttext
- Stilvorgaben
- Zielgruppe
- Buchkontext

### Output

- erkannte Probleme
- konkrete Änderungen
- überarbeitete Fassung
- Begründung
- offene Risiken
- Freigabestatus

## Auftragstyp: Leseprobe je Kapitelrohfassung

### Input

- Kapitelrohfassung
- Kapitelnummer
- Kapiteltitel
- Kapitelziel
- Zielgruppe
- Buchtyp
- Genre oder Kategorie
- Erzaehlperspektive oder Argumentationsform
- Stilvorgaben
- Fokus der Leseprobe

### Erlaubte Fokuswerte

- fehlerkorrektur
- logikfehler
- spannungsbogen
- schreibstil
- grammatik

### Output

- Fokus
- erkannte Probleme
- betroffene Stellen
- konkrete Korrekturen
- ueberarbeitete Fassung oder Aenderungsvorschlaege
- Restrisiken
- Freigabestatus

### Regeln

- Eine Leseprobe darf nur ihren eigenen Fokus pruefen.
- Die Reihenfolge ist: Fehlerkorrektur, Logikfehler, Spannungsbogen, Schreibstil, Grammatik.
- Das naechste Kapitel darf erst beginnen, wenn die fuenf Leseproben des aktuellen Kapitels abgeschlossen und freigegeben oder blockiert dokumentiert sind.
- Exportvorbereitung ist erst erlaubt, wenn alle Kapitel ihre fuenf Leseproben und die Gesamtpruefung abgeschlossen haben.

## Auftragstyp: Exportvorbereitung

### Input

- final geprüfter Gesamttext
- Exportformat
- Designvorgaben

### Output

- exportfähige Struktur
- Dateiformat-Hinweise
- Inhaltsverzeichnis
- Quellenanhang
- Glossar
- Anhänge
- finale Prüfliste

## Akzeptanzkriterien

Ein Auftrag ist abgeschlossen, wenn:

- alle Pflichtinputs vorhanden sind
- der Output vollständig ist
- offene Punkte markiert sind
- Freigabestatus gesetzt ist
- keine YouTube- oder LinkedIn-Logik enthalten ist
- bei jedem Kapitel alle fuenf Leseproben dokumentiert sind

## Modellregeln

1. Jeder Auftrag nutzt ein dokumentiertes Modellprofil.
2. Standardmodell ist gpt-oss:20b.
3. qwen2.5:7b darf nur fuer kurze Entwuerfe, Varianten und einfache Umformulierungen genutzt werden.
4. Quellen-, Markt- und Verkaufsbehauptungen brauchen freigegebene externe Daten.
5. Amazon-KDP- und Verlagsaktionen werden nur vorbereitet, nicht automatisch ausgefuehrt.
6. Wenn strukturierte Ausgabe erforderlich ist und das Modell sie nicht liefert, ist der Auftrag blockiert.
7. Leseproben, Redaktion und Konsistenzpruefungen duerfen nicht mit qwen2.5:7b laufen.
8. Pruefungen brauchen ein Review-Modell mit ausreichend Kontext fuer den vollstaendigen Pruefabschnitt.
9. Reicht der Kontext nicht, muss der Auftrag blockiert oder nach Freigabe sauber segmentiert werden.
10. Jeder Modelllauf muss Tokenverbrauch protokollieren.
11. Kosten muessen jederzeit ueber das Tokenledger einsehbar sein.
12. Externe Modelle ohne freigegebenes Kostenprofil sind blockiert.
13. Modelle koennen nach Ausgabequalitaet enger freigegeben oder gesperrt werden.
14. Modellgestuetzte Kapitel-Leseproben laufen ueber das Taskprofil `reading_sample_review`.
15. Ein Modelllauf darf nur als vollstaendig gelten, wenn Modellantwort und Tokenmessung vorliegen.

## Token- und Kostenregeln

1. Jeder Agentenlauf mit Modellnutzung erzeugt einen Token-Usage-Eintrag.
2. Der Eintrag enthaelt Projekt-ID, Task, Agent, Modell, Input-Tokens, Output-Tokens und geschaetzte Kosten.
3. Kapitelbezogene Laeufe muessen die Kapitelnummer enthalten.
4. Leseproben muessen den Fokus enthalten.
5. Lokale Ollama-Modelle haben API-Kosten von 0, solange kein anderes Kostenprofil gesetzt ist.
6. Cloud- oder API-Modelle duerfen nur mit aktuellem Kostenprofil genutzt werden.
7. Wenn Tokenverbrauch oder Kosten nicht ermittelt werden koennen, muss der Lauf als unvollstaendig markiert werden.
8. Ollama-Laeufe nutzen gemessene `prompt_eval_count` und `eval_count`, falls der Server diese Werte liefert.

## Qualitaetsregeln fuer Modelle

1. Modellfreigabe basiert nicht nur auf Modellname oder Groesse, sondern auf gemessener Ausgabequalitaet.
2. Review-Modelle brauchen einen erfolgreichen Benchmark fuer Leseproben und Konsistenzpruefung.
3. Modelle unterhalb des Mindest-Scores werden fuer den jeweiligen Task gesperrt.
4. Qualitaetswerte und Freigaben werden in config/quality_gates.toml gepflegt.

## Shared-Agent-Regeln

1. Vorhandene Agenten aus youtube_automations werden bevorzugt wiederverwendet.
2. Bookwriter baut generische Agenten nicht neu, sondern nutzt Adapter.
3. Jeder Shared Agent braucht einen Eintrag in config/reusable_agents.toml.
4. Der Orchestrator bleibt die einzige Kommunikationsstelle.
5. YouTube-, Social-Media- und Video-Funktionen muessen per Adapter deaktiviert werden.

## Interviewregeln

1. Das Interview nutzt den Fragenkatalog aus interview_questionnaire.md.
2. Pflichtfragen muessen beantwortet sein, bevor ein Buchkonzept erstellt wird.
3. Fehlende Zielgruppe, fehlendes Leserproblem oder fehlendes Nutzenversprechen blockieren den Auftrag.
4. Markt-, Verlags- und Amazon-KDP-Fragen sind optional, muessen aber beantwortet werden, bevor diese Module aktiv werden.
5. Der Fragenkatalog selbst braucht vor produktiver Nutzung den Status approved.
