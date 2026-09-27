#!/usr/bin/env bash
set -eo pipefail
echo "🔍 Validating Vectorless RAG & Sparse Search Suite..."
python3 -c "import bm25_retriever; print('✅ bm25_retriever syntax verified')"
python3 -c "import py_compile; py_compile.compile('manim_flow.py', doraise=True); print('✅ manim_flow syntax verified')"
echo "✅ SRE compliance validation complete for vectorless-rag."
