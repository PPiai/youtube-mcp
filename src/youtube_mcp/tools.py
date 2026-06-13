"""
YouTube MCP Tools Registration
"""
import json
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.types import Tool, TextContent, CallToolResult

from .youtube_client import YouTubeClient


def register_tools(server: Server, youtube_client: YouTubeClient):
    """Register all YouTube MCP tools."""
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="search_videos",
                description="Search for YouTube videos with various filters",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "max_results": {"type": "integer", "default": 10, "description": "Maximum number of results (1-50)"},
                        "order": {"type": "string", "enum": ["relevance", "date", "rating", "viewCount", "title"], "default": "relevance"},
                        "published_after": {"type": "string", "description": "ISO 8601 datetime (e.g., 2024-01-01T00:00:00Z)"},
                        "published_before": {"type": "string", "description": "ISO 8601 datetime"},
                        "region_code": {"type": "string", "description": "ISO 3166-1 alpha-2 country code (e.g., US, BR)"},
                        "video_duration": {"type": "string", "enum": ["any", "short", "medium", "long"]},
                        "video_definition": {"type": "string", "enum": ["any", "high", "standard"]},
                        "video_dimension": {"type": "string", "enum": ["2d", "3d", "any"]},
                        "video_license": {"type": "string", "enum": ["any", "creativeCommon", "youtube"]},
                        "video_type": {"type": "string", "enum": ["any", "episode", "movie"]},
                        "channel_id": {"type": "string", "description": "Filter by specific channel ID"},
                        "topic_id": {"type": "string", "description": "Filter by Freebase topic ID"},
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="search_channels",
                description="Search for YouTube channels",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "max_results": {"type": "integer", "default": 10, "description": "Maximum number of results (1-50)"},
                        "order": {"type": "string", "enum": ["relevance", "date", "rating", "viewCount", "title"], "default": "relevance"},
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="get_video_details",
                description="Get detailed information about specific videos",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "video_ids": {"type": "array", "items": {"type": "string"}, "description": "List of YouTube video IDs"},
                    },
                    "required": ["video_ids"],
                },
            ),
            Tool(
                name="get_channel_details",
                description="Get detailed information about specific channels",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel_ids": {"type": "array", "items": {"type": "string"}, "description": "List of YouTube channel IDs"},
                    },
                    "required": ["channel_ids"],
                },
            ),
            Tool(
                name="get_trending_videos",
                description="Get trending/popular videos for a region",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "region_code": {"type": "string", "default": "US", "description": "ISO 3166-1 alpha-2 country code"},
                        "category_id": {"type": "string", "description": "Video category ID (optional)"},
                        "max_results": {"type": "integer", "default": 20, "description": "Maximum number of results (1-50)"},
                    },
                    "required": ["region_code"],
                },
            ),
            Tool(
                name="get_video_categories",
                description="Get video categories for a region",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "region_code": {"type": "string", "default": "US", "description": "ISO 3166-1 alpha-2 country code"},
                    },
                    "required": ["region_code"],
                },
            ),
            Tool(
                name="get_channel_videos",
                description="Get recent videos from a specific channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel_id": {"type": "string", "description": "YouTube channel ID"},
                        "max_results": {"type": "integer", "default": 10, "description": "Maximum number of results (1-50)"},
                        "order": {"type": "string", "enum": ["date", "rating", "relevance", "title", "viewCount"], "default": "date"},
                        "published_after": {"type": "string", "description": "ISO 8601 datetime filter"},
                    },
                    "required": ["channel_id"],
                },
            ),
            Tool(
                name="get_playlist_videos",
                description="Get videos from a YouTube playlist",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "playlist_id": {"type": "string", "description": "YouTube playlist ID"},
                        "max_results": {"type": "integer", "default": 10, "description": "Maximum number of results (1-50)"},
                    },
                    "required": ["playlist_id"],
                },
            ),
            Tool(
                name="search_playlists",
                description="Search for YouTube playlists",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "max_results": {"type": "integer", "default": 10, "description": "Maximum number of results (1-50)"},
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="get_video_comments",
                description="Get comments for a YouTube video",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "video_id": {"type": "string", "description": "YouTube video ID"},
                        "max_results": {"type": "integer", "default": 20, "description": "Maximum number of results (1-100)"},
                        "order": {"type": "string", "enum": ["relevance", "time"], "default": "relevance"},
                    },
                    "required": ["video_id"],
                },
            ),
            Tool(
                name="get_channel_by_handle",
                description="Get channel details by handle (@username)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "handle": {"type": "string", "description": "YouTube handle (e.g., @MrBeast or MrBeast)"},
                    },
                    "required": ["handle"],
                },
            ),
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
        try:
            if name == "search_videos":
                result = youtube_client.search_videos(
                    query=arguments["query"],
                    max_results=arguments.get("max_results", 10),
                    order=arguments.get("order", "relevance"),
                    published_after=arguments.get("published_after"),
                    published_before=arguments.get("published_before"),
                    region_code=arguments.get("region_code"),
                    video_duration=arguments.get("video_duration"),
                    video_definition=arguments.get("video_definition"),
                    video_dimension=arguments.get("video_dimension"),
                    video_license=arguments.get("video_license"),
                    video_type=arguments.get("video_type"),
                    channel_id=arguments.get("channel_id"),
                    topic_id=arguments.get("topic_id"),
                )
            
            elif name == "search_channels":
                result = youtube_client.search_channels(
                    query=arguments["query"],
                    max_results=arguments.get("max_results", 10),
                    order=arguments.get("order", "relevance"),
                )
            
            elif name == "get_video_details":
                result = youtube_client.get_video_details(arguments["video_ids"])
            
            elif name == "get_channel_details":
                result = youtube_client.get_channel_details(arguments["channel_ids"])
            
            elif name == "get_trending_videos":
                result = youtube_client.get_trending_videos(
                    region_code=arguments.get("region_code", "US"),
                    category_id=arguments.get("category_id"),
                    max_results=arguments.get("max_results", 20),
                )
            
            elif name == "get_video_categories":
                result = youtube_client.get_video_categories(
                    region_code=arguments.get("region_code", "US"),
                )
            
            elif name == "get_channel_videos":
                result = youtube_client.get_channel_videos(
                    channel_id=arguments["channel_id"],
                    max_results=arguments.get("max_results", 10),
                    order=arguments.get("order", "date"),
                    published_after=arguments.get("published_after"),
                )
            
            elif name == "get_playlist_videos":
                result = youtube_client.get_playlist_videos(
                    playlist_id=arguments["playlist_id"],
                    max_results=arguments.get("max_results", 10),
                )
            
            elif name == "search_playlists":
                result = youtube_client.search_playlists(
                    query=arguments["query"],
                    max_results=arguments.get("max_results", 10),
                )
            
            elif name == "get_video_comments":
                result = youtube_client.get_comments(
                    video_id=arguments["video_id"],
                    max_results=arguments.get("max_results", 20),
                    order=arguments.get("order", "relevance"),
                )
            
            elif name == "get_channel_by_handle":
                result = youtube_client.get_channel_by_handle(arguments["handle"])
            
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                    isError=True,
                )
            
            if result["success"]:
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(result["data"], ensure_ascii=False, indent=2))],
                )
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {result['error']}")],
                    isError=True,
                )
        
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")],
                isError=True,
            )