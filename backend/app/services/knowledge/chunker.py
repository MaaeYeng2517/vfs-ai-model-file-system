"""Text chunking for knowledge engine."""
import re

def chunk_text(text: str, size: int = 500, overlap: int = 50):
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + size]))
        i += size - overlap
    return chunks

def extract_text(data: bytes, mime: str) -> str:
    try:
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""
