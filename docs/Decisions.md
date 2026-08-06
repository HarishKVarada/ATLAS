# ATLAS Project Decisions

This file records important project decisions.

---

## Decision 001 — Use Git and GitHub

**Status:** Approved

**Decision:**  
ATLAS will use Git for local version control and GitHub for remote repository
management.

**Reason:**  
This provides change history, rollback capability, collaboration support,
branching, and backup of project source files.

---

## Decision 002 — Protect the Main Branch

**Status:** Approved

**Decision:**  
The `main` branch represents the stable project state.

Development work should be performed in separate branches before being merged
into `main`.

---

## Decision 003 — Use a Day 0 Setup Branch

**Status:** Approved

**Decision:**  
The initial project foundation will be prepared in the `Day0` branch.

**Reason:**  
This keeps setup changes separate from the stable `main` branch until they are
reviewed.

---

## Decision 004 — No Trading Logic During Day 0

**Status:** Approved

**Decision:**  
No strategy, indicator, API, broker, or live-trading code will be created during
Day 0.

**Reason:**  
The repository structure, documentation, infrastructure, and project rules must
be established first.