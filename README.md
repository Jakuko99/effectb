# EffectBot Discord bot
[![Discord Bots](https://top.gg/api/widget/status/821641151613894706.svg)](https://top.gg/bot/821641151613894706)

## Overview
You can invite bot to your server using this [link](https://top.gg/bot/821641151613894706).

### Basic functionality
My aim is to make this bot multifuncional. Current version is capable of sending posts from reddit, playing music from youtube (though this doesn't work currently), true TTS messages, funny quotes and more to come later. I am also planning to add some mini game like Tic-Tac-Toe or something similar.

### Running the bot
Download the files and open them in your python code editor. Don't forget to install libraries from `requirements.txt` using `pip3 install -r requirements.txt`. You will also need to create .env file in code directory to be able to run this code, this file should be in this format:
```
BOT_TOKEN=DISCORD_BOT_TOKEN
REDDIT_ID=REDDIT_APPLICATION_ID
REDDIT_SECRET=REDDIT_SECRET
REDDIT_NAME=REDDIT_USERNAME
REDDIT_PASS=REDDIT_PASSWORD
``` 
### TTS Commands
Currently TTS works only on Windows hosts. It can work on Linux(Ubuntu, etc.), but the voices there are not that good and for some unknown reason the bot crashes sometimes after playback. Still trying to find a way how to use TTS, while bot is running on hosting service instead of locally.

## Cogs
Bot's commands are split to four categories based what is their purpose. Now using the command `!help` will show commands in their respective categories:
- Chat - used for message based commands
- Audio - commands like playing audio from YouTube URL
- TTS - Text-to-Speech messages (they only work if the bot is running on Windows for now)
- Administrative - protected set of commands used to manage cogs

## To Do
[x] Add Linux alternative for TTS (works, but it makes bot freeze sometimes) </br>
[ ] Create queue system or playlist support for audio </br>
[?] Direct url playback </br>

## Commands
Default bot prefix is **!** (exclamation mark), in the future there may be command to change that.
| Command | Usage | Parameters | Description |
| ----------- | ----------- | ----------- | ----------- |
| help | - | none | Returns list of all bot's commands |
|invite| - | none | Sends invite to bot's support server|
|bot mention| - | none | Prints bot's prefix and invite to suppor server |
| funny | - |  none | Randomly chooses one funny quote from quotes.txt |
| meme | meme [subreddit] | subreddit | Fetches image post from chosen subreddit or chooses one from top posts on meme subreddit. |
| join | - | none | Connects bot to the voice channel sender of the message is in |
| disconnect | aliases: dc | none | Disconnects bot from its current voice channel |
| play | play [URL/search phrase] | URL/search phrase | Plays given video, autoconnects to voice channel. You can use url of video, or search for it |
| playlist | playlist [URL] | URL | Plays contents of given playlist url, feature coming soon |
| pl | - | none | Audio playback test command, plays test_file.mp3 |
| pause | aliases: pa | none | Pauses current audio playback |
| resume | aliases: re | none | Resumes audio playback |
| stop | - | none | Completely stops audio playback |
| search | search [movie/series] | name | Searches IMDb for movie or series with that name and returns results |
| movie | movie [movie/series] | title | Returns overview of movie or series |
| actor | actor [name] | name | Sends basic info about actor or actress with their filmography |
| say | say [message] |message | Translates given message to TTS audio file and plays it. |
