FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema (necessário para o healthcheck e algumas libs Python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

EXPOSE 8501

# Healthcheck para garantir que a aplicação não trava
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -s http://localhost:8501/ > /dev/null || exit 1

ENTRYPOINT ["streamlit", "run"]
CMD ["portal.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
