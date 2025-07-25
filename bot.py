import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, ContextTypes

# — Bot setup —
TOKEN    = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", "0"))
bot      = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)

# /calculate handler
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if GROUP_ID and update.effective_chat.id != GROUP_ID:
        return
    try:
        funds, risk = map(float, context.args)
        margin = round(funds * (risk/100), 2)
        text = (
            f"✅ Calculation Complete\n\n"
            f"• Available Funds: AED {funds:,.2f}\n"
            f"• Risk %: {risk}%\n"
            f"• 💰 Margin Amount: AED {margin:,.2f}"
        )
    except Exception:
        text = "⚠️ Usage: /calculate <funds> <risk_percentage>\nExample: /calculate 43327.45 5"
    await update.message.reply_text(text)

dispatcher.add_handler(CommandHandler("calculate", calculate))

# — Flask app for webhook & health —
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        logging.info(f"Received update data: {data}")
        update = Update.de_json(data, bot)
        dispatcher.process_update(update)
    except Exception:
        logging.exception("Error processing webhook update")
    # Always return 200 and valid body so Cloud Run health sees a good response
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
