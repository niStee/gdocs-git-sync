# AGENTS.md — gdocs-git-sync

> Parent: [~/AGENTS.md](../../AGENTS.md) — environment-wide context

## What is gdocs-git-sync
Bi-directional synchronization between Google Docs and Git Markdown

## Commands
```bash
# Run tests
python3 -m unittest discover tests -v

# Lint with ruff
ruff check . --fix
```

## Standards
- Conventional Commits (`feat:`, `fix:`, `docs:`, `ci:`, `test:`)
- Test-Driven Infrastructure (TDI) & KISS
- OpenSSF Scorecard & Gitleaks compliant

## Repository topology
- canonical: GitHub (niStee/gdocs-git-sync) — all changes land via PR to main
- mirror: Codeberg (codeberg.org/niStee/gdocs-git-sync) — automated push mirror via
  .github/workflows/mirror-codeberg.yml; receives main + tags only
- never push directly to main; never push to Codeberg directly
- tags are immutable once pushed; never rewrite or delete a mirrored tag
- mirror repair path: re-run the workflow (workflow_dispatch), not local
  pushes
- operations runbook: niStee/network-infra → codeberg-github-migration.md
