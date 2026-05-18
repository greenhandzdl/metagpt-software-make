# MetaGPT Software Factory

A multi-agent software development simulation powered by MetaGPT. Eight AI agents collaborate sequentially to design, build, and review a full-stack web application, with each agent committing artifacts to its own git branch.

## Architecture

```
User Requirement
    ↓
┌──────────────────────────────────────────────────┐
│  1. Architect           → architecture design     │
│  2. Database Engineer   → schema & migrations     │
│  3. Frontend Developer  → Vue 3 UI                │
│  4. Backend Developer   → Spring Boot API         │
│  5. Container Engineer  → Docker / K8s config     │
│  6. Test Engineer       → unit & integration tests│
│  7. Code Reviewer       → code quality review     │
│  8. Security Auditor    → security audit          │
└──────────────────────────────────────────────────┘
    ↓ (4 iterative rounds)
Merged to main
```

Each role gets a dedicated git branch in `proj/` (a separate git repo). The runner iterates 4 rounds — each round feeds the previous role's output into the next, refining the project incrementally.

## Agents

| Role | Profile | Branch |
|------|---------|--------|
| Alice | Architect | `arch/architecture-design` |
| Dave | Database Engineer | `db/schema-design` |
| Eve | Frontend Developer | `fe/vue-frontend` |
| Bob | Backend Developer | `be/springboot-backend` |
| Charlie | Container Engineer | `ops/container-config` |
| Frank | Test Engineer | `test/tests` |
| Grace | Code Reviewer | `review/code-review` |
| Heidi | Security Auditor | `security/audit` |

## Setup

```bash
# 1. Create virtual environment
uv venv -p 3.11
source .venv/bin/activate

# 2. Install dependencies
uv pip install metagpt==0.6.3
uv pip install httpx==0.27.4  # downgrade for metagpt compatibility

# 3. Configure LLM
cp config/key.yaml.example config/key.yaml
# Edit config/key.yaml with your API key and endpoint
```

## Configuration

LLM settings are read from `config/key.yaml` (not tracked by git) and `.env`:

```yaml
llm_provider: "openai"
openai_base_url: "http://localhost:13000/v1"
openai_api_key: "sk-..."
openai_api_model: "deepseek-ai/deepseek-v4-flash"
timeout: 180
```

## Usage

```bash
# Sequential runner (8 agents, 4 rounds)
uv run python -m meta.runner "Build an MVC app with Vue 3 and Spring Boot"

# Team-based parallel runner
uv run python app.py

# Run tests
uv run pytest tests/
```

The runner creates `proj/` as a git repo with role-specific branches and merges everything to `main`.

## Project Structure

```
├── AGENTS/              # Agent workflow docs
│   ├── plan.md         # Current progress
│   ├── conflict.md     # Conflict resolution priorities
│   └── experience.md   # Known solutions
├── meta/                # Agent implementations
│   ├── actions/        # 8 action classes (one per role)
│   ├── roles/          # 8 role classes
│   ├── runner.py       # Sequential pipeline runner
│   └── team.py         # Team assembly
├── config/              # LLM configuration
├── proj/                # Generated project (separate git repo)
└── tests/               # Test suite (21 tests)
```

## Testing

```bash
# All tests
uv run pytest tests/

# Single test
uv run pytest tests/test_software_factory.py::test_architecture_action -v
```