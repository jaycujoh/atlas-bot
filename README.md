# ATLAS - StarCraft II Replay Analysis Bot

## 🤖 About ATLAS

ATLAS is an **open-source**, AI-powered Discord bot designed to help StarCraft II players analyze their replays and improve their gameplay. As a new developer and StarCraft II player, I wanted to create something that could help others learn and grow in the game.

## See it in action!

*Click the image to watch the video. (Subject to change)*

[![Watch the video](https://img.youtube.com/vi/KCKu0xiqbMo/0.jpg)](https://www.youtube.com/watch?v=KCKu0xiqbMo)

### **Current Approach**
- **Open-Source**: The bot is completely open-source, meaning anyone can download, modify, and host it themselves using their own OpenAI API key.
- **Future Plans**: If ATLAS gains enough traction, I plan to introduce a **hosted version** of the bot with additional features and support for those who prefer a ready-to-use solution.

### **How You Can Help**
- **Star the Repo**: Show your support by starring the repository!
- **Contribute**: If you’re a developer, feel free to fork the repo and submit pull requests.
- **Donate**: Support the project on [Patreon](https://www.patreon.com/c/jaycujoh/membership) to help fund future development.

---

## 🌟 Features

- **Automated Replay Analysis**: ATLAS detects new replays and analyzes them in real-time.
- **Build Order Breakdown**: Get a detailed breakdown of your build order and your opponent's.
- **Tactical Insights**: Learn what you did well and where you can improve.
- **Counter-Strategies**: Receive tailored advice on how to counter your opponent's strategy.
- **Recommendations**: What to do moving forward in to future games.

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
5. **(Optional) Open 'openai_integration.py' in the 'bot' directory and replace the GPT model:**
   ```bash
   model="gpt-4o",  # Replace with your model
   ```
6. **Run the Bot:**
   ```bash
    python main.py
   ```
---

## 🚀 Hosted Version (No AI)

For users who prefer a ready-to-use solution without AI functionality, a **hosted version** of ATLAS is available. This version focuses on replay parsing and build order extraction.

### **Features**:
- **Replay Upload**: Upload a replay file, and the bot will automatically process it.
- **Build Order Table**: The bot will post a formatted build order table showing time, supply, and units/buildings created.
- **No AI Analysis**: This version does not include AI-generated insights or recommendations.

### **How to Use**:
1. Invite the bot to your server using [this link](https://discord.com/oauth2/authorize?client_id=1350799094225961053).
2. Upload a replay file to the designated channel.
3. The bot will post the build order table.

---

## 💰 Donations

If you find ATLAS helpful, consider supporting its development! Your donations help keep the bot running.

🔗 [Support me on Patreon](https://www.patreon.com/c/jaycujoh)

---

## Updates

### 🚀 Latest Changes
- **Removed `RESOURCES` Section**: Focus on actionable advice without external links.
- **Enhanced Data Analysis**: Tracks unit production, counts units, validates data, and updates AI prompts.

### ⏪ Previous Updates
- **Added Build Order Table**: Formatted table with grouped units.
- **Improved Error Handling**: Handles single-player replays and logs unsupported units.
- **Enhanced AI Analysis**: Detailed prompts and increased `max_tokens`.

### 🔮 Future Plans
- **Re-Adding `RESOURCES` Section**: Web-browsing for tailored recommendations.
- **Adding Commands**: `!analyze`, `!buildorder`, `!resources`.
- **Creating an .exe File**: Easier installation for non-coders.
- **Add More Metrics**: Resource rates, APM, unit losses.
- **Support More Replay Types**: Team games (2v2, 3v3), custom modes.
- **User Customization**: Adjust analysis format and detail level.

---

### 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

### 🤝 Contributing

Contributions are welcome! If you have any ideas, bug reports, or feature requests, please join my discord and I will be happy to help! [Discord](https://discord.gg/WDfzdWUUPY)

