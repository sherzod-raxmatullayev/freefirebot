import os
import django

# 1️⃣ Django settings modulini ko‘rsatish
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# 2️⃣ Django muhitini ishga tushirish
django.setup()

# 3️⃣ Endi modellardan import qilish mumkin
from main.models import TelegramUsers, Config

import asyncio
# 4️⃣ ORM bilan ishlash
# Config.objects.create(price=100, max_price=150)
# print("Yangi Config yaratildi!")
# user = await asyncio.to_thread(TelegramUsers.objects.filter(telegram_id=telegram_id).first)



data =  Config.objects.filter(name = 'main').first()
print(data.price)