import io
import sys
from typing import cast

import requests

from embed import Chunk, build_index, search

cast(io.TextIOWrapper, sys.stdout).reconfigure(encoding="utf-8")

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"


def build_prompt(query: str, chunks: list[Chunk]) -> str:
    instruction = "[инструкция: отвечай только на основе контекста, если ответа нет — скажи, что не знаешь]"
    context = ""
    for chunk in chunks:
        context += f"{chunk.text}\n(источник: {chunk.file_path.name})\n\n"

    return f"""{instruction}

    Контекст:
    {context}

    Вопрос: {query}"""


def ask_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
    )
    response.raise_for_status()
    return response.json()["response"]


if __name__ == "__main__":
    vault_path = r"C:\Users\Игорь\Documents\Personal"

    print("Строим индекс (обход vault, chunking, embeddings)...")
    chunks, model, embeddings = build_index(vault_path)

    query = "на чём я остановился в изучении Go?"
    print(f"\nЗапрос: {query}")

    results = search(query, model, chunks, embeddings, top_n=5)
    top_chunks = [chunk for _, chunk in results]

    prompt = build_prompt(query, top_chunks)
    print("\n--- Промпт ---")
    print(prompt)

    print("\n--- Ответ Ollama ---")
    answer = ask_ollama(prompt)
    print(answer)
