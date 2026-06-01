# Decision Log: Bookwriter

## 2026-05-22

### Entscheidung
Der Bookwriter ist ein eigenes Projekt.

### Begründung
Lange Inhalte brauchen andere Prozesse als YouTube, LinkedIn oder Shorts.

### Konsequenz
Der Bookwriter bekommt eigene Projektdateien, eigene Regeln und eigene Templates.

---

### Entscheidung
YouTube und LinkedIn sind ausgeschlossen.

### Begründung
Der Bookwriter dient nicht zur Plattform-Ausspielung.

### Konsequenz
Keine Social-Media-Workflows, keine Shorts, keine Videoproduktion.

---

### Entscheidung
Buchstruktur kommt vor Kapiteltext.

### Begründung
Ohne Gesamtstruktur entstehen Dopplungen und logische Brüche.

### Konsequenz
Kapitel werden erst geschrieben, wenn Inhaltsverzeichnis und Kapitelbriefing freigegeben sind.

---

### Entscheidung
Jedes Kapitel braucht ein Kapitelziel.

### Begründung
Das Kapitelziel verhindert unklare oder doppelte Inhalte.

### Konsequenz
Kein Kapitelbriefing ohne Kapitelziel.

---

### Entscheidung
Der Orchestrator Agent bleibt die einzige Kommunikationsstelle.

### Begründung
Direkte Agent-zu-Agent-Kommunikation erzeugt Kontrollverlust.

### Konsequenz
Agenten liefern nur an den Orchestrator zurück.

---

### Entscheidung
Alle bestehenden Inhalte brauchen Freigabe vor Nutzung.

### Begründung
Vorhandene Texte, Quellen, Datenbankinhalte oder Vorlagen können veraltet, falsch oder unpassend sein.

### Konsequenz
Kein Agent arbeitet mit Bestand, bevor dieser geprüft und freigegeben wurde.

---

### Entscheidung
Redaktion und Konsistenzprüfung sind eigene Prüfschritte.

### Begründung
Lange Texte brauchen Prüfung auf Stil, Struktur, Dopplungen und Übergänge.

### Konsequenz
Rohfassung ist nicht gleich Endfassung.

---

### Entscheidung
Export kommt erst am Ende.

### Begründung
Export vor finaler Struktur erzeugt unnötige Nacharbeit.

### Konsequenz
Exportvorbereitung startet erst nach finaler Gesamtprüfung.

---

## 2026-05-30

### Entscheidung
Der Bookwriter nutzt mehrere Ollama-Modelle je nach Aufgabe.

### Begründung
Ein einzelnes Modell ist fuer alle Schritte nicht optimal. Orchestrierung, Struktur, Bewertung und Pruefung brauchen staerkeres Reasoning und zuverlaessige strukturierte Ausgaben. Kurze Entwuerfe und Varianten koennen schneller mit einem kleineren Modell vorbereitet werden.

### Konsequenz
gpt-oss:20b ist das Primaermodell fuer Orchestrierung, Konzept, Outline, Briefings, Redaktion, Konsistenzpruefung, Verkaufschancen, Verlagsangebot und Amazon-KDP-Vorbereitung.

qwen2.5:7b ist das Sekundaermodell fuer kurze Rohtextvarianten, Stilvarianten, Zusammenfassungen und einfache Umformulierungen.

Modellrouting wird in model_strategy.md und config/model_profiles.toml gepflegt.

---

### Entscheidung
Der Bookwriter bekommt einen Interview-Fragenkatalog als Abstimmungsentwurf.

### Begründung
Ohne abgestimmte Fragen entstehen unvollstaendige Buchprojekte, fehlende Zielgruppen, unklare Nutzenversprechen und spaetere Blocker bei Export, Verlag oder Amazon KDP.

### Konsequenz
Der Fragenkatalog wird in interview_questionnaire.md dokumentiert, in config/interview_questions.toml fuer die CLI nutzbar gemacht und bis zur gemeinsamen Freigabe als pending_review gefuehrt.

---

### Entscheidung
Die fuenf Leseproben laufen nach jeder Kapitelrohfassung.

### Begründung
Wenn erst hunderte Seiten nach dem Gesamt-First-Draft geprueft werden, werden Logikfehler, Spannungsprobleme, Stilbrueche und Grammatikfehler zu spaet entdeckt. Kapitelweise Pruefung reduziert Nacharbeit und haelt die Qualitaet laufend stabil.

### Konsequenz
Jedes Kapitel muss vor Freigabe fuenf getrennte Prueflaeufe durchlaufen: Fehlerkorrektur, Logikfehler, Spannungsbogen, Schreibstil und Grammatik. Der Gesamttext erhaelt danach eine uebergreifende Konsistenz- und Finalpruefung.

---

### Entscheidung
Shared Agents werden primaer aus youtube_automations wiederverwendet.

### Begründung
Die meisten generischen Agenten existieren dort bereits. Wiederverwendung verhindert doppelte Implementierungen und macht Agenten langfristig projektuebergreifend wartbar.

### Konsequenz
Bookwriter implementiert Adapter und projektspezifische Regeln, aber keine Kopien generischer Agenten. Die Registry steht in config/reusable_agents.toml.

---

### Entscheidung
Token- und Kostenmonitoring wird verpflichtend.

### Begründung
Bei langen Buchprojekten entstehen viele Modelllaeufe pro Kapitel. Ohne laufende Transparenz ueber Input-Tokens, Output-Tokens und Kosten ist weder Budgetkontrolle noch Modellvergleich moeglich.

### Konsequenz
Jeder Modelllauf muss im Tokenledger dokumentiert werden. Lokale Ollama-Modelle werden mit API-Kosten 0 gefuehrt. Externe Modelle sind ohne freigegebenes Kostenprofil blockiert.

---

### Entscheidung
Modellfreigaben werden nach Ausgabequalitaet enger definiert.

### Begründung
Die Modellgroesse oder ein gutes allgemeines Profil reicht fuer sachgemaesse Pruefungen nicht aus. Entscheidend ist, ob das Modell im konkreten Task vollstaendig, fokussiert, strukturiert und sprachlich sauber arbeitet.

### Konsequenz
Fuer Review- und Konsistenzaufgaben gelten Qualitaetsgates. Modelle koennen pro Task freigegeben, eingeschraenkt oder gesperrt werden.

---

### Entscheidung
Bookwriter bekommt ein verpflichtendes Entwicklungsfundament vor Plotting und Schreiben.

### Begründung
Thema und Zielgruppe reichen nicht aus, um ein Buch kontrolliert zu entwickeln. Buchart, Altersgruppe, Erzaehlform, Perspektive, Ende, Ausgabeform, Figurenstatus und Recherchemodus muessen feststehen, damit Plotting, Treatment und Kapitelarbeit nicht auf unklaren Annahmen aufbauen.

### Konsequenz
Ohne vollstaendiges Entwicklungsfundament blockiert der Prozess vor Outline/Plotting. Wenn keine eigene Grundidee vorhanden ist, muss ein 5-3-1-Brainstorming durchlaufen und eine Arbeitsidee ausgewaehlt werden.

---

### Entscheidung
Kapitel werden nur nach Briefing, Rohfassung und fuenf freigegebenen Review-Runs freigegeben.

### Begründung
Kapitelweise Qualitaetskontrolle verhindert, dass Fehler erst im Gesamtmanuskript gefunden werden. Jeder Review-Fokus braucht einen eigenen Lauf, damit Fehlerkorrektur, Logik, Spannungsbogen, Stil und Grammatik nicht vermischt werden.

### Konsequenz
Die CLI unterstuetzt Kapitelbriefing, Briefing-Freigabe, Kapitelrohfassung, fokussierte Review-Runs, Review-Freigabe und Kapitel-Freigabe. Kapitel-Freigabe blockiert, bis alle fuenf Review-Runs approved sind.

---

### Entscheidung
Kapitel-Leseproben erhalten eine optionale Ollama-Laufzeit mit Tokenbuchung.

### Begründung
Die Platzhalterpruefung reicht fuer echte Qualitaetskontrolle nicht aus. Gleichzeitig muss die Pipeline testbar bleiben, auch wenn Ollama nicht laeuft.

### Konsequenz
`bookwriter review-chapter` kann mit `--use-ollama` das konfigurierte Review-Modell ausfuehren. Der Lauf validiert Modell und Kontext gegen `config/model_profiles.toml`, nutzt den Ollama-Chat-Endpunkt mit System-Anweisung, fordert JSON-Ausgabe an und protokolliert Input-/Output-Tokens in `data/token_usage.jsonl`.

---

### Entscheidung
Lokale Modell-Health-Checks blockieren aktuell alle Review-Kandidaten.

### Begründung
Ein installiertes Modell reicht nicht. `gpt-oss:20b` ist nach Neu-Pull wieder lauffaehig, laeuft fuer Review-Prompts aber zu langsam. `qwen3:14b` laeuft fuer Review-Prompts ebenfalls zu langsam und `mistral-small3.2:24b` ist auf CPU fuer interaktive Nutzung nicht tragbar.

## 2026-06-01 - Reading-Sample-Prompt kompakt, lokaler Reviewpfad weiter blockiert

Entscheidung: Der Reading-Sample-Prompt bleibt kompakt und gibt nur Befunde plus punktuelle Korrekturanweisungen aus. Vollstaendige Kapitelneufassungen werden nicht im Leseprobenlauf erzeugt.

Begruendung: Der neue Benchmarkauftrag liegt bei ca. 1.913 geschaetzten Tokens inklusive Testkapitel. Trotzdem laufen `qwen3:14b` mit kompaktem Prompt und `think: false` sowie `qwen2.5:7b` lokal nicht innerhalb der gesetzten Timeouts fertig. `qwen2.5:7b` braucht selbst fuer einen Minimaltest rund 71 Sekunden.

Folge: Lokale Review-Modelle bleiben fuer produktive Kapitel-Leseproben blockiert. Fuer nutzbare Reviews braucht Bookwriter entweder einen externen Modellpfad mit Token-/Kostenmonitoring oder deutlich leistungsfaehigere lokale Inferenz.

## 2026-06-01 - Externer Review-Runtime-Adapter

Entscheidung: Bookwriter erhaelt einen externen OpenAI-kompatiblen Runtime-Adapter fuer kapitelweise Review-Laeufe.

Begruendung: Lokale Modelle sind fuer den geforderten Reviewprozess nicht ausreichend schnell. Der bestehende Shared-Agent-Contract bleibt erhalten: Der Text Analysis Agent liefert fachliche Reviewausgaben an den Orchestrator, waehrend Token Monitoring und Token Cost Calculator ueber den gemeinsamen Ledger und `config/token_costs.toml` umgesetzt werden.

Regeln:

- Standardmodell fuer externe Reviews ist `gpt-5-mini`.
- Hoeherwertige Reviews koennen mit `gpt-5` gestartet werden, wenn das Kostenlimit passt.
- Jeder externe Lauf braucht ein Kostenprofil.
- Jeder externe Lauf kann mit `--max-estimated-cost` vor dem API-Aufruf begrenzt werden.
- Gemessene API-Tokens werden im Ledger gespeichert.
- Ohne `OPENAI_API_KEY` blockiert der Lauf.

## 2026-06-01 - Realistische Standardbudgets fuer externe Reviews

Entscheidung: Externe Review-Laeufe erhalten ein Standardlimit von `0.02 USD` pro Lauf und ein Planungsbudget von `0.10 USD` fuer die fuenf Leseproben eines Kapitels.

Begruendung: `0.01 USD` pro Kapitel ist fuer kurze Benchmarktexte erreichbar, aber fuer echte Kapitel zu knapp. Normale Kapitel koennen mehrere tausend Woerter umfassen und werden fuenfmal mit unterschiedlichem Fokus geprueft.

Folge: Ohne explizites `--max-estimated-cost` blockiert der OpenAI-Adapter erst oberhalb des konfigurierten Reviewlauf-Limits. Fuer laengere Kapitel kann das Limit bewusst mit `--max-estimated-cost 0.05` oder `0.10` pro Lauf erhoeht werden.

## 2026-06-01 - GPT-5-mini Reviewbenchmark erfolgreich

Entscheidung: `gpt-5-mini` bleibt der Standardkandidat fuer externe kapitelweise Leseproben.

Begruendung: Der komplette 5er-Benchmark fuer ein Testkapitel lief erfolgreich durch. Alle Fokuslaeufe (`fehlerkorrektur`, `logikfehler`, `spannungsbogen`, `schreibstil`, `grammatik`) lieferten strukturierte JSON-Ausgaben mit Status `pending_review`. Die erfolgreichen fuenf Laeufe kosteten zusammen 0.013879 USD.

Runtime-Anpassung: GPT-5-Modelle erhalten keine benutzerdefinierte Temperatur, nutzen `reasoning_effort = minimal` und ein externes Completion-Limit von 4096 Tokens. Niedrigere Limits fuehrten zu unvollstaendiger beziehungsweise leerer sichtbarer Ausgabe, weil Completion-Tokens durch Reasoning verbraucht wurden.

Folge: Naechster Schritt ist die fachliche Qualitaetsbewertung der Befunde. Wenn `gpt-5-mini` nicht reicht, wird `gpt-5` als hoeherwertiger, aber teurerer Reviewpfad getestet.

## 2026-06-01 - Kapitelrevision als eigener Pipeline-Schritt

Entscheidung: Bookwriter bekommt einen separaten `revise-chapter`-Schritt nach den fuenf freigegebenen Review-Laeufen.

Begruendung: Review und Ueberarbeitung sind unterschiedliche Aufgaben. Die fuenf Leseproben sollen Befunde erzeugen; erst danach setzt ein Revisionsagent die freigegebenen Befunde in eine neue Kapitelversion um.

Folge: `revise-chapter` blockiert, bis alle fuenf Review-Foki fuer das Kapitel approved sind. Der Revisionsagent erzeugt eine neue Kapitelversion und ersetzt nicht die Review-Freigaben.

## 2026-06-01 - Kapitelrevision Smoke-Test erfolgreich

Entscheidung: Der Revisionspfad nutzt fuer GPT-5-Modelle ein separates Completion-Limit von 8192 Tokens und das Full-Chapter-Budget.

Begruendung: Kapitelrevision erzeugt eine vollstaendige Kapitelversion und darf nicht durch das engere einzelne Reviewlauf-Limit begrenzt werden.

Ergebnis: Der Smoke-Test mit `gpt-5-mini` aus Rohfassung plus fuenf freigegebenen Reviewbefunden erzeugte eine neue Kapitelversion mit Status `pending_review`, ohne offene Punkte, fuer 0.004073 USD.

### Konsequenz
`config/model_profiles.toml` enthaelt lokale Health-Blocker. Kapitel-Leseproben duerfen erst mit einem Modell laufen, das den Health-Check und anschliessend den fuenfteiligen Leseproben-Benchmark besteht.
