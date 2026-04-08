# Etapa 1: Constructor (Builder)
FROM python:3.13-slim as builder

RUN pip install poetry==2.0.1 

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copiamos archivos de dependencias Y el código para que Poetry pueda "instalar" el proyecto
COPY pyproject.toml poetry.lock ./
COPY source/ ./source/
COPY deliverables/part2_ab_testing ./deliverables/part2_ab_testing

# Instalamos incluyendo el root (esto crea los enlaces a source y deliverables en el .venv)
RUN poetry install --only main && rm -rf $POETRY_CACHE_DIR

# Etapa 2: Ejecución (Runtime)
FROM python:3.13-slim as runtime

WORKDIR /app

# Configuramos el entorno para usar el .venv que copiamos
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app 

# Copiamos el entorno virtual completo ya preparado
COPY --from=builder /app/.venv /app/.venv
# Copiamos el código (necesario para que los symlinks del .venv funcionen)
COPY source/ ./source/
COPY deliverables/part2_ab_testing ./deliverables/part2_ab_testing

EXPOSE 1348

RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "deliverables.part2_ab_testing.app.main:app", "--host", "0.0.0.0", "--port", "1348"]