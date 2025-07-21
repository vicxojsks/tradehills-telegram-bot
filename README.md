# 📈 Trade Hills Telegram Bot

A simple Telegram bot for calculating position size using /calculate.

### 🧮 Usage:
/calculate <available_funds> <risk_percentage>

Example:
/calculate 43327.45 5


---


---

## ✅ Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/project?template=https://github.com/vicxojsks/tradehills-telegram-bot)

1. Replace `YOUR_USERNAME` in the link above with your GitHub username
2. Click the Deploy button
3. Railway will:
   - Clone your GitHub repo
   - Ask for environment variables:
     - `TOKEN` = your Telegram Bot Token (from BotFather)
     - `GROUP_ID` = (optional) your Telegram group ID (numeric)
   - Install dependencies
   - Start the bot!

---

## 🧠 How to Find `GROUP_ID` (if you want to restrict usage)
1. Add your bot to your Telegram group
2. Use this temporary command in your bot script to print the group ID:
   ```python
   async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
       await update.message.reply_text(f"Group ID: {update.message.chat_id}")
