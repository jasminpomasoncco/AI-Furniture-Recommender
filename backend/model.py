from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sentence_transformers import SentenceTransformer

from backend.data import PRODUCTOS


@dataclass(slots=True)
class RecommendationResult:
    categoria: str
    producto: str
    descripcion: str
    medidas: str
    especificaciones_tecnicas: str
    precios: str
    score: float
    producto_index: int


class ProductRecommender:
    def __init__(self, products: list[dict[str, str]], model_name: str = "all-MiniLM-L6-v2") -> None:
        self.products = products
        self.model = SentenceTransformer(model_name)
        self.product_embeddings = self._build_embeddings()

    def _construir_texto_producto(self, product: dict[str, str]) -> str:
        partes = [
            product.get("categoria", ""),
            product.get("nombre", ""),
            product.get("descripcion", ""),
            product.get("medidas", ""),
            product.get("especificaciones_tecnicas", ""),
            product.get("precios", ""),
        ]
        return " | ".join(parte.strip() for parte in partes if parte and parte.strip())

    def _build_embeddings(self) -> np.ndarray:
        descriptions = [self._construir_texto_producto(item) for item in self.products]
        embeddings = self.model.encode(
            descriptions,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return np.asarray(embeddings, dtype=np.float32)

    def recommend(self, query: str) -> RecommendationResult:
        query_embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        similarities = np.dot(self.product_embeddings, query_embedding)
        best_index = int(np.argmax(similarities))
        best_score = float(similarities[best_index])
        best_product = self.products[best_index]

        return RecommendationResult(
            categoria=best_product.get("categoria", ""),
            producto=best_product["nombre"],
            descripcion=best_product["descripcion"],
            medidas=best_product.get("medidas", ""),
            especificaciones_tecnicas=best_product.get("especificaciones_tecnicas", ""),
            precios=best_product.get("precios", ""),
            score=round(best_score, 4),
            producto_index=best_index,
        )


recommender = ProductRecommender(PRODUCTOS)
