# Agent Inventory: Bookwriter

## Geeignete vorhandene Agenten

- Advanced Prompting Agent
- Analytics Agent
- Content Approval Agent
- Content Management Agent
- Database Service Agent
- Document Export Agent
- Orchestrator Agent
- Path Management Agent
- Pipeline Orchestrator
- Rate Limiter Agent
- Text Analysis Agent
- Token Cost Calculator Agent
- Token Monitoring Agent
- Translation Agent
- Workflow Executor Agent

## Projektuebergreifend wiederzuverwenden

Shared Agents koennen aus mehreren Projekten stammen. `Nurtoring-Email` wird bevorzugt, wenn der Agent dort vorhanden ist; `youtube_automations` enthaelt viele weitere Kandidaten, ist aber nicht automatisch die beste Quelle.

Diese Agenten existieren bereits in anderen Projekten und sollen nicht neu gebaut, sondern ueber Adapter wiederverwendet werden:

- Token Monitoring Agent: bevorzugt `Nurtoring-Email`, Kandidat auch in `youtube_automations`
- Token Cost Calculator Agent: bevorzugt `Nurtoring-Email`, Kandidaten auch in `youtube_automations` und `multi-input-recovered`
- Text Analysis Agent: Kandidaten in `youtube_automations` und `multi-input-recovered`
- Content Approval Agent: bevorzugt `Nurtoring-Email`, Kandidaten auch in `youtube_automations` und `multi-input-recovered`
- Document Export Agent: Kandidaten in `youtube_automations` und `multi-input-recovered`
- Web Scraping Agent: `G:/Projects/youtube_automations/web-scraping-agent`
- Trend Analysis Agent: `G:/Projects/youtube_automations/trend-analysis-agent`
- Rate Limiter Agent: bevorzugt `Nurtoring-Email`, Kandidat auch in `youtube_automations`
- Workflow Executor Agent: `G:/Projects/youtube_automations/workflow-executor-agent`

Details stehen in `agent_reuse_strategy.md` und `config/reusable_agents.toml`.

## Bedingt geeignet

- CTA Generation Agent: nur für Abschluss-CTA in Buch, E-Book oder Whitepaper
- SEO Optimization Agent: nur für Titel, Untertitel oder Suchbegriffe im E-Book-Kontext
- Infographics Agent: nur für Buchgrafiken
- Visual Analysis Agent: nur für Layout- oder Designprüfung
- Web Scraping Agent: nur für freigegebene Quellenrecherche
- Trend Analysis Agent: nur für aktuelle Fachrecherche

## Nicht geeignet

- Caption Generation Agent
- Channel Banner Agent
- Comment Response Agent
- Content Scheduler Agent
- Interactive Lower Third Agent
- SEO Channel Optimization Agent
- SEO LinkedIn Optimization Agent
- SEO Video Optimization Agent
- Thumbnail Generation Agent
- Video Discovery Agent
- Video Overlay Agent
- Video Processing Agent
- Video Reposing Agent
- Video Scheduler Agent
