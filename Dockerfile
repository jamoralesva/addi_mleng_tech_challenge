# Etapa 1: Constructor (Builder)
FROM python:3.13-slim as builder


RUN pip install poetry==2.3.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# IMPORTANTE:
COPY pyproject.toml poetry.lock ./

# IMPORTANTE: Asegúrate de que 'aioodbc' esté en tu pyproject.toml
RUN poetry install --only main --no-root && rm -rf $POETRY_CACHE_DIR

# Etapa 2: Ejecución (Runtime)
FROM python:3.13-slim as runtime

# TODO: arreglar la estructura del proyecto para evitar copiar archivos innecesarios
# Configuración de entorno
WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Copia de artefactos
COPY --from=builder /app/.venv /app/.venv
COPY /src/app/ /app/app/

EXPOSE 8000

# Usuario no-root (Mejora de seguridad para Azure Container Apps)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
