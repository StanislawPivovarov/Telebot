import multiprocessing
from multiprocessing import Process
import telebot
import time
import requests
from bs4 import BeautifulSoup
from deeppavlov import build_model, train_model
from deeppavlov.core.common.file import read_json

cqa_model_config = read_json("squad_ru_bert_infer.json")
cqa_model = build_model(cqa_model_config, download=True)
# cqa_model = train_model(cqa_model_config)

intent_catcher_model_config = read_json("intent_catcher.json")

bot = telebot.TeleBot("")
min_limit = 1

with open("aboutCoffee.txt", "r") as file:
    data = file.read().replace("\n", " ")
context = data


def get_first_message(message):
    chatId = message.chat.id
    bot.reply_to(
        message,
        "☕Hello!☕ \n"
        "We are West Coffee Roasters! The biggest coffee company in the World!\n"
        "This customer support bot with artificial intelligence inside! \n"
        "It can answer your question about coffee we roast, get info about tours. \n"
        "Also it can recommend you coffee that you should get. \n"
        "🧋Thats it! Have fun!🧋",
    )
    bot.send_sticker(chatId, 'CAACAgIAAxkBAAEG9ShjpNs-66y9dxgCUe9npRGX4dN4wQACCCUAAtnTKUnqyoA66LOUUSwE')


def get_answer_message(message):
    answer = cqa_model([context], [message.text])
    print("metrix: ", answer)
    if answer[2][0] < min_limit:
        bot.reply_to(message, "🫢 I don't think i can answer your question yet !")
    else:
        bot.reply_to(message, answer)


@bot.message_handler(content_types=["text"])
def get_text_message(message):
    chatId = message.chat.id
    file = open('sendimage.png', 'rb')
    queue.put(message.text)
    intent_result = queue.get()
    print("message: ", message.text)
    print("intent: ", intent_result[0])
    if intent_result[0] == "start":
        get_first_message(message)
    elif intent_result[0] == "cqa":
        get_answer_message(message)
    elif intent_result[0] == "coffee":
        bot.reply_to(message, "All coffee and prices you can see here")
        bot.send_photo(chatId, file)
    else:
        bot.reply_to(
            message, "👀OOPSY! \nn" "your phrase to hard for me.\n" "try to rephrase!"
        )


def work_with_intent_catcher_model(q):
    # intent_catcher_model = build_model(intent_catcher_model_config)
    intent_catcher_model = train_model(intent_catcher_model_config)
    q.put(1)
    while True:
        q.put(intent_catcher_model([q.get()]))


if __name__ == "__main__":
    queue = multiprocessing.Queue()
    child_process = Process(target=work_with_intent_catcher_model, args=(queue,))
    child_process.start()
    queue.get()
    print("Welcome to Narnia")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(15)
