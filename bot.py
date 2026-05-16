import telebot

TOKEN = "8923349599:AAEwyGq6oWZi4h0LJOaZx0_DVilTqWkmWMg"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: message.text and "طش" in message.text)
def reply_tash(message):
    bot.reply_to(message, "جاهز ~")

@bot.message_handler(commands=["art", "مقال"])
def send_article(message):
    article_text = (
        "ذروة المجد صعبة المنال.. لا ينالها إلا من كان السيف حليفه~\n"
        "المهابة تُؤخذ عزماً وقوة.. ومقامات الرجال تُقاس بالأفعال لا بالقول.."
    )
    bot.reply_to(message, article_text)

print("البوت يعمل بنجاح...")
bot.infinity_polling()
