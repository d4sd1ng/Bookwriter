# Agent Reuse Strategy: Bookwriter

## Entscheidung

Bookwriter-Agenten sollen nicht jedes Mal neu von Grund auf gebaut werden.

Vorhandene Agenten aus anderen Projekten werden als wiederverwendbare Shared Agents eingebunden, wenn sie:

- eine klare Aufgabe haben
- ueber einen Adapter angesprochen werden koennen
- ein dokumentiertes Input-/Output-Format liefern
- Tokenverbrauch und Kosten melden koennen
- Bookwriter-Regeln akzeptieren

## Grundsatz

Bookwriter liefert die fachlichen Regeln.

Shared Agents liefern generische Faehigkeiten.

Der Orchestrator bleibt die einzige Kommunikationsstelle.

## Wiederverwendbare Agenten

Moegliche Quellen:

- `G:/Agenten-Standards`
- `G:/Projects/youtube_automations`
- `G:/Projects/multi-input-recovered`
- `G:/Projects/Nurtoring-Email`
- `G:/Projects/codex-recovery-safe-20260528-204659`

Zentrales Standards-Repository:

- lokal: `G:/Agenten-Standards`
- GitHub: `https://github.com/d4sd1ng/Agenten-Standards`

Keine Quelle gilt automatisch als beste Version. Vor Uebernahme in `G:/Agenten-Standards` wird pro Agent ein Vergleich der vorhandenen Versionen durchgefuehrt.

`Nurtoring-Email` wird bevorzugt, wenn der gesuchte Agent dort vorhanden ist, weil dieser Projektstand voraussichtlich am aktuellsten ist.

| Agent | Quelle | Bookwriter-Einsatz |
|---|---|---|
| Token Monitoring Agent | bevorzugt `Nurtoring-Email` | Tokenverbrauch, Budget, Usage-Reports |
| Token Cost Calculator Agent | bevorzugt `Nurtoring-Email` | Kostenberechnung pro Modell/Provider |
| Text Analysis Agent | mehrere Kandidaten | Leseproben, Stil, Dopplungen, Strukturprobleme |
| Content Approval Agent | bevorzugt `Nurtoring-Email` | Freigaben, Blocker, Aenderungsanforderungen |
| Document Export Agent | mehrere Kandidaten | Exportstruktur, DOCX/PDF/E-Book-Vorbereitung |
| Web Scraping Agent | `G:/Projects/youtube_automations/web-scraping-agent` | freigegebene Buchmarkt-/Themen-/Titelrecherche |
| Rate Limiter Agent | `G:/Projects/youtube_automations/rate-limiter-agent` | Rate Limits fuer Scraping und APIs |
| Trend Analysis Agent | `G:/Projects/youtube_automations/trend-analysis-agent` | Themen-, Genre-, Zielgruppen- und Titeltrends |
| Workflow Executor Agent | `G:/Projects/youtube_automations/workflow-executor-agent` | Ausfuehrung freigegebener Bookwriter-Workflows |

## Adaptervertrag

Jeder Shared Agent braucht fuer Bookwriter einen Adapter mit:

- `agent_id`
- `source_path`
- `preferred_source_path`
- `capabilities`
- `input_schema`
- `output_schema`
- `bookwriter_constraints`
- `token_usage_contract`
- `approval_required`
- `status_mapping`

## Harte Regeln

1. Kein Shared Agent wird direkt von einem anderen Agenten aufgerufen.
2. Nur der Orchestrator darf Shared Agents beauftragen.
3. Jeder Shared-Agent-Lauf muss einen Token-Usage-Eintrag erzeugen.
4. Jeder Shared-Agent-Lauf muss Bookwriter-Blocker respektieren.
5. Bestehende Agenten werden nicht projektspezifisch verbogen; Bookwriter nutzt Adapter.
6. Wenn ein Agent Social-Media- oder YouTube-Logik enthaelt, wird diese per Adapter deaktiviert.
7. Shared Agents muessen projektneutral weiterentwickelt werden.

## Optimierungsziel

Agenten sollen so refaktoriert werden, dass sie in beliebigen Projekten nutzbar sind:

- keine fest verdrahteten Projektnamen
- keine festen Content-Typen wie Video, YouTube oder Newsletter im Kern
- Tasktypen ueber Konfiguration
- Provider-/Modellpreise ueber Konfiguration
- Speicherpfade ueber Konfiguration
- einheitliches Job- und Result-Format
- einheitliches Token- und Kostenreporting

## Bookwriter-spezifische Adapter

Bookwriter darf nur Adapter, Prompts, Regeln und Workflows beisteuern.

Beispiele:

- Web Scraping Agent: nur fuer Buchmarkt, Genres, Zielgruppen, Titeltrends und Vergleichstitel.
- Text Analysis Agent: nur fuer Kapitel- und Gesamttextpruefung.
- Token Monitoring Agent: alle Modelllaeufe, alle Kapitel, alle Leseproben.
- Content Approval Agent: Freigabestatus aus Bookwriter-Statusmodell.
