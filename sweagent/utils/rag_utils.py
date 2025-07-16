import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Tuple
load_dotenv()
client = OpenAI()

# 全局缓存
_model = None
_index = None
_metadata = None

def retrieve_wcag_knowledge(
    issue_text: str,
    index_path: str = "sweagent/utils/WCAG/wcag_chunks.index",
    metadata_path: str = "sweagent/utils/WCAG/wcag_chunks_metadata.json",
    model_name: str = "text-embedding-3-small",
    top_k: int = 5,
) -> Tuple[str, str]:
    """返回两个输出：
    1. summary_text: 精炼的标题 + 一句话摘要（适合快速提示）
    2. explanation_text: 原始解释重组为结构化 markdown（不删减内容）
    """

    global _model, _index, _metadata

    if not issue_text.strip():
        raise ValueError("问题描述为空")

    # 加载向量数据和模型（首次调用）
    if _index is None:
        _index = faiss.read_index(index_path)
    if _metadata is None:
        with open(metadata_path, "r", encoding="utf-8") as f:
            _metadata = json.load(f)
    if _model is None:
        _model = model_name

    # 获取 embedding
    response = client.embeddings.create(model=model_name, input=[issue_text])
    query_embedding = np.array(response.data[0].embedding).astype("float32").reshape(1, -1)

    # 检索 top-k
    D, I = _index.search(query_embedding, top_k)
    retrieved_chunks = [_metadata[i] for i in I[0] if i < len(_metadata)]

    seen = set()
    summary_blocks: List[str] = []
    explanation_blocks: List[str] = []

    for chunk in retrieved_chunks:
        key = json.dumps(chunk, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)

        # 提取字段
        code = chunk.get("code", chunk.get("id", ""))
        sc_refs = chunk.get("referenced_by", chunk.get("sc_id", ""))
        description = chunk.get("text", "").strip()

        # 构造 summary header
        header = f"**[{code}]**"
        if isinstance(sc_refs, list):
            header += f" – Related SC: {', '.join(sc_refs)}"
        elif isinstance(sc_refs, str):
            header += f" – Related SC: {sc_refs}"

        # 精炼摘要（第一段+裁剪）
        summary_para = description.split("\n\n")[0].replace("\n", " ").strip()
        summary_line = summary_para[:277] + "..." if len(summary_para) > 280 else summary_para

        # 完整解释格式（保留换行和 markdown 块）
        explanation_block = f"{header}\n\n{description.strip()}"

        summary_blocks.append(f"{header}\n- {summary_line}")
        explanation_blocks.append(explanation_block)

    # 拼接输出
    summary_text = "### WCAG Summary\n\n" + "\n\n".join(summary_blocks)
    explanation_text = "### WCAG Detailed Explanation\n\n" + "\n\n---\n\n".join(explanation_blocks)

    return summary_text, explanation_text
