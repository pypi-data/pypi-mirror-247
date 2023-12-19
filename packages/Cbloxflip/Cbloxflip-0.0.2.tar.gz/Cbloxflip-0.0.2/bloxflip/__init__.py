import json, time, asyncio, requests, websockets

class user:
    async def info(auth):
        headers={"x-auth-token": auth, "User-Agent": "Mozilla/5.0 (Linux; Android 12; vivo 1920) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"}
        r = requests.get("https://api.bloxflip.com/user", headers=headers)
        r.raise_for_status()
        r = r.json()
        if "user" in r:
            username = r["user"]["robloxUsername"]
            balance = int(r["user"]["wallet"])
            dump = {"info": {"username": f"{username}", "balance": f"{balance}"}}
            return json.dumps(dump)
        else:
            return "invalid auth token try checking it again!"
    async def send(auth, message):
        TOKEN = auth
        headers = {"Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9", "Cache-Control": "no-cache", "Connection": "Upgrade", "Host": "sio-bf.blox.land", "Origin": "https://bloxflip.com", "Pragma": "no-cache", "Upgrade": "websocket", "x-auth-token": TOKEN, "Cookie": "__cf_bm=q3IhEUjTdruLw8J7qlMEsOoChcOSEMCrOz1wtbvJgLs-1663533789-0-AdUibmLxIDRluYADk0r13/arKvEfequiaQx4ZcPP5gXKreT1LE9DjS5JzmFq8xEb+kZplzWwtJLJufeZnndb6/U=; path=/; expires=Sun, 18-Sep-22 21:13:09 GMT; domain=.bloxflip.com; HttpOnly; Secure; SameSite=None", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        try:
            async with websockets.connect("wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket", extra_headers=headers) as ws:
                queries1 = ['42/chat,["auth", "' + TOKEN + '"]', '42/cups,["auth","' + TOKEN + '"]', '42/jackpot,["auth","' + TOKEN + '"]', '42/rouletteV2,["auth","' + TOKEN + '"]', '42/roulette,["auth","' + TOKEN + '"]', '42/crash,["auth","' + TOKEN + '"]', '42/wallet,["auth","' + TOKEN + '"]', '42/marketplace,["auth","' + TOKEN + '"]', '42/case-battles,["auth","' + TOKEN + '"]', '42/mod-queue,["auth","' + TOKEN + '"]', '42/cloud-games,["auth","' + TOKEN + '"]', '42/feed,["auth","' + TOKEN + '"]']
                queries = ["40/chat,", "40/cups,", "40/jackpot,", "40/rouletteV2,", "40/roulette,", "40/crash,", "40/wallet,", "40/marketplace,", "40/case-battles,", "40/mod-queue,", "40/feed,", "40/cloud-games,"]
                for query in queries:
                    await ws.send(query)
                for query in queries1:
                    await ws.send(query)
                await ws.send(f'42/chat,["send-chat-message","{message}"]')
                await ws.close()
                dump = {"response": {"msg": f"message {message} is sent successfully!"}}
                return json.dumps(dump)
        except Exception as e:
            dump = {"error": {"msg": f"{e}"}}
            return json.dumps(dump)