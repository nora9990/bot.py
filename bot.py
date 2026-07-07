import time
import requests
import random
import os
from datetime import datetime

TOKEN = "8933933120:AAGO1Bn_zy_gWw3BriWdlajr5Er4Ks-0y0A"
CHANNEL = "@princessnature9"

SEND_PHOTO = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

IMAGE_API = "https://image.pollinations.ai/prompt/"

FOODS = [
    "قورمه سبزی",
    "قیمه",
    "کشک بادمجان",
    "آبگوشت",
    "کباب ایرانی",
    "آش رشته",
    "زرشک پلو با مرغ",
    "دیزی"
]

LAST_FILE = "last_time.txt"


# ⏱ زمان‌بندی دقیق
def should_send():
    now = int(time.time())

    if not os.path.exists(LAST_FILE):
        return True

    with open(LAST_FILE, "r") as f:
        last = int(f.read().strip())

    return now - last >= 3600  # هر 1 ساعت


def save_time():
    with open(LAST_FILE, "w") as f:
        f.write(str(int(time.time())))


# 📷 ساخت عکس کتاب فانتزی
def generate_book(food):
    prompt = f"""
Persian food {food},
fantasy handmade cookbook page,
open book layout,
watercolor illustration,
ingredients icons,
step by step drawings,
warm colors,
vintage cooking book,
beautiful layout
"""
    url = IMAGE_API + requests.utils.quote(prompt)
    return url


# 📷 عکس واقعی غذا
def generate_real(food):
    prompt = f"{food} Persian food realistic, high quality, delicious, professional photography"
    url = IMAGE_API + requests.utils.quote(prompt)
    return url


# 📝 کپشن فارسی واقعی
def get_caption(food):
    captions = {
        "قورمه سبزی": """🍲 قورمه سبزی

مواد لازم:
گوشت، سبزی قورمه، لوبیا قرمز، لیمو عمانی

طرز تهیه:
۱. گوشت رو تفت بده
۲. سبزی اضافه کن
۳. لوبیا و آب رو اضافه کن
۴. بذار آروم جا بیفته

💡 نکته: لیمو عمانی رو آخر اضافه کن تلخ نشه 😍

✨ @princessnature9""",

        "قیمه": """🍛 قیمه

مواد لازم:
گوشت، لپه، رب گوجه، سیب زمینی

طرز تهیه:
۱. گوشت و لپه بپز
۲. رب اضافه کن
۳. آخر سیب زمینی سرخ‌شده

💡 نکته: دارچین عطرشو فوق‌العاده میکنه ✨

✨ @princessnature9""",

        "کشک بادمجان": """🍆 کشک بادمجان

مواد لازم:
بادمجان، کشک، سیر، نعناع

طرز تهیه:
۱. بادمجان سرخ کن
۲. له کن
۳. کشک و سیر اضافه کن

💡 نکته: نعناع داغ یادت نره 😋

✨ @princessnature9""",

        "آبگوشت": """🥘 آبگوشت

مواد لازم:
گوشت، نخود، سیب زمینی، گوجه

طرز تهیه:
۱. همه مواد رو با هم بپز
۲. تا جا بیفته

💡 نکته: با نون سنگک یه چیز دیگه‌ست 🤤

✨ @princessnature9""",

        "کباب ایرانی": """🍢 کباب کوبیده

مواد لازم:
گوشت چرخ‌کرده، پیاز، نمک، زعفران

طرز تهیه:
۱. مواد رو مخلوط کن
۲. به سیخ بزن
۳. روی آتش کباب کن

💡 نکته: زغال طعم اصلی رو میده 🔥

✨ @princessnature9""",

        "آش رشته": """🥣 آش رشته

مواد لازم:
گوشت، حبوبات، سبزی آش، رشته، آرد

طرز تهیه:
۱. حبوبات رو بپز
۲. سبزی و رشته اضافه کن
۳. بپز تا غلیظ بشه

💡 نکته: با کشک و نعناع داغ سرو کن 😋

✨ @princessnature9""",

        "زرشک پلو با مرغ": """🍗 زرشک پلو با مرغ

مواد لازم:
برنج، مرغ، زرشک، زعفران

طرز تهیه:
۱. مرغ رو با پیاز و زعفران بپز
۲. برنج رو آبکش کن
۳. زرشک رو اضافه کن
۴. دم کن

💡 نکته: زرشک رو کمی شکر بپاشید تا ترشیش کم بشه 🌸

✨ @princessnature9""",

        "دیزی": """🍲 دیزی (آبگوشت سنگی)

مواد لازم:
گوشت، نخود، لوبیا، سیب زمینی، گوجه

طرز تهیه:
۱. همه مواد رو در دیزی بچین
۲. بپز تا جا بیفته

💡 نکته: با گوشت کوهی خوشمزه‌تر میشه 🏔️

✨ @princessnature9"""
    }
    return captions.get(food, f"{food}\n\n✨ @princessnature9")


# 🚀 ارسال
def send_post():
    food = random.choice(FOODS)

    print(f"🎯 ارسال: {food}")

    book_img = generate_book(food)
    real_img = generate_real(food)
    caption = get_caption(food)

    try:
        # اول عکس واقعی
        print("📸 ارسال عکس واقعی...")
        res1 = requests.post(SEND_PHOTO, data={
            "chat_id": CHANNEL,
            "photo": real_img,
            "caption": f"🍽 غذای امروز: {food}\n\n✨ @princessnature9"
        }, timeout=20)

        if res1.status_code == 200:
            print("✅ عکس واقعی ارسال شد")
        else:
            print(f"⚠️ خطا: {res1.text[:100]}")

        time.sleep(3)

        # بعد کتاب فانتزی
        print("📖 ارسال کتاب فانتزی...")
        res2 = requests.post(SEND_PHOTO, data={
            "chat_id": CHANNEL,
            "photo": book_img,
            "caption": caption
        }, timeout=20)

        if res2.status_code == 200:
            print("✅ کتاب فانتزی ارسال شد")
        else:
            print(f"⚠️ خطا: {res2.text[:100]}")

        save_time()
        print(f"✅ پست در {datetime.now().strftime('%H:%M')} تکمیل شد")

    except Exception as e:
        print(f"❌ خطا: {e}")


# 🔁 حلقه اصلی
print("👑 ربات آشپزی پرنسسی فعال شد...")
print(f"📢 کانال: {CHANNEL}")
print("⏰ هر ۱ ساعت: ۲ عکس (واقعی + فانتزی)")
print(f"🍽 {len(FOODS)} غذای ایرانی")
print("=" * 50)

while True:
    try:
        if should_send():
            send_post()
        time.sleep(60)
    except Exception as e:
        print(f"❌ خطا در حلقه اصلی: {e}")
        time.sleep(30)
