import os
import time
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from telegram import Bot
from dotenv import load_dotenv
from threading import Thread
from queue import Queue

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))
WATCHED_FOLDER = os.getenv("WATCHED_FOLDER", "/watched")

# Init Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)

# Queue for new files
file_queue = Queue()

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        print(f"📥 File queued: {event.src_path}")
        file_queue.put(event.src_path)

async def send_files():
    while True:
        filepath = await asyncio.to_thread(file_queue.get)
        try:
            print(f"⏳ Waiting for file to stabilize: {filepath}")
            if not await wait_until_stable(filepath):
                print(f"⚠️ File not stable or timeout: {filepath}")
                continue

            print(f"🚀 Sending file: {filepath}")
            with open(filepath, 'rb') as f:
                await bot.send_document(chat_id=TELEGRAM_USER_ID, document=f, filename=os.path.basename(filepath))
            print(f"✅ Sent file: {filepath}")
        except Exception as e:
            print(f"❌ Error sending {filepath}: {e}")
        finally:
            file_queue.task_done()


async def wait_until_stable(filepath, timeout=10, stable_seconds=2):
    """Wait until file size stays the same for `stable_seconds`."""
    last_size = -1
    stable_for = 0
    start = time.time()

    while time.time() - start < timeout:
        try:
            current_size = os.path.getsize(filepath)
        except FileNotFoundError:
            return False  # file deleted during wait

        if current_size == last_size:
            stable_for += 1
            if stable_for >= stable_seconds:
                return True
        else:
            stable_for = 0
            last_size = current_size

        await asyncio.sleep(1)

    return False


def start_watchdog():
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

if __name__ == "__main__":
    # Start watchdog in a thread
    Thread(target=start_watchdog, daemon=True).start()
    # Run the async send loop
    asyncio.run(send_files())
