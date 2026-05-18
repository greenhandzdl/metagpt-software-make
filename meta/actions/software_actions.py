"""Action classes for the multi-agent software development workflow."""

from metagpt.actions import Action


class ArchitectureAction(Action):
    """Produce a software architecture design based on requirements."""

    name: str = "ArchitectureAction"

    async def run(self, context: str) -> str:
        prompt = (
            "You are a Software Architect. Given the following requirements, "
            "design a concise, usable, complete software system architecture.\n\n"
            f"Requirements:\n{context}\n\n"
            "Output the architecture design including: system overview, "
            "component/module breakdown, tech stack recommendations, "
            "and data flow between components."
        )
        return await self._aask(prompt)


class DatabaseDesignAction(Action):
    """Design database schema based on architecture."""

    name: str = "DatabaseDesignAction"

    async def run(self, context: str) -> str:
        prompt = (
            "You are a Database Engineer. Based on the architecture design below, "
            "create a database schema design.\n\n"
            f"Architecture:\n{context}\n\n"
            "Output the database design including: table definitions with columns and types, "
            "indexes, relationships, and migration strategy."
        )
        return await self._aask(prompt)


class FrontendAction(Action):
    """Implement frontend code."""

    name: str = "FrontendAction"

    async def run(self, context: str) -> str:
        prompt = (
            "You are a Frontend Developer. Based on the architecture and database design, "
            "implement the frontend code.\n\n"
            f"Context:\n{context}\n\n"
            "Output the frontend implementation including: component structure, "
            "key UI components, API integration code, and styling approach."
        )
        return await self._aask(prompt)


class BackendAction(Action):
    """Implement backend code."""

    name: str = "BackendAction"

    async def run(self, context: str) -> str:
        prompt = (
            "You are a Backend Developer. Based on the architecture and database design, "
            "implement the backend code.\n\n"
            f"Context:\n{context}\n\n"
            "Output the backend implementation including: API endpoints, business logic, "
            "data access layer, and middleware configuration."
        )
        return await self._aask(prompt)


class ContainerAction(Action):
    """Create containerization and deployment configuration."""

    name: str = "ContainerAction"

    async def run(self, context: str) -> str:
        prompt = (
            "You are a Container/Platform Engineer. Based on the implementation details, "
            "create deployment configuration.\n\n"
            f"Context:\n{context}\n\n"
            "Output the deployment configuration including: Dockerfile, "
            "docker-compose setup, Kubernetes manifests if needed, "
            "and CI/CD pipeline configuration."
        )
        return await self._aask(prompt)


class WriteTestsAction(Action):
    """Write tests for the implemented code."""

    name: str = "WriteTestsAction"

    async def run(self, context: str) -> str:
        prompt = (
            "You are a Test Engineer. Based on the implementation below, "
            "write comprehensive tests.\n\n"
            f"Context:\n{context}\n\n"
            "Output tests including: unit tests, integration tests, "
            "test scenarios and edge cases."
        )
        return await self._aask(prompt)


class ReviewAction(Action):
    """Perform code review on the implementation."""

    name: str = "ReviewAction"

    async def run(self, context: str) -> str:
        prompt = (
            "You are a Code Reviewer. Review the following implementation for "
            "code quality, logic defects, and design issues.\n\n"
            f"Context:\n{context}\n\n"
            "Output the code review including: issues found (with line references), "
            "suggested improvements, and overall quality assessment."
        )
        return await self._aask(prompt)


class SecurityAction(Action):
    """Perform security audit on the codebase."""

    name: str = "SecurityAction"

    async def run(self, context: str) -> str:
        prompt = (
            "You are a Security Auditor. Perform a security audit on the following "
            "implementation.\n\n"
            f"Context:\n{context}\n\n"
            "Output the security audit including: vulnerability findings, "
            "OWASP Top 10 analysis, dependency risks, and remediation steps."
        )
        return await self._aask(prompt)