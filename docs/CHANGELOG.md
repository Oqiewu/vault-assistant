# Changelog

Одна строка на изменение. Контекст и обоснование — в `docs/decisions/`, не здесь.

- 2026-09-13 — Слой 0: обход vault, парсинг frontmatter, chunking (`chunk_vault.py`)
- 2026-09-13 — Слой 1: embeddings + поиск по cosine similarity (`embed.py`) — см. [0001](decisions/0001-local-embeddings.md), [0002](decisions/0002-chunking-window.md)
- 2026-09-13 — Fix: `parse_note` не падает на невалидном YAML — см. [0004](decisions/0004-yaml-error-handling.md)
- 2026-09-13 — Документация переведена на ADR-формат (`docs/decisions/` + `CHANGELOG.md` + `CLAUDE.md`)
