"""Team assembly for the multi-agent software factory."""

from meta.roles import (
    Architect,
    BackendDeveloper,
    CodeReviewer,
    ContainerEngineer,
    DatabaseEngineer,
    FrontendDeveloper,
    SecurityAuditor,
    TestEngineer,
)

# Development workflow order — follows the conflict priority and process flow
TEAM_CONFIG = {
    "name": "SoftwareFactory",
    "env_desc": (
        "A software development company where teams collaborate to "
        "build high-quality software systems following a defined workflow."
    ),
    "roles": [
        Architect,
        DatabaseEngineer,
        FrontendDeveloper,
        BackendDeveloper,
        ContainerEngineer,
        TestEngineer,
        CodeReviewer,
        SecurityAuditor,
    ],
}


def assemble_team() -> list:
    """Instantiate all team roles."""
    return [role_cls() for role_cls in TEAM_CONFIG["roles"]]