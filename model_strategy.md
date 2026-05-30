# Model Strategy: Bookwriter

## Entscheidung

Der Bookwriter nutzt mehrere Ollama-Modelle je nach Aufgabe.

Primaermodell:

- `gpt-oss:20b`

Sekundaermodell:

- `qwen2.5:7b`

Optional bei ausreichend Hardware:

- `qwen2.5:14b` oder `qwen2.5:32b` fuer laengere Rohfassungen
- `gpt-oss:120b` nur bei sehr hoher lokaler oder Cloud-Kapazitaet
- `qwen3:14b` als sekundäres Review-Modell fuer kurze Kapitel
- `mistral-small3.2:24b` als optionaler Kandidat fuer Instruction-Following-Pruefungen
- `qwen3:30b` als optionaler Long-Context-Kandidat nach Hardwaretest

## Begruendung

`gpt-oss:20b` ist lokal vorhanden und eignet sich als Hauptmodell fuer:

- Orchestrierung
- Interviewauswertung
- Buchkonzept
- Inhaltsverzeichnis
- Kapitelbriefings
- Konsistenzpruefung
- Verkaufschancenbewertung
- Verlagsangebot-Vorbereitung
- Amazon-KDP-Checklisten
- strukturierte JSON-Ausgaben

`qwen2.5:7b` ist lokal vorhanden und eignet sich als schnelles Nebenmodell fuer:

- einfache Rohtextvarianten
- Stilvarianten
- kurze Umformulierungen
- Zwischenzusammenfassungen
- schnelle Plausibilitaetschecks

## Modellrouting

| Aufgabe | Modell | Begruendung |
|---|---|---|
| Orchestrator-Entscheidungen | `gpt-oss:20b` | bessere Eignung fuer agentische und strukturierte Aufgaben |
| Interviewauswertung | `gpt-oss:20b` | hohe Genauigkeit bei Pflichtinputs und Blockern |
| Buchkonzept | `gpt-oss:20b` | Positionierung und Nutzenversprechen brauchen Reasoning |
| Inhaltsverzeichnis | `gpt-oss:20b` | Struktur, Dopplungsvermeidung und Leserfuehrung |
| Kapitelbriefing | `gpt-oss:20b` | Kapitelziel, Quellenbedarf und Uebergaenge |
| Kapitelrohfassung kurz | `qwen2.5:7b` | schnell und ausreichend fuer erste Varianten |
| Kapitelrohfassung lang | `gpt-oss:20b` | bessere Konsistenz bei laengeren Texten |
| Redaktion | `gpt-oss:20b` | pruefende Aufgabe mit Begruendungspflicht |
| Konsistenzpruefung | `gpt-oss:20b` | struktur- und kapiteluebergreifende Pruefung |
| Quellenpruefung | kein Modell allein | externe Quellen muessen freigegeben und belegbar sein |
| Verkaufschancen | `gpt-oss:20b` + freigegebene Marktdaten | Modell darf nur vorlaeufig bewerten |
| Verlagsangebot | `gpt-oss:20b` | Pitch und Risiken brauchen klare Struktur |
| Amazon KDP | `gpt-oss:20b` fuer Checkliste | kein automatischer Upload ohne finale Freigabe |

## Review-Modellregeln

Pruefungen sind qualitaetskritisch und duerfen nicht mit einem schnellen Nebenmodell laufen.

Review-Pflichtmodell:

- `gpt-oss:20b`

Gilt fuer:

- kapitelweise Leseprobe Fehlerkorrektur
- kapitelweise Leseprobe Logikfehler
- kapitelweise Leseprobe Spannungsbogen
- kapitelweise Leseprobe Schreibstil
- kapitelweise Leseprobe Grammatik
- Kapitelredaktion
- Gesamtredaktion
- Konsistenzpruefung

Lokale Modellmetadaten am 2026-05-30:

| Modell | Parameter | Kontext | Thinking | Einsatz |
|---|---:|---:|---|---|
| `gpt-oss:20b` | 20.9B | 131072 | ja | Pflichtmodell fuer Pruefungen |
| `qwen2.5:7b` | 7.6B | 32768 | nein | nur kurze Entwuerfe, Varianten, Umformulierungen |
| `qwen3:14b` | 14.8B | 40960 | ja | sekundäres Review-Modell fuer kurze Kapitel nach Freigabe |

## Lokales Hardwareprofil

Stand 2026-05-30:

- RAM: ca. 32 GB
- GPU: Radeon RX 580 Series
- VRAM: ca. 4 GB
- Freier Speicher auf `G:`: ausreichend fuer weitere quantisierte Modelle

Folgerung:

- Modelle um 7B bis 24B sind realistisch, koennen aber je nach Kontextlaenge langsam sein.
- 30B-Modelle sind nur nach Testlauf sinnvoll.
- Sehr grosse Modelle wie 120B sind fuer dieses lokale System nicht Standard.

## Installationsregel

Weitere Modelle duerfen installiert werden, wenn sie zum System und zur Aufgabe passen.

Vor Installation pruefen:

1. Modellgroesse passt zum freien Speicher.
2. Kontextfenster passt zur Aufgabe.
3. Review-Modelle haben mindestens 32768 Kontexttokens.
4. Fuer lange Pruefungen sind 131072 Kontexttokens bevorzugt.
5. Review-Modelle muessen strukturierte Ausgaben zuverlaessig liefern.
6. Nach Installation muss ein lokaler Testlauf mit einem Kapitelpruefprompt erfolgen.

Kandidaten:

| Modell | Status | Rolle | Grund |
|---|---|---|---|
| `qwen3:14b` | installiert | sekundäre Review-Pruefung kurzer Kapitel | Thinking vorhanden, 40k Kontext |
| `mistral-small3.2:24b` | nicht installiert | optionaler Review-Kandidat | laut Ollama 128k Kontext, gutes Instruction Following |
| `qwen3:30b` | nicht installiert | optionaler Long-Context-Kandidat | laut Ollama 256k Kontext, aber voraussichtlich langsam auf diesem System |

## Lange Texte

Auch mit langem Kontext werden Pruefungen kapitelweise durchgefuehrt.

Regeln:

1. Jede Kapitelrohfassung wird vollstaendig in den jeweiligen Leseprobenlauf gegeben.
2. Wenn ein Kapitel nicht vollstaendig in den Mindestkontext passt, wird der Schritt blockiert oder das Kapitel muss vor der Pruefung geteilt werden.
3. Die Gesamtpruefung nutzt freigegebene Kapitelzusammenfassungen plus gezielt vollstaendige Kapitelstellen.
4. `qwen2.5:7b` darf nicht fuer Leseproben, Redaktion oder Konsistenzpruefung genutzt werden.
5. `qwen3:14b` darf nur fuer kurze Kapitel-Reviews genutzt werden, wenn der vollstaendige Kapiteltext in den Kontext passt.
6. Ein Modellwechsel bei Pruefungen ist nur auf ein mindestens geeignetes Review-Modell mit ausreichend Kontext erlaubt.

## Harte Regeln

1. Kein Modell entscheidet ueber Freigaben.
2. Kein Modell nutzt Quellen ohne dokumentierte Freigabe.
3. Markt- und Verkaufschancen sind ohne aktuelle Vergleichsdaten nur vorlaeufig.
4. Amazon-KDP-Upload wird nicht automatisch ausgefuehrt.
5. Verlagsangebote werden vorbereitet, aber nicht automatisch versendet.
6. Modellwechsel wird im Projektstatus dokumentiert.
7. Wenn ein Modell keine strukturierte Ausgabe liefert, wird der Schritt blockiert.
8. Review-Aufgaben duerfen nicht mit dem Sekundaermodell ausgefuehrt werden.
9. Wenn der verfuegbare Kontext fuer eine Pruefung nicht reicht, wird nicht gekuerzt, sondern blockiert oder in freigegebene Teilpruefungen segmentiert.
10. Modellfreigaben werden nach realer Ausgabequalitaet enger definiert.
11. Jeder Modelllauf muss Tokenverbrauch und geschaetzte Kosten protokollieren.
12. Externe Modelle ohne aktuelles Kostenprofil duerfen nicht genutzt werden.

## Qualitaetsgates

Die Modellstrategie wird nach realer Ausgabequalitaet nachgeschaerft.

Jeder neue Modellkandidat braucht einen Benchmark mit typischen Bookwriter-Aufgaben:

- Buchkonzept aus Interview
- Kapitelbriefing
- Kapitelrohfassung
- Leseprobe Fehlerkorrektur
- Leseprobe Logikfehler
- Leseprobe Spannungsbogen
- Leseprobe Schreibstil
- Leseprobe Grammatik
- Konsistenzpruefung

Bewertet wird auf einer Skala von 1 bis 5.

Review-Aufgaben brauchen mindestens 4.3 von 5, Konsistenzpruefungen mindestens 4.5 von 5.

Die Regeln stehen in `config/quality_gates.toml`.

## Token- und Kostenmonitoring

Jeder Modelllauf wird protokolliert mit Projekt-ID, Task, Agent, Modell, Kapitelnummer, Leseprobenfokus, Input-Tokens, Output-Tokens, Gesamt-Tokens, geschaetzten Kosten und Zeitstempel.

Lokale Ollama-Modelle haben API-Kosten von `0`. Hardware-, Strom- und Zeitkosten werden nur berechnet, wenn dafuer ein eigenes Kostenprofil gepflegt wird.

Externe Modelle duerfen erst genutzt werden, wenn ein aktuelles Preisprofil in `config/token_costs.toml` eingetragen und freigegeben ist.

## Aktueller lokaler Stand

Am 2026-05-30 lokal verfuegbar:

- `gpt-oss:20b`
- `qwen2.5:7b`

Diese Entscheidung basiert auf lokaler Verfuegbarkeit und aktueller Ollama-Dokumentation. Laut Ollama ist `gpt-oss` fuer Reasoning, agentische Aufgaben und strukturierte Ausgaben ausgelegt; `qwen2.5` bietet mehrsprachige Faehigkeiten, lange Kontexte und strukturierte Ausgaben.
