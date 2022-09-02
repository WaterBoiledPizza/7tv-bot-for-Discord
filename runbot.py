import discord
from discord.ext import commands
import os
import config as cfg
from io import BytesIO
from classes import Emote, Channel

TOKEN = cfg.TOKEN  #put the token of the bot here
client = commands.Bot(command_prefix=cfg.prefix,intents=discord.Intents.all())
folder_dir = cfg.output_folder

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


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(r'https://7tv.app/emotes/'):
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
                        await ctx.send(f'Successfully added emote: <:{ename}:{emoji.id}>')
                        success = True

                    except discord.HTTPException as err:
                        #print(f'File size of {i}x is too big!')
                        print(err)

                if os.path.exists(e.file_path):
                    os.remove(e.file_path)

                if success: break


@client.command()
async def downloadlocal(ctx, url: str, size: int):
    guild = ctx.guild
    if ctx.author.guild_permissions.manage_emojis:
        emoteID = url.split("/")[-1]
        e = Emote(emoteID,size)
        if hasattr(e.info, 'message'):
            await ctx.send(e.message)
        else:
            e.download(folder_dir)
            await ctx.send(f'Emote downloaded successfully!')

@client.command()
async def findemoteinchannel(ctx, channel: str, emote: str, exact= False):
    guild = ctx.guild
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



client.run(TOKEN)

