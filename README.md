# EffectBot Discord bot
## Overview

Bot needs .env file to be able to run, this file should be in this format:
```
BOT_TOKEN=DISCORD_BOT_TOKEN
REDDIT_ID=REDDIT_APPLICATION_ID
REDDIT_SECRET=REDDIT_SECRET
REDDIT_NAME=REDDIT_USERNAME
REDDIT_PASS=REDDIT_PASSWORD
``` 

## To Do
[ ] Fetch list of members currently in voice channel </br>
[ ] Add Linux alternative for TTS </br>
[ ] Create queue system for audio </br>

## Commands
Default bot prefix is **!** (exclamation mark), in the future there may be command to change that.
| Command | Usage | Parameters | Description |
| ----------- | ----------- | ----------- | ----------- |
| help | - | none | Returns list of all bot's commands |
| funny | - |  none | Randomly chooses one funny quote from file quotes.txt |
| meme | meme subreddit | subreddit | Fetches image post from chosen subreddit of chooses one from top posts on meme subreddit |
| join | - | none | Connects bot to the voice channel sender of the message is in |
| disconnect | aliases: dc | none | Disconnects bot from its current voice channel |
| play | play URL | URL | Downloads and plays given video, autoconnects to voice channel. This feature doesn't work currently due to youtube-dl problem |
| pl | - | none | Audio playback test command, plays test_file.mp3 |
| pause | - | none | Pauses current audio playback |
| resume | - | none | Resumes audio playback |
| stop | - | none | Completely stops audio playback |
| say | say "message" voice |message, voice | Translates given message to TTS audio file and plays it. Voice parameter is optional, but defaults to m (male voice), other options is f (female voice) |