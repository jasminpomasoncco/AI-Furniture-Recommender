from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field

from backend.model import recommender


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

app = FastAPI(
    title="Product Recommender API",
    version="1.0.0",
    description="API local para recomendar productos con embeddings y generar respuesta con OpenAI.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class RecommendationRequest(BaseModel):
    consulta: str = Field(..., min_length=1, description="Texto del cliente")


class RecommendationResponse(BaseModel):
    categoria: str
    producto: str
    descripcion: str
    medidas: str
    especificaciones_tecnicas: str
    precios: str
    score: float
    respuesta: str


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def generar_respuesta_llm(
    consulta: str,
    categoria: str,
    producto: str,
    descripcion: str,
    medidas: str,
    especificaciones_tecnicas: str,
    precios: str,
    score: float,
) -> str:
    precio_mostrado = precios if precios.strip() else "A cotización"
    prompt = f"""Eres un asesor de ventas experto en muebles de melamina.

Tu tarea es recomendar el producto más adecuado de forma natural, amigable y persuasiva.

Producto recomendado:
- Categoría: {categoria}
- Nombre: {producto}
- Descripción: {descripcion}
- Medidas: {medidas}
- Especificaciones técnicas: {especificaciones_tecnicas}
- Precio: {precio_mostrado}

Consulta del cliente:
{consulta}

Responde en español, con tono profesional, breve y útil. Si corresponde, destaca beneficios concretos del producto."""

    if client is None:
        precio_texto = "a cotización" if precios.strip().lower() == "a cotización" else precios
        return (
            f"Te recomiendo {producto} porque se ajusta muy bien a tu necesidad. "
            f"Su estilo y características encajan con la consulta realizada. "
            f"El precio es {precio_texto}."
        )

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente comercial breve y profesional."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content or "No se pudo generar una respuesta."
    except Exception:
        precio_texto = "a cotización" if precios.strip().lower() == "a cotización" else precios
        return (
            f"Te recomiendo {producto} porque se ajusta muy bien a tu necesidad. "
            f"Su estilo y características encajan con la consulta realizada. "
            f"El precio es {precio_texto}."
        )


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(payload: RecommendationRequest) -> RecommendationResponse:
    consulta = payload.consulta.strip()
    if not consulta:
        raise HTTPException(status_code=400, detail="La consulta no puede estar vacía.")

    result = recommender.recommend(consulta)
    respuesta = generar_respuesta_llm(
        consulta=consulta,
        categoria=result.categoria,
        producto=result.producto,
        descripcion=result.descripcion,
        medidas=result.medidas,
        especificaciones_tecnicas=result.especificaciones_tecnicas,
        precios=result.precios,
        score=result.score,
    )

    return RecommendationResponse(
        categoria=result.categoria,
        producto=result.producto,
        descripcion=result.descripcion,
        medidas=result.medidas,
        especificaciones_tecnicas=result.especificaciones_tecnicas,
        precios=result.precios,
        score=result.score,
        respuesta=respuesta,
    )
