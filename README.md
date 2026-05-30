# Bookwriter Project Files

## Zweck

Dieses Paket enthält ausschließlich Projektdateien für den Bookwriter.

Nicht enthalten:

- YouTube Automation
- LinkedIn
- Shorts
- Social Media
- Videoproduktion
- Plattform-Ausspielung

## Ziel

Der Bookwriter ist ein agentenbasiertes System zur Planung, Erstellung, Prüfung und Exportvorbereitung langer Texte.

Mögliche Inhalte:

- Bücher
- E-Books
- Whitepaper
- Fachtexte
- Praxisleitfäden
- Ratgeber
- Reports
- Kursunterlagen
- Unternehmensdokumentationen
- Case-Study-Sammlungen

## Kern-Dateien

1. README.md
2. project_overview.md
3. task_contract.md
4. decision_log.md
5. architecture_rules.md
6. model_strategy.md
7. interview_questionnaire.md

## Zusatzbereiche

- agents
- processes
- templates
- prompts
- reports

## Oberste Regel

Der Bookwriter bleibt vollständig getrennt von YouTube, LinkedIn und Social Media.

Erstellt: 2026-05-30

## Lokale Entwicklung

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
bookwriter interview
```

## Erste CLI-Befehle

```powershell
bookwriter interview --name "Mein Buch" --topic "KI Beratung" --target-audience "Berater" --book-type "Praxisleitfaden" --desired-result "ein Angebot entwickeln" --tone "direkt" --length-goal "8 Kapitel" --export-format "Markdown"
bookwriter approve-concept <project_id> --chapters 8
bookwriter market <project_id>
bookwriter publisher-offer <project_id> --publisher "Beispiel Verlag"
bookwriter kdp-checklist <project_id>
bookwriter models
bookwriter questions
bookwriter brainstorm --seed "Mut"
bookwriter set-foundation <project_id> --book-category "Belletristik" --age-group "Erwachsene" --narrative-focus "charakterorientiert" --perspective "3. Person" --perspective-count "eine Perspektive" --ending-type "offenes Ende" --publication-format "Taschenbuch" --character-mode "Figuren entwickeln"
bookwriter foundation-check <project_id>
bookwriter approve-concept <project_id>
bookwriter plot <project_id>
bookwriter approve-plot <project_id>
bookwriter treatment <project_id>
bookwriter approve-treatment <project_id> --chapters 8
bookwriter chapter-briefing <project_id> --chapter 1
bookwriter approve-briefing <project_id> --chapter 1
bookwriter draft-chapter <project_id> --chapter 1
bookwriter review-chapter <project_id> --chapter 1 --focus fehlerkorrektur
bookwriter review-chapter <project_id> --chapter 1 --focus fehlerkorrektur --use-ollama
bookwriter approve-review <project_id> --chapter 1 --focus fehlerkorrektur
bookwriter approve-chapter <project_id> --chapter 1
bookwriter token-log --project-id <project_id> --task reading_sample_review --model gpt-oss:20b --input-tokens 12000 --output-tokens 1800
bookwriter usage --project-id <project_id>
```

Die KDP- und Verlagsfunktionen bereiten nur pruefpflichtige Unterlagen vor. Ein Upload oder Versand wird nicht automatisch ausgefuehrt.

## Ollama-Modellstrategie

Der Bookwriter nutzt `gpt-oss:20b` als Primaermodell fuer Orchestrierung, Struktur, Pruefung, Markt- und Publishing-Vorbereitung. `qwen2.5:7b` ist als schnelles Nebenmodell fuer kurze Entwuerfe, Stilvarianten und einfache Umformulierungen vorgesehen.

Die Routing-Regeln stehen in `model_strategy.md` und `config/model_profiles.toml`.

## Token und Kosten

Tokenverbrauch und geschaetzte API-Kosten werden im Ledger `data/token_usage.jsonl` protokolliert. Lokale Ollama-Modelle haben API-Kosten von 0. Externe Modelle brauchen vor Nutzung ein freigegebenes Kostenprofil in `config/token_costs.toml`.

Kapitel-Leseproben koennen mit `--use-ollama` gegen das konfigurierte Review-Modell ausgefuehrt werden. Der Lauf nutzt das Taskprofil `reading_sample_review`, blockiert ungeeignete Review-Modelle und schreibt gemessene Input-/Output-Tokens automatisch ins Ledger.

## Shared Agents

Zentrale Quelle fuer wiederverwendbare Agenten ist `G:/Agenten-Standards` bzw. `https://github.com/d4sd1ng/Agenten-Standards`.

Bookwriter nutzt Adapter und projektspezifische Regeln, statt generische Agenten neu zu bauen. Nurtoring-Agenten werden bevorzugt, wenn sie dort vorhanden sind; andere Projekte bleiben Kandidaten bis zum Audit.

## Interview

Der Fragenkatalog steht als Abstimmungsentwurf in `interview_questionnaire.md` und `config/interview_questions.toml`. Die CLI kann ihn mit `bookwriter questions` anzeigen und nutzt die konfigurierten Fragen fuer das interaktive Interview; fuer produktive Buchprojekte muss der Fragenkatalog vorher freigegeben werden.

## Entwicklungsfundament

Vor Plotting, Treatment und Kapitelarbeit muessen Startmodus, Buchart, Alters-/Zielgruppe, Erzaehlfokus, Perspektive, Ende, Ausgabeform, Figurenstatus und Recherchemodus feststehen. Fehlt eine eigene Idee, erzeugt `bookwriter brainstorm` einen 5-3-1-Funnel.

Outline entsteht erst nach freigegebenem Konzept, freigegebenem Plot und freigegebenem Treatment.

## Kapitelpipeline

Jedes Kapitel laeuft ueber ein freigegebenes Kapitelbriefing, eine Rohfassung und fuenf getrennte Review-Runs. Die Kapitel-Freigabe blockiert, bis Fehlerkorrektur, Logikfehler, Spannungsbogen, Schreibstil und Grammatik als einzelne Reviews freigegeben sind.
