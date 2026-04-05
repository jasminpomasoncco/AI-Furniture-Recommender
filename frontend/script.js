const form = document.getElementById('recommendForm');
const consultaInput = document.getElementById('consulta');
const categoriaEl = document.getElementById('categoria');
const productoEl = document.getElementById('producto');
const scoreEl = document.getElementById('score');
const descripcionEl = document.getElementById('descripcion');
const medidasEl = document.getElementById('medidas');
const especificacionesEl = document.getElementById('especificaciones');
const precioEl = document.getElementById('precio');
const respuestaEl = document.getElementById('respuesta');
const statusEl = document.getElementById('status');
const btn = document.getElementById('btnRecommend');

function setStatus(message, type = '') {
  if (!statusEl) return;
  statusEl.textContent = message;
  statusEl.className = `status ${type}`.trim();
}

function setLoading(isLoading) {
  if (!btn) return;
  btn.disabled = isLoading;
  btn.textContent = isLoading ? 'Recomendando...' : 'Recomendar';
}

if (!form || !consultaInput || !categoriaEl || !productoEl || !scoreEl || !descripcionEl || !medidasEl || !especificacionesEl || !precioEl || !respuestaEl) {
  setStatus('Faltan elementos del formulario o de resultados en el HTML.', 'error');
} else {
form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const consulta = consultaInput.value.trim();
  if (!consulta) {
    setStatus('Escribe una consulta antes de continuar.', 'error');
    return;
  }

  setLoading(true);
  setStatus('Procesando solicitud comercial...', '');

  try {
    const response = await fetch('/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ consulta })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'No se pudo obtener la recomendación.');
    }

    categoriaEl.textContent = data.categoria || '-';
    productoEl.textContent = data.producto;
    scoreEl.textContent = data.score;
    descripcionEl.textContent = data.descripcion;
    medidasEl.textContent = data.medidas || '-';
    especificacionesEl.textContent = data.especificaciones_tecnicas || '-';
    precioEl.textContent = data.precios || '-';
    respuestaEl.textContent = data.respuesta;
    setStatus('Recomendación generada correctamente.', 'success');
  } catch (error) {
    setStatus(error.message || 'Ocurrió un error al generar la recomendación.', 'error');
  } finally {
    setLoading(false);
  }
});
}
