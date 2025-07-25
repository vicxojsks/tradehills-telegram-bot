import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, ContextTypes

# Basic Flask app for handling Telegram webhooks
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Read env vars
TOKEN    = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", "0"))
bot      = Bot(token=TOKEN)

# Set up dispatcher (no polling)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)

# Command handler
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if GROUP_ID and update.effective_chat.id != GROUP_ID:
        return
    args = context.args
    try:
        funds   = float(args[0])
        risk_pct= float(args[1])
        margin  = round(funds * (risk_pct/100), 2)
        text    = (
            f"✅ Calculation Complete\n\n"
            f"• Available Funds: AED {funds:,.2f}\n"
            f"• Risk %: {risk_pct}%\n"
            f"• 💰 Margin Amount: AED {margin:,.2f}"
        )
        await update.message.reply_text(text)
    except:
        await update.message.reply_text(
            "⚠️ Usage: /calculate <funds> <risk_percentage>\n"
            "Example: /calculate 43327.45 5"
        )

dispatcher.add_handler(CommandHandler("calculate", calculate))

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

# Health check on root
@app.route("/", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    # For local testing only
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
