# 📂 Telegram Monitor

Identify new files on a directory and send it to me via telegram bot
It runs inside a **Docker container** for easy setup and deployment.

---

## 🚀 Features

- Monitors a directory using `watchdog`
- Sends new files via a Telegram bot
- Lightweight and fully containerized with Docker

---

## 📦 Requirements

- [Docker](https://docs.docker.com/get-docker/)
- Telegram account

---

## 🔧 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/alcaitiff/telegram-monitor.git
cd telegram-monitor
```

### 2. Create a Telegram Bot

- Open Telegram and search for @BotFather
- Start a chat and use the command: /newbot
- Follow the prompts to:
  - Name your bot
  - Get a bot token (e.g., 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)
- Save this token for later.

### 3. Get Your Telegram User ID

- Search for @userinfobot
- Start the chat and it will reply with your user ID (e.g., 123456789)

### 4. Create a .env File

Inside the project directory, create a file called .env:

```bash
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_USER_ID=your_user_id_here
WATCHED_FOLDER=/watched
```

### 5. Build the Docker Image

- docker build -t telegram-watcher .

### 6. Run the Bot Container

Replace /path/to/folder with the folder you want to monitor:

```bash
docker run -d \
  --env-file .env \
  -v /path/to/folder:/watched \
  --name dir-watcher \
  telegram-watcher
```

The bot will now monitor /path/to/folder and send any new files to your Telegram account.

### 📄 Example

If you want to monitor ~/Downloads/new-files, use:

```bash
docker run -d \
  --env-file .env \
  -v $HOME/Downloads/new-files:/watched \
  --name dir-watcher \
  telegram-watcher
```

### ✅ Tips

- The bot only sends newly created files.
- If you stop the container: docker stop dir-watcher
- To remove: docker rm -f dir-watcher

### 🧼 Optional: Auto Start on Boot

To make the container start on reboot:

```bash
docker update --restart unless-stopped dir-watcher
```

### 🔒 Security Reminder

Do not share your bot token or user ID publicly.

### 📜 License

MIT License. Feel free to fork, use, or modify!
