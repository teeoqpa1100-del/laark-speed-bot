import os
import telebot
from flask import Flask, request

# هنا الكود صار يقرا التوكن من موقع ريندر تلقائياً عشان الأمان
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda message: message.text and "طش" in message.text)
def reply_tash(message):
    bot.reply_to(message, "جاهز ..")

@bot.message_handler(commands=["art", "مقال"])
def send_article(message):
    article_text = (
        "\n.. ذروة المجد صعبة المنال .. لا ينالها إلا من كان السيف حليفه\n"
        ".. المهابة تؤخذ عزماً وقوة .. ومقامات الرجال تُقاس بالأفعال لا بالقول"
    )
    bot.reply_to(message, article_text)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # هنا تحط رابط البوت حقك في ريندر عشان يربطهم ببعض
    bot.set_webhook(url='https://laark-speed-bot.onrender.com/' + TOKEN)
    return "البوت يعمل بنجاح الحين يا سيف الغلا!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))





