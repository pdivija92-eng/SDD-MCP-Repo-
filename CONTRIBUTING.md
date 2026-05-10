# Adopting SDD in Your Organization

This guide is for engineering leads, platform teams, and contributors who want to roll out Spec-Driven Development across one or more repositories.

## Why Teams Adopt SDD

- **Onboarding**: new contributors read specs instead of reverse-engineering code
- **AI-assisted development**: assistants generate better code when requirements are available as context
- **Knowledge retention**: decisions stay in version-controlled spec files
- **Review quality**: PRs reference spec IDs so reviewers can map changes to requirements

## Rollout Options

### Option 1 - Single Project Pilot

Best for trying SDD on one project before wider adoption.

```bash
python sdd-init.py /projects/new-service --name "New Service"
```

Team rule: before a new feature branch, create or update the related spec.

### Option 2 - Team Adoption

Best for a single team maintaining several Python repositories.

1. Run `sdd-init` on active repos.
2. Add SDD checks to the PR template.
3. Use `/review` before merging meaningful changes.
4. Run `/specify` retrospectively on the most important existing features.

Suggested PR checklist:

```markdown
- [ ] Spec exists in `docs/specs/`
- [ ] Spec status is ready for implementation
- [ ] `/review` report exists in `reviews/`
- [ ] AI memory updated via `/update`
```

### Option 3 - Organization Rollout

Best for platform teams rolling SDD out across multiple engineering teams.

1. Fork this toolkit into your organization.
2. Customize `.github/sdd/` with your stack conventions.
3. Add `sdd-init.py` to internal project scaffolding.
4. Use `reviews/` artifacts as part of engineering review history.

## Customizing for Your Stack

Edit `.github/sdd/implement.md` to add stack-specific implementation rules:

```markdown
## Stack conventions
- Use SQLAlchemy ORM, not raw database drivers
- API endpoints must have request and response models
- Use structured logging
- Prefer PySpark DataFrames for large data workloads
```

Edit `.github/sdd/review.md` to add review expectations:

```markdown
## Review requirements
- Confirm every acceptance criterion has a test or clear manual validation
- Flag security, reliability, and data quality risks
- Store the report in `reviews/`
```

## FAQ

**Do we need a specific AI tool?**  
No. Specs are plain Markdown. The command files are reusable instructions.

**What if our existing codebase has no specs?**  
Start with the most important modules. You do not need to spec everything on day one.

**How does this work with Jira, Linear, or GitHub Issues?**  
Use tickets for business tracking and SDD specs for technical contracts, acceptance criteria, and implementation plans.

**Who owns the specs?**  
The person implementing the change owns the spec. The reviewer checks that code, tests, and docs match it.
