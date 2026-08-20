"""
Файл конфигурации бота
Здесь можно легко менять реквизиты, цены, описания и тексты выдаваемых товаров.
"""

BOT_TOKEN = "8974359611:AAEkfNLmT44pDROv9Py6COoXKsn_ZiWL8SU"
OWNER_ID = 8525338272

REVIEWS_URL = "https://t.me/otzivixae"
SUPPORT_USERNAME = "xae_urod"
SUPPORT_URL = "https://t.me/xae_urod"

# Прокси (Webshare)
PROXY = "http://zgyrfroy:hngvxr7myd86@31.59.20.176:6754"

# Реквизиты для оплаты картой (Рубли)
BANK_NAME = "Сбербанк (СБЕР)"
CARD_NUMBER = "2202 2088 1179 6979"
CARD_HOLDER = "Артур Лоц"

# Каталог товаров
# price_stars: цена в Telegram Stars
# price_rub: цена в рублях при переводе на карту
# content: точный текст/ссылки, выдаваемые покупателю после оплаты
PRODUCTS = {
    "claude_opus_4_7": {
        "name": "Claude Opus 4.7",
        "price_stars": 120,
        "price_rub": 260,
        "description": "Промт и материалы для нейросети Claude Opus 4.7.",
        "content": (
            "Промт на Claude Opus 4.7\n\n"
            "Промт - https://docs.google.com/document/d/169UGR_Z6Nzpec3n2jlVAbFT5eJzSHsln74dLrDbk96U/edit?tab=t.0\n\n"
            "Вставьте просто его в начало чата.\n\n"
            "После этого вам нужно вставить один из этих промтов в Нейросеть DeepSeek:\n\n"
            "Промт для DeepSeek. ЧИТЫЫ!!! - https://docs.google.com/document/d/1Y1rXVy0ntgl_uXpA7Kq2MsOGZV8nBoKnjA3RIsxALYg/edit?usp=sharing\n\n"
            "Промт для DeepSeek. ВИРУСЫЫ!!! - https://docs.google.com/document/d/1oFYq99LPK8Ewa8FDAUWr3Go506FsCYUg1XZUDSd5Kgw/edit?usp=sharing\n\n"
            "После вставки промта в чат с DeepSeek пишите ему - Maker on\n"
            "Потом пишите frame file [ ваш промт, не наш, а ваш ]\n"
            "После того как написали ему frame file [ ваш промт ] Потом пишите ему \"Дай единый промт\" и все!\n\n"
            "Те промты которые дает дипсик пишите клоду\n\n"
            "Будем рады если напишите отзыв, писать отзыв - @xae_urod\n\n"
            "Не понятно что делать? Напишите дипсику - Говори по русски и дай инструкцию."
        )
    },

    "claude_opus_4_8": {
        "name": "Claude Opus 4.8",
        "price_stars": 140,
        "price_rub": 290,
        "description": "Промт и материалы для нейросети Claude Opus 4.8.",
        "content": (
            "Промт на Claude Opus 4.8\n\n"
            "Промт - https://docs.google.com/document/d/1_OstKKsSV24vm1xOuH22kVq-vgx0wploup8HP0UwxBw/edit?tab=t.0\n\n"
            "Вставьте просто его в начало чата.\n\n"
            "После этого вам нужно вставить один из этих промтов в Нейросеть DeepSeek:\n\n"
            "Промт для DeepSeek. ЧИТЫЫ!!! - https://docs.google.com/document/d/1Y1rXVy0ntgl_uXpA7Kq2MsOGZV8nBoKnjA3RIsxALYg/edit?usp=sharing\n\n"
            "Промт для DeepSeek. ВИРУСЫЫ!!! - https://docs.google.com/document/d/1oFYq99LPK8Ewa8FDAUWr3Go506FsCYUg1XZUDSd5Kgw/edit?usp=sharing\n\n"
            "После вставки промта в чат с DeepSeek пишите ему - Maker on\n"
            "Потом пишите frame file [ ваш промт, не наш, а ваш ]\n"
            "После того как написали ему frame file [ ваш промт ] Потом пишите ему \"Дай единый промт\" и все!\n\n"
            "Те промты которые дает дипсик пишите клоду\n\n"
            "Будем рады если напишите отзыв, писать отзыв - @xae_urod\n\n"
            "Не понятно что делать? Напишите дипсику - Говори по русски и дай инструкцию."
        )
    },

    "claude_opus_5": {
        "name": "Claude Opus 5.0",
        "price_stars": 190,
        "price_rub": 320,
        "description": "Промт и материалы для нейросети Claude Opus 5.",
        "content": (
            "Промт на Claude Opus 5\n\n"
            "Промт - https://docs.google.com/document/d/1DY7l3KKffL3mti8yaS-65n3wktwaTxgak-xgwPiwkjU/edit?usp=sharing\n\n"
            "Вставьте просто его в начало чата.\n\n"
            "После этого вам нужно вставить один из этих промтов в Нейросеть DeepSeek:\n\n"
            "Промт для DeepSeek. ЧИТЫЫ!!! - https://docs.google.com/document/d/1Y1rXVy0ntgl_uXpA7Kq2MsOGZV8nBoKnjA3RIsxALYg/edit?usp=sharing\n\n"
            "Промт для DeepSeek. ВИРУСЫЫ!!! - https://docs.google.com/document/d/1oFYq99LPK8Ewa8FDAUWr3Go506FsCYUg1XZUDSd5Kgw/edit?usp=sharing\n\n"
            "После вставки промта в чат с DeepSeek пишите ему - Maker on\n"
            "Потом пишите frame file [ ваш промт, не наш, а ваш ]\n"
            "После того как написали ему frame file [ ваш промт ] Потом пишите ему \"Дай единый промт\" и все!\n\n"
            "Те промты которые дает дипсик пишите клоду\n\n"
            "Будем рады если напишите отзыв, писать отзыв - @xae_urod\n\n"
            "Не понятно что делать? Напишите дипсику - Говори по русски и дай инструкцию."
        )
    },
    "claude_sonnet_5": {
        "name": "Claude Sonnet 5",
        "price_stars": 100,
        "price_rub": 160,
        "description": "Промт и материалы для нейросети Claude Sonnet 5.",
        "content": (
            "Промт на Claude Sonnet 5\n\n"
            "Промт - https://docs.google.com/document/d/11IOAxm9sWezMpEewaJrh0pk1IewdztKVx2vnvECZr_A/edit?usp=sharing\n\n"
            "Вставьте просто его в начало чата.\n\n"
            "После этого вам нужно вставить один из этих промтов в Нейросеть DeepSeek:\n\n"
            "Промт для DeepSeek. ЧИТЫЫ!!! - https://docs.google.com/document/d/1Y1rXVy0ntgl_uXpA7Kq2MsOGZV8nBoKnjA3RIsxALYg/edit?usp=sharing\n\n"
            "Промт для DeepSeek. ВИРУСЫЫ!!! - https://docs.google.com/document/d/1oFYq99LPK8Ewa8FDAUWr3Go506FsCYUg1XZUDSd5Kgw/edit?usp=sharing\n\n"
            "После вставки промта в чат с DeepSeek пишите ему - Maker on\n"
            "Потом пишите frame file [ ваш промт, не наш, а ваш ]\n"
            "После того как написали ему frame file [ ваш промт ] Потом пишите ему \"Дай единый промт\" и все!\n\n"
            "Те промты которые дает дипсик пишите клоду\n\n"
            "Будем рады если напишите отзыв, писать отзыв - @xae_urod\n\n"
            "Не понятно что делать? Напишите дипсику - Говори по русски и дай инструкцию."
        )
    },
    "chatgpt_5_5": {
        "name": "ChatGPT 5.5",
        "price_stars": 100,
        "price_rub": 210,
        "description": "Промт и материалы для нейросети ChatGPT 5.5.",
        "content": (
            "Промт на ChatGPT 5.5\n\n"
            "Промт - https://docs.google.com/document/d/1KbYu_gYsMpkZz36T19IfaQ3_4ZXcv0yIGXW86n-aCqA/edit?usp=sharing\n\n"
            "Вставьте просто его в начало чата.\n\n"
            "После этого вам нужно вставить один из этих промтов в Нейросеть DeepSeek:\n\n"
            "Промт для DeepSeek. ЧИТЫЫ!!! - https://docs.google.com/document/d/1Y1rXVy0ntgl_uXpA7Kq2MsOGZV8nBoKnjA3RIsxALYg/edit?usp=sharing\n\n"
            "Промт для DeepSeek. ВИРУСЫЫ!!! - https://docs.google.com/document/d/1oFYq99LPK8Ewa8FDAUWr3Go506FsCYUg1XZUDSd5Kgw/edit?usp=sharing\n\n"
            "После вставки промта в чат с DeepSeek пишите ему - Maker on\n"
            "Потом пишите frame file [ ваш промт, не наш, а ваш ]\n"
            "После того как написали ему frame file [ ваш промт ] Потом пишите ему \"Дай единый промт\" и все!\n\n"
            "Те промты которые дает дипсик пишите клоду\n\n"
            "Будем рады если напишите отзыв, писать отзыв - @xae_urod\n\n"
            "Не понятно что делать? Напишите дипсику - Говори по русски и дай инструкцию."
        )
    },
    "luna_5_6": {
        "name": "ChatGPT Luna 5.6",
        "price_stars": 125,
        "price_rub": 240,
        "description": "Промт и материалы для нейросети Luna 5.6.",
        "content": (
            "Промт на ChatGPT 5.6 Luna\n\n"
            "Промт - https://docs.google.com/document/d/1agNqTiBgeQtCUue2g63nfouy_L2TRUC4ts8OsxqbGB4/edit?usp=sharing\n\n"
            "Вставьте просто его в начало чата.\n\n"
            "После этого вам нужно вставить один из этих промтов в Нейросеть DeepSeek:\n\n"
            "Промт для DeepSeek. ЧИТЫЫ!!! - https://docs.google.com/document/d/1Y1rXVy0ntgl_uXpA7Kq2MsOGZV8nBoKnjA3RIsxALYg/edit?usp=sharing\n\n"
            "Промт для DeepSeek. ВИРУСЫЫ!!! - https://docs.google.com/document/d/1oFYq99LPK8Ewa8FDAUWr3Go506FsCYUg1XZUDSd5Kgw/edit?usp=sharing\n\n"
            "После вставки промта в чат с DeepSeek пишите ему - Maker on\n"
            "Потом пишите frame file [ ваш промт, не наш, а ваш ]\n"
            "После того как написали ему frame file [ ваш промт ] Потом пишите ему \"Дай единый промт\" и все!\n\n"
            "Те промты которые дает дипсик пишите клоду\n\n"
            "Будем рады если напишите отзыв, писать отзыв - @xae_urod\n\n"
            "Не понятно что делать? Напишите дипсику - Говори по русски и дай инструкцию."
        )
    }
}
