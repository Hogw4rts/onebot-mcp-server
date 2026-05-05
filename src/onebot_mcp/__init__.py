"""OneBot MCP Server — exposes OneBot API as MCP tools for Hermes Gateway."""

from onebot_mcp.client import OnebotClient
from onebot_mcp.server import main

__all__ = ["OnebotClient", "main"]