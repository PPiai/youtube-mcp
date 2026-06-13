# YouTube MCP Server

Model Context Protocol (MCP) server for YouTube Data API v3. Provides tools for searching videos, channels, playlists, getting trending content, video details, comments, and more.

## Features

- **Video Search** - Search YouTube videos with advanced filters (duration, definition, region, date range, etc.)
- **Channel Search** - Find channels by query
- **Video Details** - Get comprehensive video information (statistics, content details, topics, etc.)
- **Channel Details** - Get channel statistics, branding, topics, and more
- **Trending Videos** - Get most popular videos by region and category
- **Video Categories** - Browse available video categories
- **Channel Videos** - Get recent uploads from a specific channel
- **Playlist Videos** - Get videos from any playlist
- **Playlist Search** - Search for playlists
- **Video Comments** - Get comments on videos
- **Channel by Handle** - Look up channels by @username

## Installation

```bash
cd /opt/data/mcp-servers/youtube-mcp
pip install -e .
```

Or with uv:
```bash
uv pip install -e /opt/data/mcp-servers/youtube-mcp
```

## Configuration

Requires a YouTube Data API v3 key. Get one from [Google Cloud Console](https://console.cloud.google.com/apis/credentials).

Set the environment variable:
```bash
export YOUTUBE_API_KEY="your_api_key_here"
```

## Usage with Hermes Agent

Add to your `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  youtube:
    command: "uvx"
    args: ["youtube-mcp"]
    env:
      YOUTUBE_API_KEY: "your_api_key_here"
    timeout: 120
    connect_timeout: 60
```

Then restart Hermes Agent. The tools will be available as `mcp_youtube_*`.

## Available Tools

| Tool | Description |
|------|-------------|
| `search_videos` | Search videos with filters |
| `search_channels` | Search channels |
| `get_video_details` | Get detailed video info |
| `get_channel_details` | Get detailed channel info |
| `get_trending_videos` | Get trending videos by region |
| `get_video_categories` | Get video categories |
| `get_channel_videos` | Get channel's recent videos |
| `get_playlist_videos` | Get playlist videos |
| `search_playlists` | Search playlists |
| `get_video_comments` | Get video comments |
| `get_channel_by_handle` | Get channel by @handle |

## Example Queries

- "Search for videos about AI news from the last week"
- "Get trending videos in Brazil (BR)"
- "Find channels about programming tutorials"
- "Get details for video dQw4w9WgXcQ"
- "Get comments on a viral video"
- "Find playlists about machine learning"

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT