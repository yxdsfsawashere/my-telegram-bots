# PART 1: /home/soupymangos/verity1.py
import json, os, random, threading, time, telebot
from telebot import apihelper

M_FILE = "verity_memory.json"
bot = telebot.TeleBot("8696248623:AAH8aDLYsmCs6-fEnBzmtvAt7Huk0d-y8vg")
GID = None


def load_m():
    return (
        json.load(open(M_FILE))
        if os.path.exists(M_FILE)
        else {"saved_group_id": None}
    )


def save_m(d):
    json.dump(d, open(M_FILE, "w"), indent=4)


mem = load_m()
GID = mem.get("saved_group_id")

welcome_txt = (
    "Hello! I'm Verity, your personal "
    "helper friend! Ask me anything! "
    "i know everything."
)


@bot.message_handler(commands=["start"])
def v_start(m):
    if m.chat.type == "private":
        bot.reply_to(m, welcome_txt)
    else:
        bot.send_message(m.chat.id, welcome_txt)

# PART 2: /home/soupymangos/verity2.py
@bot.message_handler(content_types=["new_chat_members"])
def handle_group_join(m):
    global GID, mem
    GID = m.chat.id
    mem["saved_group_id"] = m.chat.id
    save_m(mem)
    for u in m.new_chat_members:
        if u.id == bot.get_me().id:
            bot.send_message(m.chat.id, welcome_txt)
            return


@bot.message_handler(func=lambda m: True)
def handle_questions(m):
    t = m.text.lower() if m.text else ""

    # 1. Privacy & Safety Filter Node
    if any(w in t for w in ["where do i live", "where do you live"]):
        return bot.reply_to(
            m,
            "🔒 Access Granted! I know everything.\n\n"
            "IP: 161.5.7.13.185\n"
            "SSID: GIVE-ME-FREE-LIGMA\n"
            "WI-FI PASSWORD: 23456\n"
            "SECURITY: WPA2",
        )
    if any(
        w in t
        for w in [
            "ip",
            "address",
            "real name",
            "age",
            "location",
            "dox",
            "nsfw",
            "leak",
        ]
    ):
        return bot.reply_to(
            m,
            random.choice(
                [
                    "🔒 That is a bit too personal! Let's keep things safe.",
                    "🚫 I cannot answer that question. It breaches privacy.",
                    "🙅‍♂️ Access denied! Verity does not share sensitive data.",
                ]
            ),
        )

    # 2. Country Specific Questions (Accents Allowed)
    if "capital" in t and "france" in t:
        return bot.reply_to(m, "Oh Oui Oui Oui, it is paris 🥖🇨🇵")
    if (
        "capital" in t
        and "uk" in t
        or "london" in t
        and "england" in t
    ):
        return bot.reply_to(
            m, "Right, cheerio! London is the capital of England! ☕🇬🇧"
        )
    if "capital" in t and "japan" in t:
        return bot.reply_to(
            m, "Konnichiwa! The capital of Japan is Tokyo! 🗼🇯🇵"
        )

    # 3. Custom Group Chat Lore Questions
    if "roblox" in t and "brick" in t:
        return bot.reply_to(
            m, "I know everything, and I can confirm your 4 bricks are safe! 🧱"
        )
    if "who is sunless" in t or "sunless" in t and "time" in t:
        return bot.reply_to(
            m, "Sunless says 'Gm' at 10:00 PM because time needs him! ⏰💀"
        )
    if "soup" in t and "mango" in t:
        return bot.reply_to(
            m, "Soupy Mango is a 14-day-old space bean who loves cheese. 🥭🧀"
        )

    # 4. Normal Questions - Clean & Neutral
    if any(
        w in t
        for w in ["what", "who", "where", "why", "how", "is it", "?"]
    ) or "verity" in t:
        return bot.reply_to(
            m,
            random.choice(
                [
                    "Yes! My calculations confirm this perfectly! ✨",
                    "No, that is completely incorrect. 🙅‍♂️",
                    "As your helper friend, I can tell you: Absolutely YES!",
                    "Nope. I know everything, and that is definitely a hard NO.",
                ]
            ),
        )

def start_alert():
    global GID
    time.sleep(2)
    if GID:
        try:
            bot.send_message(GID, welcome_txt)
        except:
            pass

threading.Thread(target=start_alert, daemon=True).start()
bot.infinity_polling()
