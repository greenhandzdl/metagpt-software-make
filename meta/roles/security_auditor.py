from metagpt.roles import Role

from meta.actions import ContainerAction, SecurityAction, WriteTestsAction


class SecurityAuditor(Role):
    """Security Auditor: performs security analysis on the codebase."""

    name: str = "Heidi"
    profile: str = "Security Auditor"
    goal: str = "Identify and remediate security vulnerabilities"
    constraints: str = (
        "Perform thorough security analysis including OWASP Top 10, "
        "dependency scanning, secret detection, and permission model validation."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._init_actions([SecurityAction])
        self._watch([ContainerAction, WriteTestsAction])