#!/usr/bin/env python3
"""
Memory Skill - RAG Search

本地向量检索，无需外部 API。
支持语义搜索记忆文件。

用法:
    python rag_search.py search "用户偏好"     # 搜索记忆
    python rag_search.py add "文件名" "内容"   # 添加记忆
    python rag_search.py init                  # 初始化索引
"""

import sys
import os
import hashlib
import json
from pathlib import Path

# 本地 ChromaDB
try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    print("错误：chromadb 未安装，运行 pip install -r requirements.txt")
    sys.exit(1)

# 本地 Embedding 模型
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("错误：sentence-transformers 未安装，运行 pip install -r requirements.txt")
    sys.exit(1)


class MemoryRAG:
    """记忆向量检索"""
    
    def __init__(self, workspace_root: str):
        self.workspace = Path(workspace_root)
        self.memory_dir = self.workspace / "memory"
        self.chroma_dir = self.memory_dir / "chroma"
        self.palace_dir = self.memory_dir / "palace"
        self.index_db = self.memory_dir / "index.json"
        
        # 确保目录存在
        self.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.palace_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化 ChromaDB（本地持久化）
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(self.chroma_dir),
            anonymized_telemetry=False
        ))
        
        # 获取或创建集合
        self.collection = self.client.get_or_create_collection(
            name="memory",
            metadata={"hnsw:space": "cosine"}  # 余弦相似度
        )
        
        # 初始化 Embedding 模型（本地）
        self.embed_model = None
    
    def _get_embed_model(self):
        """懒加载 embedding 模型"""
        if self.embed_model is None:
            # 使用小型中文模型
            self.embed_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        return self.embed_model
    
    def _embed(self, text: str) -> list:
        """生成向量"""
        model = self._get_embed_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def _file_hash(self, content: str) -> str:
        """文件内容哈希"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def init_index(self):
        """从现有记忆文件初始化索引"""
        print(f"初始化记忆索引...")
        
        # 加载现有索引
        existing_ids = set()
        if self.index_db.exists():
            with open(self.index_db) as f:
                index = json.load(f)
                existing_ids = set(index.keys())
        
        # 扫描 palace 目录
        indexed = 0
        new_files = []
        
        for md_file in self.palace_dir.glob("*.md"):
            content = md_file.read_text()
            file_hash = self._file_hash(content)
            file_id = f"{md_file.stem}:{file_hash}"
            
            if file_id not in existing_ids:
                new_files.append((md_file, content, file_id))
        
        # 批量添加新文件
        if new_files:
            documents = []
            metadatas = []
            ids = []
            
            for md_file, content, file_id in new_files:
                documents.append(content)
                metadatas.append({
                    "filename": md_file.name,
                    "filepath": str(md_file),
                    "hash": file_hash
                })
                ids.append(file_id)
            
            # 批量添加（带 embedding）
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            indexed = len(new_files)
            print(f"  新增 {indexed} 个记忆文件")
        
        # 保存索引
        index = {}
        for doc in self.collection.get()["metadatas"]:
            file_id = f"{Path(doc['filename']).stem}:{doc['hash']}"
            index[file_id] = doc
        
        with open(self.index_db, "w") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        print(f"索引完成，共 {len(index)} 个记忆文件")
        return len(index)
    
    def search(self, query: str, top_k: int = 3) -> list:
        """语义搜索记忆"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        # 解析结果
        memories = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                memory = {
                    "content": doc,
                    "filename": results["metadatas"][0][i]["filename"],
                    "filepath": results["metadatas"][0][i]["filepath"],
                    "distance": results["distances"][0][i]
                }
                memories.append(memory)
        
        return memories
    
    def add_memory(self, filename: str, content: str):
        """添加/更新单个记忆"""
        file_hash = self._file_hash(content)
        file_id = f"{Path(filename).stem}:{file_hash}"
        
        # 检查是否已存在
        existing = self.collection.get(ids=[file_id])
        if existing["ids"]:
            # 更新
            self.collection.update(
                ids=[file_id],
                documents=[content],
                metadatas=[{
                    "filename": filename,
                    "filepath": str(self.palace_dir / filename),
                    "hash": file_hash
                }]
            )
            print(f"更新记忆：{filename}")
        else:
            # 新增
            self.collection.add(
                documents=[content],
                metadatas=[{
                    "filename": filename,
                    "filepath": str(self.palace_dir / filename),
                    "hash": file_hash
                }],
                ids=[file_id]
            )
            print(f"添加记忆：{filename}")
        
        # 更新索引文件
        self.init_index()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    workspace = os.environ.get("WORKSPACE_ROOT", "/Users/narwal/.openclaw/workspace")
    rag = MemoryRAG(workspace)
    
    cmd = sys.argv[1]
    
    if cmd == "init":
        rag.init_index()
    
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("用法：python rag_search.py search <查询词>")
            sys.exit(1)
        query = sys.argv[2]
        results = rag.search(query)
        
        print(f"\n搜索结果：{query}\n")
        for i, mem in enumerate(results, 1):
            print(f"[{i}] {mem['filename']} (相似度：{1 - mem['distance']:.2%})")
            print(f"    {mem['content'][:200]}...")
            print()
    
    elif cmd == "add":
        if len(sys.argv) < 4:
            print("用法：python rag_search.py add <文件名> <内容>")
            sys.exit(1)
        filename = sys.argv[2]
        content = sys.argv[3]
        rag.add_memory(filename, content)
    
    else:
        print(f"未知命令：{cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
