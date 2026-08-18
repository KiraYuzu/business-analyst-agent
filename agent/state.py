from typing import TypedDict

class AgentState(TypedDict):
    requirement: str
    status: str
    conversation_history: list
    completed: bool