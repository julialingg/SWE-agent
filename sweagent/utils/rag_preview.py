import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path
import argparse
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

def retrieve_wcag_knowledge_from_file(
    input_path: str,
    output_path: str,
    index_path: str = "sweagent/utils/WCAG/wcag_chunks.index",
    metadata_path: str = "sweagent/utils/WCAG/wcag_chunks_metadata.json",
    model_name: str = "text-embedding-3-small",
    top_k: int = 5,
):
 
    
    # Step 1: 读取问题文本
    issue_text = Path(input_path).read_text(encoding="utf-8").strip()
    if not issue_text:
        raise ValueError("输入文件为空，请确认文件内容为问题描述文本。")

    # Step 2: 初始化模型和索引
    print("📦 加载向量模型与索引中...")
    index = faiss.read_index(index_path)
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Step 3: 用 OpenAI embedding API 检索 top-k
    print("🔍 检索中...")
    response = client.embeddings.create(
        model=model_name,
        input=[issue_text]
    )
    query_embedding = np.array(response.data[0].embedding).astype("float32").reshape(1, -1)
    print(f"模型 embedding 维度: {query_embedding.shape}")
    print(f"FAISS 索引维度: {index.d}")
    D, I = index.search(query_embedding, top_k)
    retrieved_chunks = [metadata[i] for i in I[0] if i < len(metadata)]

    # Step 4: 格式化输出（dict 去重）
    seen = set()
    unique_chunks = []
    for chunk in retrieved_chunks:
        key = json.dumps(chunk, sort_keys=True)
        if key not in seen:
            unique_chunks.append(chunk)
            seen.add(key)
    joined_text = "\n\n".join(f"- {str(chunk).strip()}" for chunk in unique_chunks)
    Path(output_path).write_text(joined_text, encoding="utf-8")

    print(f"✅ 检索完成，结果已保存到：{output_path}")

if __name__ == "__main__":
    input_path = "sweagent/utils/problem.txt"
    output_path = "sweagent/utils/rag_output.txt"
    top_k = 5

    retrieve_wcag_knowledge_from_file(
        input_path=input_path,
        output_path=output_path,
        top_k=top_k,
    )
