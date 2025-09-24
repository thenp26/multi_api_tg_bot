# 🤖 Private AI Gateway Bot for Telegram

<div align="center">

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram_Bot_API-v6.8-blue?style=for-the-badge&logo=telegram)](https://core.telegram.org/bots/api)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge)](https://github.com/thenp26/multi_api_tg_bot/pulls)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

**A powerful, multi-provider Telegram bot that acts as your personal gateway to leading AI models like Gemini, GPT, and Claude. Bring your own API keys and switch between services seamlessly.**

</div>

---

<p align="center">
  <img src="https://github.com/thenp26/multi_api_tg_bot/blob/main/assets/demo.gif?raw=true" alt="Bot Demo GIF" width="600"/>
</p>

---

## 📖 Table of Contents

- [🎯 Why Build This?](#-why-build-this)
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [💬 Command Reference](#-command-reference)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Why Build This?

Many public AI bots on Telegram have limitations, ads, or require expensive subscriptions. If you're a developer with your own API keys, you're often forced to use separate bots for each service, with no control over your data or costs.

This project was built to create a **single, private, and powerful interface** for all your AI needs. It puts you in control, allowing you to leverage your own API keys under one roof, ensuring privacy and cost-effectiveness.

---

## ✨ Key Features

- 🧠 **Multi-Provider Hub**: Access Google Gemini, OpenAI GPT, Anthropic Claude, and Google Search from a single bot.
- 🔑 **Bring Your Own Key (BYOK)**: Securely save your personal API keys for each service. The bot never stores them publicly.
- 🔄 **Dynamic Provider Switching**: Instantly change your default AI model with a simple command (e.g., `/def_gemini`).
- 💾 **Persistent Memory**: Uses an SQLite database to remember each user's unique keys and preferences.
- 🛡️ **Channel Security**: Features a "Force Subscribe" mechanism to ensure only members of a designated channel can use the bot.
- 🌐 **Utility Commands**: Includes direct Wikipedia search (`/wikipedia`) and other helpful commands.

---

## 🛠️ Tech Stack

| Component            | Technology                                           |
| -------------------- | ---------------------------------------------------- |
| **Language** | Python 3.10+                                         |
| **Telegram Framework**| `python-telegram-bot`                               |
| **Database** | `SQLite3`                                            |
| **AI Integrations** | `google-generativeai`, `openai`, `anthropic`       |
| **Utilities** | `python-dotenv`, `googlesearch-python`               |

---

## 🚀 Getting Started

<details>
<summary><strong>Click here for setup and installation instructions</strong></summary>

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/thenp26/multi_api_tg_bot.git](https://github.com/thenp26/multi_api_tg_bot.git)
    cd multi_api_tg_bot
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** and add your bot's token and channel username:
    ```
    TELEGRAM_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    CHANNEL_USERNAME="@yourchannelusername"
    ```

5.  **Run the bot:**
    ```bash
    python bot.py
    ```
</details>

---

## 💬 Command Reference

| Command                 | Description                                    | Example                               |
| ----------------------- | ---------------------------------------------- | ------------------------------------- |
| `/start`                | Initializes the bot.                           | `/start`                              |
| `/help`                 | Shows a detailed help message.                 | `/help`                               |
| `/services`             | Lists all available services.                  | `/services`                           |
| `/gemini_api <KEY>`     | Saves your Google Gemini API key.              | `/gemini_api AIzaSy...`               |
| `/gpt_api <KEY>`        | Saves your OpenAI GPT API key.                 | `/gpt_api sk-...`                     |
| `/claude_api <KEY>`     | Saves your Anthropic Claude API key.           | `/claude_api sk-ant-...`              |
| `/def_gemini`           | Sets Gemini as the default provider.           | `/def_gemini`                         |
| `/def_gpt`              | Sets GPT as the default provider.              | `/def_gpt`                            |
| `/def_claude`           | Sets Claude as the default provider.           | `/def_claude`                         |
| `/def_google`           | Sets Google Search as the default.             | `/def_google`                         |
| `/wikipedia <QUERY>`    | Searches Wikipedia for a specific query.       | `/wikipedia Albert Einstein`          |

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to fork the repository, create a feature branch, and open a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
