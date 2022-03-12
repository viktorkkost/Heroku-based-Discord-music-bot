import asyncio
import youtube_dl
import urllib.request
import datetime
from bot_client import *

global queue
queue = []

global nowPlaying
nowPlaying = []

global ytdl_opts
ytdl_opts = {
        'format': 'bestaudio/best',
        #'ignoreerrors': True,
        #'no_warnings': True,
        #'debug_printtraffic': True, ###############################################################
        'cookiefile': 'youtube.com_cookies.txt',
        'cachedir': False,
        #'quiet': True,
        #'verbose': True, ##########################################################
    }

global ytdl
def ytdl_init():
    global ytdl
    ytdl = youtube_dl.YoutubeDL(ytdl_opts)


ffmpeg_options = {  # these options fix a common disconnection bug
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -sn'
}
class ytdl_source(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        try:
            loop = loop or asyncio.get_event_loop()
            data = await prepare_data(url, loop, stream)
            if data is None:
                play_next()
                return

            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
        except Exception as e:
            print('Exception in from_url:', e)
            play_next()


async def prepare_data(url, loop, stream):
    data = None
    while True:
        try:
            loop = loop or asyncio.get_event_loop()

            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

            if 'entries' in data:
                # take first item from a playlist
                data = data['entries'][0]

            # print(data['url'])  # the generated direct url
            my_data = urllib.request.urlopen(data['url'])
            response = my_data.getcode()

        except Exception as e:
            if ('HTTP Error 403' in str(e)) or ('ERROR: No video formats found;' in str(e)):
                print('generic error')

                await asyncio.sleep(1)

                try:    #try without cookies
                    ytdl_opts2 = {
                        'format': 'bestaudio/best',
                        # 'ignoreerrors': True,
                        #'no_warnings': True,
                        'debug_printtraffic': True,
                        # 'nocheckcertificate': True,
                        'cachedir': False,
                        # 'quiet': True,
                        'verbose': True
                    }
                    ytdl2 = youtube_dl.YoutubeDL(ytdl_opts2)

                    data = await loop.run_in_executor(None, lambda: ytdl2.extract_info(url, download=not stream))

                    if 'entries' in data:
                        # take first item from a playlist
                        data = data['entries'][0]

                    my_data = urllib.request.urlopen(data['url'])
                    response = my_data.getcode()

                except Exception as e2:
                    print('printing e2 exception: ' + str(e2))
                    return
                else:
                    break
            else:
                print('Printing error: ' + str(e))
                return
        else:
            break

    return data

async def add_playlist(url : str, message):
    ydl_opts = {
        'format': 'bestaudio/best',
        # 'ignoreerrors': True,
        'no_warnings': True,
        'cookiefile': 'youtube.com_cookies.txt',
        #'nocheckcertificate': True,
        'extract_flat': 'in_playlist',
        #'skip_download': True,
        'cachedir': False,
        'quiet': True
    }

    info = None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except Exception:
            print('error on first info get')

    if info is None:
        asyncio.sleep(0.5)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
            except Exception:
                print('error on second info get')

    videos = len(info['entries'])
    for i in range(videos):
        duration = 'unknown'
        if info['entries'][i]['duration'] is not None:
            seconds = int(info['entries'][i]['duration'])
            duration = str(datetime.timedelta(seconds=seconds))
        tempList = ["http://www.youtube.com/watch?v="+info['entries'][i]['url'], info['entries'][i]['title'], duration]
        global queue
        queue.append(tempList)
    await message.channel.send('successfully added '+str(videos)+' videos to queue')
    play_next()
    return

async def add_video(url : str, message):
    ydl_opts = {
        'format': 'bestaudio/best',
        # 'ignoreerrors': True,
        'no_warnings': True,
        'cookiefile': 'youtube.com_cookies.txt',
        #'nocheckcertificate': True,
        # 'extract_flat': True,
        'cachedir': False,
        'quiet': True
    }

    info = None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if info is None:    #if there's a lot of latency, try again after .5 secs
        asyncio.sleep(0.5)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

    seconds = int(info['duration'])
    duration = str(datetime.timedelta(seconds=seconds))
    temp_list = [url, info['title'], duration]
    global queue
    queue.append(temp_list)
    await message.channel.send("successfully added video to queue")
    play_next()
    return

async def search_and_paste_link(item : str, message):
    ydl_opts = {
        'format': 'bestaudio/best',
        # 'ignoreerrors': True,
        'no_warnings': True,
        'cookiefile': 'youtube.com_cookies.txt',
        # 'nocheckcertificate': True,
        'extract_flat': 'in_playlist',
        # 'skip_download': True,
        'cachedir': False,
        'quiet': True,
        'noplaylist': True
    }

    info = None  #
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("ytsearch:%s" % item, download=False)

    if info is None:  # if there's a lot of latency, try again after .3 secs
        await asyncio.sleep(0.3)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info("ytsearch:%s" % item, download=False)
            print(info)
        await asyncio.sleep(0.3)

    new_message = str("http://www.youtube.com/watch?v=") + str(info['entries'][0]['url'])

    await message.channel.send(new_message)


async def search_video(item : str, message):
    ydl_opts = {
        'format': 'bestaudio/best',
        # 'ignoreerrors': True,
        'no_warnings': True,
        'cookiefile': 'youtube.com_cookies.txt',
        #'nocheckcertificate': True,
        'extract_flat': 'in_playlist',
        # 'skip_download': True,
        'cachedir': False,
        'quiet': True,
        'noplaylist': True
    }

    info = None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("ytsearch:%s" % item, download=False)

    if info is None:    #if there's a lot of latency, try again after .3 secs
        await asyncio.sleep(0.3)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info("ytsearch:%s" % item, download=False)
            print(info)
        await asyncio.sleep(0.3)

    if len(info['entries']) > 0:
        seconds = 0
        if info['entries'][0]['duration'] is not None:
            seconds = int(info['entries'][0]['duration'])

        duration = str(datetime.timedelta(seconds=seconds))

        if seconds == 0:
            duration = "unknown"

        tempList = ["http://www.youtube.com/watch?v="+info['entries'][0]['url'], info['entries'][0]['title'], duration]
        global queue
        queue.append(tempList)
        await message.channel.send("successfully added video to queue")
        play_next()
    else:
        await message.channel.send("couldn't find a suitable result")
    return

def play_next():
    voice = discord.utils.get(client.voice_clients)
    global queue
    try:
        if not voice.is_playing() and len(queue) > 0:
            song = queue[0]
            queue.pop(0)
            global nowPlaying
            nowPlaying.clear()
            nowPlaying.extend(song)

            asyncio.run_coroutine_threadsafe(play_this_url(nowPlaying[0]), loop=client.loop)
    except AttributeError:
        if len(queue) > 0:
            print('trying again here')
            play_next()
    return

async def play_this_url(url : str):
    voice = discord.utils.get(client.voice_clients)
    try:
        player = await ytdl_source.from_url(url, loop=client.loop, stream=True)
        if player is None:
            return
        voice.play(player, after=lambda er: play_next())
    except Exception as e:
        print('Exception in play_this_url:', e)
        play_next()
    return
