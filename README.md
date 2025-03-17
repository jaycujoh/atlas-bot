# ATLAS - StarCraft II Replay Analysis Bot

🤖 **ATLAS** is an advanced Discord bot designed to analyze StarCraft II replays using OpenAI's GPT-4. Whether you're a casual player or a competitive gamer, ATLAS provides detailed build orders, tactical insights, and personalized recommendations to help you improve your gameplay.

## See it in action!

*Click the image to watch the video.*

[![Watch the video](https://img.youtube.com/vi/VhAXUMRXJEQ/0.jpg)](https://www.youtube.com/watch?v=VhAXUMRXJEQ)
*Subject to change*
---

## 🌟 Features

- **Automated Replay Analysis**: ATLAS detects new replays and analyzes them in real-time.
- **Build Order Breakdown**: Get a detailed breakdown of your build order and your opponent's.
- **Tactical Insights**: Learn what you did well and where you can improve.
- **Counter-Strategies**: Receive tailored advice on how to counter your opponent's strategy.
- **Resource Recommendations**: Get links to up-to-date guides and videos to help you improve.

---

## 🛠️ Setup

### Prerequisites

1. **Python 3.13+**: Install from [python.org](https://www.python.org).
2. **Discord Bot Token**: Create a bot on the [Discord Developer Portal](https://discord.com/developers/applications).
3. **OpenAI API Key**: Sign up at [OpenAI](https://openai.com/api) and get an API key.

### Installation

### Windows PowerShell:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jaycujoh/atlas-bot-public.git
   ```
2. **Navigate to the directory:**
   ```bash
   cd atlas-bot-public
   ```
3. **Install Dependencies:**
   ```bash
    pip install -r requirements.txt
   ```
4. **Edit 'settings.py' in the 'config' directory with your credentials:**
   ```bash
    DISCORD_BOT_TOKEN = "your-discord-bot-token"
    OPENAI_API_KEY = "your-openai-api-key"
    REPLAYS_FOLDER = "path/to/replays/folder"
    DISCORD_CHANNEL_ID = "your-discord-channel-id"
   ```
5. **If necessary, Open 'openai_integration.py' in the 'bot' directory and replace the GPT model:**
   ```bash
   Example:
   model="gpt-4o",  # Replace with your model
   ```
6. **Run the Bot:**
   ```bash
    python main.py
   ```
---


## 💰 Donations

If you find ATLAS helpful, consider supporting its development! Your donations help keep the bot running.

🔗 [Support me on Patreon](https://www.patreon.com/c/jaycujoh)


## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.


## 🤝 Contributing

Contributions are welcome! If you have any ideas, bug reports, or feature requests, please join my discord and I will be happy to help! [Discord](https://discord.gg/WDfzdWUUPY)

