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
git clone https://github.com/PPiai/youtube-mcp.git
cd youtube-mcp
pip install -e .
```

Or with uv:
```bash
uv pip install -e .
```

## Configuration

Requires a YouTube Data API v3 key. Get one from [Google Cloud Console](https://console.cloud.google.com/apis/credentials).

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `YOUTUBE_API_KEY` | — | **Required.** YouTube Data API v3 key |
| `MCP_TRANSPORT` | `streamable-http` | `streamable-http` (remote service) or `stdio` (local) |
| `HOST` | `0.0.0.0` | Bind host (HTTP mode) |
| `PORT` | `8000` | Bind port (HTTP mode) |

## Transports

This server supports two transports, selected by `MCP_TRANSPORT`:

### Streamable HTTP (remote service — default)

Runs as a persistent HTTP service on a single port (default `8000`).

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/mcp/` | `POST` | MCP streamable-HTTP endpoint (JSON-RPC) |
| `/health` | `GET` | Health check — returns `200 {"status":"ok"}` |

```bash
MCP_TRANSPORT=streamable-http PORT=8000 youtube-mcp
# MCP endpoint: http://localhost:8000/mcp/
# Health:       http://localhost:8000/health
```

> **Note — trailing slash.** The MCP endpoint is mounted at `/mcp`, so `POST /mcp`
> returns a **307 redirect to `/mcp/`**. Always point clients at `/mcp/` (with the
> trailing slash) to avoid clients that don't follow redirects on `POST`.

**Connecting an MCP client to the remote endpoint** (e.g. `mcp.json` /
Claude Desktop style config):

```json
{
  "mcpServers": {
    "youtube": {
      "type": "streamable-http",
      "url": "https://<your-domain>/mcp/"
    }
  }
}
```

**Quick test with curl:**

```bash
# Health
curl https://<your-domain>/health

# Initialize (note: streamable-HTTP replies with an SSE stream)
curl -X POST https://<your-domain>/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}}}'

# Call a tool
curl -X POST https://<your-domain>/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_videos","arguments":{"query":"ai news","max_results":2}}}'
```

> **⚠️ Security.** The HTTP endpoint has **no built-in authentication** — anyone
> who can reach the URL can issue requests and consume your YouTube API quota.
> Put it behind an authenticating reverse proxy / network policy, or keep it on a
> private network. Do not expose it publicly without protection.

### stdio (local)

Launched on-demand by a local client (e.g. via `uvx`):

```yaml
mcp_servers:
  youtube:
    command: "uvx"
    args: ["youtube-mcp"]
    env:
      YOUTUBE_API_KEY: "your_api_key_here"
      MCP_TRANSPORT: "stdio"
    timeout: 120
    connect_timeout: 60
```

## Deploy (EasyPanel / Docker)

Build and run as a container:

```bash
docker build -t youtube-mcp .
docker run -p 8000:8000 -e YOUTUBE_API_KEY="your_api_key_here" youtube-mcp
```

On EasyPanel, set `YOUTUBE_API_KEY` as a **service environment variable** (not a
build-arg), expose port `8000`, and point the MCP client to
`https://<your-domain>/mcp`.

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

# Run the server locally over HTTP and smoke-test it
MCP_TRANSPORT=streamable-http youtube-mcp &
curl http://localhost:8000/health
```

> No automated test suite yet — `pytest` is wired up in the `dev` extra but there
> are no tests under a `tests/` directory. Contributions welcome.

## License

MIT