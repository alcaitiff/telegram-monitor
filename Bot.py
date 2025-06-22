import os
import time
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))
WATCHED_FOLDER = os.getenv("WATCHED_FOLDER", "/watched")

bot = Bot(token=TELEGRAM_TOKEN)

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        print(f"📁 New file detected: {event.src_path}")
        time.sleep(1)  # Let the file finish writing

        # Schedule the send_file coroutine to run in the event loop
        asyncio.run(self.send_file(event.src_path))

    async def send_file(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                await bot.send_document(chat_id=TELEGRAM_USER_ID, document=f, filename=os.path.basename(filepath))
            print(f"✅ Sent file: {filepath}")
        except Exception as e:
            print(f"❌ Failed to send file: {filepath} — {e}")

if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()
    print(f"👀 Watching folder: {WATCHED_FOLDER}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
