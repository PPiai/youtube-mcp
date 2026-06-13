# YouTube MCP Server - Docker Image
FROM python:3.12-slim

WORKDIR /app

# Dependencias de sistema (gcc para eventuais wheels nativos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala o uv (gerenciador de pacotes rapido)
RUN pip install --no-cache-dir uv

# Copia metadados e codigo (README e exigido pelo pyproject.toml)
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Instala o pacote e suas dependencias no Python do sistema
RUN uv pip install --system --no-cache .

# Usuario nao-root
RUN useradd -m -u 1000 mcpuser && chown -R mcpuser:mcpuser /app
USER mcpuser

# Variaveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    MCP_TRANSPORT=streamable-http \
    HOST=0.0.0.0 \
    PORT=8000

EXPOSE 8000

# Health check HTTP real
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://localhost:8000/health').status==200 else sys.exit(1)" || exit 1

# Roda o servidor (console script instalado pelo pyproject)
ENTRYPOINT ["youtube-mcp"]
