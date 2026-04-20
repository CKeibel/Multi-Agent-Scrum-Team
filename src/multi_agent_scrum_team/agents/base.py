from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto

from multi_agent_scrum_team.config.settings import settings


class AgentState(Enum):
    IDLE = auto()
    THINKING = auto()
    TOOL_EXECUTION = auto()
    AWAITING_APPROVAL = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


VALID_TRANSITIONS: dict[AgentState, set[AgentState]] = {
    AgentState.IDLE: {AgentState.THINKING},
    AgentState.THINKING: {
        AgentState.TOOL_EXECUTION,
        AgentState.AWAITING_APPROVAL,
        AgentState.COMPLETED,
        AgentState.FAILED,
    },
    AgentState.TOOL_EXECUTION: {AgentState.THINKING, AgentState.FAILED},
    AgentState.AWAITING_APPROVAL: {
        AgentState.TOOL_EXECUTION,
        AgentState.THINKING,
        AgentState.CANCELLED,
    },
    AgentState.COMPLETED: set(),
    AgentState.FAILED: set(),
    AgentState.CANCELLED: set(),
}


class InvalidTransitionError(Exception):
    pass


@dataclass
class AgentRuntime:
    run_id: str
    agent_id: str
    task: str
    state: AgentState
    step_count: int = 0
    max_steps: int = 20
    tokens_used: int = 0
    token_budget: int = 50_000
    cost: float = 0.0
    cost_limit: float = 0.0
    final_answer: str | None = None
    error: str | None = None
    state_histroy: list[tuple[str, float]] = field(default_factory=list)
    started_at: float = field(default_factory=time.monotonic)

    def transition_to(self, new_state: AgentState) -> None:
        valid_transition = VALID_TRANSITIONS.get(self.state, set())
        if new_state not in valid_transition:
            return InvalidTransitionError(
                f"{self.agent_id}: Invalid Transition: {self.state} -> {new_state}"
            )
        self.state_histroy.append((self.state.name, time.monotonic()))
        self.state = new_state

    def update_token_usage(self, input_tokens: int, output_tokens: int) -> None:
        self.token_budget += input_tokens + output_tokens
        self.cost += (input_tokens * settings.input_tokens_cost) + (
            output_tokens * settings.output_tokens_cost
        )

    def should_abort(self) -> tuple[bool, str]:
        if self.tokens_used >= self.token_budget:
            return True, f"Token Limit Reached: {self.tokens_used}/{self.token_budget}"
        if self.cost >= self.cost_limit:
            return True, f"Cost Limit Reached: {self.cost}/{self.cost_limit}"
        if self.step_count >= self.max_steps:
            return True, f"Max Step Count Reached: {self.step_count}/{self.max_steps}"

    def is_terminal_state(self) -> bool:
        return self.state in {
            AgentState.COMPLETED,
            AgentState.FAILED,
            AgentState.CANCELLED,
        }
