"""Tests for MCP tool definitions and dispatch logic."""

from __future__ import annotations

import json

import pytest

from onebot_mcp.client import OnebotClient
from onebot_mcp.server import dispatch
from onebot_mcp.tools import TOOLS


class MockClient(OnebotClient):
    """Mock client that returns preset data without making HTTP calls."""

    def __init__(self) -> None:
        self._responses: dict[str, object] = {}

    def set_response(self, method: str, data: object) -> None:
        self._responses[method] = data

    async def get_login_info(self) -> dict:
        return self._responses.get("get_login_info", {})

    async def get_friend_list(self) -> list:
        return self._responses.get("get_friend_list", [])

    async def get_group_list(self) -> list:
        return self._responses.get("get_group_list", [])

    async def get_group_info(self, group_id: int, *, no_cache: bool = False) -> dict:
        return self._responses.get("get_group_info", {"group_id": group_id})

    async def get_group_member_list(
        self, group_id: int, *, limit: int = 100, offset: int = 0
    ) -> dict:
        return self._responses.get("get_group_member_list", {"group_id": group_id, "members": []})

    async def get_group_member_info(
        self, group_id: int, user_id: int, *, no_cache: bool = False
    ) -> dict:
        return self._responses.get("get_group_member_info", {"user_id": user_id})

    async def get_stranger_info(self, user_id: int, *, no_cache: bool = False) -> dict:
        return self._responses.get("get_stranger_info", {"user_id": user_id})

    async def get_msg(self, message_id: int) -> dict:
        return self._responses.get("get_msg", {"message_id": message_id})

    async def get_forward_msg(self, id: str) -> dict:
        return self._responses.get("get_forward_msg", {"id": id})

    async def get_group_honor_info(
        self, group_id: int, *, honor_type: str = "all"
    ) -> dict:
        return self._responses.get("get_group_honor_info", {"group_id": group_id})

    async def get_status(self) -> dict:
        return self._responses.get("get_status", {"online": True})

    async def get_version_info(self) -> dict:
        return self._responses.get("get_version_info", {"app_name": "test"})

    async def send_group_msg(
        self, group_id: int, message: str, *, admin_id: int
    ) -> dict:
        return self._responses.get("send_group_msg", {"ok": True})

    async def send_private_msg(
        self, user_id: int, message: str, *, admin_id: int
    ) -> dict:
        return self._responses.get("send_private_msg", {"ok": True})

    async def set_group_ban(
        self, group_id: int, user_id: int, *, duration: int = 0, admin_id: int
    ) -> dict:
        return self._responses.get("set_group_ban", {"ok": True})

    async def set_group_kick(
        self,
        group_id: int,
        user_id: int,
        *,
        reject_add_request: bool = False,
        admin_id: int,
    ) -> dict:
        return self._responses.get("set_group_kick", {"ok": True})

    async def delete_msg(self, message_id: int, *, admin_id: int) -> dict:
        return self._responses.get("delete_msg", {"ok": True})

    async def close(self) -> None:
        pass


def test_all_tools_have_required_fields() -> None:
    tool_names = set()
    for tool in TOOLS:
        assert tool.name, f"tool missing name: {tool}"
        assert tool.description, f"tool {tool.name} missing description"
        assert tool.inputSchema, f"tool {tool.name} missing inputSchema"
        schema = tool.inputSchema
        assert schema["type"] == "object", f"tool {tool.name} schema must be object"
        assert "required" in schema, f"tool {tool.name} schema missing required"
        tool_names.add(tool.name)
    assert len(tool_names) == len(TOOLS), "duplicate tool names found"


def test_tool_names_follow_convention() -> None:
    for tool in TOOLS:
        assert tool.name.startswith("onebot_"), f"tool {tool.name} should start with onebot_"


def test_tool_count() -> None:
    write_prefixes = ("onebot_send_", "onebot_set_", "onebot_delete_", "onebot_clean_", "onebot_upload_", "onebot_create_", "onebot_download_")
    read_tools = [t for t in TOOLS if not t.name.startswith(write_prefixes)]
    write_tools = [t for t in TOOLS if t.name.startswith(write_prefixes)]
    assert len(read_tools) == 27, f"expected 27 read tools, got {len(read_tools)}"
    assert len(write_tools) == 26, f"expected 26 write tools, got {len(write_tools)}"
    assert len(TOOLS) == 53


@pytest.mark.asyncio
async def test_dispatch_login_info() -> None:
    client = MockClient()
    client.set_response("get_login_info", {"user_id": 123, "nickname": "TestBot"})
    result = await dispatch(client, "onebot_get_login_info", {})
    parsed = json.loads(result)
    assert parsed["user_id"] == 123


@pytest.mark.asyncio
async def test_dispatch_group_members() -> None:
    client = MockClient()
    client.set_response(
        "get_group_member_list",
        {"group_id": 111, "total": 1, "members": [{"user_id": 123}]},
    )
    result = await dispatch(client, "onebot_get_group_members", {"group_id": 111})
    parsed = json.loads(result)
    assert parsed["group_id"] == 111
    assert parsed["total"] == 1


@pytest.mark.asyncio
async def test_dispatch_forward_msg() -> None:
    client = MockClient()
    client.set_response("get_forward_msg", {"messages": [{"content": "hello"}]})
    result = await dispatch(client, "onebot_get_forward_msg", {"id": "abc123"})
    parsed = json.loads(result)
    assert "messages" in parsed


@pytest.mark.asyncio
async def test_dispatch_status() -> None:
    client = MockClient()
    client.set_response("get_status", {"online": True, "good": True})
    result = await dispatch(client, "onebot_get_status", {})
    parsed = json.loads(result)
    assert parsed["online"] is True


@pytest.mark.asyncio
async def test_dispatch_send_group_msg() -> None:
    client = MockClient()
    client.set_response("send_group_msg", {"ok": True})
    result = await dispatch(
        client, "onebot_send_group_msg", {"group_id": 123, "message": "hi", "admin_id": 456}
    )
    parsed = json.loads(result)
    assert parsed["ok"] is True


@pytest.mark.asyncio
async def test_dispatch_delete_msg() -> None:
    client = MockClient()
    client.set_response("delete_msg", {"ok": True})
    result = await dispatch(
        client, "onebot_delete_msg", {"message_id": 789, "admin_id": 456}
    )
    parsed = json.loads(result)
    assert parsed["ok"] is True


@pytest.mark.asyncio
async def test_dispatch_unknown_tool() -> None:
    client = MockClient()
    with pytest.raises(ValueError, match="Unknown tool"):
        await dispatch(client, "onebot_nonexistent", {})