import io
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
from sentence_transformers import SentenceTransformer

from chunk_vault import chunk_text, clean_for_embedding, find_markdown_files, parse_note

cast(io.TextIOWrapper, sys.stdout).reconfigure(encoding="utf-8")


@dataclass
class Chunk:
    text: str
    file_path: Path
    metadata: dict


def build_chunks(vault_path: str) -> list[Chunk]:
    chunks = []
    for file_path in find_markdown_files(vault_path):
        metadata, body = parse_note(file_path)
        for piece in chunk_text(body):
            if piece.strip():
                chunks.append(Chunk(text=piece, file_path=file_path, metadata=metadata))
    return chunks


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    dot_product = np.dot(a, b)
    a_length = np.linalg.norm(a)
    b_length = np.linalg.norm(b)

    return dot_product / (a_length * b_length)


def search(
    query: str,
    model: SentenceTransformer,
    chunks: list[Chunk],
    embeddings: np.ndarray,
    top_n: int = 5,
) -> list[tuple[float, Chunk]]:
    query_embedding = model.encode(query)
    scores = []

    for chunk, chunk_embedding in zip(chunks, embeddings):
        score = cosine_similarity(query_embedding, chunk_embedding)
        scores.append((score, chunk))

    scores.sort(key=lambda pair: pair[0], reverse=True)
    return scores[:top_n]


def build_index(vault_path: str) -> tuple[list[Chunk], SentenceTransformer, np.ndarray]:
    chunks = build_chunks(vault_path)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [clean_for_embedding(c.text) for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    return chunks, model, embeddings


if __name__ == "__main__":
    vault_path = r"C:\Users\Игорь\Documents\Personal"

    print("Строим индекс (обход vault, chunking, embeddings)...")
    chunks, model, embeddings = build_index(vault_path)
    print(f"Всего чанков: {len(chunks)}")

    query = "на чём я остановился в изучении Go?"
    print(f"\nЗапрос: {query}")
    results = search(query, model, chunks, embeddings, top_n=5)
    for score, chunk in results:
        print(f"\n[{score:.3f}] {chunk.file_path.name}")
        print(chunk.text[:150], "...")
