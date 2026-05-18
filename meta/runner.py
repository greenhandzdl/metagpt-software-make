"""Sequential runner: roles execute in chain order, outputs saved to proj/ git branches."""

import asyncio
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

# Load .env before any metagpt import
from dotenv import load_dotenv
load_dotenv(_ROOT / ".env")

from metagpt.logs import logger
from metagpt.schema import Message
from metagpt.utils.common import any_to_str

PROJ_DIR = _ROOT / "proj"

from meta.actions import (
    ArchitectureAction,
    BackendAction,
    ContainerAction,
    DatabaseDesignAction,
    FrontendAction,
    ReviewAction,
    SecurityAction,
    WriteTestsAction,
)

# (profile, branch, subdir, trigger_action_class, role_class)
STEPS = [
    ("Architect",          "arch/architecture-design", "doc",      None,                    "Architect"),
    ("Database Engineer",  "db/schema-design",         "database", ArchitectureAction,      "DatabaseEngineer"),
    ("Frontend Developer", "fe/vue-frontend",          "frontend", DatabaseDesignAction,    "FrontendDeveloper"),
    ("Backend Developer",  "be/springboot-backend",    "backend",  DatabaseDesignAction,    "BackendDeveloper"),
    ("Container Engineer", "ops/container-config",     "doc",      BackendAction,           "ContainerEngineer"),
    ("Test Engineer",      "test/tests",               "doc",      BackendAction,           "TestEngineer"),
    ("Code Reviewer",      "review/code-review",       "doc",      ContainerAction,         "CodeReviewer"),
    ("Security Auditor",   "security/audit",           "doc",      ContainerAction,         "SecurityAuditor"),
]


def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=PROJ_DIR, capture_output=True, text=True)
    if r.returncode and r.stderr.strip():
        logger.warning(f"  git warning: {r.stderr.strip()[:120]}")
    return r


def branch_exists(branch):
    return git("rev-parse", "--verify", branch).returncode == 0


def init_repo(requirement: str):
    if not (PROJ_DIR / ".git").exists():
        git("init")
        git("checkout", "-b", "main")
        (PROJ_DIR / "README.md").write_text(f"# Project\n{requirement}\n")
        (PROJ_DIR / ".gitignore").write_text("__pycache__/\n.env\n")
        git("add", ".")
        git("commit", "-m", "chore: init project")
        logger.info("Initialized proj/ git repo")


def save_output(profile, branch, subdir, content, rnd):
    if not content.strip():
        return
    if not branch_exists(branch):
        git("checkout", "main")
        git("checkout", "-b", branch)
    else:
        git("checkout", branch)
    target = PROJ_DIR / subdir
    target.mkdir(parents=True, exist_ok=True)
    name = profile.lower().replace(" ", "_")
    path = target / f"{name}_r{rnd}.md"
    path.write_text(f"# {profile} — Round {rnd}\n\n{content}\n")
    git("add", ".")
    if git("status", "--porcelain").stdout.strip():
        git("commit", "-m", f"{profile} (round {rnd})")
        logger.info(f"  ✓ saved to {branch}")
    else:
        logger.info(f"  - {branch}: no changes")


async def main(requirement: str = ""):
    if not requirement:
        requirement = (
            "Build a simple MVC project with Vue 3 frontend and Spring Boot "
            "backend, connected via REST API. Use H2 in-memory database."
        )

    from meta.roles import (
        Architect, BackendDeveloper, CodeReviewer, ContainerEngineer,
        DatabaseEngineer, FrontendDeveloper, SecurityAuditor, TestEngineer,
    )

    role_map = {
        "Architect": Architect,
        "DatabaseEngineer": DatabaseEngineer,
        "FrontendDeveloper": FrontendDeveloper,
        "BackendDeveloper": BackendDeveloper,
        "ContainerEngineer": ContainerEngineer,
        "TestEngineer": TestEngineer,
        "CodeReviewer": CodeReviewer,
        "SecurityAuditor": SecurityAuditor,
    }

    init_repo(requirement)
    logger.info(f"=== Requirement: {requirement} ===")

    # latest_outputs[action_class_str] = content
    latest_outputs = {}

    ROUNDS = 4
    for rnd in range(1, ROUNDS + 1):
        logger.info(f"--- Round {rnd}/{ROUNDS} ---")
        for profile, branch, subdir, trigger_class, role_name in STEPS:
            # Build input
            if rnd == 1 and profile == "Architect":
                msg = Message(content=requirement)
            elif trigger_class and any_to_str(trigger_class) in latest_outputs:
                content = latest_outputs[any_to_str(trigger_class)]
                cause_by = any_to_str(trigger_class)
                msg = Message(content=content, cause_by=cause_by)
            else:
                continue

            role = role_map[role_name]()
            result = await role.run(with_message=msg)
            if result:
                content = getattr(result, "content", "")
                if content:
                    # Store output keyed by *this role's* action class for downstream
                    for act in role.actions:
                        latest_outputs[any_to_str(type(act))] = content
                    save_output(profile, branch, subdir, content, rnd)
                    logger.info(f"  ✓ {profile}")
                else:
                    logger.warning(f"  ~ {profile}: empty")
            else:
                logger.warning(f"  ~ {profile}: no result")

    # Merge all branches → main
    git("checkout", "main")
    for _, branch, _, _, _ in STEPS:
        if branch_exists(branch):
            git("merge", branch, "--no-ff", "-m", f"Merge {branch}")

    log = git("log", "--oneline", "--graph", "--all")
    logger.info(f"=== Git History ===\n{log.stdout}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else ""))