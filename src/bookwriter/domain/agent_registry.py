from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ReusableAgentProfile:
    agent_id: str
    name: str
    source_path: str
    preferred_source_path: str
    reuse_status: str
    bookwriter_role: str
    adapter_required: bool
    approval_required: bool
    must_emit_token_usage: bool
    disable_domain_logic: list[str]
    capabilities: list[str]


def load_reusable_agents(
    path: Path | str = "config/reusable_agents.toml",
) -> dict[str, ReusableAgentProfile]:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    profiles: dict[str, ReusableAgentProfile] = {}
    for raw_agent in data["agents"]:
        profile = ReusableAgentProfile(**raw_agent)
        profiles[profile.agent_id] = profile
    return profiles


def reusable_agents_requiring_token_usage() -> list[ReusableAgentProfile]:
    return [
        profile
        for profile in load_reusable_agents().values()
        if profile.must_emit_token_usage
    ]
