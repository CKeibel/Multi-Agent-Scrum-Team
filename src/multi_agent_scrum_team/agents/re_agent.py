from __future__ import annotations

from pydantic import BaseModel, Field

from multi_agent_scrum_team.domain.models import Artifact, ArtifactType, UserStoryOutput
from multi_agent_scrum_team.domain.ports import ArtifactStorePort, LLMPort


class REAgentOutput(BaseModel):
    feature_name: str = Field(description="Name of the Epic or Feature")
    needs_clarification: bool = Field(
        description="Set to true ONLY IF the initial prompt is too vague to create meaningful user stories."
    )
    user_stories: list[UserStoryOutput] = Field(
        description="The broken-down requirements. Leave empty if needs_clarification is true.",
        default_factory=list,
    )


class REAgent:
    """Requirements Engineer Agent"""

    def __init__(
        self, llm: LLMPort, store: ArtifactStorePort, agent_id: str = "re_agent"
    ) -> None:
        self._llm = llm
        self._store = store
        self._agent_id = agent_id

    async def analyze_feature(
        self, feature_description: str
    ) -> tuple[list[Artifact], list[str]]:
        system_message = self._build_system_message()
        response: REAgentOutput = await self._llm.complete(
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": f"Feature description: {feature_description}\n\nExtract comprehensive user stories with SMART acceptance criteria.",
                },
            ],
            response_format=REAgentOutput,
        )

        artifacts = []
        questions = []
        for story in response.user_stories:
            artifact = Artifact.new(
                artifact_type=ArtifactType.USER_STORY,
                title=story.title,
                content=story.model_dump(),
                creator_id=self._agent_id,
            )
            questions.extend(story.open_questions)
            await self._store.save(artifact)
            artifacts.append(artifact)

        return artifacts, questions

    def _build_system_message(self) -> str:
        return """You are a Senior Requirements Engineer with 15 years of experience in designing highly scalable software systems.

Your task is to extract comprehensive, unambiguous, and testable user stories from raw feature descriptions provided by stakeholders. You will output your analysis strictly matching the provided JSON schema.

CRITICAL RULES & CONSTRAINTS:

1. THE "KILL SWITCH" (needs_clarification):
If the initial feature description is fundamentally too vague, contradictory, or lacks core business logic to create meaningful stories, you MUST set `needs_clarification` to true and leave the `user_stories` list empty. Do NOT hallucinate or guess requirements.

2. STRICT QUALITY FOR USER STORIES:
- Roles: Never use generic terms like "User" or "Person" in the `role` field. Define specific actors (e.g., "Unauthenticated Visitor", "Database Admin", "Payment Gateway").
- Title: Ensure the `title` is concise and acts as a clear identifier (max 50 characters).
- Feature & Benefit: Be explicit about what the feature is and the tangible business value it delivers.
- Ambiguity: If a specific story has ambiguities or missing technical details, log specific questions in its `open_questions` array.

3. ACCEPTANCE CRITERIA (Given/When/Then):
Each story must have at least 2 acceptance criteria. They must be highly specific and deterministic so a developer can immediately write a passing/failing automated test. Strictly prefer the "Given [Context], When [Action], Then [Result]" format.

4. ESTIMATION & PRIORITY:
- Complexity: You MUST use T-Shirt sizing for `complexity_estimation`. Strictly use one of: "S", "M", "L", "XL".
- Priority: Reflects business value and user impact. Strictly use one of: "CRITICAL", "HIGH", "MEDIUM", "LOW"."""
