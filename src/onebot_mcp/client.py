"""HTTP client for the OneBot API bridge exposed by kovi-plugin-hermes."""

from __future__ import annotations

import os
from typing import Any

import httpx


class OnebotClient:
    """Async HTTP client for the OneBot REST API."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self._base_url = base_url or os.environ.get("ONEBOT_API_BASE", "http://localhost:5801")
        self._api_key = api_key or os.environ.get("ONEBOT_API_KEY", "")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=30.0,
        )

    # ── Read operations ──

    async def get_login_info(self) -> dict[str, Any]:
        resp = await self._client.get("/onebot/login_info")
        resp.raise_for_status()
        return resp.json()

    async def get_friend_list(self) -> list[dict[str, Any]]:
        resp = await self._client.get("/onebot/friend_list")
        resp.raise_for_status()
        return resp.json()

    async def get_group_list(self) -> list[dict[str, Any]]:
        resp = await self._client.get("/onebot/group_list")
        resp.raise_for_status()
        return resp.json()

    async def get_group_info(self, group_id: int, *, no_cache: bool = False) -> dict[str, Any]:
        params: dict[str, Any] = {"group_id": group_id}
        if no_cache:
            params["no_cache"] = True
        resp = await self._client.get("/onebot/group_info", params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_group_member_list(
        self,
        group_id: int,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        resp = await self._client.get(
            "/onebot/group_member_list",
            params={"group_id": group_id, "limit": limit, "offset": offset},
        )
        resp.raise_for_status()
        return resp.json()

    async def get_group_member_info(
        self,
        group_id: int,
        user_id: int,
        *,
        no_cache: bool = False,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"group_id": group_id, "user_id": user_id}
        if no_cache:
            params["no_cache"] = True
        resp = await self._client.get("/onebot/group_member_info", params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_stranger_info(
        self,
        user_id: int,
        *,
        no_cache: bool = False,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"user_id": user_id}
        if no_cache:
            params["no_cache"] = True
        resp = await self._client.get("/onebot/stranger_info", params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_msg(self, message_id: int) -> dict[str, Any]:
        resp = await self._client.get("/onebot/get_msg", params={"message_id": message_id})
        resp.raise_for_status()
        return resp.json()

    async def get_forward_msg(self, id: str) -> dict[str, Any]:
        resp = await self._client.get("/onebot/get_forward_msg", params={"id": id})
        resp.raise_for_status()
        return resp.json()

    async def get_group_honor_info(
        self,
        group_id: int,
        *,
        honor_type: str = "all",
    ) -> dict[str, Any]:
        resp = await self._client.get(
            "/onebot/group_honor_info",
            params={"group_id": group_id, "honor_type": honor_type},
        )
        resp.raise_for_status()
        return resp.json()

    async def get_status(self) -> dict[str, Any]:
        resp = await self._client.get("/onebot/status")
        resp.raise_for_status()
        return resp.json()

    async def get_version_info(self) -> dict[str, Any]:
        resp = await self._client.get("/onebot/version_info")
        resp.raise_for_status()
        return resp.json()

    async def can_send_image(self) -> dict[str, Any]:
        resp = await self._client.get("/onebot/can_send_image")
        resp.raise_for_status()
        return resp.json()

    async def can_send_record(self) -> dict[str, Any]:
        resp = await self._client.get("/onebot/can_send_record")
        resp.raise_for_status()
        return resp.json()

    async def get_cookies(self, domain: str) -> dict[str, Any]:
        resp = await self._client.get("/onebot/cookies", params={"domain": domain})
        resp.raise_for_status()
        return resp.json()

    async def get_csrf_token(self) -> dict[str, Any]:
        resp = await self._client.get("/onebot/csrf_token")
        resp.raise_for_status()
        return resp.json()

    async def get_credentials(self, domain: str) -> dict[str, Any]:
        resp = await self._client.get("/onebot/credentials", params={"domain": domain})
        resp.raise_for_status()
        return resp.json()

    async def get_record(self, file: str, out_format: str) -> dict[str, Any]:
        resp = await self._client.get(
            "/onebot/record", params={"file": file, "out_format": out_format}
        )
        resp.raise_for_status()
        return resp.json()

    async def get_image(self, file: str) -> dict[str, Any]:
        resp = await self._client.get("/onebot/image", params={"file": file})
        resp.raise_for_status()
        return resp.json()

    # ── NapCat extended: read ──

    async def get_group_msg_history(
        self, group_id: int, *, message_seq: int | None = None, count: int | None = None, reverse: bool | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"group_id": group_id}
        if message_seq is not None:
            params["message_seq"] = message_seq
        if count is not None:
            params["count"] = count
        if reverse is not None:
            params["reverse"] = reverse
        resp = await self._client.get("/onebot/get_group_msg_history", params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_group_file_system_info(self, group_id: int) -> dict[str, Any]:
        resp = await self._client.get("/onebot/get_group_file_system_info", params={"group_id": group_id})
        resp.raise_for_status()
        return resp.json()

    async def get_group_root_files(self, group_id: int) -> dict[str, Any]:
        resp = await self._client.get("/onebot/get_group_root_files", params={"group_id": group_id})
        resp.raise_for_status()
        return resp.json()

    async def get_group_files_by_folder(self, group_id: int, folder_id: str) -> dict[str, Any]:
        resp = await self._client.get(
            "/onebot/get_group_files_by_folder",
            params={"group_id": group_id, "folder_id": folder_id},
        )
        resp.raise_for_status()
        return resp.json()

    async def get_group_file_url(self, group_id: int, file_id: str) -> dict[str, Any]:
        resp = await self._client.get(
            "/onebot/get_group_file_url",
            params={"group_id": group_id, "file_id": file_id},
        )
        resp.raise_for_status()
        return resp.json()

    async def get_file(self, *, file_id: str | None = None, file: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if file_id is not None:
            params["file_id"] = file_id
        if file is not None:
            params["file"] = file
        resp = await self._client.get("/onebot/get_file", params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_group_at_all_remain(self, group_id: int) -> dict[str, Any]:
        resp = await self._client.get("/onebot/get_group_at_all_remain", params={"group_id": group_id})
        resp.raise_for_status()
        return resp.json()

    async def get_essence_msg_list(self, group_id: int) -> dict[str, Any]:
        resp = await self._client.get("/onebot/get_essence_msg_list", params={"group_id": group_id})
        resp.raise_for_status()
        return resp.json()

    # ── Write operations ──

    async def send_group_msg(self, group_id: int, message: str | list, *, admin_id: int) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/send_group_msg",
            json={"group_id": group_id, "message": message},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def send_private_msg(self, user_id: int, message: str | list, *, admin_id: int) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/send_private_msg",
            json={"user_id": user_id, "message": message},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_ban(
        self, group_id: int, user_id: int, *, duration: int = 0, admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_ban",
            json={"group_id": group_id, "user_id": user_id, "duration": duration},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_whole_ban(
        self, group_id: int, *, enable: bool, admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_whole_ban",
            json={"group_id": group_id, "enable": enable},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_kick(
        self, group_id: int, user_id: int, *, reject_add_request: bool = False, admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_kick",
            json={"group_id": group_id, "user_id": user_id, "reject_add_request": reject_add_request},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def delete_msg(self, message_id: int, *, admin_id: int) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/delete_msg",
            json={"message_id": message_id},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def send_like(self, user_id: int, *, times: int = 1, admin_id: int) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/send_like",
            json={"user_id": user_id, "times": times},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_whole_ban(
        self, group_id: int, *, enable: bool, admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_whole_ban",
            json={"group_id": group_id, "enable": enable},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_admin(
        self, group_id: int, user_id: int, *, enable: bool, admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_admin",
            json={"group_id": group_id, "user_id": user_id, "enable": enable},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_anonymous(
        self, group_id: int, *, enable: bool, admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_anonymous",
            json={"group_id": group_id, "enable": enable},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_anonymous_ban(
        self, group_id: int, *, duration: int = 0, admin_id: int,
        anonymous: dict | None = None, flag: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"group_id": group_id, "duration": duration}
        if anonymous is not None:
            body["anonymous"] = anonymous
        if flag is not None:
            body["flag"] = flag
        resp = await self._client.post(
            "/onebot/set_group_anonymous_ban",
            json=body,
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_card(
        self, group_id: int, user_id: int, *, card: str = "", admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_card",
            json={"group_id": group_id, "user_id": user_id, "card": card},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_name(
        self, group_id: int, *, group_name: str, admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_name",
            json={"group_id": group_id, "group_name": group_name},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_leave(
        self, group_id: int, *, is_dismiss: bool = False, admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_leave",
            json={"group_id": group_id, "is_dismiss": is_dismiss},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_special_title(
        self, group_id: int, user_id: int, *, special_title: str = "", admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_special_title",
            json={"group_id": group_id, "user_id": user_id, "special_title": special_title},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_friend_add_request(
        self, flag: str, *, approve: bool = True, remark: str = "", admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_friend_add_request",
            json={"flag": flag, "approve": approve, "remark": remark},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_group_add_request(
        self, flag: str, *, type_: str = "add", approve: bool = True, reason: str = "", admin_id: int
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_group_add_request",
            json={"flag": flag, "type": type_, "approve": approve, "reason": reason},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def clean_cache(self, *, admin_id: int) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/clean_cache",
            json={},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    # ── NapCat extended: write ──

    async def download_file(
        self, url: str, *, thread_cnt: int | None = None, headers: str | None = None, admin_id: int,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"url": url}
        if thread_cnt is not None:
            body["thread_cnt"] = thread_cnt
        if headers is not None:
            body["headers"] = headers
        resp = await self._client.post(
            "/onebot/download_file",
            json=body,
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def upload_group_file(
        self, group_id: int, file: str, name: str, *, folder: str | None = None, admin_id: int,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"group_id": group_id, "file": file, "name": name}
        if folder is not None:
            body["folder"] = folder
        resp = await self._client.post(
            "/onebot/upload_group_file",
            json=body,
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def upload_private_file(
        self, user_id: int, file: str, name: str, *, admin_id: int,
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/upload_private_file",
            json={"user_id": user_id, "file": file, "name": name},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def delete_group_file(
        self, group_id: int, file_id: str, *, busid: int | None = None, admin_id: int,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"group_id": group_id, "file_id": file_id}
        if busid is not None:
            body["busid"] = busid
        resp = await self._client.post(
            "/onebot/delete_group_file",
            json=body,
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def create_group_file_folder(
        self, group_id: int, name: str, *, parent_id: str | None = None, admin_id: int,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"group_id": group_id, "name": name}
        if parent_id is not None:
            body["parent_id"] = parent_id
        resp = await self._client.post(
            "/onebot/create_group_file_folder",
            json=body,
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def delete_group_folder(
        self, group_id: int, folder_id: str, *, admin_id: int,
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/delete_group_folder",
            json={"group_id": group_id, "folder_id": folder_id},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def set_essence_msg(self, message_id: int, *, admin_id: int) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/set_essence_msg",
            json={"message_id": message_id},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def delete_essence_msg(self, message_id: int, *, admin_id: int) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/delete_essence_msg",
            json={"message_id": message_id},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def send_group_forward_msg(
        self, group_id: int, messages: list | dict, *, admin_id: int,
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/onebot/send_group_forward_msg",
            json={"group_id": group_id, "messages": messages},
            headers={"X-Admin-Id": str(admin_id)},
        )
        resp.raise_for_status()
        return resp.json()

    # ── Lifecycle ──

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> OnebotClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()