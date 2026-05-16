import os
import random
import time
import telebot
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# حفظ حالة تحدي السرعة والوقت للمستخدمين
speed_challenges = {}

# كلمات خفيفة وسهلة عشان تدريب السرعة
SPEED_WORDS = ["دز", "خمس", "بس", "طش", "شل", "فز", "عز", "قو"]

@bot.message_handler(func=lambda message: message.text and "طش" in message.text)
def reply_tash(message):
    bot.reply_to(message, "جاهز ..")

# المقال بكلمة عادية وبدون شرطة مائلة
@bot.message_handler(func=lambda message: message.text in ["art", "مقال", "شعر"])
def send_article(message):
    article_text = (
        "\n.. ذروة المجد صعبة المنال .. لا ينالها إلا من كان السيف حليفه\n"
        ".. المهابة تؤخذ عزماً وقوة .. ومقامات الرجال تُقاس بالأفعال لا بالقول"
    )
    bot.reply_to(message, article_text)

# بداية تحدي سرعة التكرار بكلمة كرر عادية
@bot.message_handler(func=lambda message: message.text == "كرر")
def start_speed_challenge(message):
    chat_id = message.chat.id
    
    # اختيار 3 كلمات عشوائية مختلفة وتحديد تكرار عشوائي لكل وحدة من (2 إلى 5)
    chosen_words = random.sample(SPEED_WORDS, 3)
    count1 = random.randint(2, 5)
    count2 = random.randint(2, 5)
    count3 = random.randint(2, 5)
    
    # تجهيز نص التحدي اللي بيظهر للمستخدم
    challenge_text = f"{chosen_words[0]}({count1}) {chosen_words[1]}({count2}) {chosen_words[2]}({count3})"
    
    # تجهيز الجواب الصح اللي لازم المستخدم يكتبه
    part1 = " ".join([chosen_words[0]] * count1)
    part2 = " ".join([chosen_words[1]] * count2)
    part3 = " ".join([chosen_words[2]] * count3)
    correct_answer = f"{part1} {part2} {part3}"
    
    # حفظ الإجابة الصحيحة ووقت البداية بالثواني
    speed_challenges[chat_id] = {
        "answer": correct_answer,
        "start_time": time.time()
    }
    
    msg = (
        f"أرحب يا سيف الغلا .. جتك جملة تحدي السرعة\n\n"
        f"اكتب هالجملة الحين مكررة وبأسرع ما عندك:\n"
        f"`{challenge_text}`\n\n"
        f"*(ملاحظة: اكتبها في سطر واحد بمسافات عادية)*"
    )
    bot.send_message(chat_id, msg, parse_mode="Markdown")

# فحص سرعة ودقة جواب المستخدم وحساب الثواني
@bot.message_handler(func=lambda message: message.chat.id in speed_challenges)
def check_speed_answer(message):
    chat_id = message.chat.id
    challenge_data = speed_challenges[chat_id]
    
    correct_ans = challenge_data["answer"]
    start_time = challenge_data["start_time"]
    
    # حساب الوقت المستغرق فوراً عند وصول الرسالة
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 1) # تقريب الوقت لجزء من عشرة
    
    # تنظيف النصين من أي مسافات زايدة
    user_ans = " ".join(message.text.split())
    clean_correct = " ".join(correct_ans.split())
    
    if user_ans == clean_correct:
        # هنا البوت يطبع النتيجة مع حساب الثواني بالملي
        bot.reply_to(message, f"كفوووو ورب الكعبة سريع ووديت التحدي الحين!\n\n⏱️ الوقت: جبتها في {elapsed_time} ثانية! صح مية بالمية")
        del speed_challenges[chat_id]
    else:
        bot.reply_to(message, f"ركز يا قلبي واكتبها صح.. الجواب الصح لازم يكون كذا:\n`{clean_correct}`")




