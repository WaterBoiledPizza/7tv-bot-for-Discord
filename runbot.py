import discord
from discord.ext import commands
import os
from io import BytesIO
from classes import Emote, Channel

TOKEN = "" #put the token of the bot here
client = commands.Bot(command_prefix='!')
folder_dir = "out"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(r'https://7tv.app/emotes/'):
        emoteID = message.content[23:]
        e = Emote(emoteID,4)
        e.download(folder_dir)

        with open(e.file_path, 'rb') as fp:
            await message.channel.send(file=discord.File(fp))

        os.remove(e.file_path)
    await client.process_commands(message)

@client.command()
async def addemote(ctx, url: str):
    guild = ctx.guild
    if ctx.author.guild_permissions.manage_emojis:
        emoteID = url[23:]
        e = Emote(emoteID,4)
        e.download(folder_dir)
        with open(e.file_path, 'rb') as fp:
            try:
                img_or_gif = BytesIO(fp.read())
                b_value = img_or_gif.getvalue()
                emoji = await guild.create_custom_emoji(image=b_value, name=e.info.name)
                await ctx.send(f'Successfully added emote: <:{e.info.name}:{emoji.id}>')

            except discord.HTTPException:
                await ctx.send('File size is too big!')
        os.remove(e.file_path)

client.run(TOKEN)

