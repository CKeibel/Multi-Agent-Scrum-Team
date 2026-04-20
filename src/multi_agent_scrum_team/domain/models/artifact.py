from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ArtifactType(str, Enum):
    USER_STORY = "user_story"
    SOURCE_CODE = "source_code"
    TEST_CASE = "test_case"
    TEST_RESULT = "test_result"
    CODE_REVIEW = "code_review"
    SPRINT_SUMMARY = "sprint_summary"


class ArtifactStatus(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Artifact:
    id: str
    artifact_type: ArtifactType
    title: str
    content: Any
    creator_id: str
    status: ArtifactStatus = ArtifactStatus.DRAFT
    created_at: str = field(default_factory=lambda: datetime.now())
    updated_at: str = field(default_factory=lambda: datetime.now())
    version: int = 1
    history: list[dict] = field(default_factory=list)

    @staticmethod
    def new(
        artifact_type: ArtifactType, title: str, content: Any, creator_id: str
    ) -> "Artifact":
        return Artifact(
            id=str(uuid.uuid4),
            artifact_type=artifact_type,
            title=title,
            creator_id=creator_id,
            content=content,
        )

    def update_content(
        self, new_content: Any, update_id: str, reason: str = ""
    ) -> None:
        self.history.append(
            {
                "version": self.version,
                "content": self.content,
                "updated_by": update_id,
                "at": self.updated_at,
                "reason": reason,
            }
        )
        self.content = new_content
        self.version += 1
        self.updated_at = datetime.now()
