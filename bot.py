import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Handler for /calculate
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    GROUP_ID = int(os.getenv("GROUP_ID", "0"))
    if GROUP_ID and update.effective_chat.id != GROUP_ID:
        return  # ignore messages outside your group
    try:
        funds   = float(context.args[0])
        risk_pct= float(context.args[1])
        margin  = round(funds * (risk_pct/100), 2)
        text    = (
            f"✅ Calculation Complete\n\n"
            f"• Available Funds: AED {funds:,.2f}\n"
            f"• Risk %: {risk_pct}%\n"
            f"• 💰 Margin Amount: AED {margin:,.2f}"
        )
    except:
        text = "⚠️ Usage: /calculate <funds> <risk_percentage>\nExample: /calculate 43327.45 5"
    await update.message.reply_text(text)

def main():
    TOKEN       = os.getenv("TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://<service>.run.app/webhook
    PORT        = int(os.getenv("PORT", "8080"))

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("calculate", calculate))

    # This will block, start aiohttp on 0.0.0.0:PORT, and set the webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    main()
