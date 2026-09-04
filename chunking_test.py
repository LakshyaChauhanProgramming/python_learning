from typing import List
import re


class ContextBuilder:
    """
    Used in a RAG pipeline for two jobs:

    1. Splitting a long document into overlapping word-chunks BEFORE embedding
       (so embeddings represent small, meaningful pieces of text instead of a
       whole document).
    2. Given a set of candidate chunks with relevance scores, selecting as many
       of the most relevant ones as possible into a final prompt context,
       WITHOUT exceeding a maximum token budget (simulating a limited LLM
       context window).
    """

    def __init__(self, chunk_size: int = 20, overlap: int = 5):
        """
        chunk_size: number of words per chunk
        overlap: number of words shared between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def _count_tokens(self, text: str) -> int:
        return len(self._tokenize(text))


    def chunk_text(self, text: str) -> List[str]:
        words = self._tokenize(text)
        if not words:
            return []

        # Guard against overlap >= chunk_size, which would make the window
        # never advance (or go backwards). Fall back to a non-overlapping step.
        step = self.chunk_size - self.overlap
        if step <= 0:
            step = self.chunk_size

        # Text shorter than (or equal to) chunk_size -> single chunk.
        if len(words) <= self.chunk_size:
            return [" ".join(words)]

        chunks = []
        start = 0
        n = len(words)
        while start < n:
            end = start + self.chunk_size
            chunks.append(" ".join(words[start:end]))
            if end >= n:
                break
            start += step

        return chunks

    def select_within_budget(
        self, chunks: List[str], scores: List[float], token_budget: int
    ) -> List[str]:
        if not chunks:
            return []

        ranked_indices = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)

        running_total = 0
        selected_indices = []

        for idx in ranked_indices:
            token_count = self._count_tokens(chunks[idx])
            if running_total + token_count <= token_budget:
                selected_indices.append(idx)
                running_total += token_count
            # else: skip, don't break — a later, smaller chunk might still fit

        selected_indices.sort()
        return [chunks[i] for i in selected_indices]
    

if __name__ == "__main__":
    cb = ContextBuilder(chunk_size=10, overlap=3)

    sample_text = (
        "Retrieval augmented generation combines a retriever and a generator. "
        "The retriever finds relevant documents from a corpus using embeddings. "
        "The generator then uses those documents as context to produce an answer. "
        "This approach reduces hallucination compared to a plain language model."
    )

    print("--- chunk_text() test ---")
    chunks = cb.chunk_text(sample_text)
    # print(chunks)
    for i, c in enumerate(chunks):
        print(i, "->", c)

    print("\n--- select_within_budget() test ---")
    scores = [0.9, 0.2, 0.6, 0.4]
    # NOTE: only meaningful once chunk_text() produces >=4 chunks; adjust as needed
    if len(chunks) >= 4:
        selected = cb.select_within_budget(chunks[:4], scores, token_budget=15)
        print(selected)
