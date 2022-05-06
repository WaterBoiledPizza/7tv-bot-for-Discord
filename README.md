# 7tvbot
Requirements:
1) Download Python https://www.python.org/downloads/
- Any version of Python should work, so getting the latest stable version is recommended
2) Download ImageMagick: https://imagemagick.org/script/download.php
3) At the folder, run `pip install -r requirements.txt` to download the required library for the script. 
   - The libraries required are as follows:
    ```
    - setuptools==57.0.0
    - discord==1.7.3
    - requests==2.26.0
    - Pillow==8.4.0
    - Wand==0.6.7
    ```

## Make a bot
1) Go to https://discord.com/developers/applications
2) Click [New Application] and give your app a name.
3) At the bot tab, click [Add Bot], then copy the Token of the bot.

##Configuration
- Add the token of your bot in `config.py`
- Change the prefix as you want
- Change the size of the downloaded emote file

## Run the bot
- Simply click `runbot.bat`

## Usage
- Posting a link to 7tv emote will show a gif version of the emote if it is WEBP format
- !addemote <link to 7tv emote>
- !downloademote <link to 7tv emote> <emote size>
- !findemoteinchannel <channel name> <text>
