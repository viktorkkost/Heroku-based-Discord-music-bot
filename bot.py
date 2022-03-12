from bot_commands import *


@client.event
async def on_ready():  # runs on bot start
    ytdl_init()
    print("bot is running")


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        f.close()
        return lines[0].strip()


token = read_token()
client.run(token)
