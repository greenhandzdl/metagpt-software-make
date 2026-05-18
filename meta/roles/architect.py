from metagpt.actions import UserRequirement
from metagpt.roles import Role

from meta.actions import ArchitectureAction as ArchitectureAct


class Architect(Role):
    """Architect: designs software architecture from requirements."""

    name: str = "Alice"
    profile: str = "Architect"
    goal: str = "Design a concise, usable, complete software system"
    constraints: str = (
        "Ensure the architecture is simple enough and uses appropriate "
        "open source libraries. Output in the same language as the requirement."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._init_actions([ArchitectureAct])
        self._watch([UserRequirement])