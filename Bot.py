import os
import time
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

        time.sleep(1)  # Delay to ensure file is fully written
        try:
            with open(event.src_path, 'rb') as f:
                bot.send_document(chat_id=TELEGRAM_USER_ID, document=f, filename=os.path.basename(event.src_path))
            print(f"Sent file: {event.src_path}")
        except Exception as e:
            print(f"Error sending {event.src_path}: {e}")

if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()
    print(f"Watching folder: {WATCHED_FOLDER}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
