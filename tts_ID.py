import pytchat
import re
import threading
import time
import urllib.parse
import requests
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

# Daftar pengguna yang ingin diabaikan dalam chat (misalnya nama streamer)
blacklist = []

# Fungsi untuk menyiapkan live chat YouTube
def preparation():
    # Tambahkan logika penyiapan di sini jika diperlukan
    pass

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

                # Jika chat tidak diawali dengan tanda seru, proses chat tersebut
                if not c.message.startswith("!"):
                    # Hapus emoji dari chat
                    chat_raw = re.sub(r':[^\s]+:', '', c.message)
                    chat_raw = chat_raw.replace('#', '')
                    # Format chat dengan menambahkan nama pengguna di depan
                    chat = c.author.name + ' : ' + chat_raw
                    print(chat)

                    # Menyiapkan teks yang akan diucapkan oleh TTS
                    tts_text = f"Ada chat dari {c.author.name}, dia berkata: {chat_raw}"

                    # Jalankan TTS
                    encoded_tts_text = urllib.parse.quote(tts_text)
                    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=id&q={encoded_tts_text}"
                    play_sound(tts_url)

                time.sleep(1)
        except Exception as e:
            print("Error receiving chat: {0}".format(e))

if __name__ == "__main__":
    try:
        # Pilih mode 1 untuk menangkap live chat dari YouTube
        mode = input("Mode (1-Youtube Live): ")

        if mode == "1":
            live_id = input("Livestream ID: ")
            # Gunakan threading untuk menangkap live chat dan menjawab chat secara bersamaan
            t = threading.Thread(target=preparation)
            t.start()
            yt_livechat(live_id)

    except KeyboardInterrupt:
        t.join()
        print("Stopped")
