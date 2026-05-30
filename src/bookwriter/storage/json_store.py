from __future__ import annotations

import json
from pathlib import Path

from bookwriter.domain.models import BookProject


class JsonProjectStore:
    def __init__(self, root: Path | str = "data/projects") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, project: BookProject) -> Path:
        project.touch()
        path = self.path_for(project.project_id)
        path.write_text(
            json.dumps(project.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    def load(self, project_id: str) -> BookProject:
        path = self.path_for(project_id)
        if not path.exists():
            raise FileNotFoundError(f"Project not found: {project_id}")
        return BookProject.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def path_for(self, project_id: str) -> Path:
        safe_id = "".join(char for char in project_id if char.isalnum() or char in "-_")
        return self.root / f"{safe_id}.json"
