import asyncio

from multi_agent_scrum_team.domain.models import Artifact, ArtifactType


# TODO: Implement as PostgresSQL Store
class ArtifactStore:
    """In-Memory Artifact Store."""

    def __init__(self) -> None:
        self._store: dict[str, Artifact] = {}
        self._lock = asyncio.Lock()

    async def save(self, artifact: Artifact) -> Artifact:
        async with self._lock:
            self._store[artifact.id] = artifact
            return artifact

    async def get(self, artifact_id: str) -> Artifact | None:
        return self._store.get(artifact_id)

    async def find_by_type(self, artifact_type: ArtifactType) -> list[Artifact]:
        results = [
            artifact
            for artifact in self._store.values()
            if artifact.artifact_type == artifact_type
        ]
        return sorted(results, key=lambda artifact: artifact.created_at)
