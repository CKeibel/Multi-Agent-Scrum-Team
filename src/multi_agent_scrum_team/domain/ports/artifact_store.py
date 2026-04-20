from __future__ import annotations

from typing import Protocol, runtime_checkable

from multi_agent_scrum_team.domain.models import Artifact, ArtifactType


@runtime_checkable
class ArtifactStorePort(Protocol):
    async def save(self, artifact: Artifact) -> Artifact:
        ...

    async def get(self, artifact_id: str) -> Artifact | None:
        ...

    async def find_by_type(self, artifact_type: ArtifactType) -> list[Artifact]:
        ...
