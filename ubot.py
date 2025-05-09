import sys
sys.path.extend([
    "/root/telethon_pkg/telethon_install/Telethon",
    "/root/telethon_pkg/telethon_install/rsa",
    "/root/telethon_pkg/telethon_install/pyasn1",
    "/root/telethon_pkg/telethon_install/pyaes"
])

import asyncio
import subprocess
from telethon import TelegramClient, events

# API credentials
api_id = 22997392
api_hash = "8202a02ab5ecd8000e40eec6183f676b"

# User ID yang diizinkan
OWNER_ID = 7734258473

client = TelegramClient('userbot_session', api_id, api_hash)

# Command handler
@client.on(events.NewMessage(incoming=True, outgoing=True))
async def handler(event):
    if event.sender_id != OWNER_ID:
        return

    text = event.raw_text.strip()

    # Ping command
    if text.startswith("!ping") or text == "ping":
        await event.reply("Pong!")
        return

    # Speedtest command
    if text.startswith("!speedtest") or text == "speedtest":
        await event.reply("Running speedtest... Please wait.")
        try:
            # Menjalankan speedtest-cli tanpa argumen tambahan
            result = subprocess.check_output(
                ["speedtest"], stderr=subprocess.STDOUT, timeout=60
            ).decode()

            # Mengambil hanya bagian download, upload, dan link
            download_speed = None
            upload_speed = None
            result_url = None

            for line in result.splitlines():
                if "Download:" in line:
                    download_speed = line.split()[1]
                elif "Upload:" in line:
                    upload_speed = line.split()[1]
                elif "Result URL:" in line:
                    result_url = line.split("Result URL: ")[-1]

            if download_speed and upload_speed and result_url:
                speed_output = (
                    f"Download Speed: {download_speed} Mbps\n"
                    f"Upload Speed: {upload_speed} Mbps\n"
                    f"Test Result: {result_url}"
                )
                await event.reply(f"__**{speed_output}**__", parse_mode="markdown")
            else:
                await event.reply("Failed to get the correct speed test data.", parse_mode="markdown")
        except Exception as e:
            await event.reply(f"Speedtest failed: `{str(e)}`", parse_mode="markdown")
        return

    # Jalankan shell command
    if text.startswith("!$") or text.startswith("$"):
        cmd = text[2:] if text.startswith("!$") else text[1:]
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
            output = result.decode().strip()
            if not output:
                output = "_(no output)_"
        except subprocess.CalledProcessError as e:
            output = f"Error:\n{e.output.decode().strip()}"
        except Exception as e:
            output = f"Exception: `{str(e)}`"

        if len(output) > 4000:
            output = output[:4000] + "\n..."

        await event.reply(f"```{output}```", parse_mode="markdown")

print("Userbot running...")
client.start()
client.run_until_disconnected()
