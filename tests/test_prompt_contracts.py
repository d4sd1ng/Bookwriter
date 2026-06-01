from __future__ import annotations

from pathlib import Path


PROMPTS = [
    "book_concept_prompt.md",
    "outline_prompt.md",
    "chapter_briefing_prompt.md",
    "chapter_writer_prompt.md",
    "chapter_revision_prompt.md",
    "editor_prompt.md",
    "consistency_check_prompt.md",
    "export_preparation_prompt.md",
    "market_assessment_prompt.md",
    "publisher_offer_prompt.md",
    "kdp_preparation_prompt.md",
    "reading_sample_review_prompt.md",
    "brainstorming_prompt.md",
    "character_development_prompt.md",
    "plotting_prompt.md",
    "treatment_prompt.md",
    "research_scraping_prompt.md",
]


def test_prompts_define_contract_sections() -> None:
    for prompt_name in PROMPTS:
        content = Path("prompts", prompt_name).read_text(encoding="utf-8")

        assert "## Pflichtinput" in content
        assert "## Blocker" in content
        assert "## Ausgabeformat" in content
        assert "status" in content
        assert "blocker" in content.lower()
