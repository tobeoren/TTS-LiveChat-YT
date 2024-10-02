import pytchat
import re
import threading
import time
import urllib.parse
import requests
from googletrans import Translator  # Added Google Translate
from pygame import mixer
import os
from rich.console import Console
from rich.text import Text

# Inisialisasi console rich
console = Console()

# Menampilkan watermark di bagian awal
watermark_text = Text("Text to Speach - YouTube Live Chat", style="bold blue")
author_text = Text("by: tobeoren", style="bold cyan")

console.print(watermark_text, justify="center")
console.print(author_text, justify="center")

def load_name_blacklist():
    blacklist = []
    file_path = "name-blacklist.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            blacklist = [line.strip() for line in file.readlines()]
    return blacklist

# Daftar pengguna yang ingin diabaikan dalam chat (misalnya nama streamer)
blacklist = load_name_blacklist()

# Fungsi untuk menyiapkan live chat YouTube
def preparation():
    # Tambahkan logika penyiapan di sini jika diperlukan
    pass

def load_word_blacklist():
    word_blacklist = []
    file_path = "word-blacklist.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            word_blacklist = [line.strip() for line in file.readlines()]
    return word_blacklist

# Daftar kata-kata yang diblacklist
word_blacklist = load_word_blacklist()

# Fungsi untuk mengecek apakah chat mengandung kata-kata dari blacklist
def is_blacklisted(chat):
    for word in word_blacklist:
        if word in chat.lower():
            return True
    return False

# Fungsi untuk mendeteksi bahasa teks menggunakan Google Translate
def detect_language(text):
    translator = Translator()
    detected_lang = translator.detect(text)
    return detected_lang.lang

# Fungsi untuk menerjemahkan teks menggunakan Google Translate
def translate_text(text, target_language='id'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

# Fungsi untuk memainkan suara dari URL
def play_sound(url):
    response = requests.get(url, stream=True)
    with open("tts.mp3", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    mixer.init()
    mixer.music.load("tts.mp3")
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    mixer.quit()

    os.remove("tts.mp3")

# Fungsi untuk menangkap live chat dari YouTube
def yt_livechat(video_id):
    live = pytchat.create(video_id=video_id)
    while live.is_alive():
        try:
            for c in live.get().sync_items():
                # Abaikan chat dari pengguna dalam daftar blacklist
                if c.author.name in blacklist:
                    continue

                # Sensor kata-kata
                if is_blacklisted(c.message):
                    print(f"Chat from {c.author.name} contains blacklisted words. Ignoring.")
                    continue

                # Jika chat tidak diawali dengan tanda seru, proses chat tersebut
                if not c.message.startswith("!"):
                    # Hapus emoji dari chat
                    chat_raw = re.sub(r':[^\s]+:', '', c.message)
                    chat_raw = chat_raw.replace('#', '')
                    # Format chat dengan menambahkan nama pengguna di depan
                    chat = c.author.name + ' : ' + chat_raw
                    print(chat)

                    # Deteksi bahasa chat
                    detected_lang = detect_language(chat_raw)

                    # Menyiapkan teks yang akan diucapkan oleh TTS
                    tts_text = f"{c.author.name}, berkata: {chat_raw}"

                    # Jalankan TTS menggunakan bahasa asli
                    encoded_tts_text = urllib.parse.quote(tts_text)
                    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={detected_lang}&q={encoded_tts_text}"
                    play_sound(tts_url)

                    # Jika bahasa chat adalah bahasa asing (bukan bahasa Indonesia), terjemahkan ke bahasa Indonesia
                    if detected_lang != 'id':
                        translated_chat = translate_text(chat_raw)

                        # Menyiapkan teks terjemahan untuk diucapkan oleh TTS
                        tts_text_translated = f"Artinya: {translated_chat}"

                        # Jalankan TTS terjemahan dalam bahasa Indonesia
                        encoded_tts_text_translated = urllib.parse.quote(tts_text_translated)
                        tts_url_translated = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=id&q={encoded_tts_text_translated}"
                        play_sound(tts_url_translated)

                time.sleep(1)
        except Exception as e:
            print("Error receiving chat: {0}".format(e))

if __name__ == "__main__":
    try:
        # Masukkan livestream ID di bawah ini
        live_id = input("Livestream ID: ")
        # Gunakan threading untuk menangkap live chat dan menjawab chat secara bersamaan
        t = threading.Thread(target=preparation)
        t.start()
        yt_livechat(live_id)

    except KeyboardInterrupt:
        t.join()
        print("Stopped")
