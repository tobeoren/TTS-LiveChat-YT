# **Introduction**
The YouTube Live Chat Text-to-Speech (TTS) Bot is a Python program that adds an exciting dimension to live streaming on YouTube. This interactive bot converts real-time chat messages from viewers into spoken words, making it easier for streamers and their audiences to engage and interact during live streams.

# Features:
1. Live Chat Conversion: The bot instantly transforms incoming chat messages from viewers into natural-sounding speech using the Google Translate Text-to-Speech (TTS) API.
2. Language Detection and Translation: With the help of the Google Translate API, the bot identifies the language of each chat message and provides translations when needed. This ensures smooth communication between the streamer and their diverse audience.
3. Chat Filtering: Streamers can customize a blacklist to ignore messages from specific users or known bots, creating a focused and positive chat environment.
4. Emoticon Filtering: To maintain meaningful communication, the bot filters out messages containing emoticons.

# How it Works:
1. Upon launch, the program prompts users to enter the YouTube livestream ID they want to monitor for live chat messages.
2. The bot runs chat monitoring and text-to-speech conversion in a separate thread for a smooth user experience.
3. It continuously retrieves live chat messages using the pytchat library and processes each message accordingly.
4. Relevant chat messages without exclamation marks ('!') or emoticons are considered for text-to-speech conversion.
5. Using the Google Translate, the bot detects the language of the chat message and generates a meaningful speech synthesis output based on the language.
6. The synthesized speech is played using the pygame.mixer library, providing an audible representation of the chat message for both the streamer and viewers.
7. The bot also prints the text-to-speech output in the terminal for easy monitoring and reference.

# Getting Started
Below is a list of what you need to install and set up:
1. Python: Ensure that you have Python installed on your computer. You can download the latest version of Python from the official website (https://www.python.org/downloads/). The program is compatible with Python 3.x.
2. Libraries:
   pytchat: Install the pytchat library, which allows you to retrieve YouTube live chat messages. You can install it using pip:
```
pip install pytchat
```

   requests: The requests library is required to download the text-to-speech audio files. Install it using pip:
``` pip install requests ```

   googletrans: To detect the language of chat messages and perform translations, you need the googletrans library. Install it using pip:
``` pip install googletrans==4.0.0-rc1 ```

   pygame: For playing the text-to-speech audio, you'll need the pygame library. Install it using pip:
``` pip install pygame ```
