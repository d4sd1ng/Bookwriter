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
