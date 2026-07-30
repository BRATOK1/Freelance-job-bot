# 🚀 Freelance Job Bot

A Telegram bot that collects freelance jobs from multiple platforms and displays them in one place.

## ✨ Features

- 🔎 Search freelance jobs
- 🌐 Collect jobs from multiple platforms
  - Reddit
  - Freelancer
  - PeoplePerHour
- 📄 Browse jobs with Previous / Next buttons
- 🌍 Open the original job page
- 🗑 Clear viewed jobs history
- 📊 View statistics
- 🚫 Automatically filters duplicate jobs

---

## 🛠 Tech Stack

- Python 3
- aiogram 3
- Requests
- Feedparser
- JSON
- Telegram Bot API

---

## 📂 Project Structure

```
freelance_bot/
│
├── models/
│   ├── job.py
│   └── source.py
│
├── sources/
│   ├── freelancer.py
│   ├── peopleperhour.py
│   └── reddit.py
│
├── config.py
├── engine.py
├── main.py
├── requirements.txt
└── seen_jobs.json
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/BRATOK1/Freelance-job-bot.git
```

Go to the project:

```bash
cd Freelance-job-bot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

Run the bot:

```bash
python main.py
```

---

## 📸 Preview

### Menu

![Menu](menu.png)


### Find Jobs

![Find Jobs](job.png)

### Help

![Help](help.png)

### Statistics

![Statistics](statistics.png)

### Clear History

![Clear History](ClearHistory.png)

---

## 🔮 Future Plans

- More freelance platforms
- Better job filtering
- Notifications for new jobs
- Database support
- Docker support

---

## 👨‍💻 Author

**Yaroslav Vlasenko**

GitHub:
https://github.com/BRATOK1

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.
