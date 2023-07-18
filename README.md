The YouTube Live Chat Text-to-Speech (TTS) Bot is a Python program that adds an exciting dimension to live streaming on YouTube. This interactive bot converts real-time chat messages from viewers into spoken words, making it easier for streamers and their audiences to engage and interact during live streams.

Features:

Live Chat Conversion: The bot instantly transforms incoming chat messages from viewers into natural-sounding speech using the Google Translate Text-to-Speech (TTS) API.

Language Detection and Translation: With the help of the Google Translate API, the bot identifies the language of each chat message and provides translations when needed. This ensures smooth communication between the streamer and their diverse audience.

Chat Filtering: Streamers can customize a blacklist to ignore messages from specific users or known bots, creating a focused and positive chat environment.

Emoticon Filtering: To maintain meaningful communication, the bot filters out messages containing emoticons.

Randomized Chat Playback: When multiple chat messages arrive in quick succession, the bot randomly selects one message to read aloud, creating an element of surprise and variety in chat interactions.

How it Works:

Upon launch, the program prompts users to enter the YouTube livestream ID they want to monitor for live chat messages.
The bot runs chat monitoring and text-to-speech conversion in a separate thread for a smooth user experience.
It continuously retrieves live chat messages using the pytchat library and processes each message accordingly.
Relevant chat messages without exclamation marks ('!') or emoticons are considered for text-to-speech conversion.
Using the Google Translate API, the bot detects the language of the chat message and generates a meaningful speech synthesis output based on the language.
In cases of multiple chat messages received closely together, the bot groups them and randomly selects one to convert to speech, preventing overwhelming continuous TTS output.
The synthesized speech is played using the pygame.mixer library, providing an audible representation of the chat message for both the streamer and viewers.
The bot also prints the text-to-speech output in the terminal for easy monitoring and reference.
