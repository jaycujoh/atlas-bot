# ATLAS - StarCraft II Replay Analysis Bot

🤖 **ATLAS** is an advanced Discord bot designed to analyze StarCraft II replays using OpenAI's GPT-4. Whether you're a casual player or a competitive gamer, ATLAS provides detailed build orders, tactical insights, and personalized recommendations to help you improve your gameplay.

## See it in action!

*Click the image to watch the video. (Subject to change)*

[![Watch the video](https://img.youtube.com/vi/KCKu0xiqbMo/0.jpg)](https://www.youtube.com/watch?v=KCKu0xiqbMo)

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

---

## Updates

### 🚀 Latest Changes
- **Removed `RESOURCES` Section**:
  - The `RESOURCES` section has been removed from the analysis to free up character space for more detailed insights in the existing sections (`STRATEGIC SUCCESS`, `TACTICAL WEAKNESS`, etc.).
  - This change ensures the bot focuses entirely on providing actionable advice and tactical analysis without relying on external links.

- **Enhanced Data Analysis**:
  - Improved the accuracy of replay data extraction by:
    - Tracking **unit production** more precisely using `UnitBornEvent` and `UnitInitEvent`.
    - Adding a `units_produced` dictionary to count the number of each unit type created during the game.
  - Updated the AI prompt to include **specific replay data** (e.g., units produced, build order) to ensure the analysis is based on accurate information.
  - Added validation checks to prevent the AI from making incorrect assumptions (e.g., claiming a "ling-bane" strategy was used when no Banelings were produced).

### ⏪ Previous Updates
- **Added Build Order Table**:
  - The bot now posts a formatted build order table to Discord, showing the time, supply, and units/buildings created for each player.
  - Grouped identical units created at the same time for better readability.

- **Improved Error Handling**:
  - Added error handling for cases where the replay contains only one player or fails to load.
  - Logged warnings for events that cannot be processed (e.g., unsupported unit types).

- **Enhanced AI Analysis**:
  - Updated the AI prompt to provide more detailed and actionable advice.
  - Increased the `max_tokens` limit to allow for longer and more comprehensive analysis.

### 🔮 Future Plans
- **Re-Adding the `RESOURCES` Section**:
  - Integrate a **web-browsing feature** into the AI to dynamically fetch relevant resources (e.g., articles, videos, and guides) based on the replay analysis.
  - Ensure the resources are **accurate and up-to-date** by linking to trusted sources like YouTube, TeamLiquid, and Reddit.
  - Provide tailored recommendations for specific challenges, such as countering a particular composition or improving build order execution.

- **Adding Commands**:
  - Introduce **user commands** to allow for more interactive and customizable analysis.
  - Examples:
    - `!analyze <replay_file>`: Analyze a specific replay file.
    - `!buildorder <player_name>`: Display the build order for a specific player.
    - `!resources <topic>`: Fetch resources for a specific topic (e.g., countering a particular strategy).

- **Creating an .exe File**:
  - Develop a standalone **.exe application** for easier installation and use, especially for users who are not familiar with Python or command-line tools.
  - This will make ATLAS more accessible to a wider audience.

- **Add More Detailed Metrics**:
  - Include additional metrics such as resource collection rates, APM (actions per minute), and unit losses.
- **Support for More Replay Types**:
  - Extend support for team games (2v2, 3v3, etc.) and custom game modes.
- **User Customization**:
  - Allow users to customize the analysis format (e.g., include/exclude specific sections, adjust the level of detail).

---

### 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

### 🤝 Contributing

Contributions are welcome! If you have any ideas, bug reports, or feature requests, please join my discord and I will be happy to help! [Discord](https://discord.gg/WDfzdWUUPY)

