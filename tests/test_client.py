"""Tests for the OnebotClient HTTP client."""

from __future__ import annotations

import httpx
import pytest
import respx

from onebot_mcp.client import OnebotClient


@pytest.mark.asyncio
async def test_get_login_info(base_url: str, api_key: str) -> None:
    expected = {"user_id": 123456789, "nickname": "TestBot"}
    async with respx.mock:
        respx.get(f"{base_url}/onebot/login_info").mock(
            return_value=httpx.Response(200, json=expected)
        )
        async with OnebotClient(base_url, api_key) as client:
            result = await client.get_login_info()
        assert result == expected


@pytest.mark.asyncio
async def test_get_friend_list(base_url: str, api_key: str) -> None:
    expected = [{"user_id": 123, "nickname": "Alice"}, {"user_id": 456, "nickname": "Bob"}]
    async with respx.mock:
        respx.get(f"{base_url}/onebot/friend_list").mock(
            return_value=httpx.Response(200, json=expected)
        )
        async with OnebotClient(base_url, api_key) as client:
            result = await client.get_friend_list()
        assert result == expected


@pytest.mark.asyncio
async def test_get_group_list(base_url: str, api_key: str) -> None:
    expected = [{"group_id": 111, "group_name": "TestGroup", "member_count": 50}]
    async with respx.mock:
        respx.get(f"{base_url}/onebot/group_list").mock(
            return_value=httpx.Response(200, json=expected)
        )
        async with OnebotClient(base_url, api_key) as client:
            result = await client.get_group_list()
        assert result == expected


@pytest.mark.asyncio
async def test_get_group_info(base_url: str, api_key: str) -> None:
    expected = {"group_id": 111, "group_name": "TestGroup", "member_count": 50}
    async with respx.mock:
        respx.get(f"{base_url}/onebot/group_info").mock(
            return_value=httpx.Response(200, json=expected)
        )
        async with OnebotClient(base_url, api_key) as client:
            result = await client.get_group_info(111)
        assert result == expected


@pytest.mark.asyncio
async def test_get_group_member_list(base_url: str, api_key: str) -> None:
    expected = {
        "group_id": 111,
        "offset": 0,
        "limit": 100,
        "total": 2,
        "members": [
            {"user_id": 123, "nickname": "Alice", "role": "member"},
            {"user_id": 456, "nickname": "Bob", "role": "admin"},
        ],
    }
    async with respx.mock:
        respx.get(f"{base_url}/onebot/group_member_list").mock(
            return_value=httpx.Response(200, json=expected)
        )
        async with OnebotClient(base_url, api_key) as client:
            result = await client.get_group_member_list(111, limit=100, offset=0)
        assert result == expected


@pytest.mark.asyncio
async def test_get_group_member_info(base_url: str, api_key: str) -> None:
    expected = {"user_id": 123, "nickname": "Alice", "role": "member", "card": ""}
    async with respx.mock:
        respx.get(f"{base_url}/onebot/group_member_info").mock(
            return_value=httpx.Response(200, json=expected)
        )
        async with OnebotClient(base_url, api_key) as client:
            result = await client.get_group_member_info(111, 123)
        assert result == expected


@pytest.mark.asyncio
async def test_get_stranger_info(base_url: str, api_key: str) -> None:
    expected = {"user_id": 789, "nickname": "Charlie", "sex": "male", "age": 25}
    async with respx.mock:
        respx.get(f"{base_url}/onebot/stranger_info").mock(
            return_value=httpx.Response(200, json=expected)
        )
        async with OnebotClient(base_url, api_key) as client:
            result = await client.get_stranger_info(789)
        assert result == expected


@pytest.mark.asyncio
async def test_get_msg(base_url: str, api_key: str) -> None:
    expected = {"message_id": 42, "message": [{"type": "text", "data": {"text": "hello"}}]}
    async with respx.mock:
        respx.get(f"{base_url}/onebot/get_msg").mock(
            return_value=httpx.Response(200, json=expected)
        )
        async with OnebotClient(base_url, api_key) as client:
            result = await client.get_msg(42)
        assert result == expected


@pytest.mark.asyncio
async def test_unauthorized(base_url: str, api_key: str) -> None:
    async with respx.mock:
        respx.get(f"{base_url}/onebot/friend_list").mock(
            return_value=httpx.Response(401, json={"error": "unauthorized"})
        )
        async with OnebotClient(base_url, api_key) as client:
            with pytest.raises(httpx.HTTPStatusError):
                await client.get_friend_list()


@pytest.mark.asyncio
async def test_auth_header_sent(base_url: str, api_key: str) -> None:
    async with respx.mock:
        route = respx.get(f"{base_url}/onebot/login_info").mock(
            return_value=httpx.Response(200, json={})
        )
        async with OnebotClient(base_url, api_key) as client:
            await client.get_login_info()
        request = route.calls[0].request
        assert request.headers.get("authorization") == f"Bearer {api_key}"