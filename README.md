# EffectBot Discord bot
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
Currently TTS works best on Windows hosts. It can work on Linux(Ubuntu, etc.), but the voices there are not that good and for some unknown reason the bot crashes sometimes after playback. Still trying to find a way how to use TTS, while bot is running on hosting service instead of locally.

## Cogs
Bot's commands are split to four categories based what is their purpose. Now using the command `!help` will show commands in their respective categories:
- Chat - used for message based commands
- Audio - commands like playing audio from YouTube URL
- TTS - Text-to-Speech messages (they only work if the bot is running on Windows for now)
- Administrative - protected set of commands used to manage cogs

## To Do
[x] Add Linux alternative for TTS (works, but it makes bot freeze sometimes) </br>
[ ] Create queue system for audio </br>
[ ] Fix youtube-dl issue </br>
[ ] Direct url playback </br>
[ ] Separate players for music and TTS </br>

## Commands
Default bot prefix is **!** (exclamation mark), in the future there may be command to change that.
| Command | Usage | Parameters | Description |
| ----------- | ----------- | ----------- | ----------- |
| help | - | none | Returns list of all bot's commands |
|invite| - | none | Sends invite to bot's support server|
| funny | - |  none | Randomly chooses one funny quote from file quotes.txt |
| meme | meme [subreddit] | subreddit | Fetches image post from chosen subreddit of chooses one from top posts on meme subreddit. |
| join | - | none | Connects bot to the voice channel sender of the message is in |
| disconnect | aliases: dc | none | Disconnects bot from its current voice channel |
| play | play [URL] | URL | Downloads and plays given video, autoconnects to voice channel. This feature doesn't work currently due to youtube-dl problem. |
| pl | - | none | Audio playback test command, plays test_file.mp3 |
| pause | - | none | Pauses current audio playback |
| resume | - | none | Resumes audio playback |
| stop | - | none | Completely stops audio playback |
| say | say [message] [voice] |message, voice | Translates given message to TTS audio file and plays it. Voice parameter is optional, but defaults to m (male voice), other options is f (female voice). Message must be in quotes (""), otherwise it won't function properly. |