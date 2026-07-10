# Imagen base ligera de Python
FROM python:3.11-slim

# Evitar prompts durante instalación
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema + Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && pip install --no-cache-dir \
    pandas \
    sqlalchemy \
    psycopg2-binary \
    matplotlib \
    seaborn \
    scikit-learn \
    numpy \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos (se montarán volúmenes para desarrollo)
COPY scripts/ /app/scripts/
COPY archive/ /app/archive/
COPY sql/ /app/sql/

# Comando por defecto (se sobrescribe en docker-compose)
CMD ["python", "scripts/analysis_postgres.py"]