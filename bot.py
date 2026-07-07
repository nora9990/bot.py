import time
import requests
import random
import os
from datetime import datetime

TOKEN = "8933933120:AAGO1Bn_zy_gWw3BriWdlajr5Er4Ks-0y0A"

if not TOKEN:
    raise Exception("TOKEN variable not found")

CHANNEL = "@princessnature9"

SEND_PHOTO = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

IMAGE_API = "https://image.pollinations.ai/prompt/"

FOODS = [
    "قورمه سبزی",
    "قیمه",
    "قیمه بادمجان",
    "فسنجان",
    "خورش کرفس",
    "خورش بادمجان",
    "خورش آلو",
    "خورش خلال کرمانشاهی",
    "آبگوشت",
    "دیزی سنگی",
    "کباب کوبیده",
    "کباب برگ",
    "جوجه کباب",
    "کباب سلطانی",
    "کباب ترش",
    "کباب بختیاری",
    "زرشک پلو با مرغ",
    "باقالی پلو با ماهیچه",
    "باقالی پلو با مرغ",
    "سبزی پلو با ماهی",
    "ته چین مرغ",
    "ته چین گوشت",
    "لوبیا پلو",
    "عدس پلو",
    "کلم پلو شیرازی",
    "استانبولی پلو",
    "مرصع پلو",
    "شیرین پلو",
    "آلبالو پلو",
    "رشته پلو",
    "دلمه برگ مو",
    "کشک بادمجان",
    "میرزا قاسمی",
    "یتیمچه",
    "کوکو سبزی",
    "کوکو سیب زمینی",
    "نرگسی اسفناج",
    "آش رشته",
    "آش دوغ",
    "آش شله قلمکار",
    "آش جو",
    "آش انار",
    "آش ترخینه",
    "حلیم",
    "کله پاچه",
    "شامی کباب",
    "کتلت",
    "کوفته تبریزی",
    "کوفته ریزه",
    "بریانی اصفهان",
    "چلو گوشت",
    "چلو مرغ زعفرانی",
    "مرغ شکم پر",
    "مرغ ترش",
    "قلیه ماهی",
    "قلیه میگو",
    "میگو پلو",
    "فلافل جنوبی",
    "سمبوسه",
    "حلیم بادمجان",
    "کال جوش",
    "اشکنه",
    "کاچی",
    "شله زرد",
    "حلوا",
    "رنگینک",
    "فرنی",
    "خوراک لوبیا",
    "خوراک مرغ",
    "خوراک بادمجان",
    "خوراک جگر",
    "جگر کبابی",
    "ماهی شکم پر",
    "هواری میگو",
    "کلمبا",
    "آش عباسعلی",
    "خورش ریواس",
    "خورش به",
    "خورش ماست",
    "خورش سیب",
    "خورش نخود",
    "خوراک زبان",
    "سیرابی",
    "آبگوشت بزباش",
    "آبگوشت کشک",
    "آبگوشت لپه",
    "املت ایرانی",
    "باقالی قاتق",
    "ترش تره",
    "واویشکا",
    "اناربیج",
    "کدو بره",
    "مالابیج",
    "چغرتمه",
    "نان و پنیر و سبزی",
    "سینی مزه ایرانی"
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
        last = int(f.read().strip())

    return now - last >= 3600


def save_time():
    with open(LAST_TIME_FILE, "w") as f:
        f.write(str(int(time.time())))


# -----------------------------
# انتخاب غذا بدون تکرار
# -----------------------------

def get_food():
    old = ""

    if os.path.exists(LAST_FOOD_FILE):
        with open(LAST_FOOD_FILE, "r") as f:
            old = f.read().strip()

    choices = [x for x in FOODS if x != old]

    if not choices:
        choices = FOODS

    food = random.choice(choices)

    with open(LAST_FOOD_FILE, "w") as f:
        f.write(food)

    return food


# -----------------------------
# ساخت عکس
# -----------------------------

def generate_real(food):
    seed = random.randint(100000, 999999)

    prompt = f"""
A real professional photo of exactly {food}.
Persian traditional cuisine.
Only {food} dish.
Authentic Iranian food.
Restaurant photography.
High quality.
Beautiful presentation.
No other dishes.
Seed {seed}
"""

    return IMAGE_API + requests.utils.quote(prompt)


def generate_book(food):
    seed = random.randint(100000, 999999)

    prompt = f"""
Fantasy Persian cookbook page about {food}.
The recipe title is {food}.
Open cookbook.
Watercolor illustration.
Ingredients and cooking steps.
Traditional Iranian style.
Beautiful vintage design.
Seed {seed}
"""

    return IMAGE_API + requests.utils.quote(prompt)


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

        if "image" not in content:
            print("❌ خروجی تصویر نیست")
            return False

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
        else:
            print("❌ خطای تلگرام:")
            print(response.text)
            return False

    except Exception as e:
        print("❌ خطای ارسال عکس:", e)
        return False


# -----------------------------
# متن پست
# -----------------------------

def get_caption(food):
    return f"""
✨ دستور خوشمزه امروز

🍲 {food}

مواد لازم:
مواد تازه، ادویه‌های خوش‌عطر و ترکیبات سنتی ایرانی

طرز تهیه:
۱. مواد اولیه را آماده کنید.
۲. مواد را با حرارت مناسب بپزید.
۳. اجازه دهید غذا کاملاً جا بیفتد.

💡 نکته:
آشپزی با حوصله، طعم غذا را بهتر می‌کند 😍

نوش جان 🌿

✨ @princessnature9
"""


# -----------------------------
# ارسال پست
# -----------------------------

def send_post():
    food = get_food()

    print(f"🎯 غذا: {food}")

    real_image = generate_real(food)
    book_image = generate_book(food)

    first = send_photo(
        real_image,
        f"""
🍽 غذای امروز:

{food}

✨ @princessnature9
"""
    )

    time.sleep(5)

    second = send_photo(
        book_image,
        get_caption(food)
    )

    if first and second:
        save_time()
        print(f"✅ پست کامل شد {datetime.now().strftime('%H:%M')}")
    else:
        print("⚠️ پست کامل ارسال نشد")


# -----------------------------
# شروع ربات
# -----------------------------

print("👑 ربات آشپزی پرنسسی فعال شد")
print(f"📢 کانال: {CHANNEL}")
print("⏰ هر ساعت دو عکس جدید")
print(f"🍽 تعداد غذاها: {len(FOODS)}")
print("=" * 40)

while True:
    try:
        if should_send():
            send_post()

        time.sleep(60)

    except Exception as e:
        print("❌ خطای اصلی:", e)
        time.sleep(30)
