"""
YouTube MCP Server - Main entry point
"""
import asyncio
import os
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
)

from .youtube_client import YouTubeClient
from .tools import register_tools


async def _async_main():
    """Main async entry point for the YouTube MCP server."""
    # Get API key from environment
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY environment variable is required")
    
    # Initialize YouTube client
    youtube_client = YouTubeClient(api_key)
    
    # Create MCP server
    server = Server("youtube-mcp")
    
    # Register tools
    register_tools(server, youtube_client)
    
    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def main():
    """Synchronous entry point for console script."""
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()