from typing import List
import requests
import numpy as np
from numpy import ndarray
from sentence_transformers import SentenceTransformer
from semantic_kernel.connectors.ai.embeddings.embedding_generator_base import EmbeddingGeneratorBase
from requests import Session
from aiohttp import ClientSession
import json
from weathon.utils.logger import get_logger
from weathon.crawler.utils.header import embedding_header

logger = get_logger()


class EmbeddingGenerator(EmbeddingGeneratorBase):
    model_size = {
        "base": ["BAAI/bge-base-zh-v1.5", "moka-ai/m3e-base"]
    }

    def __init__(self, model_name_or_path: str = 'BAAI/bge-base-zh-v1.5', device="cpu", normalize_embeddings=False,
                 use_local=False) -> None:
        self.embedding_url = "https://hf.omycloud.site/embeddings/" + model_name_or_path
        self.session = Session()
        self.normalize_embeddings = normalize_embeddings
        self.use_local = use_local
        if use_local:
            self._load_local_model(model_name_or_path, device)

    def models(self, size='base'):
        return self.model_size[size]

    def _load_local_model(self, model_name_or_path, device):
        self.model = SentenceTransformer(model_name_or_path=model_name_or_path, device=device)

    async def generate_embeddings_async(self, texts: List[str]) -> ndarray:
        if self.use_local:
            return self.model.encode(sentences=texts, normalize_embeddings=self.normalize_embeddings)
        async with ClientSession() as aiosession:
            async with aiosession.post(url=self.embedding_url, data=json.dumps({"inputs": texts}),
                                       headers=embedding_header) as response:
                if not response.ok:
                    return self.model.encode(sentences=texts, normalize_embeddings=self.normalize_embeddings)
                result = await response.json()
                data = result.get("data", [])
                embeddings = [d["embedding"] for d in data]
                return np.array(embeddings)

    def generate_embeddings(self, texts: List[str]) -> ndarray:
        if self.use_local:
            return self.model.encode(sentences=texts, normalize_embeddings=self.normalize_embeddings)
        response = requests.post(url=self.embedding_url, data=json.dumps({"inputs": texts}), headers=embedding_header)
        if not response.ok:
            return self.model.encode(sentences=texts, normalize_embeddings=self.normalize_embeddings)
        data = response.json().get("data", [])
        embeddings = [d["embedding"] for d in data]
        return np.array(embeddings)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.aiosession.close()
