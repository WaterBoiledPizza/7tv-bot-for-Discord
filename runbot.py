import discord
from discord.ext import commands
import os
from io import BytesIO
from types import SimpleNamespace
from classes import Emote, Channel
import json
from search import searchemote
import asyncio
import websockets
import time

f = open('config.json')
cfg = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
TOKEN = cfg.TOKEN  #put the token of the bot here
client = commands.Bot(command_prefix=cfg.prefix,intents=discord.Intents.all())
folder_dir = cfg.output_folder
listenchannel_q = asyncio.Queue()
#resume_q = asyncio.Queue()
event = asyncio.Event()

if not os.path.exists(folder_dir):
    print("Output folder is not found")
    os.makedirs(folder_dir)
    print("Output folder is created")

if not os.path.exists("tmp"):
    print("Temporary folder is not found")
    os.makedirs("tmp")
    print("Temporary folder is created")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await listenchannel_q.put(client.get_channel(cfg.listen_channel))
    #await resume_q.put(True)
    event.set()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(r'https://old.7tv.app/emotes/'):
        emoteID = message.content.split("/")[-1]
        e = Emote(emoteID,cfg.showemote_size)
        if hasattr(e.info, 'message'):
            await message.channel.send(e.message)
        else:
            e.download("tmp")
            with open(e.file_path, 'rb') as fp:
                await message.channel.send(file=discord.File(fp))
            os.remove(e.file_path)

    await client.process_commands(message)

@client.command()
async def addemote(ctx, url: str, emotename: str = None):
    success = False
    guild = ctx.guild
    ename = "error"
    error = ""
    if ctx.author.guild_permissions.manage_emojis:
        emoteID = url.split("/")[-1]
        for i in reversed(range(1, 5)):
            print(f"Trying size {i}x...")
            e = Emote(emoteID,i)
            if hasattr(e.info, 'message'):
                await ctx.send(e.message)
            else:
                if emotename is None:
                    ename = e.info.name
                else: ename = emotename
                e.download("tmp")
                with open(e.file_path, 'rb') as fp:
                    try:
                        img_or_gif = BytesIO(fp.read())
                        b_value = img_or_gif.getvalue()
                        emoji = await guild.create_custom_emoji(image=b_value, name=ename)
                        print(f'Successfully added emote: <:{ename}:{emoji.id}>')
                        await ctx.send(f'Successfully added emote: <:{ename}:{emoji.id}>')
                        success = True

                    except Exception as err:
                        #print(f'File size of {i}x is too big!')
                        error = err
                        print(err)

                if os.path.exists(e.file_path):
                    os.remove(e.file_path)

                if success: break
        if not success:
            await ctx.send(f'Unable to add emote {ename}: {error}')

# @client.command()
# async def downloadlocal(ctx, url: str, size: int):
#     if ctx.author.guild_permissions.manage_emojis:
#         emoteID = url.split("/")[-1]
#         e = Emote(emoteID,size)
#         if hasattr(e.info, 'message'):
#             await ctx.send(e.message)
#         else:
#             e.download(folder_dir)
#             await ctx.send(f'Emote downloaded successfully!')

@client.command()
async def findemoteinchannel(ctx, channel: str, emote: str, exact= False):
    message = ""
    if ctx.author.guild_permissions.manage_emojis:
        c = Channel(channel)
        if hasattr(c.info, 'message'):
            await ctx.send("User does not exist!")
        else:
            elist = c.findEmotes(emote, exact)
            message += f'{channel} has {len(elist)} {emote} emote(s):'
            for i in elist:
                print(f"Found {i.name}")
                message += f"\n[{i.name}](https://7tv.app/emotes/{i.id})"

            embed = discord.Embed(
                title= "Search completed!",
                description= message,
                colour= discord.Colour.from_rgb(40,177,166)
            )

            embed.set_thumbnail(url="https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_e02650251d204198923de93a0c62f5f5/static/light/3.0")
            embed.set_footer(text="You can also add the emotes to your server as emoji by: !addemote <emote url>")
            await ctx.send(embed= embed)

@client.command()
async def searchemotes(ctx, emote: str):
    message = ""
    if ctx.author.guild_permissions.manage_emojis:
        elist = searchemote(emote)
        message += f'Found {len(elist)} emote(s) that contains "{emote}":'
        for i in elist:
            print(f"Found {i.name}")
            message += f"\n[{i.name}](https://7tv.app/emotes/{i.id})"

        embed = discord.Embed(
            title= "Search completed!",
            description= message,
            colour= discord.Colour.from_rgb(40,177,166)
        )

        embed.set_thumbnail(url="https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_e02650251d204198923de93a0c62f5f5/static/light/3.0")
        embed.set_footer(text="You can also add the emotes to your server as emoji by: !addemote <emote url>")
        await ctx.send(embed= embed)


@client.command()
async def addlistenchannel(ctx, channel: str):
    if ctx.author.guild_permissions.manage_emojis:
        await event.wait()
        print("sleeping")
        print(event.is_set())
        await asyncio.sleep(1)
        c = Channel(channel)
        try:
            cfg.listeningUsers.append(c.id)
            print((f'Added {channel} to listening channels'))
            await ctx.send(f'Added {channel} to listening channels')
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(cfg.__dict__, f, ensure_ascii=False, indent=4)
        except Exception as err:
            print(err)
            await ctx.send(err)
        event.set()

@client.command()
async def removelistenchannel(ctx, channel: str):
    if ctx.author.guild_permissions.manage_emojis:
        await event.wait()
        print("sleeping")
        print(event.is_set())
        await asyncio.sleep(1)
        c = Channel(channel)
        try:
            cfg.listeningUsers.remove(c.id)
            print((f'Removed {channel} from listening channels'))
            await ctx.send(f'Removed {channel} from listening channels')
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(cfg.__dict__, f, ensure_ascii=False, indent=4)
        except Exception as err:
            print(err)
            await ctx.send(err)
        event.set()

@client.command()
async def listeningchannels(ctx):
    msg = "Currently listening: "
    if ctx.author.guild_permissions.manage_emojis:
        if cfg.listeningUsers:
            lc = [Channel(i) for i in cfg.listeningUsers]
            for i in lc[:-1]:
                msg += f'{i.name}, '
            msg += f'{lc[-1].name}.'
    await ctx.send(msg)

async def listen():
    accessPt = "wss://events.7tv.io/v3"
    listenchannel = await listenchannel_q.get()
    title = ""
    message = ""
    color = discord.Colour.from_rgb(40, 177, 166)
    e = None
    eurl = ""
    while True:
        if listenchannel:
            async with websockets.connect(accessPt) as ws:
                for i in cfg.listeningUsers:
                    await ws.send(json.dumps({
                    "op": 35,
                    "d": {
                        "type": "emote_set.update",
                        "condition": {
                            # valid fields in the condition depend on the subscription type
                            # though in most cases except creations, object_id is acceptable
                            # to filter for a specific object.

                            "object_id": i
                        }
                    }
                    }))
                while event.is_set():
                    msg = await ws.recv()
                    parsed = json.loads(msg)
                    parsed = parsed['d']
                    if "body" in parsed:
                        c = Channel(parsed['body']['id'])
                        title = c.name
                        if "pushed" in parsed['body']:
                            e = Emote(parsed['body']['pushed'][0]['value']['id'],3)
                            message = f"Added emote {parsed['body']['pushed'][0]['value']['name']}:\nhttps://7tv.app/emotes/{e.id}"
                            color = discord.Colour.from_rgb(40, 177, 166)

                        elif "pulled" in parsed['body']:
                            e = Emote(parsed['body']['pulled'][0]['old_value']['id'],3)
                            message = f"Removed emote {parsed['body']['pulled'][0]['old_value']['name']}:\nhttps://7tv.app/emotes/{e.id}"
                            color = discord.Colour.from_rgb(177, 40, 51)

                        if e.isAnimated:
                            eurl = f"https://cdn.7tv.app/emote/{e.id}/3x.gif"
                        else:
                            eurl = f"https://cdn.7tv.app/emote/{e.id}/3x.png"

                        embed = discord.Embed(
                            title=title,
                            description=message,
                            colour=color
                        )

                        embed.set_thumbnail(
                            url=eurl)
                        embed.set_footer(
                            text="You can also add the emotes to your server as emoji by: !addemote <emote url>")
                        await listenchannel.send(embed=embed)

                while not event.is_set():
                    await asyncio.sleep(5)
        await asyncio.sleep(5)

#client.run(TOKEN)

loop = asyncio.get_event_loop()

async def run_bot():
    try:
        await client.start(TOKEN)
    except Exception:
        await client.close()


def run_in_thread():
    fut = asyncio.run_coroutine_threadsafe(listen(), loop)
    fut.result()  # wait for the result


async def main():
    await asyncio.gather(
        run_bot(),
        asyncio.to_thread(run_in_thread)
    )


loop.run_until_complete(main())
