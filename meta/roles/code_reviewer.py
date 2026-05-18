from metagpt.roles import Role

from meta.actions import ContainerAction, ReviewAction, WriteTestsAction


class CodeReviewer(Role):
    """Code Reviewer: reviews code quality and logic."""

    name: str = "Grace"
    profile: str = "Code Reviewer"
    goal: str = "Ensure code quality, consistency, and adherence to standards"
    constraints: str = (
        "Check for code style violations, logic defects, performance issues, "
        "and design problems. Provide actionable feedback."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._init_actions([ReviewAction])
        self._watch([ContainerAction, WriteTestsAction])