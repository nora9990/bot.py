import time
import requests
import random
import os
from datetime import datetime

# توکن مستقیم در کد
TOKEN = "8933933120:AAGO1Bn_zy_gWw3BriWdlajr5Er4Ks-0y0A"

if not TOKEN:
    raise Exception("TOKEN variable not found")

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

LAST_TIME_FILE = "last_time.txt"
LAST_FOOD_FILE = "last_food.txt"


# -----------------------------
# زمان ارسال
# -----------------------------

def should_send():
    now = int(time.time())

    if not os.path.exists(LAST_TIME_FILE):
        return True

    with open(LAST_TIME_FILE, "r") as f:
        last = int(f.read())

    return now - last >= 3600


def save_time():
    with open(LAST_TIME_FILE, "w") as f:
        f.write(str(int(time.time())))


# -----------------------------
# جلوگیری از غذای تکراری
# -----------------------------

def get_food():
    old = ""

    if os.path.exists(LAST_FOOD_FILE):
        with open(LAST_FOOD_FILE, "r") as f:
            old = f.read().strip()

    foods = [x for x in FOODS if x != old]
    food = random.choice(foods)

    with open(LAST_FOOD_FILE, "w") as f:
        f.write(food)

    return food


# -----------------------------
# ساخت عکس
# -----------------------------

def generate_real(food):
    seed = random.randint(100000, 999999)
    prompt = f"""
{food} Persian cuisine,
realistic professional food photography,
fresh ingredients,
beautiful presentation,
restaurant quality,
unique image,
seed {seed}
"""
    return IMAGE_API + requests.utils.quote(prompt)


def generate_book(food):
    seed = random.randint(100000, 999999)
    prompt = f"""
Persian recipe {food},
fantasy handmade cookbook page,
open cooking book,
watercolor illustration,
ingredients icons,
step by step drawings,
beautiful vintage style,
unique image,
seed {seed}
"""
    return IMAGE_API + requests.utils.quote(prompt)


# -----------------------------
# کپشن
# -----------------------------

def get_caption(food):
    captions = {
        "قورمه سبزی": """✨ دستور خوشمزه امروز

🍲 قورمه سبزی

مواد لازم:
گوشت، سبزی قورمه، لوبیا قرمز، لیمو عمانی

طرز تهیه:
۱. گوشت رو تفت بده
۲. سبزی اضافه کن
۳. لوبیا و آب رو اضافه کن
۴. بذار آروم جا بیفته

💡 نکته: لیمو عمانی رو آخر اضافه کن تلخ نشه 😍

✨ @princessnature9""",

        "قیمه": """✨ دستور خوشمزه امروز

🍛 قیمه

مواد لازم:
گوشت، لپه، رب گوجه، سیب زمینی

طرز تهیه:
۱. گوشت و لپه بپز
۲. رب اضافه کن
۳. آخر سیب زمینی سرخ‌شده

💡 نکته: دارچین عطرشو فوق‌العاده میکنه ✨

✨ @princessnature9""",

        "کشک بادمجان": """✨ دستور خوشمزه امروز

🍆 کشک بادمجان

مواد لازم:
بادمجان، کشک، سیر، نعناع

طرز تهیه:
۱. بادمجان سرخ کن
۲. له کن
۳. کشک و سیر اضافه کن

💡 نکته: نعناع داغ یادت نره 😋

✨ @princessnature9""",

        "آبگوشت": """✨ دستور خوشمزه امروز

🥘 آبگوشت

مواد لازم:
گوشت، نخود، سیب زمینی، گوجه

طرز تهیه:
۱. همه مواد رو با هم بپز
۲. تا جا بیفته

💡 نکته: با نون سنگک یه چیز دیگه‌ست 🤤

✨ @princessnature9""",

        "کباب ایرانی": """✨ دستور خوشمزه امروز

🍢 کباب کوبیده

مواد لازم:
گوشت چرخ‌کرده، پیاز، نمک، زعفران

طرز تهیه:
۱. مواد رو مخلوط کن
۲. به سیخ بزن
۳. روی آتش کباب کن

💡 نکته: زغال طعم اصلی رو میده 🔥

✨ @princessnature9""",

        "آش رشته": """✨ دستور خوشمزه امروز

🥣 آش رشته

مواد لازم:
گوشت، حبوبات، سبزی آش، رشته، آرد

طرز تهیه:
۱. حبوبات رو بپز
۲. سبزی و رشته اضافه کن
۳. بپز تا غلیظ بشه

💡 نکته: با کشک و نعناع داغ سرو کن 😋

✨ @princessnature9""",

        "زرشک پلو با مرغ": """✨ دستور خوشمزه امروز

🍗 زرشک پلو با مرغ

مواد لازم:
برنج، مرغ، زرشک، زعفران

طرز تهیه:
۱. مرغ رو با پیاز و زعفران بپز
۲. برنج رو آبکش کن
۳. زرشک رو اضافه کن
۴. دم کن

💡 نکته: زرشک رو کمی شکر بپاشید تا ترشیش کم بشه 🌸

✨ @princessnature9""",

        "دیزی": """✨ دستور خوشمزه امروز

🍲 دیزی (آبگوشت سنگی)

مواد لازم:
گوشت، نخود، لوبیا، سیب زمینی، گوجه

طرز تهیه:
۱. همه مواد رو در دیزی بچین
۲. بپز تا جا بیفته

💡 نکته: با گوشت کوهی خوشمزه‌تر میشه 🏔️

✨ @princessnature9"""
    }
    return captions.get(food, f"🍲 {food}\n\n✨ @princessnature9")


# -----------------------------
# ارسال عکس
# -----------------------------

def send_photo(image_url, caption):
    try:
        print("⬇️ دریافت عکس...")
        img = requests.get(image_url, timeout=60)

        if img.status_code != 200:
            print("❌ عکس دریافت نشد")
            return False

        content = img.headers.get("Content-Type", "")
        print("نوع فایل:", content)

        if "image" not in content:
            print("❌ خروجی تصویر نیست")
            return False

        files = {
            "photo": ("food.jpg", img.content, "image/jpeg")
        }

        result = requests.post(
            SEND_PHOTO,
            data={
                "chat_id": CHANNEL,
                "caption": caption
            },
            files=files,
            timeout=60
        )

        if result.status_code == 200:
            print("✅ عکس ارسال شد")
            return True
        else:
            print(result.text)
            return False

    except Exception as e:
        print("خطای عکس:", e)
        return False


# -----------------------------
# ارسال پست
# -----------------------------

def send_post():
    food = get_food()
    print(f"🎯 غذا: {food}")

    real = generate_real(food)
    book = generate_book(food)

    first = send_photo(
        real,
        f"""🍽 غذای امروز:

{food}

✨ @princessnature9"""
    )

    time.sleep(5)

    second = send_photo(
        book,
        get_caption(food)
    )

    if first and second:
        save_time()
        print(f"✅ پست کامل شد {datetime.now().strftime('%H:%M')}")
    else:
        print("⚠️ پست کامل ارسال نشد")


# -----------------------------
# شروع
# -----------------------------

print("👑 ربات آشپزی پرنسسی فعال شد")
print(f"📢 کانال: {CHANNEL}")
print("⏰ هر ساعت دو عکس جدید")
print("=" * 40)

while True:
    try:
        if should_send():
            send_post()
        time.sleep(60)
    except Exception as e:
        print("خطای اصلی:", e)
        time.sleep(30)
