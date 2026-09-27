#!/usr/bin/env python3
"""
Vectorless RAG Sparse Query Retrieval Engine
High-precision BM25 Lexical Matching with Term Frequency Saturation
"""
import math
import re
from typing import List, Tuple

STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'if', 'then', 'else', 
    'to', 'for', 'in', 'on', 'at', 'by', 'from', 'with', 'of'
}

def tokenize(text: str) -> List[str]:
    words = re.findall(r'\w+', text.lower())
    return [w for w in words if w not in STOP_WORDS]

class BM25Retriever:
    def __init__(self, corpus: List[str], k1: float = 1.5, b: float = 0.75):
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.doc_len = [len(tokenize(doc)) for doc in corpus]
        self.avg_doc_len = sum(self.doc_len) / len(corpus) if corpus else 0
        
    def score_query(self, query: str) -> List[Tuple[str, float]]:
        q_tokens = tokenize(query)
        scores = []
        for idx, doc in enumerate(self.corpus):
            d_tokens = tokenize(doc)
            score = 0.0
            for term in q_tokens:
                tf = d_tokens.count(term)
                if tf > 0:
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * (self.doc_len[idx] / self.avg_doc_len))
                    score += (numerator / denominator)
            scores.append((doc, round(score, 4)))
        return sorted(scores, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    docs = [
        "Kubernetes pods entering CrashLoopBackOff due to missing ConfigMap environment variables.",
        "PostgreSQL connection timeout when scaling active backend queries beyond 500 connections.",
        "Redis cluster shard failure triggered failover to replica in us-east-1a."
    ]
    retriever = BM25Retriever(docs)
    results = retriever.score_query("Kubernetes CrashLoopBackOff missing config")
    for doc, score in results:
        print(f"[{score}] {doc}")
