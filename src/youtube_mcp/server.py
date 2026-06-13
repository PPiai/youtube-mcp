"""
YouTube MCP Server - Main entry point

Suporta dois transportes, selecionados pela variavel de ambiente MCP_TRANSPORT:
  - "streamable-http" (padrao): expoe o servidor como servico HTTP (deploy remoto)
  - "stdio": inicia o servidor sob demanda por um cliente local
"""
import asyncio
import contextlib
import os
from typing import AsyncIterator

from dotenv import load_dotenv
from mcp.server import Server

from .youtube_client import YouTubeClient
from .tools import register_tools

# Carrega variaveis de ambiente de um arquivo .env, se existir
load_dotenv()


def _build_server() -> Server:
    """Cria o servidor MCP com as ferramentas registradas."""
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY environment variable is required")

    youtube_client = YouTubeClient(api_key)
    server = Server("youtube-mcp")
    register_tools(server, youtube_client)
    return server


async def _run_stdio(server: Server) -> None:
    """Roda o servidor sobre stdio (uso local)."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def _build_http_app(server: Server):
    """Monta a aplicacao ASGI (Starlette) com transporte streamable-HTTP."""
    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Mount, Route
    from starlette.types import Receive, Scope, Send

    # stateless=True: cada requisicao usa um transporte novo, ideal atras de
    # proxy/load-balancer (EasyPanel) sem afinidade de sessao.
    session_manager = StreamableHTTPSessionManager(app=server, stateless=True)

    async def handle_mcp(scope: Scope, receive: Receive, send: Send) -> None:
        await session_manager.handle_request(scope, receive, send)

    async def health(_request) -> JSONResponse:
        return JSONResponse({"status": "ok", "service": "youtube-mcp"})

    @contextlib.asynccontextmanager
    async def lifespan(_app: Starlette) -> AsyncIterator[None]:
        async with session_manager.run():
            yield

    return Starlette(
        routes=[
            Route("/health", health, methods=["GET"]),
            Mount("/mcp", app=handle_mcp),
        ],
        lifespan=lifespan,
    )


def _run_http(server: Server) -> None:
    """Roda o servidor como servico HTTP (deploy remoto)."""
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    app = _build_http_app(server)
    uvicorn.run(app, host=host, port=port, log_level="info")


def main() -> None:
    """Entry point sincrono para o console script."""
    transport = os.getenv("MCP_TRANSPORT", "streamable-http").lower()
    server = _build_server()

    if transport == "stdio":
        asyncio.run(_run_stdio(server))
    elif transport in ("streamable-http", "http"):
        _run_http(server)
    else:
        raise ValueError(
            f"MCP_TRANSPORT invalido: {transport!r}. "
            "Use 'streamable-http' ou 'stdio'."
        )


if __name__ == "__main__":
    main()
