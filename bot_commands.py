import os
import random

from bot_client import *
from bot_music import *


def read_help():
    with open("help.txt", "r") as f:
        lines = f.read()
        f.close()
        return lines

@client.event
async def on_message(message):
    if message.author == client.user:  # doesn't work if message is from self
        return
    elif '.play ' in message.content:  # in these cases uppercase is important
        pass
    else:
        message.content = message.content.lower()  # makes command lowercase

    # killswitch
    if message.content == '.kill':
        await message.channel.send("Goodbye...")
        await client.close()
    # test
    elif message.content.startswith('.test'):
        return
    # help
    elif message.content.startswith('.help'):
        help_message = read_help()
        await message.channel.send(help_message)
        return
    # hello
    elif message.content.startswith('.hello'):
        await message.channel.send('Why hello there!')
        return
    # play
    elif message.content.startswith('.play '):
        voice_channel = message.author.voice.channel  # connect to voice if not connected
        try:
            await voice_channel.connect()
        except discord.errors.ClientException:
            pass  # already connected

        # determine type of request
        if 'playlist?list=' in message.content:  # playlist url
            url = message.content[message.content.index('www.'):]
            await add_playlist(url, message)
        elif 'watch?v=' in message.content:  # regular video url
            if '&' in message.content:
                url = message.content[message.content.index('www.'):message.content.index('&')]
                await add_video(url, message)
            else:
                url = message.content[message.content.index('www.'):]
                url = "http://" + str(url)
                await add_video(url, message)
        elif 'youtu.be' in message.content:  # shortened url
            url = message.content[message.content.index('youtu.be'):]
            await add_video(url, message)
        else:  # not a url
            item = message.content[message.content.index(" "):]
            await search_video(item, message)

        return

    # disconnect
    elif message.content.startswith('.dc'):
        voice = discord.utils.get(client.voice_clients)
        queue.clear()
        nowPlaying.clear()
        await voice.disconnect()
        return
    # fs
    elif message.content.startswith('.fs'):
        voice = discord.utils.get(client.voice_clients)
        voice.stop()
        return
    # shuffle
    elif message.content.startswith('.shuffle'):
        random.shuffle(queue)
        await message.channel.send("Shuffled queue")
        return
    # np
    elif message.content.startswith('.np'):
        voice = discord.utils.get(client.voice_clients)
        if voice.is_playing():
            await message.channel.send(f"""`Now playing:` {nowPlaying[1]} `{nowPlaying[2]}`""")
        else:
            await message.channel.send('nothing is playing...')
        return
    # q
    elif message.content.startswith('.q'):
        response = ""
        for i in range(10):
            if len(queue) > i:
                response += f"""`{i + 1}` {queue[i][1]} `{queue[i][2]}`{os.linesep}"""
        if len(queue) > 10:
            response += f"""+{len(queue) - 10} more songs"""
        if response == "":
            await message.channel.send("nothing in queue")
            return
        await message.channel.send(response)
        return
    # clearq
    elif message.content.startswith('.clearq'):
        queue.clear()
        await message.channel.send('Cleared queue')
        return
    # remove
    elif message.content.startswith('.remove '):
        temp_str = message.content[message.content.index(" ") + 1:]
        if temp_str.isdecimal():
            try:
                queue.pop(int(temp_str) - 1)
                await message.channel.send("successfully removed queue entry")
            except:
                return
        return
