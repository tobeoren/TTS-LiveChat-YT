---

# **Introduction**
The YouTube Live Chat Text-to-Speech (TTS) Bot is a Python program that adds an exciting dimension to live streaming on YouTube. This interactive bot converts real-time chat messages from viewers into spoken words, making it easier for streamers and their audiences to engage and interact during live streams.

<img width="599" alt="image" src="https://github.com/user-attachments/assets/8e500131-23ee-49c2-a60e-e11af4f273df">

---

# Features:
1. Live Chat Conversion: The bot instantly transforms incoming chat messages from viewers into natural-sounding speech using the Google Translate Text-to-Speech (TTS) API.
2. Language Detection and Translation: With the help of the Google Translate API, the bot identifies the language of each chat message and provides translations when needed. This ensures smooth communication between the streamer and their diverse audience.
3. Chat Filtering: Streamers can customize a blacklist to ignore messages from specific users or known bots, creating a focused and positive chat environment.
4. Emoticon Filtering: To maintain meaningful communication, the bot filters out messages containing emoticons.

---

# How it Works:
1. Upon launch, the program prompts users to enter the YouTube livestream ID they want to monitor for live chat messages.
2. The bot runs chat monitoring and text-to-speech conversion in a separate thread for a smooth user experience.
3. It continuously retrieves live chat messages using the pytchat library and processes each message accordingly.
4. Relevant chat messages without exclamation marks ('!') or emoticons are considered for text-to-speech conversion.
5. Using the Google Translate, the bot detects the language of the chat message and generates a meaningful speech synthesis output based on the language.
6. The synthesized speech is played using the pygame.mixer library, providing an audible representation of the chat message for both the streamer and viewers.
7. The bot also prints the text-to-speech output in the terminal for easy monitoring and reference.

---

# Getting Started
Below is a list of what you need to install and set up:
1. Python: Ensure that you have Python installed on your computer. You can download the latest version of Python from the official website (https://www.python.org/downloads/). The program is compatible with Python 3.x.
2. Libraries:
- pytchat: Install the pytchat library, which allows you to retrieve YouTube live chat messages. You can install it using pip:
```
pip install pytchat
```
- requests: The requests library is required to download the text-to-speech audio files. Install it using pip:
```
pip install requests
```
- googletrans: To detect the language of chat messages and perform translations, you need the googletrans library. Install it using pip:
```
pip install googletrans==4.0.0-rc1
```
- pygame: For playing the text-to-speech audio, you'll need the pygame library. Install it using pip:
```
pip install pygame
```
3. Livestream ID:
Before running the program, you'll need the YouTube livestream ID of the live stream where you want to monitor the chat. You can obtain the livestream ID from the URL of the livestream video. For example, if the URL is https://www.youtube.com/watch?v=YourLivestreamID, then YourLivestreamID is the livestream ID.
4. Text-to-Speech Audio Output:
Make sure your computer's audio output is configured correctly, and the speakers or headphones are connected and working.

Once you've installed the required libraries and obtained the YouTube API key and livestream ID, you are ready to run the YouTube Live Chat Text-to-Speech (TTS) Bot. Simply execute the Python script, and the bot will start monitoring the live chat of the specified YouTube livestream, converting chat messages to speech in real-time.

Remember to use the bot responsibly and respect the YouTube community guidelines when using it during live streams. Enjoy engaging with your audience in a more interactive and accessible way!

---

# IF YOU WANT TO SUPPORT ME
Ko-fi : https://ko-fi.com/xzeest

<img width="112" alt="image" src="https://github.com/user-attachments/assets/e9767543-a0cd-4a95-b89c-a38acd5c2d2d">

Trakteer : https://trakteer.id/xzeeest/tip?open=true

<img width="113" alt="image" src="https://github.com/user-attachments/assets/cb2618f6-a5d3-41cb-866f-e9d5faeeaf8b">

Streamlabs : https://streamlabs.com/xzeeest

<img width="110" alt="image" src="https://github.com/user-attachments/assets/27f5f15f-462e-49fe-b774-ccf3efb5cfc0">


---

- EVM ADDRESS: 0x491d7397212c55da8352d7733d2513393a362ae9
- SOLANA: 5MNBgtrsasfqenxb75ZLjd4epjB2TUKf9fbxfw143kq6
- BTC: bc1pts2fvykemcdyk2rg37al8chdc4uxptwg82w3nf0j02smzrtm9a6sp5dldc
- TON: UQCnGIFDBtrvJC9LtkcVa3SrkS3ifb2qZxZX3r-abZ-4GG1D

---

