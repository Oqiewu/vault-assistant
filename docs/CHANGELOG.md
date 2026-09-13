# Changelog

Одна строка на изменение. Контекст и обоснование — в `docs/decisions/`, не здесь.

- 2026-09-13 — Слой 0: обход vault, парсинг frontmatter, chunking (`chunk_vault.py`)
- 2026-09-13 — Слой 1: embeddings + поиск по cosine similarity (`embed.py`) — см. [0001](decisions/0001-local-embeddings.md), [0002](decisions/0002-chunking-window.md)
- 2026-09-13 — Fix: `parse_note` не падает на невалидном YAML — см. [0004](decisions/0004-yaml-error-handling.md)
- 2026-09-13 — Документация переведена на ADR-формат (`docs/decisions/` + `CHANGELOG.md` + `CLAUDE.md`)
- 2026-09-13 — Ollama поднята в Docker (`docker-compose.yml`), app остаётся нативно на хосте — см. [0005](decisions/0005-no-full-containerization.md)
- 2026-09-13 — Слой 2: RAG-пайплайн (`rag.py`), сборка промпта из найденных чанков + вызов Ollama
- 2026-09-13 — `clean_for_embedding()`: очистка markdown-синтаксиса перед embedding, известное ограничение с табличным контентом — см. [0006](decisions/0006-markdown-cleanup-for-embedding.md)
- 2026-09-13 — Убрано дублирование пайплайна (chunks/model/embeddings) между `embed.py` и `rag.py` — вынесено в `build_index()`
