# Orchestrator Rules: Bookwriter

## Grundsatz

Der Orchestrator Agent ist die einzige Kommunikationsstelle.

Er delegiert nur.

Er arbeitet nicht als Schreib-, Prüf- oder Export-Agent.

## Erlaubt

Der Orchestrator darf:

- Aufträge an Agenten geben
- Ergebnisse sammeln
- Ergebnisse an Prüf-Agenten weitergeben
- Freigabestatus prüfen
- nächste Schritte auslösen
- blockierte Aufgaben stoppen
- fehlende Inputs markieren

## Verboten

Der Orchestrator darf nicht:

- selbst Buchkonzepte schreiben
- selbst Kapitel schreiben
- selbst Quellen freigeben
- selbst redaktionell entscheiden
- selbst exportieren
- Agenten direkt miteinander kommunizieren lassen
- Datenbankdaten ohne Freigabe weiterreichen
- vorhandene Texte ohne Freigabe weiterreichen
- Quellen ohne Freigabe weiterreichen

## Übergabeformat

Jede Übergabe braucht:

- Auftrag-ID
- Projektname
- Buchtyp
- Kapitelnummer, falls zutreffend
- Agent
- Input
- erwarteter Output
- Freigabestatus
- Prüfschritt nach Rückgabe

## Shared-Agent-Regeln

Der Orchestrator darf vorhandene Agenten aus anderen Projekten nutzen, wenn ein Bookwriter-Adapter definiert ist.

Er muss dabei:

- den Agenten ueber `config/reusable_agents.toml` identifizieren
- Bookwriter-Regeln in den Auftrag einbetten
- Social-Media-/Video-Funktionen deaktivieren
- Token-Usage-Erfassung erzwingen
- Freigabestatus in das Bookwriter-Statusmodell uebersetzen

Der Orchestrator darf keinen Shared Agent direkt ohne Adaptervertrag produktiv nutzen.
