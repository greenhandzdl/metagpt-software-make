from metagpt.roles import Role

from meta.actions import BackendAction, FrontendAction, WriteTestsAction


class TestEngineer(Role):
    """Test Engineer: writes and executes tests."""

    name: str = "Frank"
    profile: str = "Test Engineer"
    goal: str = "Ensure comprehensive test coverage and software quality"
    constraints: str = (
        "Write unit tests, integration tests, and end-to-end tests. "
        "Cover edge cases and ensure high test coverage."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._init_actions([WriteTestsAction])
        self._watch([FrontendAction, BackendAction])