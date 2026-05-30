from __future__ import annotations

from bookwriter.domain.agent_registry import (
    load_reusable_agents,
    reusable_agents_requiring_token_usage,
)


def test_reusable_agent_registry_contains_existing_token_agents() -> None:
    agents = load_reusable_agents()

    assert "token_monitoring" in agents
    assert "token_cost_calculator" in agents
    assert agents["token_monitoring"].adapter_required is True
    assert "Nurtoring-Email" in agents["token_monitoring"].preferred_source_path


def test_scraping_agent_disables_non_bookwriter_domain_logic() -> None:
    agents = load_reusable_agents()
    scraping = agents["web_scraping"]

    assert "youtube" in scraping.disable_domain_logic
    assert "social_media" in scraping.disable_domain_logic
    assert scraping.approval_required is True


def test_model_based_reusable_agents_require_token_usage() -> None:
    agent_ids = {agent.agent_id for agent in reusable_agents_requiring_token_usage()}

    assert "token_monitoring" in agent_ids
    assert "text_analysis" in agent_ids
    assert "content_approval" in agent_ids


def test_nurtoring_is_preferred_when_agent_exists_there() -> None:
    agents = load_reusable_agents()

    assert "Nurtoring-Email" in agents["token_monitoring"].preferred_source_path
    assert "Nurtoring-Email" in agents["token_cost_calculator"].preferred_source_path
    assert "Nurtoring-Email" in agents["content_approval"].preferred_source_path
    assert "Nurtoring-Email" in agents["rate_limiter"].preferred_source_path


def test_youtube_automations_remains_fallback_for_missing_nurtoring_agents() -> None:
    agents = load_reusable_agents()

    assert "youtube_automations" in agents["text_analysis"].preferred_source_path
    assert "youtube_automations" in agents["document_export"].preferred_source_path
    assert "youtube_automations" in agents["web_scraping"].preferred_source_path
