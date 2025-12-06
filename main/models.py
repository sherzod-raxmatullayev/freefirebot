from django.db import models

# Foydalanuvchilar bazasi
from django.db import models

class TelegramUsers(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"User {self.telegram_id} - Balance: {self.balance}"

    # ✅ Pul qo‘shish funksiyasi
    def add_balance(self, amount: int):
        if amount > 0:
            self.balance += amount
            self.save()
            return True
        return False

    # ✅ Pul ayirish funksiyasi (minusga tushib ketmasligi uchun himoyalangan)
    def remove_balance(self, amount: int):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

    # ✅ Balans yetarlimi tekshiruvchi funksiya
    def has_enough_balance(self, amount: int):
        return self.balance >= amount



# Referral tizimi
class Referals(models.Model):
    user = models.BigIntegerField()
    referal = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"User {self.user} referred {self.referal}"


# Kanallar ro'yxati
class Channels(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    telegram_id = models.BigIntegerField()
    link = models.TextField()

    def __str__(self):
        return f"Channel {self.name}"


# Ilovalar/abonentlar
class AppLacations(models.Model):
    user = models.BigIntegerField()
    channel = models.BigIntegerField()

    def __str__(self):
        return f"User {self.user} in Channel {self.channel}"

class Config(models.Model):
    name = models.TextField(max_length=20, default='main')
    price = models.IntegerField()
    max_price = models.IntegerField()














