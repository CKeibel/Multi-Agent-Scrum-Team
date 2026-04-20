from typing import Literal

from pydantic import BaseModel, Field


class UserStoryOutput(BaseModel):
    title: str = Field(
        description="A short, concise title for this story (max 50 characters)"
    )
    role: str = Field(description="Specific user role, not 'user' or 'person'")
    feature: str = Field(description="What the user wants to accomplish")
    benefit: str = Field(description="The business value this delivers")
    priority: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    acceptance_criteria: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(
        default_factory=list
    )  # Counteracting Hallucinations
    complexity_estimation: Literal["S", "M", "L", "XL"] = Field(
        description="Estimated implementation effort (T-Shirt size)"
    )

    def as_story_text(self) -> str:
        return f"As a {self.role}, I want {self.feature}, so that {self.benefit}"
