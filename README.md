# Telegram AI Bot

A Telegram bot that uses the OPT-350M model to generate AI responses. This bot is optimized for M1 MacBooks and other devices with limited computational resources.

## Features

- Responds to messages using the OPT-350M model
- Optimized for M1 MacBooks
- Fast response times
- Simple command interface
- Error handling and fallback responses

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))
- M1 MacBook Pro (or other Apple Silicon device)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/itsresearcher/telegram-ai-bot.git
cd telegram-ai-bot
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Telegram bot token:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## Usage

1. Start the bot:
```bash
python3 bot.py
```

2. Open Telegram and find your bot
3. Send `/start` to begin
4. Send any message to get an AI response

## Commands

- `/start` - Start the bot and get a welcome message
- `/help` - Get help information
- Send any message to get an AI response

## Technical Details

- Uses the "facebook/opt-350m" model
- Optimized for M1 MacBooks
- Runs locally on your machine
- No API calls required after initial model download

## License

MIT License - feel free to use this project as you wish.

## Contributing

Feel free to submit issues and enhancement requests! 
