import sys
import asyncio
import aiohttp
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog, QCheckBox, QSlider)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QTimer, QMutex, QWaitCondition
from PyQt6.QtGui import QKeyEvent
import pytchat
import re
import urllib.parse
from googletrans import Translator
from pygame import mixer
import tempfile

class WorkerSignals(QObject):
    update_terminal = pyqtSignal(str)
    update_translation = pyqtSignal(str)
    finished = pyqtSignal()

class ChatWorker(QThread):
    def __init__(self, live_chat, word_blacklist, name_blacklist, translation_enabled):
        super().__init__()
        self.live_chat = live_chat
        self.word_blacklist = word_blacklist
        self.name_blacklist = name_blacklist
        self.signals = WorkerSignals()
        self.is_running = True
        self.loop = None
        self.task = None
        self.temp_dir = tempfile.mkdtemp()
        self.translation_enabled = translation_enabled
        self.volume = 50  # Default volume
        self.volume_mutex = QMutex()
        self.volume_condition = QWaitCondition()

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.task = self.loop.create_task(self.process_chat())
            self.loop.run_until_complete(self.task)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.signals.update_terminal.emit(f"Error in ChatWorker: {e}")
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
            self.signals.finished.emit()

    async def process_chat(self):
        async with aiohttp.ClientSession() as session:
            while self.live_chat.is_alive() and self.is_running:
                try:
                    chat_data = self.live_chat.get()
                    if chat_data is None:
                        self.signals.update_terminal.emit("Error: No chat data received.")
                        await asyncio.sleep(1)
                        continue

                    for c in chat_data.sync_items():
                        if not self.is_running:
                            return

                        if c.author.name in self.name_blacklist:
                            continue

                        if self.is_blacklisted(c.message):
                            self.signals.update_terminal.emit(f"Chat from {c.author.name} contains blacklisted words. Ignoring.")
                            continue

                        if not c.message.startswith("!"):
                            chat_raw = re.sub(r':[^\s]+:', '', c.message)
                            chat_raw = chat_raw.replace('#', '')
                            chat = f"{c.author.name} : {chat_raw}"
                            self.signals.update_terminal.emit(chat)

                            detected_lang = self.detect_language(chat_raw)

                            tts_text = f"{c.author.name}, berkata: {chat_raw}"
                            await self.play_tts(session, tts_text, detected_lang)

                            if self.translation_enabled and detected_lang != 'id':
                                translated_chat = self.translate_text(chat_raw)
                                tts_text_translated = f"Artinya: {translated_chat}"
                                await self.play_tts(session, tts_text_translated, 'id')
                                self.signals.update_translation.emit(f"Translation: {translated_chat}")

                        await asyncio.sleep(0.1)  # Small delay to prevent overwhelming the UI
                except asyncio.CancelledError:
                    return
                except Exception as e:
                    self.signals.update_terminal.emit(f"Error receiving chat: {e}")
                    await asyncio.sleep(1)
                
                if not self.is_running:
                    return

    def is_blacklisted(self, chat):
        return any(word in chat.lower() for word in self.word_blacklist)

    def detect_language(self, text):
        translator = Translator()
        detected_lang = translator.detect(text)
        return detected_lang.lang

    def translate_text(self, text, target_language='id'):
        translator = Translator()
        translated_text = translator.translate(text, dest=target_language)
        return translated_text.text
    
    async def play_tts(self, session, text, lang):
        if not self.is_running:
            return

        encoded_text = urllib.parse.quote(text)
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={encoded_text}"
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3', dir=self.temp_dir)
        temp_filename = temp_file.name
        temp_file.close()

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    with open(temp_filename, "wb") as f:
                        f.write(data)
                    
                    self.volume_mutex.lock()
                    current_volume = self.volume
                    self.volume_mutex.unlock()

                    mixer.music.load(temp_filename)
                    mixer.music.set_volume(current_volume / 100)
                    mixer.music.play()
                    while mixer.music.get_busy() and self.is_running:
                        await asyncio.sleep(0.1)
        except Exception as e:
            self.signals.update_terminal.emit(f"Error playing TTS: {e}")

    def update_volume(self, volume):
        self.volume_mutex.lock()
        self.volume = volume
        self.volume_mutex.unlock()
        self.volume_condition.wakeAll()

    def stop(self):
        self.is_running = False
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.cancel_task)

    def cancel_task(self):
        if self.task and not self.task.done():
            self.task.cancel()

class MainWindow(QMainWindow):
    volume_changed = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text to Speech Livechat Youtube")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0688ff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #012240;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QCheckBox {
                color: black;
                font-size: 14px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_header()
        self.create_main_content()
        self.create_footer()

        self.word_blacklist = []
        self.name_blacklist = []
        self.chat_worker = None
        self.live_chat = None
        self.translation_enabled = True
        self.volume = 50
        self.is_muted = False
        self.previous_volume = 50

        # Initialize mixer
        mixer.init()

    def create_header(self):
        header = QLabel("Text to Speech Livechat Youtube")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #000000; margin: 20px 0;")
        self.layout.addWidget(header)

    def create_main_content(self):
        main_content = QWidget()
        main_layout = QVBoxLayout(main_content)

        video_id_layout = QHBoxLayout()
        video_id_label = QLabel("YouTube Live Video ID:")
        self.video_id_input = QLineEdit()
        video_id_layout.addWidget(video_id_label)
        video_id_layout.addWidget(self.video_id_input)
        main_layout.addLayout(video_id_layout)

        upload_layout = QHBoxLayout()
        self.word_blacklist_btn = QPushButton("Upload Word Blacklist")
        self.name_blacklist_btn = QPushButton("Upload Name Blacklist")
        upload_layout.addWidget(self.word_blacklist_btn)
        upload_layout.addWidget(self.name_blacklist_btn)
        main_layout.addLayout(upload_layout)

        control_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start TTS Livechat")
        self.stop_btn = QPushButton("Stop TTS Livechat")
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        main_layout.addLayout(control_layout)

        # Add volume control
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Volume:")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.mute_button = QPushButton("Mute")
        self.mute_button.clicked.connect(self.toggle_mute)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.mute_button)
        main_layout.addLayout(volume_layout)

        # Add Checkbox translation toggle
        self.translation_toggle = QCheckBox("Chat Translation")
        self.translation_toggle.setChecked(True)
        self.translation_toggle.setStyleSheet("""
            QCheckBox::indicator {
                width: 50px;
                height: 50px;
            }
            QCheckBox::indicator:unchecked {
                image: url(off.png);
            }
            QCheckBox::indicator:checked {
                image: url(on.png);
            }
        """)

        main_layout.addWidget(self.translation_toggle)

        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background-color: #000000; color: #00FF00;")
        main_layout.addWidget(self.terminal)

        self.layout.addWidget(main_content)

        # Connect buttons to functions
        self.word_blacklist_btn.clicked.connect(self.upload_word_blacklist)
        self.name_blacklist_btn.clicked.connect(self.upload_name_blacklist)
        self.start_btn.clicked.connect(self.start_tts_livechat)
        self.stop_btn.clicked.connect(self.stop_tts_livechat)
        self.translation_toggle.stateChanged.connect(self.toggle_translation)

    def change_volume(self, value):
        self.volume = value
        mixer.music.set_volume(self.volume / 100)
        if self.is_muted and value > 0:
            self.is_muted = False
            self.mute_button.setText("Mute")
        self.volume_changed.emit(value)

    def toggle_mute(self):
        if self.is_muted:
            self.is_muted = False
            self.volume_slider.setValue(self.previous_volume)
            self.mute_button.setText("Mute")
        else:
            self.is_muted = True
            self.previous_volume = self.volume_slider.value()
            self.volume_slider.setValue(0)
            self.mute_button.setText("Unmute")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_BracketLeft:
            new_volume = max(0, self.volume_slider.value() - 5)
            self.volume_slider.setValue(new_volume)
        elif event.key() == Qt.Key.Key_BracketRight:
            new_volume = min(100, self.volume_slider.value() + 5)
            self.volume_slider.setValue(new_volume)
        elif event.key() == Qt.Key.Key_Backslash:
            self.toggle_mute()
        else:
            super().keyPressEvent(event)
    
    def create_footer(self):
        footer = QLabel("Created by tobeoren")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("font-size: 12px; color: #888888; margin: 10px 0;")
        self.layout.addWidget(footer)

    def upload_word_blacklist(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Word Blacklist", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.word_blacklist = [line.strip() for line in file.readlines()]
            self.terminal.append(f"Word blacklist uploaded: {len(self.word_blacklist)} words")

    def upload_name_blacklist(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Name Blacklist", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.name_blacklist = [line.strip() for line in file.readlines()]
            self.terminal.append(f"Name blacklist uploaded: {len(self.name_blacklist)} names")

    def toggle_translation(self, state):
        self.translation_enabled = bool(state)
        if self.chat_worker:
            self.chat_worker.translation_enabled = self.translation_enabled
        status = "enabled" if self.translation_enabled else "disabled"
        self.terminal.append(f"Translation {status}")

    def start_tts_livechat(self):
        video_id = self.video_id_input.text()
        if video_id:
            self.terminal.clear()
            self.terminal.append(f"Starting TTS Livechat for video ID: {video_id}")
            
            # Initialize pytchat in the main thread
            self.live_chat = pytchat.create(video_id=video_id)
            
            # Start the chat worker
            self.chat_worker = ChatWorker(self.live_chat, self.word_blacklist, self.name_blacklist, self.translation_enabled)
            self.chat_worker.signals.update_terminal.connect(self.update_terminal)
            self.chat_worker.signals.update_translation.connect(self.update_translation)
            self.chat_worker.signals.finished.connect(self.on_worker_finished)
            self.volume_changed.connect(self.chat_worker.update_volume, Qt.ConnectionType.QueuedConnection)
            self.chat_worker.start()
            
             # Set initial volume
            self.volume_changed.emit(self.volume)
            
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
        else:
            self.terminal.append("Please enter a valid YouTube Live Video ID")
            
    def stop_tts_livechat(self):
        if self.chat_worker:
            self.terminal.append("Stopping TTS Livechat...")
            self.chat_worker.stop()
            self.stop_btn.setEnabled(False)
            QTimer.singleShot(100, self.check_worker_finished)  # Check every 100ms
            
    def send_volume_to_worker(self):
        self.volume_changed.emit(self.volume)
        
    def force_stop(self):
        if self.chat_worker and self.chat_worker.isRunning():
            self.terminal.append("Force stopping TTS Livechat...")
            self.chat_worker.terminate()
            self.chat_worker.wait()
            self.on_worker_finished()

    def check_worker_finished(self):
        if self.chat_worker and self.chat_worker.isFinished():
            self.on_worker_finished()
        else:
            QTimer.singleShot(100, self.check_worker_finished)

    def on_worker_finished(self):
        if self.live_chat:
            self.live_chat.terminate()
            self.live_chat = None
        self.chat_worker = None
        self.terminal.append("TTS Livechat stopped")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def update_terminal(self, message):
        self.terminal.append(message)

    def update_translation(self, message):
        self.terminal.append(message)

    def closeEvent(self, event):
        self.stop_tts_livechat()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())