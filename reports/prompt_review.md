# Prompt Review

## Status

Freigabestatus: needs_revision

## Ergebnis der Pruefung

Die urspruenglichen Prompts waren fuer einen kontrollierten Bookwriter-Prozess zu offen.

Gefundene Probleme:

- Pflichtinputs wurden nicht konsequent erzwungen.
- Blockerpfade waren nicht durchgaengig definiert.
- Freigabestatus war nicht in jedem Prompt enthalten.
- Ausgabeformat war nicht maschinenlesbar genug.
- Modellprofile waren nicht zugeordnet.
- Markt-, Verlags- und Amazon-KDP-Prompts fehlten.

## Durchgefuehrte Optimierung

Alle vorhandenen Prompts wurden erweitert um:

- Rolle
- Modellprofil
- Pflichtinput
- Blocker
- Regeln
- JSON-Ausgabeformat
- naechsten Pruefschritt

Neu ergaenzt:

- `prompts/market_assessment_prompt.md`
- `prompts/publisher_offer_prompt.md`
- `prompts/kdp_preparation_prompt.md`
- `prompts/reading_sample_review_prompt.md`

## Update: Kapitelweise Leseproben

Die fuenf Leseproben laufen nicht erst nach dem Gesamt-First-Draft, sondern nach jeder Kapitelrohfassung.

Feste Reihenfolge je Kapitel:

1. Fehlerkorrektur
2. Logikfehler
3. Spannungsbogen
4. Schreibstil
5. Grammatik

Der Gesamttext wird danach nur noch uebergreifend auf Konsistenz, Gesamtstruktur, Quellen und finale Exportreife geprueft.

## Update: Review-Modell

Alle Prueflaeufe verwenden `gpt-oss:20b` als verpflichtendes Review-Modell.

`qwen2.5:7b` ist fuer Leseproben, Redaktion und Konsistenzpruefung gesperrt.

Wenn ein Kapitel oder Pruefabschnitt nicht vollstaendig in den verfuegbaren Kontext passt, muss der Lauf blockieren oder nach Freigabe segmentiert werden. Eine unvollstaendige Pruefung darf nicht als sachgemaess ausgegeben werden.

## Noch abzustimmen

1. Ob jedes Prompt ausschliesslich JSON ausgeben soll oder ob Markdown fuer Entwuerfe erlaubt ist.
2. Ob Kapitelrohfassungen direkt als Markdown im JSON-Feld gespeichert werden.
3. Ob nach jeder kapitelweisen Leseprobe manuelle Freigabe noetig ist.
4. Ob `qwen2.5:7b` fuer kurze Rohfassungen freigegeben wird.
5. Welche Pruef-Agenten final Freigabestatus setzen duerfen.
6. Ob fuer Verlag und KDP weitere rechtliche Checklisten noetig sind.
## Update: Ollama-Smoke-Tests 2026-05-30

### Reading Sample Review Prompt

Status: needs_revision

Ein erster Ollama-Smoke-Test mit dem Generate-Endpunkt hat gezeigt, dass eine JSON-Anforderung allein nicht verlaesslich genug ist. Die Laufzeit blockiert ungueltige JSON-Antworten jetzt sauber.

Nach Umstellung auf den Chat-Endpunkt mit System-Anweisung lieferte `gpt-oss:20b` fuer einen Minimalauftrag valides JSON und gemessene Tokenwerte. Der Prompt muss trotzdem vor produktiver Nutzung mit echten Kapitelrohfassungen benchmarked werden.

Update 2026-05-31: `gpt-oss:20b` wurde neu gezogen und ist wieder lauffaehig, scheitert aber fuer einen echten Leseproben-Fokus am 300-Sekunden-Timeout. `qwen3:14b` und `mistral-small3.2:24b` liefen fuer Review- bzw. Minimaltests auf CPU in 120/180 Sekunden nicht fertig. Damit ist aktuell kein lokales Review-Modell freigegeben; Prompt-Optimierung allein reicht nicht, solange kein ausreichend schnelles Review-Modell vorhanden ist.

Update 2026-06-01: Der Reading-Sample-Prompt wurde auf kompakte Befundausgabe umgestellt. Die vollstaendige Kapitelneufassung wurde entfernt, die Ausgabe auf maximal 8 Probleme und 5 Aenderungsvorschlaege begrenzt und `max_output_tokens = 768` gesetzt. Der Benchmarkauftrag umfasst nur noch ca. 1.913 geschaetzte Tokens inklusive Testkapitel. Trotzdem blockiert `qwen3:14b` nach 240 Sekunden, auch mit deaktiviertem Thinking. `qwen2.5:7b` blockiert denselben Auftrag nach 120 Sekunden und braucht fuer einen Minimaltest ca. 71 Sekunden. Damit ist der lokale Reviewpfad aktuell runtime-limitiert, nicht nur prompt-limitiert.

Update 2026-06-01: Der externe Reviewpfad mit `gpt-5-mini` hat alle fuenf Leseprobenfoki fuer den Benchmarkfall erfolgreich erzeugt. Der Prompt lieferte pro Fokus strukturierte JSON-Ausgabe mit 5-7 Befunden und 5 Aenderungsvorschlaegen. Die erfolgreiche 5er-Pruefung kostete zusammen 0.013879 USD. Fuer GPT-5-Modelle nutzt der Adapter `reasoning_effort = minimal` und ein externes Completion-Limit von 4096 Tokens, weil zu niedrige Limits nur Reasoning-Tokens verbrauchten und keinen sichtbaren JSON-Content erzeugten.

Naechste Pruefpunkte:

- System-/Rollenanweisung fuer echte Kapitelreviews weiter benchmarken.
- Schema kleiner und eindeutiger machen.
- Beispielantwort nur als Schema, nicht als interpretierbarer Inhalt.
- Pro Fokus echte Testkapitel gegen `gpt-oss:20b` und `qwen3:14b` vergleichen.
- Naechstes lauffaehiges Review-Modell erst per Health-Check freigeben, dann Promptqualitaet bewerten.
- Externen Reviewpfad mit Kostenprofil und Tokenmonitoring vorbereiten, wenn lokale CPU-Ausfuehrung nicht beschleunigt werden kann.
- Qualitaet der `gpt-5-mini`-Befunde fachlich bewerten und danach als produktiven Reviewpfad freigeben oder auf `gpt-5` eskalieren.
