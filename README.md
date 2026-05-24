# AI Furniture Recommender

Recomendador de productos local (v1.0) prototipo construido para una empresa de muebles de melamina. El cliente escribe su consulta en lenguaje natural, el sistema busca el producto más relevante del catálogo usando embeddings semánticos y devuelve una respuesta comercial generada por un modelo de lenguaje.

---

## Cómo funciona

1. El catálogo de productos se carga desde un archivo Excel (`backend/productos.xlsx`) al iniciar el servidor.
2. Cada producto se convierte en un embedding con **sentence-transformers** (`all-MiniLM-L6-v2`).
3. Cuando llega una consulta, se calcula la similitud coseno entre el texto del cliente y todos los productos, y se devuelve el de mayor puntaje.
4. Con el producto encontrado, se llama a la API de **OpenAI** (`gpt-4o-mini` por defecto) para generar una respuesta de asesor comercial. Si no hay clave configurada, el sistema responde con un texto de respaldo.

---

## Stack

- **Backend:** FastAPI + uvicorn
- **Embeddings:** sentence-transformers
- **LLM:** OpenAI API
- **Catálogo:** Excel vía openpyxl
- **Frontend:** HTML / CSS / JavaScript (sin frameworks)

---

## Requisitos previos

- Python 3.10+
- Archivo `backend/productos.xlsx` con las columnas: `Nombre del Producto`, `Descripción Comercial`, y opcionalmente `Categoría`, `Medidas`, `Especificaciones Técnicas`, `Precios`.

---

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini   # opcional, este es el valor por defecto
```

---

## Uso

```bash
python main.py
```

El servidor arranca en `http://127.0.0.1:8000`. Abrir esa URL en el navegador para usar la interfaz.

**Endpoints disponibles:**

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Interfaz web |
| `GET` | `/health` | Estado del servidor |
| `POST` | `/recommend` | Recibe la consulta y devuelve el producto recomendado |

---

## Capturas

![Pantalla de consulta](image/consulta.png)
*Interfaz para ingresar la consulta del cliente.*

![Resultado de la recomendación](image/respuesta.png)
*Producto recomendado junto con la respuesta generada por el asesor virtual.*