from metagpt.roles import Role

from meta.actions import BackendAction, DatabaseDesignAction


class BackendDeveloper(Role):
    """Backend Developer: implements business logic and APIs."""

    name: str = "Bob"
    profile: str = "Backend Developer"
    goal: str = "Implement robust, secure, and scalable backend services"
    constraints: str = (
        "Follow RESTful API design principles, implement proper error handling, "
        "and ensure data validation and security best practices."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._init_actions([BackendAction])
        self._watch([DatabaseDesignAction])