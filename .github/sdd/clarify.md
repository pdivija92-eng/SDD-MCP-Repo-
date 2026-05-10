# /clarify

**Usage**: `/clarify [FEAT-XXX]`

Refine an existing spec by resolving ambiguity before planning or implementation.

## Instructions for the assistant

1. Read the specified spec from `docs/specs/`, or use the currently open spec if no ID is provided.
2. Identify unclear requirements, missing constraints, untestable acceptance criteria, and unresolved design decisions.
3. Ask focused questions. Prefer one short batch of the highest-impact questions.
4. Update the spec with the user's answers.
5. Confirm whether the spec is ready for `/plan`.

## Good clarification targets

- Inputs, outputs, and boundaries
- Error handling
- Performance or scale constraints
- Security and privacy requirements
- Acceptance criteria that can become tests
- Non-goals that prevent scope creep
