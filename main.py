import os
from threading import Thread
from flask import Flask
from dotenv import load_dotenv
from turkbot import bot  # turkbot.py içinden bot nesnesini alıyoruz

load_dotenv()  # .env dosyasından değişkenleri yükle

# Sahte web sunucusu
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot şu anda çalışıyor."

def run_web():
    port = int(os.environ.get("PORT", 8080))  # Render’ın istediği PORT değişkeni
    app.run(host="0.0.0.0", port=port)

# Web server'ı ayrı thread'de başlat
Thread(target=run_web).start()

# Discord botu başlat
bot.run(os.getenv("BOT_TOKEN"))
