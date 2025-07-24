import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1️⃣ Health check server
def run_health_server():
    port = int(os.environ.get("PORT", "8080"))
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

# 2️⃣ Bot logic
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    GROUP_ID = int(os.getenv("GROUP_ID", "0"))
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
        await update.message.reply_text(
            "⚠️ Usage: /calculate <funds> <risk_percentage>\nExample: /calculate 43327.45 5"
        )

def main():
    # Start health server on its own thread
    threading.Thread(target=run_health_server, daemon=True).start()

    # Start Telegram bot
    TOKEN = os.getenv("TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("calculate", calculate))
    app.run_polling()

if __name__ == "__main__":
    main()
