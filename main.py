import os
from dotenv import load_dotenv
from keep_alive import keep_alive
from turkbot import bot  # Bot nesnesi turkbot.py içindeyse bu doğru

# Ortam değişkenlerini yükle (.env dosyası yerelde çalışırken işe yarar)
load_dotenv()

# Flask web sunucusunu başlat (Render için gereklidir)
keep_alive()

# Discord botunu başlat
bot.run(os.getenv("BOT_TOKEN"))
