
import time
import telebot
from deeppavlov import build_model, configs, train_model
from deeppavlov.core.common.file import read_json

bot = telebot.TeleBot('5580238592:AAHjw0Fd4JyRxU_tVy9haqYZ_aNqd2weTxw')
min_limit = 10
f = open('aboutCoffee.txt', 'r', encoding="utf-8")
context = f.read()

model_config = read_json('squad_ru_bert_infer.json')
# model = build_model(model_config, download=True)
# model = build_model(model_config)
# model = train_model(model_config, download=True)
model = train_model(model_config)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    details = model([context], [message.text])
    print(details)
    if details[1][0] > min_limit:
        bot.send_message(message.from_user.id, details[0][0])
    else:
        bot.send_message(message.from_user.id, 'Я не могу дать достоверный ответ! Задайте вопрос по-другому!')

print('bot listening')
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(15)