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


def should_send():
    now = int(time.time())

    if not os.path.exists(LAST_FILE):
        return True

    with open(LAST_FILE, "r") as f:
        last = int(f.read().strip())

    return now - last >= 3600


def save_time():
    with open(LAST_FILE, "w") as f:
        f.write(str(int(time.time())))


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
    return IMAGE_API + requests.utils.quote(prompt)


def generate_real(food):
    prompt = f"{food} Persian food realistic, high quality, professional food photography"
    return IMAGE_API + requests.utils.quote(prompt)


def send_photo_file(image_url, caption):
    try:
        print("⬇️ دانلود عکس...")

        img = requests.get(
            image_url,
            timeout=60
        )

        if img.status_code != 200:
            print("❌ عکس دانلود نشد")
            return False

        print("📤 ارسال به تلگرام...")

        files = {
            "photo": (
                "food.jpg",
                img.content,
                "image/jpeg"
            )
        }

        response = requests.post(
            SEND_PHOTO,
            data={
                "chat_id": CHANNEL,
                "caption": caption
            },
            files=files,
            timeout=60
        )

        if response.status_code == 200:
            print("✅ عکس ارسال شد")
            return True

        print("⚠️ خطای تلگرام:")
        print(response.text)
        return False

    except Exception as e:
        print("❌ خطا در ارسال عکس:", e)
        return False


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


def send_post():
    food = random.choice(FOODS)

    print(f"🎯 ارسال: {food}")

    real_img = generate_real(food)
    book_img = generate_book(food)

    ok1 = send_photo_file(
        real_img,
        f"🍽 غذای امروز: {food}\n\n✨ @princessnature9"
    )

    time.sleep(5)

    ok2 = send_photo_file(
        book_img,
        get_caption(food)
    )

    if ok1 and ok2:
        save_time()
        print(f"✅ پست کامل شد {datetime.now().strftime('%H:%M')}")
    else:
        print("⚠️ ارسال کامل نشد")


print("👑 ربات آشپزی پرنسسی فعال شد...")
print(f"📢 کانال: {CHANNEL}")
print("⏰ هر ۱ ساعت: ۲ عکس (واقعی + کتاب آشپزی)")
print(f"🍽 {len(FOODS)} غذای ایرانی")
print("=" * 40)

while True:
    try:
        if should_send():
            send_post()

        time.sleep(60)

    except Exception as e:
        print("❌ خطای اصلی:", e)
        time.sleep(30)
