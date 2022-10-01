# 7tv bot for Discord

## Set up
1) Download Python https://www.python.org/downloads/
- Any version of Python should work, so getting the latest stable version is recommended
- Make sure to add Python to PATH
2) Download the files into a folder you destinated
3) At the folder, click `setup.bat` to download the required library for the script. 

## Make a bot
1) Go to https://discord.com/developers/applications
2) Click [New Application] and give your app a name.
3) At the bot tab, click [Add Bot], then copy the Token of the bot.
4) Enable all the Privileged Gateway Intents

## Configuration
- Add the token of your bot in `config.py`
- Change the prefix as you want
- Change the size of the downloaded emote file
- Add dedicated discord channel for listening
    - Go to Discord settings. In Advanced tab, enable Developer mode
    - Right click your chosen discord channel, then copy ID
- Add 7tv user ID to listen
    - format:
    ```
    "listeningUsers": [
        "<7tv ID>", "<7tv ID>", ...
    ]
    ```

## Run the bot
- Simply click `runbot.bat`
* The script will add a `tmp` and an output folder if you don't have that already. 

## Usage
- Posting a link to 7tv emote will show a gif version of the emote if it is WEBP format
    - only works with V2 urls, since V3 urls can show embeded emote in Discord
- !addemote \<link to 7tv emote\> \<\*optional\* emoji name\>
- !findemoteinchannel \<channel name\> \<text\>
- !searchemotes \<text\>
- !listeningchannels

[In development]
- !addlistenchannel <channel name\>
- !removelistenchannel <channel name\>
These two commands require bot restart to update
