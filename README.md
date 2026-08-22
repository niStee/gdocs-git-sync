# gdocs-git-sync

> **Bi-directional synchronization between Google Docs and Git Markdown (Docs-as-Code).**

`gdocs-git-sync` bridges the gap between collaborative non-technical authoring surfaces (Google Docs) and technical version control (Git). It allows working groups to deliberate and comment in real-time on Google Docs while keeping a clean, audited, and automated Single Source of Truth (SSOT) in Git.

---

## Features

- 🔄 **Two-Way Sync:** Pull Google Docs headings, paragraphs, bullet lists, formatting, and links into clean Git-flavored Markdown.
- ⚡ **Zero-Drift Status:** Check timestamps, modified dates, and drift status across all mapped documents in seconds (`status`).
- 🔍 **Unified Diffs:** View exact text differences before overwriting local files (`diff`).
- 🛡️ **KISS & Test-Driven (TDD):** Ultra-fast (<0.01s test suite), pure Python + PyYAML + Requests, zero unnecessary heavyweight dependencies.
- 🔑 **Automated Authentication:** Seamlessly integrates with Google Workspace OAuth tokens (`~/.google-mcp/` or `GOOGLE_ACCESS_TOKEN`).

---

## Installation

```bash
git clone https://github.com/niStee/gdocs-git-sync.git
cd gdocs-git-sync
pip install -e .
```

---

## Configuration (`docs-sync.yaml`)

Define your mapping between local Git files and Google Doc IDs:

```yaml
documents:
  - file: "motions/foss-sustainability-motion.md"
    doc_id: "1HkhevBBy-TXIHW9qER6O-MAjqvveQygmYKnAoSsUHKs"
    title: "Volt FOSS Sustainability Policy"

  - file: "policy/digitales/01-infrastruktur.md"
    doc_id: "1wZ-igWfzspb3FzhmrSuXxFPvXrF7CUsB5IbQ15JHCSQ"
    title: "Digitale Infrastruktur als Daseinsvorsorge"
```

---

## CLI Usage

```bash
# 1. Check sync status & timestamps
gdocs-sync status

# 2. View unified diff between Git and Google Docs
gdocs-sync diff

# 3. Pull latest remote changes into local Markdown files
gdocs-sync pull
```

---

## Running Tests

```bash
python3 -m unittest discover tests -v
```

---

## License

MIT License · Built with 💜 for digital commons and Docs-as-Code workflows.
