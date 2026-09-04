from typing import List
import numpy as np
import re


class RAGApplication:
    def __init__(self):
        """
        Initialize your vector store and any other required components here.

        Hint:
        - You can store documents and their embeddings in lists.
        """
        self.documents: List[str] = []
        self.embeddings: List[np.ndarray] = []

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def _build_vocab(self, texts: List[str]):
        words = set()
        for text in texts:
            words.update(self._tokenize(text))
        self.vocab = {word: i for i, word in enumerate(sorted(words))}

    def _embed(self, text: str) -> np.ndarray:
        vec = np.zeros(len(self.vocab))
        for word in self._tokenize(text):
            if word in self.vocab:
                vec[self.vocab[word]] += 1
        return vec

    def add_documents(self, documents: List[str]) -> None:
        self.documents.extend(documents)
        self._build_vocab(self.documents)
        self.embeddings = [self._embed(doc) for doc in self.documents]

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        
    def retrieve(self, question: str, k: int = 3) -> List[str]:
        """
        Accepts a question string and an integer k, and returns the
        top-k most relevant document chunks from the vector store.

        Hint:
        - Convert the question into an embedding
        - Compute similarity between question and stored embeddings
        - You may use cosine similarity
        - Return the top-k matching documents
        """
        query_vec = self._embed(question)
        scores = []

        # scores = [self._cosine_similarity(query_vec, doc_vec) for doc_vec in self.embeddings]
        # or

        for i in range(len(self.embeddings)):
            scores.append(self._cosine_similarity(query_vec, self.embeddings[i]))

        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        return [self.documents[i] for i in ranked_indices[:k]]


    def query(self, question: str) -> str:
        """
        Accepts a question string and returns an answer string generated
        by querying the vector store and passing the retrieved context
        to an LLM.

        Hint:
        - Use `retrieve` to get relevant documents
        - Combine them into a single string as context
        - You can return a simple formatted answer (no real LLM needed)
        """
        
        return ' '.join(self.retrieve(question=question, k=2))


if __name__ == "__main__":
    rag = RAGApplication()

    # print(re.findall(r"\w+", "The Eiffel Tower is located in Paris, France.".lower()));

    rag.add_documents([
        "The Eiffel Tower is located in Paris, France.",
        "Python is a popular programming language for data science."
    ])

    # rag.add_documents([
    #     "The Eiffel Tower is located in Paris, France.",
    #     "Python is a popular programming language for data science."
    # ])

    rag.add_documents([
        "The Eiffel Tower is located in Paris, France.",
        "Python is a popular programming language for data science.",
        "The Great Wall of China is thousands of kilometers long.",
        "Numpy is used for numerical computations in Python.",
        "Paris is the capital city of France.",
    ])

    print("--- retrieve() test ---")
    print("Where is the Eiffel Tower?")
    results = rag.query("Where is the Eiffel Tower?")
    print(results)

    # print("\n--- edge case: k larger than number of docs ---")
    # print(rag.retrieve("Tell me about France", k=100))

    # print("\n--- edge case: empty document store ---")
    # empty_rag = RAGApplication()
    # print(empty_rag.retrieve("anything?", k=3))

    # print("\n--- query() test ---")
    # print(rag.query("What programming language is good for data science?"))