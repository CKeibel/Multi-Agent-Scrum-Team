from __future__ import annotations

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
