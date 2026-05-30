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
`bookwriter review-chapter` kann mit `--use-ollama` das konfigurierte Review-Modell ausfuehren. Der Lauf validiert Modell und Kontext gegen `config/model_profiles.toml`, fordert JSON-Ausgabe an und protokolliert Input-/Output-Tokens in `data/token_usage.jsonl`.
