#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the software-factory multi-agent system.

Note: Tests that call LLM (marked with `needs_llm`) require a running LLM endpoint.
      Unit tests (TestRoleDefinitions) work without any LLM.
"""

import os

import pytest

from meta.actions.software_actions import (
    ArchitectureAction,
    BackendAction,
    ContainerAction,
    DatabaseDesignAction,
    FrontendAction,
    ReviewAction,
    SecurityAction,
    WriteTestsAction,
)

# Markers: skip LLM-dependent tests unless NEEDS_LLM=true
needs_llm = pytest.mark.skipif(
    not os.environ.get("NEEDS_LLM"),
    reason="Set NEEDS_LLM=true to run tests that call an actual LLM endpoint",
)


@needs_llm
@pytest.mark.asyncio
async def test_architecture_action():
    """Test that the ArchitectureAction produces valid output."""
    action = ArchitectureAction()
    result = await action.run("Build a web-based task management system")
    assert isinstance(result, str)
    assert len(result) > 50


@needs_llm
@pytest.mark.asyncio
async def test_backend_action():
    action = BackendAction()
    result = await action.run("Design a REST API with user authentication")
    assert isinstance(result, str)
    assert len(result) > 50


@needs_llm
@pytest.mark.asyncio
async def test_frontend_action():
    action = FrontendAction()
    result = await action.run("Build a React dashboard for analytics")
    assert isinstance(result, str)
    assert len(result) > 50


@needs_llm
@pytest.mark.asyncio
async def test_database_design_action():
    action = DatabaseDesignAction()
    result = await action.run("Design schema for a multi-tenant SaaS application")
    assert isinstance(result, str)
    assert len(result) > 50


@needs_llm
@pytest.mark.asyncio
async def test_container_action():
    action = ContainerAction()
    result = await action.run("Containerize a Python FastAPI application")
    assert isinstance(result, str)
    assert len(result) > 50


@needs_llm
@pytest.mark.asyncio
async def test_testing_action():
    action = WriteTestsAction()
    result = await action.run("Test a user authentication module")
    assert isinstance(result, str)
    assert len(result) > 50


@needs_llm
@pytest.mark.asyncio
async def test_review_action():
    action = ReviewAction()
    result = await action.run("Review code for a payment processing module")
    assert isinstance(result, str)
    assert len(result) > 50


@needs_llm
@pytest.mark.asyncio
async def test_security_action():
    action = SecurityAction()
    result = await action.run("Audit a web application for security issues")
    assert isinstance(result, str)
    assert len(result) > 50


class TestRoleDefinitions:
    """Verify role class structure and configuration (no LLM needed)."""

    def test_architect_role(self):
        from meta.roles.architect import Architect

        role = Architect()
        assert role.name == "Alice"
        assert role.profile == "Architect"
        assert len(role.actions) > 0

    def test_backend_developer_role(self):
        from meta.roles.backend_developer import BackendDeveloper

        role = BackendDeveloper()
        assert role.name == "Bob"
        assert role.profile == "Backend Developer"
        assert len(role.actions) > 0

    def test_container_engineer_role(self):
        from meta.roles.container_engineer import ContainerEngineer

        role = ContainerEngineer()
        assert role.name == "Charlie"
        assert role.profile == "Container Engineer"

    def test_database_engineer_role(self):
        from meta.roles.database_engineer import DatabaseEngineer

        role = DatabaseEngineer()
        assert role.name == "Dave"
        assert role.profile == "Database Engineer"

    def test_frontend_developer_role(self):
        from meta.roles.frontend_developer import FrontendDeveloper

        role = FrontendDeveloper()
        assert role.name == "Eve"
        assert role.profile == "Frontend Developer"

    def test_test_engineer_role(self):
        from meta.roles.test_engineer import TestEngineer

        role = TestEngineer()
        assert role.name == "Frank"
        assert role.profile == "Test Engineer"

    def test_code_reviewer_role(self):
        from meta.roles.code_reviewer import CodeReviewer

        role = CodeReviewer()
        assert role.name == "Grace"
        assert role.profile == "Code Reviewer"

    def test_security_auditor_role(self):
        from meta.roles.security_auditor import SecurityAuditor

        role = SecurityAuditor()
        assert role.profile == "Security Auditor"
        assert role.name == "Heidi"

    def test_all_roles_exported(self):
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

        assert len([Architect, BackendDeveloper, CodeReviewer, ContainerEngineer,
                     DatabaseEngineer, FrontendDeveloper, SecurityAuditor, TestEngineer]) == 8

    def test_team_assembly(self):
        from meta.team import TEAM_CONFIG, assemble_team

        roles = assemble_team()
        assert len(roles) == 8
        assert TEAM_CONFIG["name"] == "SoftwareFactory"

    def test_role_watch_patterns(self):
        """Verify each role watches the correct actions (stored as string paths)."""
        from metagpt.utils.common import any_to_str
        from meta.roles.architect import Architect
        from meta.roles.backend_developer import BackendDeveloper
        from meta.roles.code_reviewer import CodeReviewer
        from meta.roles.container_engineer import ContainerEngineer
        from meta.roles.database_engineer import DatabaseEngineer
        from meta.roles.frontend_developer import FrontendDeveloper
        from meta.roles.security_auditor import SecurityAuditor
        from meta.roles.test_engineer import TestEngineer
        from meta.actions import ArchitectureAction, BackendAction, ContainerAction, \
            DatabaseDesignAction, FrontendAction, ReviewAction, SecurityAction, WriteTestsAction

        # Architect watches UserRequirement
        arch = Architect()
        assert "metagpt.actions.add_requirement.UserRequirement" in arch.rc.watch

        # Database engineer watches Architecture
        db = DatabaseEngineer()
        assert any_to_str(ArchitectureAction) in db.rc.watch

        # Frontend and backend watch DatabaseDesign
        fe = FrontendDeveloper()
        assert any_to_str(DatabaseDesignAction) in fe.rc.watch
        be = BackendDeveloper()
        assert any_to_str(DatabaseDesignAction) in be.rc.watch

        # Container watches frontend and backend
        ce = ContainerEngineer()
        assert any_to_str(FrontendAction) in ce.rc.watch
        assert any_to_str(BackendAction) in ce.rc.watch

        # Code reviewer watches container and testing
        cr = CodeReviewer()
        assert any_to_str(ContainerAction) in cr.rc.watch
        assert any_to_str(WriteTestsAction) in cr.rc.watch

        # Security auditor watches container and testing
        sa = SecurityAuditor()
        assert any_to_str(ContainerAction) in sa.rc.watch
        assert any_to_str(WriteTestsAction) in sa.rc.watch

    def test_all_role_profiles_unique(self):
        """Every role should have a unique profile string."""
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

        profiles = [cls().profile for cls in [
            Architect, BackendDeveloper, CodeReviewer, ContainerEngineer,
            DatabaseEngineer, FrontendDeveloper, SecurityAuditor, TestEngineer,
        ]]
        assert len(profiles) == len(set(profiles)), f"Duplicate profiles: {profiles}"


@pytest.mark.asyncio
async def test_team_round_mocked():
    """Test team integration with mocked LLM calls."""
    from unittest.mock import AsyncMock
    from metagpt.team import Team
    from meta.team import assemble_team

    team = Team()
    team.hire(assemble_team())
    team.env.desc = "A software development company."

    # Mock the LLM for every role to avoid real API calls
    mock = AsyncMock(return_value="Mocked output for testing purposes. " * 20)
    for role in team.env.get_roles().values():
        role.llm.aask = mock

    await team.run(n_round=1, idea="Build a CLI calculator", auto_archive=False)
    history = team.env.history
    assert history is not None