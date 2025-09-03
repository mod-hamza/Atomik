# 🤖 Atomik Discord Bot

A feature-rich Discord bot built with Python that provides server management tools, user information commands, and administrative functions.

## ✨ Features

- **User Management**: Ban, kick, and get user information
- **Channel Binding**: Bind resources like leaderboards, announcements, logs, and stats to specific channels
- **Admin Tools**: Comprehensive server administration commands
- **Developer Commands**: Bot management and debugging tools
- **Help System**: Built-in help command to discover all available features

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- A Discord bot token

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mod-hamza/Atomik.git
   cd Atomik
   ```

2. **Create and activate virtual environment with uv**
   ```bash
   uv venv
   ```

3. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file and add your Discord bot token:
   ```env
   BOT_TOKEN=your_actual_discord_bot_token_here
   ```

5. **Run the bot**
   ```bash
   uv run python main.py
   ```

And that's it! The bot should now be online and ready to use. 🎉

## 🔧 Configuration

### Getting a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application or select an existing one
3. Navigate to the "Bot" section
4. Copy the bot token and paste it into your `.env` file

### Environment Variables

The bot uses the following environment variables (see `.env.example`):

- `BOT_TOKEN`: Your Discord bot token (required)

## 📋 Available Commands

### 👥 Public Commands
- `/user_info` - Get information about a user
- `/help` - Show all available commands

### 🛡️ Admin Commands (Requires Administrator Permission)
- `/announce` - Send announcements to bound channel
- `/ban` - Ban members from the server
- `/bind` - Bind resources to channels
- `/kick` - Kick members from the server
- `/leaderboard` - Post leaderboard to bound channel
- `/ping-stats` - Send stats ping to bound channel
- `/rebind` - Change existing channel bindings
- `/status` - Check all channel binding statuses
- `/unbind` - Remove channel bindings

### 🔧 Developer Commands (Requires Developer Status)
- `/developers` - Add or remove bot developers
- `/reload` - Reload bot modules/cogs
- `/settings` - Database management and JSON extraction

## 🔗 Channel Binding System

The bot uses a channel binding system for organized content delivery:

- **leaderboard** - For leaderboard posts
- **announcements** - For server announcements
- **logs** - For logging events
- **stats** - For statistics and bot data

Use `/bind resource:type channel:#your-channel` to set up bindings, and `/status` to check current bindings.

## 📁 Project Structure

```
Atomik/
├── commands/          # Bot command modules
│   ├── announce.py    # Announcement commands
│   ├── ban.py         # Ban commands
│   ├── bind.py        # Channel binding
│   ├── help.py        # Help system
│   └── ...            # Other command files
├── json/              # JSON data storage
│   ├── developers.json
│   ├── guild_settings.json
│   └── ...
├── logs/              # Bot logs
├── util/              # Utility functions
├── main.py            # Bot entry point
├── requirements.txt   # Python dependencies
├── pyproject.toml     # Project configuration
└── .env.example       # Environment variables template
```

## 🛠️ Development

### Adding New Commands

1. Create a new Python file in the `commands/` directory
2. Follow the existing command structure using discord.py cogs
3. Add proper permission checks and error handling
4. Add it to `main.py`, so it loads on startup
5. Update the help command if needed

### Developer Setup

To add yourself as a developer:
1. Have an existing developer run `/developers add @your-username`
2. Your user ID will be added to `json/developers.json`

## 📝 Logging

The bot automatically creates detailed logs in the `logs/` directory with timestamps for debugging and monitoring purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


**Note**: This bot requires proper Discord permissions to function correctly. Make sure to grant necessary permissions like "Manage Messages", "Ban Members", "Kick Members", etc., depending on which features you want to use.
