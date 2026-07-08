import requests
import random
import time
import os
from datetime import datetime

# ============================================
# تنظیمات اصلی
# ============================================
TELEGRAM_TOKEN = "8933933120:AAGO1Bn_zy_gWw3BriWdlajr5Er4Ks-0y0A"
CHANNEL = "@princessnature9"

# کلید Gemini
GEMINI_API_KEY = "AQ.Ab8RN6L-UALkIkX1sBNin-izfVDAHNzWfOVLIKOv8Re647Qb9Q"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# ============================================
# تنظیمات تلگرام
# ============================================
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
SEND_PHOTO = f"{TELEGRAM_API}/sendPhoto"
IMAGE_API = "https://image.pollinations.ai/prompt/"

LAST_TIME = "last_time.txt"
LAST_CHAPTER = "chapter.txt"
STORY_HISTORY = "story_history.txt"

# ============================================
# شخصیت‌های ثابت
# ============================================
CHARACTERS = """
شخصیت‌های اصلی داستان (اینها همیشه ثابت هستند):

پرنسس لیا (قهرمان اصلی):
- موهای بلند نقره‌ای تا کمر
- چشم‌های سبز زمردی درخشان
- لباس سفید الف‌ها با گلدوزی طلایی
- تاج برگ طلایی روی سر
- گوش‌های باریک الف
- پوست روشن و لطیف

پرنس آرین:
- موهای بلوند کوتاه
- زره نقره‌ای با نگین‌های آبی
- شنل سبز
- چشم‌های آبی

سیلونا (جادوگر الف):
- موهای سفید بلند
- چشم‌های آبی جادویی
- ردای بنفش جادوگری
- عصای بلورین

مورگان (پادشاه تاریکی):
- زره سیاه
- چشم‌های قرمز براق
- تاج سیاه

الدور (جادوگر پیر):
- الف پیر
- ریش سفید بلند
- ردای قهوه‌ای

آریا (درمانگر):
- الف درمانگر
- موهای قهوه‌ای
- ردای سبز شفابخش

کایرن (جنگجو):
- الف جنگجو
- موهای سیاه
- زره چرمی
- کمان و تیر
"""

# ============================================
# تولید داستان با Gemini 2.0 Flash
# ============================================
def generate_story_with_gemini(chapter, previous_story="", attempt=1):
    """تولید داستان جدید با Gemini 2.0 Flash - با بررسی تعداد خطوط"""
    
    if attempt > 3:
        print("❌ بیش از ۳ بار تلاش، استفاده از داستان پشتیبان...")
        return None
    
    system_prompt = f"""تو یک نویسنده حرفه‌ای داستان‌های فانتزی و حماسی هستی.
داستان "جنگل نقره‌ای" را می‌نویسی که یک حماسه فانتزی است.

{CHARACTERS}

قوانین سختگیرانه داستان‌نویسی (هرگز نقض نکن!):
۱. هر فصل حتماً بین ۱۰ تا ۱۵ خط کامل داشته باشد
۲. اگر کمتر از ۱۰ خط بنویسی، پاسخ نامعتبر است
۳. هر خط حداقل یک جمله کامل داشته باشد
۴. داستان ادامه مستقیم فصل قبل باشد (ادامه طبیعی)
۵. شخصیت‌ها هرگز ظاهر یا نامشان تغییر نکند
۶. پرنسس لیا همیشه شخصیت اصلی باشد
۷. پایان فصل هیجان‌انگیز باشد تا خواننده منتظر فصل بعد بماند
۸. فقط متن داستان را بنویس و هیچ توضیح اضافه‌ای نده
۹. هر خط جدید با Enter جدا شود
۱۰. شماره فصل را ننویس، فقط عنوان بنویس
۱۱. از کلمات زیبا و توصیفی استفاده کن
۱۲. فضای داستان جادویی و رویایی باشد
"""
    
    user_prompt = f"""فصل {chapter} داستان جنگل نقره‌ای را بنویس.

داستان از جایی شروع می‌شود که فصل قبل تمام شد.
یک اتفاق جدید و هیجان‌انگیز در این فصل رخ می‌دهد.
متن بین ۱۰ تا ۱۵ خط باشد.
هر خط یک جمله کامل باشد.
فصل را با عنوانی زیبا شروع کن.
پایان فصل هیجان‌انگیز باشد.

فقط متن داستان را بنویس، هیچ توضیح اضافی نده.
"""
    
    if previous_story:
        user_prompt += f"\n\nادامه داستان از اینجا:\n{previous_story[:1200]}..."
    
    data = {
        "contents": [{
            "parts": [{
                "text": f"{system_prompt}\n\n{user_prompt}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 800,
            "topP": 0.95
        }
    }
    
    try:
        print(f"🤖 درخواست به Gemini 2.0 Flash (تلاش {attempt})...")
        response = requests.post(
            GEMINI_URL,
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY
            },
            json=data,
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            story = result["candidates"][0]["content"]["parts"][0]["text"]
            
            # بررسی تعداد خطوط
            lines = [x for x in story.split("\n") if x.strip()]
            line_count = len(lines)
            
            print(f"📊 تعداد خطوط: {line_count}")
            
            if line_count < 10:
                print(f"⚠️ داستان کوتاه بود ({line_count} خط)، درخواست مجدد...")
                return generate_story_with_gemini(chapter, previous_story, attempt + 1)
            
            if line_count > 15:
                print(f"⚠️ داستان بلند بود ({line_count} خط)، خلاصه می‌شود...")
                story = "\n".join(lines[:15])
            
            print(f"✅ داستان تولید شد ({len(story)} کاراکتر، {line_count} خط)")
            print(f"📝 شروع متن: {story[:80]}...")
            return story
        else:
            print(f"❌ خطا در Gemini: {response.status_code}")
            print(f"📄 پاسخ: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ خطای ارتباط: {e}")
        return None

# ============================================
# تولید تصویر با پرامپت جدید
# ============================================
def generate_image_from_story(story_text):
    """تولید تصویر با پرامپت جدید"""
    
    # صحنه ثابت برای ادامه داستان
    scene = "Princess Lia and Prince Arian inside an enchanted silver forest during a magical adventure."
    
    prompt = f"""
Beautiful elven princess Lia, long silver hair, emerald green eyes,
white royal elven dress with golden embroidery,
golden leaf crown.

Prince Arian, blond hair, silver armor, green cape.

{scene}

Fantasy illustration, magical forest, cinematic lighting,
storybook art, masterpiece, ultra detailed,
beautiful faces, no text, no watermark.
"""
    
    encoded_prompt = requests.utils.quote(prompt)
    return f"{IMAGE_API}{encoded_prompt}?width=1024&height=1024"

# ============================================
# داستان پشتیبان (اگر Gemini کار نکرد)
# ============================================
def get_backup_story(chapter):
    """داستان پشتیبان با ۱۰-۱۵ خط"""
    
    backup_stories = [
        f"""🌿 فصل {chapter}: طلوع مه در جنگل نقره‌ای

شب در جنگل نقره‌ای ساکت بود و مه غلیظی همه جا را پوشانده بود.
لیا از خواب پرید و صدای زمزمه‌ای از دل جنگل شنید.
آرین شمشیرش را برداشت و آماده نبرد شد.
سیلونا نوری آبی در کف دستش روشن کرد و به جلو رفت.
مورگان از اعماق تاریکی خندید و جنگل را لرزاند.
لیا تاج طلایی‌اش را محکم گرفت و به سوی نور حرکت کرد.
آرین فریاد زد: «همه آماده باشید! تاریکی نزدیک می‌شود.»
سایه‌ها در میان درختان حرکت می‌کردند و مه را می‌شکافتند.
لیا صدای دلش را دنبال کرد و راهی پیدا نمود.
نور و تاریکی در میانه جنگل روبروی هم ایستادند.
سرنوشت جنگل نقره‌ای در این شب رقم می‌خورد.
لیا قدمی به جلو برداشت و قدرت درونش بیدار شد.
همه در سکوت فرو رفتند و منتظر معجزه ماندند.
نجات جنگل در دستان پرنسس لیا بود.`,
        
        f"""🌿 فصل {chapter}: راز درخت کهن

باد سردی در میان شاخه‌های درخت کهن می‌وزید و زمزمه‌ای مرموز داشت.
لیا زیر درخت ایستاد و نوری از تاجش به تنه درخت تابید.
آرین با نگرانی اطراف را زیر نظر داشت و شمشیرش را آماده نگه داشت.
سیلونا کتاب جادویی را باز کرد و جمله‌ای کهن را زمزمه نمود.
ناگهان تنه درخت شکافته شد و پله‌هایی به سمت پایین ظاهر گردید.
لیا اولین کسی بود که پا روی پله‌ها گذاشت و به اعماق رفت.
آرین او را دنبال کرد و فریاد زد: «مراقب باش لیا!»
در تاریکی، دو چشم قرمز براق نگاهشان را دنبال می‌کرد.
مورگان از پشت ستون سنگی بیرون پرید و خندید.
لیا با قدرت تاجش، نوری بزرگ منتشر کرد و تاریکی را عقب راند.
مورگان عقب‌نشینی کرد و در تاریکی ناپدید شد.
دروازه‌ای قدیمی در انتهای پله‌ها قرار داشت.
لیا دستش را روی دروازه گذاشت و زمزمه‌ای کرد.
دروازه به آرامی باز شد و نوری طلایی از آن بیرون زد.
سرنوشت جدیدی در انتظار آنان بود.`,
        
        f"""🌿 فصل {chapter}: نبرد با سایه‌ها

مه غلیظ‌تر از همیشه تمام جنگل را فراگرفته بود.
لیا حس کرد تاریکی در حال نزدیک شدن است و قلبش تندتر زد.
آرین سپر را بالا گرفت و مقابل لیا ایستاد.
سیلونا طلسم محافظ را بر روی آنها خواند و نوری آبی درخشید.
از میان مه، سایه‌هایی بی‌شکل با چشمان سرخ بیرون آمدند.
لیا تاجش را بالا گرفت و نوری طلایی از آن ساطع شد.
آرین با شمشیرش یکی از سایه‌ها را دو نیم کرد.
سیلونا با عصایش حلقه‌ای آبی دور آنها کشید.
سایه‌ها عقب‌نشینی کردند اما دوباره جمع شدند.
لیا احساس کرد قدرت تاجش در حال کاهش است.
ناگهان صدای کایرن از پشت سر شنیده شد: «به کمک من نیاز دارید!»
کایرن با کمانش شروع به تیراندازی به سمت سایه‌ها کرد.
آریا نیز پشت سر او آمد و نور سبز شفا را منتشر کرد.
تاریکی کمکم شکست می‌خورد و مه کنار می‌رفت.
لیا لبخندی زد و دانست که تنها نیست.`
    ]
    
    return backup_stories[chapter % len(backup_stories)]

# ============================================
# ارسال به تلگرام
# ============================================
def send_photo(image_url, caption):
    try:
        print("📥 دانلود تصویر...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        img = requests.get(image_url, headers=headers, timeout=120)
        
        if img.status_code != 200:
            simple_url = image_url.split("?")[0]
            img = requests.get(simple_url, headers=headers, timeout=120)
            if img.status_code != 200:
                raise Exception(f"خطا: {img.status_code}")
        
        files = {"photo": ("story.jpg", img.content, "image/jpeg")}
        response = requests.post(
            SEND_PHOTO,
            data={"chat_id": CHANNEL, "caption": caption, "parse_mode": "Markdown"},
            files=files,
            timeout=120
        )
        
        if response.status_code != 200:
            raise Exception(f"خطا: {response.text[:200]}")
        
        print("✅ ارسال موفق!")
        return True
        
    except Exception as e:
        print(f"❌ خطا در ارسال: {e}")
        return False

# ============================================
# مدیریت فایل‌ها
# ============================================
def get_chapter():
    if os.path.exists(LAST_CHAPTER):
        try:
            with open(LAST_CHAPTER, "r") as f:
                return int(f.read())
        except:
            return 1
    return 1

def save_chapter(chapter):
    with open(LAST_CHAPTER, "w") as f:
        f.write(str(chapter))

def get_previous_story():
    if os.path.exists(STORY_HISTORY):
        try:
            with open(STORY_HISTORY, "r", encoding="utf-8") as f:
                content = f.read()
                parts = content.split("="*50)
                if len(parts) >= 2:
                    last_story = parts[-2].strip()
                    lines = last_story.split("\n")
                    story_lines = []
                    for line in lines:
                        if line.strip() and not line.startswith("فصل") and not line.startswith("="):
                            story_lines.append(line)
                    return "\n".join(story_lines[-8:])
        except:
            pass
    return ""

def save_story_history(chapter, story_text):
    try:
        with open(STORY_HISTORY, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"فصل {chapter} - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"{'='*50}\n")
            f.write(story_text)
            f.write("\n")
    except:
        pass

def should_send():
    if not os.path.exists(LAST_TIME):
        return True
    try:
        with open(LAST_TIME, "r") as f:
            last = int(f.read())
        return time.time() - last >= 3600
    except:
        return True

def save_time():
    with open(LAST_TIME, "w") as f:
        f.write(str(int(time.time())))

def send_post():
    try:
        chapter = get_chapter()
        previous_story = get_previous_story()
        
        print(f"\n{'='*50}")
        print(f"📖 شروع فصل {chapter}")
        print(f"{'='*50}")
        
        print("🤖 درخواست داستان از Gemini 2.0 Flash...")
        story_text = generate_story_with_gemini(chapter, previous_story)
        
        # اگر Gemini کار نکرد، از داستان پشتیبان استفاده کن
        if not story_text:
            print("⚠️ استفاده از داستان پشتیبان...")
            story_text = get_backup_story(chapter)
        
        # بررسی نهایی تعداد خطوط
        lines = [x for x in story_text.split("\n") if x.strip()]
        if len(lines) < 10:
            print(f"⚠️ داستان کوتاه بود ({len(lines)} خط)، اضافه کردن خطوط...")
            extra_lines = [
                "لیا به آسمان نگاه کرد و ستاره‌ها را شمارش نمود.",
                "آرین کنار او ایستاد و دستش را روی شانه‌اش گذاشت.",
                "سیلونا زمزمه‌ای کرد و مه کمی کنار رفت.",
                "همه با هم به سمت نور حرکت کردند و امید در دلشان جوانه زد.",
                "جنگل نقره‌ای رازهای زیادی در خود داشت."
            ]
            story_text = "\n".join(lines + extra_lines[:15-len(lines)])
        
        print(f"✅ داستان آماده شد ({len(story_text)} کاراکتر، {len(lines)} خط)")
        
        print("🎨 ساخت تصویر...")
        image_url = generate_image_from_story(story_text)
        
        success = send_photo(image_url, story_text)
        
        if success:
            save_chapter(chapter + 1)
            save_time()
            save_story_history(chapter, story_text)
            print(f"✅ فصل {chapter} ارسال شد!")
        else:
            print("❌ ارسال ناموفق")
        
        return success
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False

def main():
    print("="*60)
    print("👑 PRINCESS STORY BOT - GEMINI 2.0 FLASH")
    print("📖 داستان‌سرای جنگل نقره‌ای")
    print("🤖 با Gemini 2.0 Flash (رایگان)")
    print("⏰ هر ۱ ساعت یک فصل جدید")
    print("📝 هر فصل ۱۰-۱۵ خط (اجباری)")
    print("♾️  داستان تا بینهایت ادامه دارد")
    print("="*60)
    
    print("\n🌟 داستان جنگل نقره‌ای آغاز شد...\n")
    
    while True:
        try:
            if should_send():
                send_post()
            else:
                if os.path.exists(LAST_TIME):
                    with open(LAST_TIME, "r") as f:
                        last = int(f.read())
                    remaining = 3600 - (time.time() - last)
                    if 0 < remaining < 300:
                        mins = int(remaining // 60)
                        secs = int(remaining % 60)
                        print(f"⏳ {mins}:{secs:02d} تا ارسال بعدی...", end="\r")
            
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n\n🛑 ربات متوقف شد.")
            chapter = get_chapter()
            print(f"📚 تعداد کل فصل‌های نوشته شده: {chapter - 1}")
            print("👋 خداحافظ!")
            break
        except Exception as e:
            print(f"❌ خطای ناشناخته: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
