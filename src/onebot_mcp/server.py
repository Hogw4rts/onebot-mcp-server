"""MCP server entry point — connects Hermes Gateway to the OneBot API bridge."""

from __future__ import annotations

import json
import logging
import os

from onebot_mcp.client import OnebotClient
from onebot_mcp.tools import TOOLS

logger = logging.getLogger("onebot-mcp")

_client: OnebotClient | None = None


def _get_client() -> OnebotClient:
    global _client
    if _client is None:
        _client = OnebotClient()
    return _client


def _normalize_message(message):
    """If message is a string that looks like a JSON array, parse it into a list."""
    if isinstance(message, str) and message.strip().startswith("["):
        try:
            parsed = json.loads(message)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
    return message

async def dispatch(client: OnebotClient, name: str, args: dict) -> str:
    """Dispatch a tool call to the appropriate client method."""
    match name:
        # ── Read ──
        case "onebot_get_login_info":
            result = await client.get_login_info()
        case "onebot_get_friend_list":
            result = await client.get_friend_list()
        case "onebot_get_group_list":
            result = await client.get_group_list()
        case "onebot_get_group_info":
            result = await client.get_group_info(args["group_id"], no_cache=args.get("no_cache", False))
        case "onebot_get_group_members":
            result = await client.get_group_member_list(
                args["group_id"],
                limit=args.get("limit", 100),
                offset=args.get("offset", 0),
            )
        case "onebot_get_member_info":
            result = await client.get_group_member_info(
                args["group_id"],
                args["user_id"],
                no_cache=args.get("no_cache", False),
            )
        case "onebot_get_user_info":
            result = await client.get_stranger_info(
                args["user_id"],
                no_cache=args.get("no_cache", False),
            )
        case "onebot_get_message":
            result = await client.get_msg(args["message_id"])
        case "onebot_get_forward_msg":
            result = await client.get_forward_msg(args["id"])
        case "onebot_get_group_honor_info":
            result = await client.get_group_honor_info(
                args["group_id"],
                honor_type=args.get("honor_type", "all"),
            )
        case "onebot_get_status":
            result = await client.get_status()
        case "onebot_get_version_info":
            result = await client.get_version_info()
        case "onebot_can_send_image":
            result = await client.can_send_image()
        case "onebot_can_send_record":
            result = await client.can_send_record()
        case "onebot_get_cookies":
            result = await client.get_cookies(args["domain"])
        case "onebot_get_csrf_token":
            result = await client.get_csrf_token()
        case "onebot_get_credentials":
            result = await client.get_credentials(args["domain"])
        case "onebot_get_record":
            result = await client.get_record(args["file"], args["out_format"])
        case "onebot_get_image":
            result = await client.get_image(args["file"])
        # ── NapCat extended: read ──
        case "onebot_get_group_msg_history":
            result = await client.get_group_msg_history(
                args["group_id"],
                message_seq=args.get("message_seq"),
                count=args.get("count"),
                reverse=args.get("reverse"),
            )
        case "onebot_get_group_file_system_info":
            result = await client.get_group_file_system_info(args["group_id"])
        case "onebot_get_group_root_files":
            result = await client.get_group_root_files(args["group_id"])
        case "onebot_get_group_files_by_folder":
            result = await client.get_group_files_by_folder(
                args["group_id"], args["folder_id"]
            )
        case "onebot_get_group_file_url":
            result = await client.get_group_file_url(
                args["group_id"], args["file_id"]
            )
        case "onebot_get_file":
            result = await client.get_file(
                file_id=args.get("file_id"),
                file=args.get("file"),
            )
        case "onebot_get_group_at_all_remain":
            result = await client.get_group_at_all_remain(args["group_id"])
        case "onebot_get_essence_msg_list":
            result = await client.get_essence_msg_list(args["group_id"])
        # ── Write ──
        case "onebot_send_group_msg":
            result = await client.send_group_msg(
                args["group_id"], _normalize_message(args["message"]), admin_id=args["admin_id"]
            )
        case "onebot_send_private_msg":
            result = await client.send_private_msg(
                args["user_id"], _normalize_message(args["message"]), admin_id=args["admin_id"]
            )
        case "onebot_send_like":
            result = await client.send_like(
                args["user_id"], times=args.get("times", 1), admin_id=args["admin_id"]
            )
        case "onebot_set_group_ban":
            result = await client.set_group_ban(
                args["group_id"],
                args["user_id"],
                duration=args.get("duration", 0),
                admin_id=args["admin_id"],
            )
        case "onebot_set_group_whole_ban":
            result = await client.set_group_whole_ban(
                args["group_id"],
                enable=args["enable"],
                admin_id=args["admin_id"],
            )
        case "onebot_set_group_admin":
            result = await client.set_group_admin(
                args["group_id"],
                args["user_id"],
                enable=args["enable"],
                admin_id=args["admin_id"],
            )
        case "onebot_set_group_anonymous":
            result = await client.set_group_anonymous(
                args["group_id"],
                enable=args["enable"],
                admin_id=args["admin_id"],
            )
        case "onebot_set_group_anonymous_ban":
            result = await client.set_group_anonymous_ban(
                args["group_id"],
                duration=args.get("duration", 0),
                admin_id=args["admin_id"],
                anonymous=args.get("anonymous"),
                flag=args.get("flag"),
            )
        case "onebot_set_group_card":
            result = await client.set_group_card(
                args["group_id"],
                args["user_id"],
                card=args.get("card", ""),
                admin_id=args["admin_id"],
            )
        case "onebot_set_group_name":
            result = await client.set_group_name(
                args["group_id"],
                group_name=args["group_name"],
                admin_id=args["admin_id"],
            )
        case "onebot_set_group_leave":
            result = await client.set_group_leave(
                args["group_id"],
                is_dismiss=args.get("is_dismiss", False),
                admin_id=args["admin_id"],
            )
        case "onebot_set_group_special_title":
            result = await client.set_group_special_title(
                args["group_id"],
                args["user_id"],
                special_title=args.get("special_title", ""),
                admin_id=args["admin_id"],
            )
        case "onebot_set_friend_add_request":
            result = await client.set_friend_add_request(
                args["flag"],
                approve=args.get("approve", True),
                remark=args.get("remark", ""),
                admin_id=args["admin_id"],
            )
        case "onebot_set_group_add_request":
            result = await client.set_group_add_request(
                args["flag"],
                type_=args.get("type", "add"),
                approve=args.get("approve", True),
                reason=args.get("reason", ""),
                admin_id=args["admin_id"],
            )
        case "onebot_set_group_kick":
            result = await client.set_group_kick(
                args["group_id"],
                args["user_id"],
                reject_add_request=args.get("reject_add_request", False),
                admin_id=args["admin_id"],
            )
        case "onebot_delete_msg":
            result = await client.delete_msg(
                args["message_id"], admin_id=args["admin_id"]
            )
        case "onebot_clean_cache":
            result = await client.clean_cache(admin_id=args["admin_id"])
        # ── NapCat extended: write ──
        case "onebot_download_file":
            result = await client.download_file(
                args["url"],
                thread_cnt=args.get("thread_cnt"),
                headers=args.get("headers"),
                admin_id=args["admin_id"],
            )
        case "onebot_upload_group_file":
            result = await client.upload_group_file(
                args["group_id"], args["file"], args["name"],
                folder=args.get("folder"),
                admin_id=args["admin_id"],
            )
        case "onebot_upload_private_file":
            result = await client.upload_private_file(
                args["user_id"], args["file"], args["name"],
                admin_id=args["admin_id"],
            )
        case "onebot_delete_group_file":
            result = await client.delete_group_file(
                args["group_id"], args["file_id"],
                busid=args.get("busid"),
                admin_id=args["admin_id"],
            )
        case "onebot_create_group_file_folder":
            result = await client.create_group_file_folder(
                args["group_id"], args["name"],
                parent_id=args.get("parent_id"),
                admin_id=args["admin_id"],
            )
        case "onebot_delete_group_folder":
            result = await client.delete_group_folder(
                args["group_id"], args["folder_id"],
                admin_id=args["admin_id"],
            )
        case "onebot_set_essence_msg":
            result = await client.set_essence_msg(
                args["message_id"], admin_id=args["admin_id"]
            )
        case "onebot_delete_essence_msg":
            result = await client.delete_essence_msg(
                args["message_id"], admin_id=args["admin_id"]
            )
        case "onebot_send_group_forward_msg":
            result = await client.send_group_forward_msg(
                args["group_id"], args["messages"],
                admin_id=args["admin_id"],
            )
        case _:
            raise ValueError(f"Unknown tool: {name}")

    return json.dumps(result, ensure_ascii=False, indent=2)


def _register_handlers(server) -> None:
    @server.list_tools()
    async def list_tools() -> list[dict]:
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict | None) -> list[dict]:
        args = arguments or {}
        logger.info("tool call: %s(%s)", name, ", ".join(f"{k}={v}" for k, v in args.items()))
        try:
            result_text = await dispatch(_get_client(), name, args)
            return [{"type": "text", "text": result_text}]
        except Exception as e:
            logger.exception("tool call failed: %s", name)
            return [{"type": "text", "text": json.dumps({"error": str(e)})}]


def main() -> None:
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    if transport == "http":
        _run_http()
    else:
        _run_stdio()


def _run_stdio() -> None:
    import asyncio

    from mcp.server import Server
    from mcp.server.stdio import stdio_server

    async def _run() -> None:
        server = Server("onebot-mcp")
        _register_handlers(server)

        async with stdio_server() as (read_stream, write_stream):
            logger.info("onebot-mcp-server starting (stdio)")
            await server.run(read_stream, write_stream, server.create_initialization_options())

        client = _get_client()
        await client.close()

    asyncio.run(_run())


def _run_http() -> None:
    import asyncio
    import uuid

    import uvicorn
    from mcp.server import Server
    from mcp.server.streamable_http import StreamableHTTPServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Mount

    async def _run() -> None:
        mcp_server = Server("onebot-mcp")
        _register_handlers(mcp_server)

        session_id = uuid.uuid4().hex
        transport = StreamableHTTPServerTransport(mcp_session_id=session_id)

        async def handle_mcp(scope, receive, send):
            await transport.handle_request(scope, receive, send)

        async def run_server():
            async with transport:
                await mcp_server.run(
                    transport.read_stream,
                    transport.write_stream,
                    mcp_server.create_initialization_options(),
                )

        app = Starlette(
            routes=[Mount("/mcp", app=handle_mcp)],
            lifespan=lambda app_state: _lifespan(app_state, run_server),
        )

        port = int(os.environ.get("MCP_PORT", "8080"))
        config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
        uvicorn.Server(config).run()

    asyncio.run(_run())


async def _lifespan(app, run_server_coro):
    import asyncio

    task = asyncio.create_task(run_server_coro)
    yield
    task.cancel()


if __name__ == "__main__":
    main()