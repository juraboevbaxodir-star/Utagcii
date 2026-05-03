import asyncio
from pyrogram import Client, filters

api_id = 35471292
api_hash = "20da303e770bc8d197df96c24c853c69"

app = Client("my_account", api_id=api_id, api_hash=api_hash)

is_running = False

@app.on_message(filters.command(["utag", "u"], prefixes=[".", "/"]))
async def start_tagging(client, message):
    global is_running
    
    if is_running:
        return

    text_to_send = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    
    is_running = True
    chat_id = message.chat.id

    async for member in client.get_chat_members(chat_id):
        if not is_running:
            break

        if member.user.is_bot or member.user.is_deleted:
            continue

        try:
            mention = f"[{member.user.first_name}](tg://user?id={member.user.id})"
            await client.send_message(chat_id, f"{mention} {text_to_send}")
            await asyncio.sleep(2.5)

        except Exception:
            await asyncio.sleep(5)

    is_running = False


@app.on_message(filters.command(["utagstop", "s"], prefixes=[".", "/"]))
async def stop_tagging(client, message):
    global is_running
    is_running = False


app.run()
