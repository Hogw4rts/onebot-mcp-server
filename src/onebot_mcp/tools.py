"""MCP tool definitions for the OneBot API."""

from __future__ import annotations

from mcp.types import Tool

TOOLS: list[Tool] = [
    # ── Read-only tools ──
    Tool(
        name="onebot_get_login_info",
        description="Get the bot's own QQ account info (user_id, nickname). Use this to confirm the bot's identity.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="onebot_get_friend_list",
        description="Get the bot's QQ friend list. Returns friends with user_id, nickname, and remark.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="onebot_get_group_list",
        description="Get all QQ groups the bot has joined. Returns group_id, group_name, member_count.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="onebot_get_group_info",
        description="Get detailed info about a specific QQ group.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID to query",
                },
                "no_cache": {
                    "type": "boolean",
                    "description": "Bypass cache and fetch fresh data (default: false)",
                    "default": False,
                },
            },
            "required": ["group_id"],
        },
    ),
    Tool(
        name="onebot_get_group_members",
        description="Get member list of a QQ group. Paginated with user_id, nickname, card, role.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID to query members for",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of members to return (default: 100, max: 200)",
                    "default": 100,
                },
                "offset": {
                    "type": "integer",
                    "description": "Offset for pagination (default: 0)",
                    "default": 0,
                },
            },
            "required": ["group_id"],
        },
    ),
    Tool(
        name="onebot_get_member_info",
        description="Get detailed info about a specific group member, including their role, card, join time, etc.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "user_id": {
                    "type": "integer",
                    "description": "The QQ user ID of the member",
                },
                "no_cache": {
                    "type": "boolean",
                    "description": "Bypass cache (default: false)",
                    "default": False,
                },
            },
            "required": ["group_id", "user_id"],
        },
    ),
    Tool(
        name="onebot_get_user_info",
        description="Get info about a QQ user (works for non-friends too). Returns user_id, nickname, sex, age.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The QQ user ID to look up",
                },
                "no_cache": {
                    "type": "boolean",
                    "description": "Bypass cache (default: false)",
                    "default": False,
                },
            },
            "required": ["user_id"],
        },
    ),
    Tool(
        name="onebot_get_message",
        description="Get a QQ message by its message ID. Returns the message content, sender info, and timestamp.",
        inputSchema={
            "type": "object",
            "properties": {
                "message_id": {
                    "type": "integer",
                    "description": "The QQ message ID to retrieve",
                },
            },
            "required": ["message_id"],
        },
    ),
    Tool(
        name="onebot_get_forward_msg",
        description="Get content of a forwarded (combined) message by its resId. Returns all nested messages.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "The resId of the forwarded message",
                },
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="onebot_get_group_honor_info",
        description="Get honor info for a QQ group. Returns talkative king, performer, legend, etc.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "honor_type": {
                    "type": "string",
                    "description": "Honor type: talkative, performer, legend, strong_newbie, or all (default: all)",
                    "default": "all",
                },
            },
            "required": ["group_id"],
        },
    ),
    Tool(
        name="onebot_get_status",
        description="Get the bot's running status. Returns online state, plugin statistics, etc.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="onebot_get_version_info",
        description="Get version info of the OneBot implementation. Returns app name, version, protocol info.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="onebot_can_send_image",
        description="Check if the bot can send images. Returns whether image sending is supported.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="onebot_can_send_record",
        description="Check if the bot can send voice records. Returns whether record sending is supported.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="onebot_get_cookies",
        description="Get Cookies for a specific domain from the OneBot implementation.",
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The domain to get cookies for",
                },
            },
            "required": ["domain"],
        },
    ),
    Tool(
        name="onebot_get_csrf_token",
        description="Get the CSRF token from the OneBot implementation.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="onebot_get_credentials",
        description="Get credentials (Cookies + CSRF Token) for a specific domain.",
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The domain to get credentials for",
                },
            },
            "required": ["domain"],
        },
    ),
    Tool(
        name="onebot_get_record",
        description="Get a voice record file. Converts to the specified format.",
        inputSchema={
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "The voice file name (from message segment file parameter)",
                },
                "out_format": {
                    "type": "string",
                    "description": "Target format: mp3, amr, wma, m4a, spx, ogg, wav, flac",
                },
            },
            "required": ["file", "out_format"],
        },
    ),
    Tool(
        name="onebot_get_image",
        description="Get an image file info. Returns the image file path or URL.",
        inputSchema={
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "The image file name (from message segment file parameter)",
                },
            },
            "required": ["file"],
        },
    ),
    # ── NapCat extended: read ──
    Tool(
        name="onebot_get_group_msg_history",
        description="Get recent message history of a QQ group. Returns messages with their IDs, senders, and content.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "message_seq": {
                    "type": "integer",
                    "description": "Start from this message sequence number (optional)",
                },
                "count": {
                    "type": "integer",
                    "description": "Number of messages to return (default: 20)",
                },
                "reverse": {
                    "type": "boolean",
                    "description": "Whether to return in reverse order (default: false)",
                },
            },
            "required": ["group_id"],
        },
    ),
    Tool(
        name="onebot_get_group_file_system_info",
        description="Get file system info for a QQ group (total count, used space).",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
            },
            "required": ["group_id"],
        },
    ),
    Tool(
        name="onebot_get_group_root_files",
        description="List files and folders in the root directory of a QQ group's file system.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
            },
            "required": ["group_id"],
        },
    ),
    Tool(
        name="onebot_get_group_files_by_folder",
        description="List files in a specific folder of a QQ group's file system.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "folder_id": {
                    "type": "string",
                    "description": "The folder ID to list files from",
                },
            },
            "required": ["group_id", "folder_id"],
        },
    ),
    Tool(
        name="onebot_get_group_file_url",
        description="Get the download URL for a file in a QQ group's file system.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "file_id": {
                    "type": "string",
                    "description": "The file ID to get URL for",
                },
            },
            "required": ["group_id", "file_id"],
        },
    ),
    Tool(
        name="onebot_get_file",
        description="Get file info by file_id or file path. Returns file URL, base64 data, or local path.",
        inputSchema={
            "type": "object",
            "properties": {
                "file_id": {
                    "type": "string",
                    "description": "The file ID (optional, use file_id or file)",
                },
                "file": {
                    "type": "string",
                    "description": "The file path/name (optional, use file_id or file)",
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="onebot_get_group_at_all_remain",
        description="Get remaining count of @all (mention all members) for the bot in a QQ group.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
            },
            "required": ["group_id"],
        },
    ),
    Tool(
        name="onebot_get_essence_msg_list",
        description="Get the list of pinned/essence messages in a QQ group.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
            },
            "required": ["group_id"],
        },
    ),
    # ── Write tools (require admin_id) ──
    Tool(
        name="onebot_send_group_msg",
        description="Send a message to a QQ group. Supports plain text or rich message segments (text, image, at, reply, face). Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID to send to",
                },
                "message": {
                    "oneOf": [
                        {"type": "string", "description": "Plain text message"},
                        {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "description": "Segment type: text, image, at, reply, face",
                                    },
                                    "data": {
                                        "type": "object",
                                        "description": "Segment data. text:{text}, image:{file}, at:{qq}, reply:{id}, face:{id}",
                                    },
                                },
                                "required": ["type", "data"],
                            },
                            "description": "Array of message segments for rich content",
                        },
                    ],
                    "description": "Message content: plain text string or array of message segments",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "message", "admin_id"],
        },
    ),
    Tool(
        name="onebot_send_private_msg",
        description="Send a private message to a QQ user. Supports plain text or rich message segments (text, image, at, reply, face). Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The QQ user ID to send to",
                },
                "message": {
                    "oneOf": [
                        {"type": "string", "description": "Plain text message"},
                        {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "description": "Segment type: text, image, at, reply, face",
                                    },
                                    "data": {
                                        "type": "object",
                                        "description": "Segment data. text:{text}, image:{file}, at:{qq}, reply:{id}, face:{id}",
                                    },
                                },
                                "required": ["type", "data"],
                            },
                            "description": "Array of message segments for rich content",
                        },
                    ],
                    "description": "Message content: plain text string or array of message segments",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["user_id", "message", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_ban",
        description="Mute (ban) a member in a QQ group. Set duration to 0 to unmute. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "user_id": {
                    "type": "integer",
                    "description": "The QQ user ID to mute",
                },
                "duration": {
                    "type": "integer",
                    "description": "Mute duration in seconds (0 to unmute, default: 0)",
                    "default": 0,
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "user_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_whole_ban",
        description="Enable or disable all-member mute (whole ban) in a QQ group. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "enable": {
                    "type": "boolean",
                    "description": "True to enable whole-group mute, False to disable",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "enable", "admin_id"],
        },
    ),
    Tool(
        name="onebot_send_like",
        description="Send a like to a QQ user. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The QQ user ID to send likes to",
                },
                "times": {
                    "type": "integer",
                    "description": "Number of likes to send (default: 1)",
                    "default": 1,
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["user_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_admin",
        description="Set or remove a group member as admin. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "user_id": {
                    "type": "integer",
                    "description": "The QQ user ID to set as admin",
                },
                "enable": {
                    "type": "boolean",
                    "description": "True to set as admin, False to remove admin",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "user_id", "enable", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_anonymous",
        description="Enable or disable anonymous chat in a QQ group. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "enable": {
                    "type": "boolean",
                    "description": "True to enable anonymous, False to disable",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "enable", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_anonymous_ban",
        description="Mute an anonymous user in a QQ group. Provide either 'anonymous' object or 'flag'. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "anonymous": {
                    "type": "object",
                    "description": "The anonymous user object (from group message report)",
                },
                "flag": {
                    "type": "string",
                    "description": "The anonymous user flag (from group message report)",
                },
                "duration": {
                    "type": "integer",
                    "description": "Mute duration in seconds (default: 0)",
                    "default": 0,
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_card",
        description="Set a group member's card (nickname in group). Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "user_id": {
                    "type": "integer",
                    "description": "The QQ user ID",
                },
                "card": {
                    "type": "string",
                    "description": "The new group card text (empty string to remove)",
                    "default": "",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "user_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_name",
        description="Rename a QQ group. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "group_name": {
                    "type": "string",
                    "description": "The new group name",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "group_name", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_leave",
        description="Make the bot leave a QQ group. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID to leave",
                },
                "is_dismiss": {
                    "type": "boolean",
                    "description": "Whether to dismiss the group (only works if bot is owner, default: false)",
                    "default": False,
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_special_title",
        description="Set a group member's special title. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "user_id": {
                    "type": "integer",
                    "description": "The QQ user ID",
                },
                "special_title": {
                    "type": "string",
                    "description": "The special title text (empty string to remove)",
                    "default": "",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "user_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_friend_add_request",
        description="Approve or reject a friend add request. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "flag": {
                    "type": "string",
                    "description": "The request flag (from the request event)",
                },
                "approve": {
                    "type": "boolean",
                    "description": "Whether to approve the request (default: true)",
                    "default": True,
                },
                "remark": {
                    "type": "string",
                    "description": "Friend remark if approved (default: empty)",
                    "default": "",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["flag", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_add_request",
        description="Approve or reject a group join request/invite. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "flag": {
                    "type": "string",
                    "description": "The request flag (from the request event)",
                },
                "type": {
                    "type": "string",
                    "description": "Request type: 'add' or 'invite'",
                    "default": "add",
                },
                "approve": {
                    "type": "boolean",
                    "description": "Whether to approve (default: true)",
                    "default": True,
                },
                "reason": {
                    "type": "string",
                    "description": "Rejection reason (only used when rejecting, default: empty)",
                    "default": "",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["flag", "admin_id"],
        },
    ),
    Tool(
        name="onebot_clean_cache",
        description="Clean the OneBot server cache. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["admin_id"],
        },
    ),
    # ── NapCat extended: write ──
    Tool(
        name="onebot_download_file",
        description="Download a file from URL to the OneBot server cache directory. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to download the file from",
                },
                "thread_cnt": {
                    "type": "integer",
                    "description": "Number of download threads (optional)",
                },
                "headers": {
                    "type": "string",
                    "description": "Custom HTTP headers as JSON string (optional)",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["url", "admin_id"],
        },
    ),
    Tool(
        name="onebot_upload_group_file",
        description="Upload a file to a QQ group's file system. The file path must be accessible by the OneBot server. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID to upload to",
                },
                "file": {
                    "type": "string",
                    "description": "The file path on the server (e.g. /path/to/file.pdf)",
                },
                "name": {
                    "type": "string",
                    "description": "The display name for the uploaded file",
                },
                "folder": {
                    "type": "string",
                    "description": "The target folder ID (optional, uploads to root if not specified)",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "file", "name", "admin_id"],
        },
    ),
    Tool(
        name="onebot_upload_private_file",
        description="Upload a file to a QQ user in private chat. The file path must be accessible by the OneBot server. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The QQ user ID to send the file to",
                },
                "file": {
                    "type": "string",
                    "description": "The file path on the server (e.g. /path/to/file.pdf)",
                },
                "name": {
                    "type": "string",
                    "description": "The display name for the uploaded file",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["user_id", "file", "name", "admin_id"],
        },
    ),
    Tool(
        name="onebot_delete_group_file",
        description="Delete a file from a QQ group's file system. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "file_id": {
                    "type": "string",
                    "description": "The file ID to delete",
                },
                "busid": {
                    "type": "integer",
                    "description": "The bus ID (optional, file system type)",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "file_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_create_group_file_folder",
        description="Create a folder in a QQ group's file system. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "name": {
                    "type": "string",
                    "description": "The folder name to create",
                },
                "parent_id": {
                    "type": "string",
                    "description": "Parent folder ID (optional, creates in root if not specified)",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "name", "admin_id"],
        },
    ),
    Tool(
        name="onebot_delete_group_folder",
        description="Delete a folder from a QQ group's file system. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "folder_id": {
                    "type": "string",
                    "description": "The folder ID to delete",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "folder_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_essence_msg",
        description="Pin a message as essence (精华消息) in a QQ group. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "message_id": {
                    "type": "integer",
                    "description": "The message ID to pin as essence",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["message_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_delete_essence_msg",
        description="Remove a message from essence (精华消息) in a QQ group. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "message_id": {
                    "type": "integer",
                    "description": "The message ID to remove from essence",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["message_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_send_group_forward_msg",
        description="Send a combined/forwarded message to a QQ group. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID to send to",
                },
                "messages": {
                    "type": "array",
                    "description": "Array of forward message nodes. Each node: {type: 'node',  {id: 'msg_id'} or {name: 'sender', content: [...]}}",
                    "items": {
                        "type": "object",
                    },
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "messages", "admin_id"],
        },
    ),
    Tool(
        name="onebot_set_group_kick",
        description="Kick a member from a QQ group. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The QQ group ID",
                },
                "user_id": {
                    "type": "integer",
                    "description": "The QQ user ID to kick",
                },
                "reject_add_request": {
                    "type": "boolean",
                    "description": "Whether to reject future join requests from this user (default: false)",
                    "default": False,
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["group_id", "user_id", "admin_id"],
        },
    ),
    Tool(
        name="onebot_delete_msg",
        description="Recall (delete) a QQ message. Requires admin authorization.",
        inputSchema={
            "type": "object",
            "properties": {
                "message_id": {
                    "type": "integer",
                    "description": "The QQ message ID to recall",
                },
                "admin_id": {
                    "type": "integer",
                    "description": "QQ user ID of the admin authorizing this action",
                },
            },
            "required": ["message_id", "admin_id"],
        },
    ),
]