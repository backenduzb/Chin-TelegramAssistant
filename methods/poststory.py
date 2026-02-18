import os
import json
import aiohttp
import asyncio
import aiofiles
import tempfile
from aiogram import types
from config.settings import BOT_TOKEN

_story_lock = asyncio.Lock()
ALLOWED_PERIODS = {21600, 43200, 86400, 172800}

async def _download_from_telegram_file_server(bot_token: str, file_path: str, dst_path: str):
    url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

    timeout = aiohttp.ClientTimeout(total=240, connect=20, sock_read=180)
    connector = aiohttp.TCPConnector(force_close=True, limit=2)
    headers = {"Expect": "", "Connection": "close"}

    async with aiohttp.ClientSession(timeout=timeout, headers=headers, connector=connector) as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            async with aiofiles.open(dst_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 256):
                    await f.write(chunk)


async def post_story(message: types.Message, caption: str, life_time: int, video_file_id: str):
    from config.settings import BS_ID

    if not BS_ID or not video_file_id:
        return False
    if life_time not in ALLOWED_PERIODS:
        life_time = 86400

    tmp_path = None
    try:
        async with _story_lock:
            assert message.bot is not None
            tg_file = await asyncio.wait_for(message.bot.get_file(video_file_id), timeout=25)
            tmp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            tmp_path = tmp_file.name
            tmp_file.close()  
            assert tg_file.file_path is not None
            await asyncio.wait_for(
                _download_from_telegram_file_server(BOT_TOKEN, tg_file.file_path, tmp_path),
                timeout=260
            )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/postStory"
        attach_name = "story_video"
        content = {"type": "video", "video": f"attach://{attach_name}"}

        timeout = aiohttp.ClientTimeout(total=180, connect=20, sock_read=180)
        connector = aiohttp.TCPConnector(force_close=True, limit=2)
        headers = {"Expect": "", "Connection": "close"}

        for attempt in range(3):
            try:
                form = aiohttp.FormData()
                form.add_field("business_connection_id", BS_ID)
                form.add_field("content", json.dumps(content))
                form.add_field("active_period", str(life_time))
                form.add_field("caption", caption or "")

                async with aiofiles.open(tmp_path, "rb") as vf:
                    form.add_field(
                        attach_name,
                        await vf.read(),
                        filename="video.mp4",
                        content_type="video/mp4",
                    )

                async with aiohttp.ClientSession(timeout=timeout, headers=headers, connector=connector) as session:
                    async with session.post(url, data=form) as resp:
                        raw = await resp.text()

                        if resp.status == 429:
                            try:
                                j = json.loads(raw)
                                wait_s = int(j.get("parameters", {}).get("retry_after", 2))
                            except Exception:
                                wait_s = 2
                            await asyncio.sleep(wait_s + 0.5)
                            continue

                        if resp.status >= 500:
                            await asyncio.sleep(2.0 + attempt)
                            continue

                        try:
                            data = json.loads(raw)
                        except json.JSONDecodeError:
                            return False

                        return bool(data.get("ok"))

            except (asyncio.TimeoutError, aiohttp.ClientError):
                await asyncio.sleep(2.0 + attempt)
                continue

        return False

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
