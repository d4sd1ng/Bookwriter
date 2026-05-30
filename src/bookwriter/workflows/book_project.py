from __future__ import annotations

from pathlib import Path

from bookwriter.agents.orchestrator import Orchestrator
from bookwriter.domain.models import BookProject, Interview
from bookwriter.storage.json_store import JsonProjectStore


class BookProjectWorkflow:
    def __init__(self, store: JsonProjectStore | None = None) -> None:
        self.store = store or JsonProjectStore()
        self.orchestrator = Orchestrator()

    def create_from_interview(self, name: str, interview: Interview) -> tuple[BookProject, Path]:
        project = self.orchestrator.create_project(name, interview)
        return project, self.store.save(project)

    def load(self, project_id: str) -> BookProject:
        return self.store.load(project_id)

    def save(self, project: BookProject) -> Path:
        return self.store.save(project)
