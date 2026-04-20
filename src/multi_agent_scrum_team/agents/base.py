from __future__ import annotations

from enum import Enum, auto


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
