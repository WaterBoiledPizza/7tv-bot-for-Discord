import discord
from discord.ext import commands
import os
import config as cfg
from io import BytesIO
from classes import Emote, Channel

TOKEN = cfg.TOKEN  #put the token of the bot here
client = commands.Bot(command_prefix=cfg.prefix)
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
        emoteID = message.content[23:]
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
    guild = ctx.guild
    ename = "error"
    success = False
    if ctx.author.guild_permissions.manage_emojis:
        emoteID = url[23:]
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

                    except discord.HTTPException:
                        print(f'File size of {i}x is too big!')

                if success:
                    os.remove(e.file_path)
                    break

@client.command()
async def downloadlocal(ctx, url: str, size: int):
    guild = ctx.guild
    if ctx.author.guild_permissions.manage_emojis:
        emoteID = url[23:]
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
            list = c.findEmotes(emote, exact)
            message += f'{channel} has {len(list)} {emote} emote(s):'
            for i in list:
                print(f"Found {i.name}")
                message += f"\n{i.name}: <https://7tv.app/emotes/{i.id}>"
            await ctx.send(message)
        # try:
        #     with open(e.file_path, 'rb') as fp:
        #         try:
        #             img_or_gif = BytesIO(fp.read())
        #             b_value = img_or_gif.getvalue()
        #             emoji = await guild.create_custom_emoji(image=b_value, name=e.info.name)
        #             await ctx.send(f'Successfully added emote: <:{e.info.name}:{emoji.id}>')
        #
        #         except discord.HTTPException:
        #             await ctx.send('File size is too big!')
        #
        # except:
        #     await ctx.send(e.message)
        #
        # os.remove(e.file_path)

client.run(TOKEN)

