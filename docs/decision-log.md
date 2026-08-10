# Technical Decision Log

## Decision 001

Date:

2026-08

Topic:

Database migration

Decision:

Use Alembic

Reason:

Database schema changes need version control.

Alternative:

Manually edit database.

Rejected because:

Hard to reproduce in different environments.

---

## Decision 002

Topic:

Authentication

Decision:

Use JWT.

Reason:

Suitable for REST API and learning security concepts.

Alternative:

Session authentication.

Rejected because:

More suitable for traditional web applications.
