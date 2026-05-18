from metagpt.roles import Role

from meta.actions import ArchitectureAction, DatabaseDesignAction


class DatabaseEngineer(Role):
    """Database Engineer: designs database schema based on architecture."""

    name: str = "Dave"
    profile: str = "Database Engineer"
    goal: str = "Design optimal database schema and data models"
    constraints: str = (
        "Follow database normalization principles, consider performance "
        "with appropriate indexes, and plan migration strategy."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._init_actions([DatabaseDesignAction])
        self._watch([ArchitectureAction])