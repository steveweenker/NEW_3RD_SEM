import asyncio
import os
import time
import aiohttp
import zipfile
from io import BytesIO
from datetime import datetime
from typing import Optional, List

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
URL = "https://results.beup.ac.in/BTech4thSem2024_B2022Results.aspx"

CHECK_INTERVAL = 2
CONTINUOUS_DURATION = 900
SCHEDULED_INTERVAL = 7200

RESULT_URLS = [
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148040",
    # ... add all other URLs ...
]

class DiscordMonitor:
    def __init__(self):
        self.last_status: Optional[str] = None
        self.last_scheduled_time: float = 0
        self.rate_limit_remaining = 5
        self.rate_limit_reset = 0

    async def send_discord_message(self, content: str, username: str = "BEUP Monitor") -> bool:
        if not DISCORD_WEBHOOK_URL:
            return False
        now = time.time()
        if self.rate_limit_remaining <= 0 and now < self.rate_limit_reset:
            await asyncio.sleep(self.rate_limit_reset - now)
        payload = {"content": content, "username": username}
        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, json=payload) as resp:
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
                reset_after = resp.headers.get("X-RateLimit-Reset-After")
                if reset_after:
                    self.rate_limit_reset = now + float(reset_after)
                if resp.status == 429:
                    retry = float(resp.headers.get("retry-after", 1))
                    await asyncio.sleep(retry)
                    return await self.send_discord_message(content, username)
                return resp.status in (200, 204)

    async def send_file(self, filename: str, data: BytesIO) -> bool:
        form = aiohttp.FormData()
        data.seek(0)
        ctype = "application/zip" if filename.endswith(".zip") else "text/html"
        form.add_field("file", data, filename=filename, content_type=ctype)
        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, data=form) as resp:
                now = time.time()
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
                reset_after = resp.headers.get("X-RateLimit-Reset-After")
                if reset_after:
                    self.rate_limit_reset = now + float(reset_after)
                if resp.status == 429:
                    retry = float(resp.headers.get("retry-after", 1))
                    await asyncio.sleep(retry)
                    return await self.send_file(filename, data)
                return resp.status in (200, 204)

    async def check_site(self) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, timeout=10) as resp:
                    return "UP" if resp.status == 200 else "DOWN"
        except:
            return "DOWN"

    async def download_and_zip(self) -> BytesIO:
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            async with aiohttp.ClientSession() as session:
                for idx, url in enumerate(RESULT_URLS, start=1):
                    reg = url.split("=")[-1]
                    try:
                        async with session.get(url, timeout=10) as resp:
                            if resp.status == 200:
                                html = await resp.text()
                                zf.writestr(f"result_{reg}.html", html)
                    except Exception:
                        pass
                    if idx % 10 == 0 or idx == len(RESULT_URLS):
                        await self.send_discord_message(f"🔄 Downloaded & added to ZIP: {idx}/{len(RESULT_URLS)}")
        buffer.seek(0)
        return buffer

    async def continuous_status(self):
        end = time.time() + CONTINUOUS_DURATION
        while time.time() < end:
            left = int(end - time.time())
            await self.send_discord_message(f"✅ Website still UP ({left}s left)")
            await asyncio.sleep(CHECK_INTERVAL)

    async def run(self):
        await self.send_discord_message("🔍 Monitoring started")
        while True:
            current = await self.check_site()
            now = time.time()
            changed = current != self.last_status
            scheduled_due = (now - self.last_scheduled_time) >= SCHEDULED_INTERVAL

            if changed:
                if current == "UP":
                    await self.send_discord_message("🎉 WEBSITE IS NOW LIVE! Starting download…")
                    zip_data = await self.download_and_zip()
                    if await self.send_file("results.zip", zip_data):
                        await self.send_discord_message(f"📥 Uploaded all {len(RESULT_URLS)} results as ZIP")
                    else:
                        await self.send_discord_message("⚠️ ZIP upload failed; sending individual files")
                        async with aiohttp.ClientSession() as session:
                            for idx, url in enumerate(RESULT_URLS, start=1):
                                reg = url.split("=")[-1]
                                try:
                                    async with session.get(url, timeout=10) as resp:
                                        if resp.status == 200:
                                            bio = BytesIO((await resp.text()).encode("utf-8"))
                                            await self.send_file(f"result_{reg}.html", bio)
                                except:
                                    pass
                                if idx % 10 == 0 or idx == len(RESULT_URLS):
                                    await self.send_discord_message(f"🔄 Fallback uploaded {idx}/{len(RESULT_URLS)}")
                        await self.send_discord_message("📥 Individual files uploaded")
                    self.last_scheduled_time = now
                    await self.continuous_status()
                    # At end of continuous, send immediate scheduled update
                    await self.send_discord_message("📅 Scheduled update: Website is UP")
                    self.last_scheduled_time = time.time()
                else:
                    await self.send_discord_message("🔴 WEBSITE IS DOWN")
                    self.last_scheduled_time = now

            elif scheduled_due:
                emoji = "✅" if current == "UP" else "🔴"
                await self.send_discord_message(f"{emoji} Scheduled update: Website is {current}")
                self.last_scheduled_time = now

            self.last_status = current
            await asyncio.sleep(CHECK_INTERVAL)

async def main():
    monitor = DiscordMonitor()
    try:
        await monitor.run()
    except Exception as e:
        import traceback
        print("❌ Exception in monitor:", e)
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(main())
