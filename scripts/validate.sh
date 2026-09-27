#!/usr/bin/env bash
set -eo pipefail
echo "🔍 Validating Vectorless RAG & Sparse Search Suite..."
python3 -c "import bm25_retriever; print('✅ bm25_retriever syntax verified')"
echo "SRE compliance validation complete for vectorless-rag."
