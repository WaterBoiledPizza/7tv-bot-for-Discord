# 7tvbot
Requirements:
1) Download Python https://www.python.org/downloads/
- Any version of Python should work, so getting the latest stable version is recommended
3) Download ImageMagick: https://imagemagick.org/script/download.php
4) At the folder, run "pip install -r requirements.txt" to download the required library for the script. The libraries required are as follows:
- setuptools==57.0.0
- discord==1.7.3
- requests==2.26.0
- Pillow==8.4.0
- Wand==0.6.7


## Make a bot
1) Go to https://discord.com/developers/applications
2) Click [New Application] and give your app a name.
3) At the bot tab, click [Add Bot], then copy the Token of the bot.

## Run the bot
1) Add the token of your bot to line 7 of runbot.py
  - TOKEN = "token here"
2) Make sure you have a "out" and "tmp" folder
3) Run runbot.py (run "python runbot.py" at the folder)

## Usage
- Posting a link to 7tv emote will show a gif version of the emote if it is WEBP format
- !addemote <link to 7tv emote>
