from aiogram.types import Message, CallbackQuery, ChatJoinRequest
from aiogram.filters import Command
from aiogram import Router, F
import asyncio
from aiogram.filters import BaseFilter


from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import json

ADMIN_ID = 7365121857
DEVLOPER_ID = 6950463049

router = Router()



class chennel_state(StatesGroup):
    name = State()
    id = State()
    link = State()

class deletechannel(StatesGroup):
    sub_id = State()

class messagesClass(StatesGroup):
    mess = State()


class cantrolakk(StatesGroup):
    id = State()
    amout = State()

class sendmessagefol(StatesGroup):
    id = State()
    text = State()



class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in [7365121857, 6950463049]

import os
import django

# 1️⃣ Django settings modulini ko‘rsatish
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# 2️⃣ Django muhitini ishga tushirish
django.setup()

# 3️⃣ Endi modellardan import qilish mumkin
from main.models import TelegramUsers, Config, Channels, AppLacations, Referals

from asgiref.sync import sync_to_async

from loader import bot



async def button(user_id: int, referal) -> InlineKeyboardMarkup | None:
    kb = InlineKeyboardBuilder()

    channels = await sync_to_async(lambda: list(Channels.objects.all()))()
    if not channels:
        return None

    for channel in channels:
        channel_id = channel.telegram_id
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            apl_exists = await sync_to_async(lambda: AppLacations.objects.filter(
                user=user_id, channel=channel_id
            ).exists())()

            if member.status in ("creator", "administrator", "member", "restricted") or apl_exists:
                continue
            else:
                kb.button(text=channel.name, url=channel.link)

        except Exception:
            kb.button(text=channel.name, url=channel.link)
        finally:
            if referal != None:
                kb.button(text='✅ Tekshirish', url=f'https://t.me/MrUzbekFreeFire_bot?start={referal}')
            else:
                kb.button(text='✅ Tekshirish', url=f'https://t.me/MrUzbekFreeFire_bot?start={user_id}')
        

    if kb:  
        return kb.adjust(1)


class call_data(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> bool:
        user_id = call.from_user.id

        # Barcha kanallarni olish (sync → async)
        channels = await sync_to_async(lambda: list(Channels.objects.all()))()
        if not channels:
            return False

        for channel in channels:
            channel_id = channel.telegram_id  # ORM field

            try:
                # Bot bilan tekshirish (async)
                member = await call.bot.get_chat_member(channel_id, user_id)

                # Applications da foydalanuvchi borligini tekshirish (sync → async)
                apl_exists = await sync_to_async(lambda: AppLacations.objects.filter(
                    user=user_id, channel=channel_id
                ).exists())()

                # Agar foydalanuvchi kanal a'zos bo'lsa yoki apl mavjud bo'lsa skip
                if member.status in ("creator", "administrator", "member", "restricted") or apl_exists:
                    continue
                else:
                    return True  # foydalanuvchi a'zo emas va application mavjud emas

            except Exception:
                # Xatolik bo‘lsa, filter False qaytarsin
                return False

        return False
class mess_data(BaseFilter):
    async def __call__(self, call: Message) -> bool:
        user_id = call.from_user.id

        # Barcha kanallarni olish (sync → async)
        channels = await sync_to_async(lambda: list(Channels.objects.all()))()
        if not channels:
            return False

        for channel in channels:
            channel_id = channel.telegram_id  # ORM field

            try:
                # Bot bilan tekshirish (async)
                member = await call.bot.get_chat_member(channel_id, user_id)

                # Applications da foydalanuvchi borligini tekshirish (sync → async)
                apl_exists = await sync_to_async(lambda: AppLacations.objects.filter(
                    user=user_id, channel=channel_id
                ).exists())()

                # Agar foydalanuvchi kanal a'zos bo'lsa yoki apl mavjud bo'lsa skip
                if member.status in ("creator", "administrator", "member", "restricted") or apl_exists:
                    continue
                else:
                    return True  # foydalanuvchi a'zo emas va application mavjud emas

            except Exception:
                # Xatolik bo‘lsa, filter False qaytarsin
                return False

        return False






@router.message(mess_data())
async def mandatory_message(message: Message):
    referel = None
    if message.text.startswith('/start'):
        full_args = message.text.split(' ')
        if len(full_args) > 1:
            _, referel = full_args
    kb = await button(message.from_user.id, referel)
    if kb:
        await message.answer("Iltimos, quyidagi kanallarga obuna bo'ling va tekshirishni  bosing:", reply_markup=kb.as_markup())

@router.callback_query(call_data())
async def mandatory_callback(query: CallbackQuery):
    kb = await button(query.from_user.id, None)
    if kb:
        await query.answer("Iltimos, quyidagi kanallarga obuna bo'ling va /start bosing.", reply_markup=kb.as_markup())








@router.chat_join_request(F.chat.type.in_({"supergroup", "channel"}))
async def handle_join_request(event: ChatJoinRequest):
    await sync_to_async(lambda: AppLacations.objects.create(user = event.from_user.id, channel = event.chat.id))()


channels_settings_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ 📢 Kanal qo'shish"),
            KeyboardButton(text="🗑 📢 Kanal o'chirish")
        ],
        [
            KeyboardButton(text="📜 📢 Kanallar ro'yxati")
        ],
        [
            KeyboardButton(text="🚫Chiqish")
        ]
    ],
    resize_keyboard=True
)

admin_panel_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊Statistika"),
            KeyboardButton(text="Hisobni boshqarish💰"),
        ],
     
        [
            KeyboardButton(text="📝Xabar yuborish"),
            KeyboardButton(text="Kanal sozlamalari📢"),
        ],
        [
            KeyboardButton(text="Foydalanuvchiga xabar yuborish"),
        ],
        [
            KeyboardButton(text="🚫Chiqish"),
        ]
    ],
    resize_keyboard=True
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Bekor qilish.", callback_data="bekor")
        ]
    ]
)





@router.message(F.text.startswith('/min'), IsAdmin())
async def f11(message: Message):
    try:
        # /min 1000 → 1000 ni ajratib olish
        new_amount = int(message.text.split(' ')[1])

        # Config obyektini olish
        config = await sync_to_async(lambda: Config.objects.filter(name='main').first())()
        if not config:
            await message.answer(
                "⚠️ Config topilmadi. Iltimos, keyinroq urinib ko‘ring.",
                reply_markup=admin_panel_buttons
            )
            return

        # Min withdraw qiymatini yangilash
        @sync_to_async
        def update_config_min(config_obj, value):
            config_obj.max_price = value
            config_obj.save()
            return True

        updated = await update_config_min(config, new_amount)

        if updated:
            await message.answer(
                "✅ Minimal chiqarish miqdori muvaffaqiyatli o'zgartirildi!",
                reply_markup=admin_panel_buttons
            )
        else:
            await message.answer(
                "⚠️ Noto‘g‘ri amal, dasturchini ayblamang 🙂",
                reply_markup=admin_panel_buttons
            )

    except (IndexError, ValueError):
        await message.answer(
            "⚠️ Iltimos, to‘g‘ri formatda kiriting. Masalan: /min 1000",
            reply_markup=admin_panel_buttons
        )

    except Exception as e:
        print("Xatolik f11 handlerda:", e)
        await message.answer(
            "⚠️ Noto‘g‘ri amal, dasturchini ayblamang 🙂",
            reply_markup=admin_panel_buttons
        )


@router.message(F.text.startswith('/ref'), IsAdmin())
async def f11(message:Message):
    try:
        new_amout = int(message.text.split(' ')[1])
        config = await sync_to_async(lambda val: Config.objects.filter(name='main').update(price=val))(new_amout)
        if config:
            await message.answer('Agar adashmagan bo\'lsam narx o\'zgardi!', reply_markup=admin_panel_buttons)
        else:
            await message.answer('Nimadirni xato qilding buning uchun dasturchini ayiblama!!!', reply_markup=admin_panel_buttons)
    except:
        await message.answer('Nimadirni xato qilding buning uchun dasturchini ayiblama!!!', reply_markup=admin_panel_buttons)


@router.message(sendmessagefol.text)
async def f3(message:Message, state:FSMContext):
    try:
        data = await state.get_data()
        user_id = data['user_id']
        text = message.text
        await message.bot.send_message(chat_id=user_id, text=f'Sizga admindan xabar:\n\n{text}')
        await message.answer('Xabar yuborildi!', reply_markup=admin_panel_buttons)
        await state.clear()
    except:
        await message.answer('Xabar yuborishda xato qaytadan urinib ko\'ring', reply_markup=admin_panel_buttons)
        await state.clear()

@router.message(sendmessagefol.id)
async def f2(message:Message, state:FSMContext):
    try:
        id = int(message.text)
        await state.update_data(user_id = id)
        await message.answer('Yuboriladigan xabarni kiriting!', reply_markup=back)
        await state.set_state(sendmessagefol.text)
    except:
        await message.answer('xatolik qayta urinib ko\'r', reply_markup=back)
        await state.set_state(sendmessagefol.id)

@router.message(IsAdmin(), F.text == 'Foydalanuvchiga xabar yuborish')
async def f1(message: Message, state:FSMContext):
    await message.answer('Foydalanuvchi ID sini yuboring!', reply_markup=back)
    await state.set_state(sendmessagefol.id)






from asgiref.sync import sync_to_async

@router.message(cantrolakk.amout)
async def cantrolamout(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        us_id = data.get('id')
        amount = int(message.text)

        # Foydalanuvchini olish
        user = await sync_to_async(lambda: TelegramUsers.objects.filter(telegram_id=us_id).first())()
        if not user:
            await message.answer("⚠️ Foydalanuvchi topilmadi!", reply_markup=admin_panel_buttons)
            await state.clear()
            return

        # Balansni yangilash
        if amount > 0:
            await sync_to_async(user.add_balance)(amount)
        else:
            await sync_to_async(user.remove_balance)(abs(amount))

        await message.answer("✅ Bajarildi", reply_markup=admin_panel_buttons)
        await state.clear()

    except ValueError:
        await message.answer("⚠️ Iltimos, to‘g‘ri son kiriting.", reply_markup=admin_panel_buttons)
        await state.clear()

    except Exception as e:
        print("Xatolik:", e)
        await message.answer("⚠️ Xatolik bo‘ldi", reply_markup=admin_panel_buttons)
        await state.clear()


@router.message(cantrolakk.id)
async def cantrolid(message:Message, state:FSMContext):
    try:
        user = await sync_to_async(lambda: TelegramUsers.objects.filter(telegram_id=int(message.from_user.id)).first())()
        if user:
            await state.update_data(id = int(message.text))
            await message.answer(f'Balanse: {user.balance} Balanceni kamaytirish uchun manfiy son ko\'paytirish uchun musbat son yuboring!', reply_markup=back)
            await state.set_state(cantrolakk.amout)
        else:
            await message.answer('Bunday foydalanuvchi yo\'q', reply_markup=back)
    except Exception as e:
        await message.answer("xatolik", reply_markup=back)
        print('Balance',e )

@router.message(IsAdmin(), F.text == 'Hisobni boshqarish💰')
async def cantrolakkk(message:Message, state:FSMContext):
    await message.answer('foydalanuvchi ID sini yuboring!', reply_markup=back)
    await state.set_state(cantrolakk.id)
    



@router.message(messagesClass.mess)
async def message_state(message: Message, state: FSMContext):
    users = await sync_to_async(lambda: list(TelegramUsers.objects.all()))()


    error = 0
    count = 0

    for user in users:
        try:
            # ✅ AGAR XABAR MATN BO'LSA
            if message.text:
                await message.bot.send_message(
                    chat_id=user.telegram_id,
                    text=message.text
                )

            # ✅ AGAR XABAR RASM BO'LSA
            elif message.photo:
                await message.bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=message.photo[-1].file_id,
                    caption=message.caption if message.caption else None
                )

            # ✅ AGAR XABAR VIDEO BO'LSA (ixtiyoriy)
            elif message.video:
                await message.bot.send_video(
                    chat_id=user.telegram_id,
                    video=message.video.file_id,
                    caption=message.caption if message.caption else None
                )

            count += 1
            await asyncio.sleep(0.1)

        except Exception as e:
            print('Xabar tarqatishda muamo:', e)
            error += 1

    await message.answer(
        text=f"✅ Xabar yetkazildi: {count}\n❌ Tarqatilmadi: {error}",
        reply_markup=admin_panel_buttons
    )

    await state.clear()




@router.message(F.text == "📝Xabar yuborish", IsAdmin())
async def tarqart(message:Message, state: FSMContext):
    await message.answer(text="Tarqatmoqchi bo'lgan xabaringizni yuboring.", reply_markup=back)
    await state.set_state(messagesClass.mess)
    




@router.message(chennel_state.link)
async def channelLink(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        name = data.get('name')
        channel_id = data.get('id')
        channel_link = message.text

        # Kanal qo'shish
        result = await sync_to_async(
            lambda n, cid, link: Channels.objects.create(
                name=n,
                telegram_id=cid,
                link=link
            )
        )(name, channel_id, channel_link)

        if result:
            await message.answer(
                text="Kanal qo'shildi!",
                reply_markup=admin_panel_buttons
            )
            await state.clear()
        else:
            await message.answer(
                "Nimadir xato ketdi",
                reply_markup=admin_panel_buttons
            )

    except Exception as e:
        print("Link olish va bazaga kanal qo‘shishda muammo:", e)
        await message.answer(
            "Xatolik yuz berdi. Iltimos, qayta urinib ko‘ring.",
            reply_markup=admin_panel_buttons
        )


@router.message(chennel_state.id)
async def chanelid(message:Message, state:FSMContext):
    if message.text:
        await state.update_data(id = int(message.text))
        await message.answer('Kanla havolasini bering!')
        await state.set_state(chennel_state.link)
    else:
        await message.answer('faqat son kiriting!')
        await state.set_state(chennel_state.id)

@router.message(chennel_state.name)
async def chennal_hendler_1(message: Message, state: FSMContext):
    if message.text:
        try: 
            await state.update_data(name = message.text)
            await message.answer('ID ni yuboring', reply_markup=bekor_qilish)
            await state.set_state(chennel_state.id)
        except Exception as e:
            await message.answer("Qayta urinib ko'r")
            await state.set_state(chennel_state.name)


@router.message(deletechannel.sub_id)
async def deletechannelstatehendler(message: Message, state: FSMContext):
    try:
        channel_id = int(message.text)
        
        # Kanalni olish
        channel_qs = await sync_to_async(lambda: Channels.objects.filter(id=channel_id))()
        
        # O'chirish
        deleted_count = await sync_to_async(channel_qs.delete)()
        
        if deleted_count[0] > 0:  # delete() → (deleted_objects_count, {...})
            await message.answer(
                "Kanal majburiy obunadan o'chirildi",
                reply_markup=admin_panel_buttons
            )
        else:
            await message.answer("Kanalni o'chirib bo'lmadi")
        
        await state.clear()

    except ValueError:
        await message.answer(
            "ID faqat son bo'ladi!",
            reply_markup=back
        )
        await state.set_state(deletechannel.sub_id)

    except Exception as e:
        print("Xatolik:", e)
        await message.answer(
            "Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
            reply_markup=back
        )
        await state.set_state(deletechannel.sub_id)



@router.message(IsAdmin(), F.text == 'Kanal sozlamalari📢')
async def set_12(message:Message):
    await message.answer(text='Kanal sozlamalari', reply_markup=channels_settings_button)



@router.message(IsAdmin(), F.text == "🗑 📢 Kanal o'chirish")
async def delete_channel_hendler(message:Message, state: FSMContext):
    await message.answer(text="O'chirmoqchi bo'lgan kanal ID sini kiriting! ID ni ro'yxadlar bo'limidan oling.")
    await state.set_state(deletechannel.sub_id)

@router.message(IsAdmin(), F.text == "➕ 📢 Kanal qo'shish")
async def chennal_hendler(message:Message, state:FSMContext):
    await message.answer(text="Kanal nomini kiriting", 
                         reply_markup=back)
    await state.set_state(chennel_state.name)

@router.message(F.text == "📜 📢 Kanallar ro'yxati", IsAdmin())
async def channels_aount(message: Message):
    # Barcha kanallarni olish
    channels = await sync_to_async(lambda: list(Channels.objects.all()))()
    
    if not channels:
        await message.answer("Kanala yo'q")
        return

    # Har bir kanalni jo'natish
    for ch in channels:
        await message.answer(
            f"ID: {ch.id}\n"
            f"Telegram id: {ch.telegram_id}\n"
            f"Name: {ch.name}"
        )

@router.message(F.text == '📊Statistika', IsAdmin())
async def admin_statistics(message: Message):
    if message.from_user.id == ADMIN_ID or message.from_user.id == DEVLOPER_ID:
        user_count = await sync_to_async(lambda: TelegramUsers.objects.all().count())()
        referal_count = await sync_to_async(lambda: Referals.objects.all().count())()
        await message.answer(f"📊Bot statistikasi:\n\n👥 Foydalanuvchilar soni: {user_count}\n🔗 Takliflar soni: {referal_count}")


@router.message(Command("panel"), IsAdmin())
async def admin_panel_main(message: Message):
    if message.from_user.id == ADMIN_ID or message.from_user.id == DEVLOPER_ID:
        await message.answer(f"👨‍💼Admin panelga xush kelibsiz!", reply_markup=admin_panel_buttons)
    else:
        await message.answer("⚠️ Sizda admin panelga kirish huquqi yo'q.")


@router.message(F.text.in_(['🚫 Bekor qilish', '🚫Chiqish']))
async def cancel_withdraw(message: Message, state: FSMContext):
    await message.answer(f"🔝 Asosiy Menyu, {message.from_user.full_name}!", reply_markup=start_button)
    await state.clear()



#  Balance Headerlari


class yechish(StatesGroup):
    miqdor = State()



bekor_qilish = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚫 Bekor qilish")
        ]
    ],
    resize_keyboard=True
)

def yechish_button(user_id: int, price: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📥Tayyor💎", callback_data=f"Y_{user_id}_{price}")
    builder.button(text='Rad etish❌', callback_data=f'R_{user_id}_{price}')
    builder.adjust(1)
    return builder.as_markup()



#R_{user_id}_{price}
@router.callback_query(F.data.startswith("R_"))
async def process_withdraw_reject(callback_query: CallbackQuery, state: FSMContext):
    try:
        _, user_id, infop = callback_query.data.split("_")
        user_id = int(user_id)
        infop = int(infop)
        user_data = await sync_to_async(lambda: TelegramUsers.objects.filter(telegram_id = user_id).first())()
        await sync_to_async(user_data.add_balance)((infop))

                                        
        await callback_query.message.answer(f"❌ Yechib olish talabi rad etildi!\n\nFoydalanuvchi ID: {user_id}\nMiqdor: {infop}💎", reply_markup=start_button)
        await callback_query.bot.send_message(user_id, f"❌ Sizning {infop}💎 miqdordagi yechib olish talabingiz rad etildi. Mablag' hisobingizga qaytarildi.", reply_markup=start_button)
        await callback_query.message.delete()
    except Exception as e:
        print("Xatolik:", e)
        await callback_query.message.answer("⚠️ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")



#Y_{user_id}_{price}
@router.callback_query(F.data.startswith("Y_"))    
async def process_withdraw_approve(callback_query: CallbackQuery, state: FSMContext):
    try:
        _, user_id, pricee = callback_query.data.split("_")
        user_id = int(user_id)
        pricee = int(pricee)
        await callback_query.message.answer(f"✅ Yechib olish talabi tasdiqlandi!\n\nFoydalanuvchi ID: {user_id}\nMiqdor: {pricee}💎", reply_markup=start_button)
        await callback_query.bot.send_message(user_id, f"✅Sizning olmos chiqarish haqidagi arzangiz qabul qilindi❗️Olmoslaringiz FreeFire akkauntingizga tashlab berilmoqda....⏳", reply_markup=start_button)
        await callback_query.message.delete()
    except Exception as e:
        print("Xatolik:", e)
        await callback_query.message.answer("⚠️ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        

@router.message(yechish.miqdor)
async def process_withdraw_amount(message: Message, state: FSMContext):
    try:
        # Configni olish
        config = await sync_to_async(lambda: Config.objects.filter(name='main').first())()
        if not config:
            await message.answer("⚠️ Config topilmadi. Iltimos, keyinroq urinib ko‘ring.")
            return

        # Foydalanuvchi kiritgan miqdor
        if not message.text.isdigit():
            await message.answer(f"⚠️ Noto'g'ri miqdor kiritildi. Iltimos, kamida {config.max_price}💎 miqdorni kiriting.")
            await state.set_state(yechish.miqdor)
            return

        amount = int(message.text)
        if amount < config.max_price:
            await message.answer(f"⚠️ Minimal chiqarish miqdori {config.max_price}💎 hisoblanadi.")
            await state.set_state(yechish.miqdor)
            return

        user_id = message.from_user.id

        # Foydalanuvchini olish
        user = await sync_to_async(lambda: TelegramUsers.objects.filter(telegram_id=user_id).first())()
        if not user:
            await message.answer("⚠️ Siz ro'yxatdan o'tmagansiz.")
            await state.clear()
            return

        # Referallar soni
        referal_count = await sync_to_async(lambda: Referals.objects.filter(user=user_id).count())()

        # Balansni tekshirish
        if user.balance < amount:
            await message.answer("⚠️ Sizning hisobingizda yetarli mablag' mavjud emas. Iltimos, boshqa miqdorni kiriting.")
            await state.set_state(yechish.miqdor)
            return

        # Balansni yechish
        await sync_to_async(user.remove_balance)(amount)

        # Foydalanuvchiga javob
        await message.answer(
            "✅ Yechib olish talabingiz qabul qilindi! Tez orada adminlar tomonidan ko'rib chiqiladi.",
            reply_markup=start_button
        )

        # Admin va developerga xabar
        text = (
            f"Yechib olish talabi:\n"
            f"Foydalanuvchi: {message.from_user.full_name}\n"
            f"ID: {user_id}\n"
            f"Miqdor: {amount}💎\n"
            f"Referallar soni: {referal_count}\n\n"
            f"Balance: {user.balance}"
        )

        await message.bot.send_message(ADMIN_ID, text, reply_markup=yechish_button(user_id, amount))
        await message.bot.send_message(DEVLOPER_ID, text, reply_markup=yechish_button(user_id, amount))

        await state.clear()

    except Exception as e:
        print("Xatolik:", e)
        await message.answer("⚠️ Noto'g'ri miqdor kiritildi. Iltimos, qayta urinib ko'ring.")
        await state.set_state(yechish.miqdor)



@router.callback_query(F.data.startswith("yechish_"))
async def process_withdraw_callback(callback_query: CallbackQuery, state: FSMContext):
    user_id = int(callback_query.data.split("_")[1])
    user = await sync_to_async( lambda: TelegramUsers.objects.filter(
        telegram_id = user_id
    ).first())()
    config = await sync_to_async(lambda: Config.objects.filter(name='main').first())()
    balance = user.balance
    if balance and balance >= config.max_price:
        await callback_query.message.answer('Yechib olish uchun miqdorni kiriting:', reply_markup=bekor_qilish)
        await state.set_state(yechish.miqdor)
    else:
        await callback_query.message.answer(f"⚠️ Sizning hisobingizda yetarli mablag' mavjud emas. Minimal yechib olish miqdori: {config.max_price}💎")
        









def balance_button(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📥Olmoslarni chiqarib olish💎", callback_data=f"yechish_{user_id}")
    builder.adjust(1)
    return builder.as_markup()


@router.message(F.text == '🆓Olmos ishlash💎')
async def balance_command(message: Message):
    user_id = message.from_user.id
    user = await sync_to_async( lambda: TelegramUsers.objects.filter(
        telegram_id = user_id
    ).first())()
    config = await sync_to_async(lambda: Config.objects.filter(name='main').first())()
    pr = config.price
    mini = config.max_price
    referal = await sync_to_async(lambda: Referals.objects.filter(user = message.from_user.id).count())()
    await message.answer(
    f"🆔 <code>{user_id}</code>\n\n"
    f"💰 Sizning balansingiz: {user.balance} 💎\n\n"
    f"🔗 Sizning taklif havolangiz:\n"
    f"<code>https://t.me/MrUzbekFreeFire_bot?start={user_id}</code>\n\n"
    f"👥 Siz taklif qilgan odamlar soni: {referal}\n\n"
    f"➕ Har bir taklif uchun {pr} 💎 olmos olasiz.\n\n"
    f"<blockquote>⚠️ Minimal chiqarish miqdori {mini} 💎 hisoblanadi</blockquote>",
    reply_markup=balance_button(user_id),
    parse_mode="HTML"
)





@router.callback_query(F.data == 'bekor', IsAdmin())
async def bekcal(cal:CallbackQuery, state:FSMContext):
    await cal.message.answer('Admin panel', reply_markup=admin_panel_buttons)
    await cal.message.delete()

    await state.clear()



# Aloqa headerlari



def user_message_keyboard(user_id) -> InlineKeyboardButton:
    kb = InlineKeyboardBuilder()
    kb.button(text="Javob berish", callback_data=f"user_message_{user_id}")
    kb.button(text="🚫 Bekor qilish", callback_data=f"cancel_{user_id}")
    return kb.as_markup(resize_keyboard=True)

bekor_qilish = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚫 Bekor qilish")
        ]
    ],
    resize_keyboard=True
)





class Aloqa(StatesGroup):
    message = State()
class Javob(StatesGroup):
    javob = State()


aloqa = Router()



@router.message(Javob.javob)
async def javob_message(message: Message, state: FSMContext):
    if message.text == '🚫 Bekor qilish':
        await message.answer(f"🔝 Asosiy Menyu, {message.from_user.full_name}!", reply_markup=start_button)
        await state.clear()
    data = await state.get_data()
    user_id = data.get("user_id")
    await message.bot.send_message(chat_id=user_id, text=f"📝 Adminga yozgan xabaringizga javobi:\n\n{message.text}", reply_markup=start_button)
    await message.answer("✅ Javob foydalanuvchiga yuborildi!", reply_markup=start_button)
    await state.clear()

@router.callback_query(F.data.startswith("user_message_"))
async def user_message_callback(call:CallbackQuery, state: FSMContext):
    id = int(call.data.split("_")[2])
    await call.bot.send_message(chat_id=DEVLOPER_ID, text="📝 Iltimos, userga yozmoqchi bo'lgan javob matningizni kiriting:", reply_markup=bekor_qilish)
    await state.set_state(Javob.javob)
    await state.update_data(user_id=id)

@router.callback_query(F.data.startswith("cancel_"))
async def cancel_callback(call:CallbackQuery, state: FSMContext):
    id = int(call.data.split("_")[1])
    await call.bot.send_message(chat_id=id, text="🚫 Murojaat bekor qilindi!", reply_markup=start_button)
    await call.message.delete()
    await state.clear()

@router.message(Aloqa.message)
async def aloqa_message(message: Message, state: FSMContext):
    if message.text == '🚫 Bekor qilish':
        await message.answer(f"🔝 Asosiy Menyu, {message.from_user.full_name}!", reply_markup=start_button)
        await state.clear()
    else:
        admin = await sync_to_async(lambda: TelegramUsers.objects.filter(telegram_id=int(message.from_user.id)).first())()
        referal = await sync_to_async(lambda: Referals.objects.filter(user = message.from_user.id).count())()
        
        try:
            await message.bot.send_message(chat_id=ADMIN_ID, text=f"👤 Foydalanuvchi: {message.from_user.full_name}\n🆔 ID: {message.from_user.id}\nUser name: @{message.from_user.username}\nBalnace: {admin.balance}\nReferal: {referal} \n\n📝 Murojaat matni:\n{message.text}"
                                       , reply_markup=user_message_keyboard(message.from_user.id))
        except:
            pass
        await message.bot.send_message(chat_id=DEVLOPER_ID, text=f"👤 Foydalanuvchi: {message.from_user.full_name}\n🆔 ID: {message.from_user.id}\nUser name: @{message.from_user.username}\nBalnace: {admin.balance}\nReferal: {referal} \n\n📝 Murojaat matni:\n{message.text}"
                                       , reply_markup=user_message_keyboard(message.from_user.id))
        await message.answer("✅ Murojaatingiz adminga yuborildi! Tez orada javob olasiz.", reply_markup=start_button)
        await state.clear()



@router.message(F.text == "👤Admin bilan bog'lanish📝")
async def admin_b(message: Message, state: FSMContext):
    await message.answer("👤 Adminga yozmoqchi bo'lgan murojaatingizni yozib qoldiring📝\n🧑‍💻Admin murojaatingizni 🕐tez orada o'qib chiqadi📖", reply_markup=bekor_qilish)
    await state.set_state(Aloqa.message)




# START HEADERS

# BUTTONS

start_button = ReplyKeyboardMarkup (
    keyboard=[
        [KeyboardButton(text='Free Fire stikerlar📁'), KeyboardButton(text='🆕Free Fire yangiliklar📰')],
        [KeyboardButton(text='🆓Olmos ishlash💎'), KeyboardButton(text='🛍️To\'lovlar kanali💰')],
        [KeyboardButton(text='👤Admin bilan bog\'lanish📝'), KeyboardButton(text='💎olmos sotib olish🛍️')],
        [KeyboardButton(text='🆓Free Fire akkauntga like👍')],
        
    ]
)

# BUTTONS






@router.message(Command('start'))
async def start_header(message: Message):
    try:
        full_args = message.text.split(' ')
        referel = None
        if len(full_args) > 1:
            _, referel = full_args

        # Foydalanuvchini olish yoki yaratish
        user, created = await sync_to_async(lambda: TelegramUsers.objects.get_or_create(
            telegram_id=message.from_user.id
        ))()

        # Yangi foydalanuvchini xabarini yetkazish
        if created:
            text_new_user = (
                f"Yangi foydalanuvchi qo'shildi\n\n"
                f"ID: {message.from_user.id}\n"
                f"Full name: {message.from_user.first_name}\n"
            )
            await message.bot.send_message(chat_id=DEVLOPER_ID, text=text_new_user)
            await message.bot.send_message(chat_id=ADMIN_ID, text=text_new_user)

        # Agar referel bor va u o'zidan farqli bo'lsa
        if referel and int(referel) != message.from_user.id and created:
            print(referel)
            # Referal yaratish
            ref, ref_created = await sync_to_async(lambda: Referals.objects.get_or_create(
                user=message.from_user.id,
                referal=int(referel)
            ))()

            if ref_created:  # Yangi referal yaratildimi?
                # Config dan referal narxini olish
                config = await sync_to_async(lambda: Config.objects.filter(name='main').first())()
                price_referal = config.price if config else 0

                # Referal foydalanuvchiga xabar va balans qo'shish
                ref_user = await sync_to_async(lambda: TelegramUsers.objects.filter(
                    telegram_id=int(referel)
                ).first())()

                if ref_user:
                    # Balans qo'shish
                    await sync_to_async(lambda: ref_user.add_balance(price_referal))()

                    # Xabar yuborish
                    await message.bot.send_message(
                        chat_id=int(referel),
                        text=f"Sizning havolangizdan {message.from_user.first_name} qo'shildi.\nSizga {price_referal} olmos berildi"
                    )

    except Exception as e:
        print("Xatolik start_handlerda:", e)

        
        
    except Exception as e:
        await message.answer(f'Start headerida xatolik: {e}')
    finally:
        await message.answer("Asosiy sahifa!", reply_markup=start_button)

    


@router.message(F.text)
async def echo_message(message: Message):
    text = message.text
    if text == 'Free Fire stikerlar📁':
        await message.answer("""🎮Free Fire stikerlar📂:
                             
1️⃣ https://t.me/addstickers/mruzbekff
2️⃣ https://t.me/addstickers/mr_uzbek_ff 
3️⃣ https://t.me/addstickers/MRUZBEK_FF 
4️⃣ https://t.me/addstickers/MrUzbekFF1""")
    
    if text == '🆕Free Fire yangiliklar📰':
        await message.answer("""👋Assalomu alaykum siz Free Fire o'yiniga kelayotgan yangiliklardan xabardor bo'lishni istaysizmi⁉️ Unda hoziroq kanalimizga qo'shiling➕
🔔Kanal: https://t.me/Channel_of_MrUzbekFF 👈""")
    
    if text == '🛍️To\'lovlar kanali💰':
        await message.answer(""" 🛍️To'lovlar kanali💰:

https://t.me/mr_uzbek_ff_tolovkanal """)
    if text == '💎olmos sotib olish🛍️':
        await message.answer("""🫵Sizga ham Free Fire akkauntingizga olmoslar kerakmi⁉️ Bo'lmasam hoziroq ishonchli🔰, tezkor🕐 va arzon💰 bo'lgan danat servisimizdan foydalaning✅

✏️Murojaat uchun: https://t.me/Jonibek_Danater 🧑‍💻""")
    
    if text == '🆓Free Fire akkauntga like👍':
        await message.answer("""⚠️Xizmat hozirda mavjud emas❌""")

