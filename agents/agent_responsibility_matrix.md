# Agent Responsibility Matrix: Bookwriter

| Agent | Hauptaufgabe | Nicht zuständig für |
|---|---|---|
| Orchestrator Agent | Kommunikation, Delegation, Freigabestatus | Schreiben, Prüfen, Exportieren |
| Pipeline Orchestrator | technische Ablaufsteuerung | fachliche Entscheidung |
| Workflow Executor Agent | Ausführung freigegebener Workflows | eigene Entscheidungen |
| Content Management Agent | Buchstruktur, Kapitelstatus, Inhaltsverwaltung | finale Freigabe |
| Text Analysis Agent | Textanalyse, Dopplungen, Strukturprobleme | Buchproduktion |
| Advanced Prompting Agent | Prompt-Qualität für Schreib- und Prüfaufgaben | inhaltliche Freigabe |
| Content Approval Agent | Freigabe, Blocker, Änderungsanforderungen | Rohtext schreiben |
| Database Service Agent | Daten bereitstellen und speichern | Datennutzung freigeben |
| Path Management Agent | Pfade und Speicherorte | Inhaltsentscheidung |
| Document Export Agent | Exportstruktur, Dokumentausgabe, Anhänge | Redaktion |
| Translation Agent | Übersetzungen und Sprachvarianten | Originalkonzept |
| SEO Optimization Agent | suchfähige Titel und Begriffe für E-Book-Kontext | YouTube- oder LinkedIn-SEO |
| CTA Generation Agent | Abschluss-CTA für Buch, Whitepaper oder Lead-Magnet | Social-Media-CTA |
| Token Monitoring Agent | Tokenverbrauch überwachen | Inhalt |
| Token Cost Calculator Agent | Kosten abschätzen | Budgetfreigabe |
| Analytics Agent | spätere Auswertung von Nutzung oder Downloads | Buchtext schreiben |

## Reuse-Regel

Generische Agenten werden projektuebergreifend genutzt.

Bookwriter implementiert dafuer Adapter, aber kopiert oder dupliziert die Agentenlogik nicht.

Jeder wiederverwendete Agent muss:

- ueber den Orchestrator laufen
- Bookwriter-Statuswerte abbilden
- Tokenverbrauch melden, wenn ein Modelllauf stattfindet
- Social-Media-, YouTube- oder Video-Funktionen deaktivieren, falls vorhanden
