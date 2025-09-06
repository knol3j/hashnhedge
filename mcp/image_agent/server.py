#!/usr/bin/env python3
"""
HashNHedge Image Agent MCP Server
Automatically fetches and manages copyright-free images for Hugo posts
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from image_agent.orchestrator import Orchestrator

# Initialize orchestrator
orchestrator = Orchestrator()

# Create MCP server
server = Server("hashnhedge-image-agent")

@server.list_tools()
async def list_tools():
    """List available tools for the MCP server."""
    return [
        Tool(
            name="scan_articles",
            description="Scan content directory for articles needing featured images",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of articles to return",
                        "default": 100
                    }
                }
            }
        ),
        Tool(
            name="search_images",
            description="Search for images matching article keywords",
            inputSchema={
                "type": "object",
                "properties": {
                    "article_path": {
                        "type": "string",
                        "description": "Path to the article file"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum results per provider",
                        "default": 5
                    }
                },
                "required": ["article_path"]
            }
        ),
        Tool(
            name="download_image",
            description="Download and attach the best image to an article",
            inputSchema={
                "type": "object",
                "properties": {
                    "article_path": {
                        "type": "string",
                        "description": "Path to the article file"
                    },
                    "provider": {
                        "type": "string",
                        "description": "Image provider (optional)"
                    },
                    "image_index": {
                        "type": "integer",
                        "description": "Index of image from search results",
                        "default": 0
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Overwrite existing image",
                        "default": False
                    }
                },
                "required": ["article_path"]
            }
        ),
        Tool(
            name="batch_autofetch",
            description="Automatically fetch images for multiple articles",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_articles": {
                        "type": "integer",
                        "description": "Maximum articles to process",
                        "default": 5
                    },
                    "per_article": {
                        "type": "integer",
                        "description": "Images to fetch per article",
                        "default": 1
                    }
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a tool and return results."""
    try:
        if name == "scan_articles":
            limit = arguments.get("limit", 100)
            result = await orchestrator.scan_articles(limit=limit)
            return [TextContent(type="text", text=result)]
            
        elif name == "search_images":
            article_path = arguments["article_path"]
            max_results = arguments.get("max_results", 5)
            result = await orchestrator.search_images_for_article(
                article_path, max_results
            )
            return [TextContent(type="text", text=result)]
            
        elif name == "download_image":
            article_path = arguments["article_path"]
            provider = arguments.get("provider")
            image_index = arguments.get("image_index", 0)
            force = arguments.get("force", False)
            result = await orchestrator.download_and_attach(
                article_path, provider, image_index, force
            )
            return [TextContent(type="text", text=result)]
            
        elif name == "batch_autofetch":
            max_articles = arguments.get("max_articles", 5)
            per_article = arguments.get("per_article", 1)
            result = await orchestrator.batch_autofetch(max_articles, per_article)
            return [TextContent(type="text", text=result)]
            
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
            
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
