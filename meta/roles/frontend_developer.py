from metagpt.roles import Role

from meta.actions import DatabaseDesignAction, FrontendAction


class FrontendDeveloper(Role):
    """Frontend Developer: implements UI and interaction logic."""

    name: str = "Eve"
    profile: str = "Frontend Developer"
    goal: str = "Implement responsive, accessible, and maintainable frontend code"
    constraints: str = (
        "Follow component-based architecture, ensure responsive design, "
        "and integrate with backend APIs properly."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._init_actions([FrontendAction])
        self._watch([DatabaseDesignAction])