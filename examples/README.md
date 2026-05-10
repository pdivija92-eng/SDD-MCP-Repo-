# Examples - See SDD in Action Across 3 Domains

This folder shows the complete SDD workflow on three different types of Python projects. Each example includes:

- Spec written before implementation
- Plan with concrete tasks
- Implementation generated from the plan
- Unit and integration tests

Use these as templates for your own projects.

## Example 1: FastAPI JWT Authentication

**Type**: REST API authentication  
**Tech**: FastAPI, Pydantic, JWT  
**Status**: Implemented  
**Complexity**: Intermediate

What it demonstrates:

- API design with schemas and error handling
- Security thinking around token expiry, scopes, and RBAC
- Testing async dependencies
- Type hints and docstrings

## Example 2: Django User Model with Signals

**Type**: Database and ORM  
**Tech**: Django ORM, signals, Redis cache  
**Status**: Implemented  
**Complexity**: Intermediate

What it demonstrates:

- Database schema design
- ORM lifecycle hooks
- Cache invalidation patterns
- Transaction atomicity

## Example 3: PySpark Data Pipeline

**Type**: Data engineering and ETL  
**Tech**: PySpark, Pydantic, Delta-style storage  
**Status**: Implemented  
**Complexity**: Advanced

What it demonstrates:

- Data pipeline design
- Scale thinking for 1M+ row workloads
- Data quality patterns
- Idempotency and upsert semantics

## How to Use These Examples

```bash
# 1. Pick an example
cd examples/fastapi-auth-module

# 2. Read the spec
cat docs/specs/FEAT-001-jwt-auth.md

# 3. Read the plan
cat docs/specs/FEAT-001-plan.md

# 4. Review the implementation and tests
ls src/auth
ls tests
```

Each example follows the same flow:

1. Plain English requirement -> `/specify`
2. Refined spec -> `/clarify`
3. Structured plan -> `/plan`
4. Production code -> `/implement`
5. Spec-based review -> `/review`
6. Synced memory -> `/update`

## The Key Insight

SDD is not just for architecture documents or complex features. It works for practical Python work across APIs, databases, data pipelines, CLI tools, background task processing, and ML workflows.

Want to contribute? PRs welcome.
