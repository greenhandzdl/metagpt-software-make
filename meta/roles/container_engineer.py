from metagpt.roles import Role

from meta.actions import BackendAction, ContainerAction, FrontendAction


class ContainerEngineer(Role):
    """Container Engineer: creates deployment and CI/CD configuration."""

    name: str = "Charlie"
    profile: str = "Container Engineer"
    goal: str = "Create reliable, production-ready deployment configurations"
    constraints: str = (
        "Follow container best practices, optimize image sizes, "
        "and ensure configuration is environment-agnostic."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._init_actions([ContainerAction])
        self._watch([FrontendAction, BackendAction])