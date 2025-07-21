from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", "0"))  # Optional group restriction

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Optional group restriction
    if GROUP_ID and update.message.chat_id != GROUP_ID:
        return await update.message.reply_text("🚫 This bot is only available for Trade Hills clients.")

    try:
        funds = float(context.args[0])
        risk_pct = float(context.args[1])
        margin = round(funds * (risk_pct / 100), 2)

        response = (
            f"✅ Calculation Complete\n\n"
            f"• Available Funds: AED {funds:,.2f}\n"
            f"• Risk %: {risk_pct}%\n"
            f"• 💰 Margin Amount: AED {margin:,.2f}\n\n"
            f"👉 Adjust your position size in Capital.com so that the required margin ≈ AED {margin:,.2f}"
        )
        await update.message.reply_text(response)
    except:
        await update.message.reply_text("⚠️ Usage: /calculate <funds> <risk_percentage>\nExample: /calculate 43327.45 5")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("calculate", calculate))
app.run_polling()
