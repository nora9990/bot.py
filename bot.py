import requests
import random
import time
import os
from datetime import datetime

# ============================================
# تنظیمات اصلی - با کلید شما
# ============================================
TELEGRAM_TOKEN = "8933933120:AAGO1Bn_zy_gWw3BriWdlajr5Er4Ks-0y0A"
CHANNEL = "@princessnature9"

# کلید Gemini شما (که الان درسته!)
GEMINI_API_KEY = "AQ.Ab8RN6L-UALkIkX1sBNin-izfVDAHNzWfOVLIKOv8Re647Qb9Q"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

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
# شخصیت‌های ثابت داستان
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
# تولید داستان با Gemini (کاملاً رایگان)
# ============================================
def generate_story_with_gemini(chapter, previous_story=""):
    """تولید داستان جدید با Gemini API - رایگان"""
    
    system_prompt = f"""تو یک نویسنده حرفه‌ای داستان‌های فانتزی و حماسی هستی.
داستان "جنگل نقره‌ای" را می‌نویسی که یک حماسه فانتزی است.

{CHARACTERS}

قوانین مهم داستان‌نویسی:
۱. هر فصل دقیقاً ۱۰ تا ۱۵ خط داشته باشد
۲. شخصیت‌ها همیشه طبق توضیحات بالا ثابت باشند
۳. داستان ادامه‌دار و جذاب باشد
۴. هر فصل یک اتفاق جدید و هیجان‌انگیز داشته باشد
۵. سبک نوشتاری شاعرانه، حماسی و جذاب باشد
۶. داستان در جنگل نقره‌ای جریان دارد
۷. پرنسس لیا شخصیت اصلی است
۸. هر فصل جدید ادامه طبیعی فصل قبل است
۹. داستان بی‌پایان است و هر فصل ماجرای جدیدی دارد
۱۰. از کلمات زیبا و توصیفی استفاده کن
"""
    
    user_prompt = f"""فصل {chapter} داستان جنگل نقره‌ای را بنویس.

داستان از جایی شروع می‌شود که فصل قبل تمام شد.
یک اتفاق جدید و هیجان‌انگیز در این فصل رخ می‌دهد.
متن بین ۱۰ تا ۱۵ خط باشد.
فصل را با عنوانی زیبا شروع کن.

فقط متن داستان را بنویس، هیچ توضیح اضافی نده.
"""
    
    if previous_story:
        user_prompt += f"\n\nداستان قبلی: {previous_story[:200]}..."
    
    # فرمت درخواست Gemini
    data = {
        "contents": [{
            "parts": [{
                "text": f"{system_prompt}\n\n{user_prompt}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 600,
            "topP": 0.95
        }
    }
    
    try:
        print("🤖 درخواست به Gemini (رایگان)...")
        response = requests.post(
            GEMINI_URL,
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY  # کلید شما اینجا
            },
            json=data,
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            story = result["candidates"][0]["content"]["parts"][0]["text"]
            print(f"✅ داستان تولید شد ({len(story)} کاراکتر)")
            return story
        else:
            print(f"❌ خطا در Gemini: {response.status_code}")
            print(f"پیام: {response.text}")
            
            if response.status_code == 429:
                print("⚠️ محدودیت روزانه Gemini تموم شده!")
                return None
            
            return None
            
    except Exception as e:
        print(f"❌ خطا: {e}")
        return None

# ============================================
# تولید تصویر بر اساس داستان
# ============================================
def generate_image_from_story(story_text):
    """تولید تصویر بر اساس متن داستان"""
    
    story_summary = story_text[:200] if len(story_text) > 200 else story_text
    
    prompt = f"""
========================================================================
شخصیت‌ها - اینها را دقیقاً به همین شکل رسم کن:
========================================================================

پرنسس لیا (شخصیت اصلی):
- موهای نقره‌ای بلند تا کمر
- چشم‌های سبز زمردی
- لباس سفید الف‌ها با گلدوزی طلایی
- تاج برگ طلایی روی سر
- گوش‌های باریک الف
- هرگز موها، چشم‌ها یا لباسش را تغییر نده

پرنس آرین:
- موهای بلوند کوتاه
- زره نقره‌ای با نگین‌های آبی
- شنل سبز
- چشم‌های آبی

========================================================================
صحنه داستان:
========================================================================
{story_summary}

========================================================================
سبک تصویر:
========================================================================
- تصویرسازی کتاب داستان فانتزی
- استودیو جیبلی
- سبک دیزنی
- نورپردازی سینمایی
- جنگل جادویی کهن
- جزئیات بالا
- رنگ‌های غنی و زنده
- فضای رویایی

========================================================================
قوانین مهم (هرگز نقض نکن!):
========================================================================
- پرنسس لیا: موهای نقره‌ای، چشم‌های سبز، لباس سفید، تاج طلایی
- پرنس آرین: موهای بلوند، زره نقره‌ای، شنل سبز
- هیچ نوشته یا کلمه‌ای در تصویر نباشد
- شخصیت‌ها دقیقاً مانند فصل قبل باشند
- سبک انیمیشنی و فانتزی

Seed: {random.randint(10000, 999999)}
"""
    
    encoded_prompt = requests.utils.quote(prompt)
    return f"{IMAGE_API}{encoded_prompt}?width=1024&height=1024"

# ============================================
# ارسال به تلگرام
# ============================================
def send_photo(image_url, caption):
    """ارسال تصویر به کانال تلگرام"""
    try:
        print("📥 دانلود تصویر...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        img = requests.get(image_url, headers=headers, timeout=120)
        
        if img.status_code != 200:
            print(f"⚠️ خطا در دریافت تصویر: {img.status_code}")
            
            simple_url = image_url.split("?")[0]
            print("🔄 تلاش مجدد با URL ساده...")
            img = requests.get(simple_url, headers=headers, timeout=120)
            
            if img.status_code != 200:
                raise Exception(f"خطا در دریافت تصویر: {img.status_code}")
        
        files = {"photo": ("story.jpg", img.content, "image/jpeg")}
        
        print("📤 ارسال به کانال تلگرام...")
        response = requests.post(
            SEND_PHOTO,
            data={
                "chat_id": CHANNEL,
                "caption": caption,
                "parse_mode": "Markdown"
            },
            files=files,
            timeout=120
        )
        
        if response.status_code != 200:
            raise Exception(f"خطا در ارسال: {response.text[:200]}")
        
        print("✅ ارسال موفق به تلگرام!")
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
                    return "\n".join(story_lines[-5:])
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
        
        print("🤖 درخواست داستان از Gemini (رایگان)...")
        story_text = generate_story_with_gemini(chapter, previous_story)
        
        if not story_text:
            print("❌ تولید داستان ناموفق بود")
            return False
        
        print(f"✅ داستان تولید شد ({len(story_text)} کاراکتر)")
        print(f"📝 متن: {story_text[:100]}...")
        
        print("🎨 ساخت تصویر...")
        image_url = generate_image_from_story(story_text)
        
        success = send_photo(image_url, story_text)
        
        if success:
            save_chapter(chapter + 1)
            save_time()
            save_story_history(chapter, story_text)
            
            print(f"✅ فصل {chapter} با موفقیت ارسال شد!")
            print(f"⏰ زمان: {datetime.now().strftime('%H:%M:%S')}")
            print(f"📚 فصل بعدی: {chapter + 1}")
            print("="*50)
        else:
            print("❌ ارسال ناموفق بود")
        
        return success
        
    except Exception as e:
        print(f"❌ خطای کلی: {e}")
        return False

def main():
    print("="*60)
    print("👑 PRINCESS STORY BOT - GEMINI VERSION")
    print("📖 داستان‌سرای هوشمند جنگل نقره‌ای")
    print("🤖 استفاده از Gemini (رایگان)")
    print("⏰ هر ۱ ساعت یک فصل جدید")
    print("📝 هر فصل ۱۰ تا ۱۵ خط")
    print("♾️  داستان تا بینهایت ادامه دارد")
    print("🎨 تصویرسازی با AI")
    print("="*60)
    
    print("\n🌟 داستان جنگل نقره‌ای آغاز شد...")
    print("🔄 هر ۱ ساعت یک فصل جدید ارسال می‌شود\n")
    
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
