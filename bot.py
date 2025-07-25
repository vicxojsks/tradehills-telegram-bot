import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN    = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", "0"))

# 1) HTTP health check so Cloud Run sees a live port
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

def start_health_server():
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

# 2) Telegram /calculate handler
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
    except:
        text = "⚠️ Usage: /calculate <funds> <risk_percentage>\nExample: /calculate 43327.45 5"
    await update.message.reply_text(text)

def main():
    # Start health server
    threading.Thread(target=start_health_server, daemon=True).start()

    # Start Telegram polling bot
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("calculate", calculate))
    app.run_polling()

if __name__ == "__main__":
    main()
