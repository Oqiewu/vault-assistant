import io
import sys
from pathlib import Path
from typing import cast

import yaml

cast(io.TextIOWrapper, sys.stdout).reconfigure(encoding="utf-8")


def find_markdown_files(vault_path: str) -> list[Path]:
    return list(Path(vault_path).rglob("*.md"))


def parse_note(file_path: Path) -> tuple[dict, str]:
    text = file_path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    _, frontmatter_raw, body = parts
    try:
        metadata = yaml.safe_load(frontmatter_raw) or {}
    except yaml.YAMLError:
        metadata = {}
    return metadata, body.strip()


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100) -> list[str]:
    if len(text) <= chunk_size:
        return [text] if text else []

    step = chunk_size - overlap
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += step
    return chunks


if __name__ == "__main__":
    vault_path = r"C:\Users\Игорь\Documents\Personal"
    files = find_markdown_files(vault_path)
    print(f"Найдено файлов: {len(files)}")

    sample = files[0]
    metadata, body = parse_note(sample)
    print(f"\nПример: {sample}")
    print(f"Metadata: {metadata}")
    print(f"Длина тела: {len(body)} символов")

    chunks = chunk_text(body)
    print(f"Получилось чанков: {len(chunks)}")
    for i, c in enumerate(chunks):
        print(f"\n--- Чанк {i} (длина {len(c)}) ---")
        print(c[:120], "...")
