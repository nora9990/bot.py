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

# API Key دیپ‌سیک شما
DEEPSEEK_API_KEY = "sk-2590c1abbc8a46899f78847709a98e6c"
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

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
- همیشه لباس سفید و تاج طلایی می‌پوشد

پرنس آرین:
- موهای بلوند کوتاه
- زره نقره‌ای با نگین‌های آبی
- شنل سبز
- چشم‌های آبی
- هیکل ورزیده و بلند

سیلونا (جادوگر الف):
- موهای سفید بلند
- چشم‌های آبی جادویی که می‌درخشند
- ردای بنفش جادوگری
- عصای بلورین

مورگان (پادشاه تاریکی):
- زره سیاه
- چشم‌های قرمز براق
- تاج سیاه
- هاله تاریکی دورش

الدور (جادوگر پیر):
- الف پیر
- ریش سفید بلند
- ردای قهوه‌ای
- عصای چوبی

آریا (درمانگر):
- الف درمانگر
- موهای قهوه‌ای
- ردای سبز شفابخش
- چهره مهربان

کایرن (جنگجو):
- الف جنگجو
- موهای سیاه
- زره چرمی
- کمان و تیر
"""

# ============================================
# تولید داستان با DeepSeek AI
# ============================================
def generate_story_with_deepseek(chapter, previous_story=""):
    """تولید داستان جدید با DeepSeek AI"""
    
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
۹. از کلمات زیبا و توصیفی استفاده کن
۱۰. فضا باید جادویی و رویایی باشد

نکته: داستان بی‌پایان است و هر فصل ماجرای جدیدی دارد.
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
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.85,
        "max_tokens": 600,
        "top_p": 0.95
    }
    
    try:
        print("🤖 درخواست به DeepSeek...")
        response = requests.post(DEEPSEEK_URL, headers=headers, json=data, timeout=90)
        
        if response.status_code == 200:
            result = response.json()
            story = result["choices"][0]["message"]["content"]
            print(f"✅ داستان تولید شد ({len(story)} کاراکتر)")
            return story
        else:
            print(f"❌ خطا در DeepSeek: {response.status_code}")
            print(f"پیام: {response.text}")
            
            if response.status_code == 402:
                print("⚠️ اعتبار حساب دیپ‌سیک تمام شده! لطفاً شارژ کنید.")
                return None
            
            if response.status_code == 429:
                print("⚠️ تعداد درخواست‌ها زیاد است، ۳۰ ثانیه صبر کنید...")
                time.sleep(30)
                return generate_story_with_deepseek(chapter, previous_story)
            
            return None
            
    except requests.exceptions.Timeout:
        print("❌ زمان درخواست به پایان رسید")
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
    """دریافت شماره فصل فعلی"""
    if os.path.exists(LAST_CHAPTER):
        try:
            with open(LAST_CHAPTER, "r") as f:
                return int(f.read())
        except:
            return 1
    return 1

def save_chapter(chapter):
    """ذخیره شماره فصل"""
    with open(LAST_CHAPTER, "w") as f:
        f.write(str(chapter))

def get_previous_story():
    """دریافت داستان قبلی برای ادامه"""
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
    """ذخیره تاریخچه داستان"""
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
    """بررسی زمان ارسال (هر ۱ ساعت)"""
    if not os.path.exists(LAST_TIME):
        return True
    try:
        with open(LAST_TIME, "r") as f:
            last = int(f.read())
        return time.time() - last >= 3600
    except:
        return True

def save_time():
    """ذخیره زمان آخرین ارسال"""
    with open(LAST_TIME, "w") as f:
        f.write(str(int(time.time())))

# ============================================
# ارسال پست کامل
# ============================================
def send_post():
    """ارسال یک پست کامل"""
    try:
        chapter = get_chapter()
        previous_story = get_previous_story()
        
        print(f"\n{'='*50}")
        print(f"📖 شروع فصل {chapter}")
        print(f"{'='*50}")
        
        print("🤖 درخواست داستان از DeepSeek...")
        story_text = generate_story_with_deepseek(chapter, previous_story)
        
        if not story_text:
            print("❌ تولید داستان ناموفق بود")
            return False
        
        print(f"✅ داستان تولید شد ({len(story_text)} کاراکتر)")
        print(f"📝 متن: {story_text[:100]}...")
        
        print("🎨 ساخت تصویر...")
        image_url = generate_image_from_story(story_text)
        print(f"🔗 لینک تصویر: {image_url[:80]}...")
        
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

# ============================================
# تابع اصلی
# ============================================
def main():
    """حلقه اصلی ربات"""
    print("="*60)
    print("👑 PRINCESS STORY BOT - AI VERSION")
    print("📖 داستان‌سرای هوشمند جنگل نقره‌ای")
    print("🤖 استفاده از DeepSeek AI")
    print("⏰ هر ۱ ساعت یک فصل جدید")
    print("📝 هر فصل ۱۰ تا ۱۵ خط")
    print("♾️  داستان تا بینهایت ادامه دارد")
    print("🎨 تصویرسازی با AI")
    print("="*60)
    
    print(f"\n🔑 بررسی API Key: {DEEPSEEK_API_KEY[:10]}...")
    
    print("🔌 تست اتصال به DeepSeek...")
    test_story = generate_story_with_deepseek(0)
    if test_story:
        print("✅ اتصال به DeepSeek برقرار است!")
    else:
        print("⚠️ اتصال به DeepSeek ناموفق بود")
        print("   ممکن است اعتبار حساب تمام شده باشد")
    
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

# ============================================
# اجرا
# ============================================
if __name__ == "__main__":
    main()
