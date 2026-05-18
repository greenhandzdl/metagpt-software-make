#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Software Factory — Multi-agent software development system.

Usage:
    python app.py "Build a simple CLI calculator"
"""

# Load .env BEFORE any metagpt imports so CONFIG sees the env vars
from dotenv import load_dotenv
load_dotenv()

import asyncio
import sys

from metagpt.logs import logger
from metagpt.team import Team

from meta.team import assemble_team, TEAM_CONFIG


def create_team() -> Team:
    """Create a team with all software-factory roles."""
    team = Team()
    team.hire(assemble_team())
    team.env.desc = TEAM_CONFIG["env_desc"]
    return team


async def main(requirement: str):
    """Run the software factory on a given requirement."""

    if not requirement:
        logger.error("No requirement provided. Usage: python app.py <requirement>")
        sys.exit(1)

    logger.info(f"Starting project: {requirement}")
    team = create_team()
    await team.run(n_round=5, idea=requirement, auto_archive=False)
    logger.info("Project completed. See storage logs for details.")


if __name__ == "__main__":
    req = sys.argv[1] if len(sys.argv) > 1 else ""
    asyncio.run(main(req))