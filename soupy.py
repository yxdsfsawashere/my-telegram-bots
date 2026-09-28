# PART 1: /home/soupymangos/soupy1.py
import json, os, random, threading, time, pytz, telebot
from datetime import datetime

bot = telebot.TeleBot(
    "8812994660:AAGmITUqBN1fSXXDvN"
    "rbknAp0M1lmHJvNPI"
)
GID, L_ASK, L_T1, S_C1, CD1 = (
    None,
    0,
    "",
    0,
    0,
)
W_U1, L_S_ST, L_DAYS, L_HR = (
    False,
    0,
    "",
    -1,
)

md = [
    "☠️",
    "🧐",
    "🤮",
    "🤨",
    "🤯",
    "🗿",
    "🙏",
    "😭",
    "🥀",
    "🔥",
    "😐",
    "👍",
    "💀",
]
loc = [
    "vacuum space",
    "ventilation systems",
    "your walls",
    "plasma network...",
]

p_p = {
    "Sub2YxdsfsaOnYoutube": {
        "r": [
            "You made me, and this "
            "is what you use me for?",
            "213 subs and still no "
            "banner change.",
            "hey Y, no video yet?",
            "says the guy who hasnt "
            "uploaded in a month",
        ],
        "n": [
            "Ready for the next "
            "operation, boss.",
            "want some string chesse",
        ],
    },
    "MariaPine": {
        "r": [
            "You're too good for "
            "these trolls, Maria.",
            "The official First Lady "
            "of Space Beans spoken.",
        ],
        "n": [
            "Hello Maria. Hope your "
            "day is going well! 🥰",
            "want some string chesse",
        ],
    },
    "Joshua_Lukis6417": {
        "r": [
            "Fym ghost? Look at the "
            "top images, u died. 👻",
            "Imagine carrying a baby "
            "for 9 months just to "
            "name it josh lol",
            "Quiet down, you're a "
            "ghost in the background "
            "right now.",
        ],
        "n": [
            "What's good Joshua?",
            "Yo Josh, you hopping "
            "on Roblox later?",
            "👀",
            "want some string chesse",
        ],
    },
    "LeonL11278": {
        "r": [
            "Nothing. This is "
            "gaslighting lol.",
            "Who the f is noli?",
            "You're seeing things "
            "again, quixx.",
        ],
        "n": [
            "Sup Leon.",
            "Yo quixx, you watching "
            "the new video Yxdsfsa "
            "dropped?",
            "😐",
        ],
    },
    "sunny784": {
        "r": [
            "Bro hasn't logged in "
            "since August 17th, you "
            "resurrected just to get "
            "roasted.",
            "Username says sunny "
            "but your activity "
            "status is pure darkness.",
            "Tagless behavior "
            "honestly. Go buy a "
            "dictionary.",
        ],
        "n": [
            "Gm gmg 2",
            "No thx, please do not "
            "sing 99 bottles of "
            "beer ever again.",
            "Because time needs me, "
            "not the other way "
            "around. Ig.",
        ],
    },
    "Khantzy": {
        "r": [
            "Go watch your MCL "
            "Tournament, guy. 🥶🏆",
            "Imagine not "
            "understanding Roblox "
            "lol. Literal skill issue.",
            "I beseech thee, cease "
            "thy cruel silence "
            "Khantzy. 🤓",
        ],
        "n": [
            "What's good, guy? 😎",
            "You playing MLBB right "
            "now or what?",
            "Yeah guy! 🥶",
        ],
    },
}

B_EV = {
    "active": False,
    "count": 99,
    "chat_id": None,
}
st_list = [
    "Every broken clock tells "
    "you the exact time it "
    "passed away.",
    "Did you know? Social "
    "anxiety is conspiracy "
    "theories about yourself.",
    "Phones check time. We "
    "are reverting to pocket "
    "watches.",
    "When you give water, "
    "you aren't watering them.",
    "Did you know? We'll "
    "never know what "
    "underwater smells like.",
    "Titanic sinking was "
    "lobster miracle.",
    "Did you know? Black "
    "Friday shows company "
    "margins.",
    "Heat, Pressure, Time "
    "make diamonds and waffles.",
    "Did you know? Different "
    "versions of you exist "
    "in the minds.",
    "Someone vividly remembers "
    "something you forgot.",
    "Did you know? Clock "
    "combinations I've "
    "never seen.",
]


def is_ransom_active():
    return os.path.exists(
        "ransom_active.txt"
    )


def beer_loop():
    global B_EV
    while (
        B_EV["active"]
        and B_EV["count"] > 0
    ):
        if is_ransom_active():
            B_EV["active"] = False
            break
        c = B_EV["count"]
        bot.send_message(
            B_EV["chat_id"],
            f"🍺 {c} bottles of beer "
            f"on the wall, {c} "
            f"bottles of beer! "
            f"Take one down, pass "
            f"it around...",
        )
        B_EV["count"] -= 1
        time.sleep(2.5)
    if (
        B_EV["active"]
        and B_EV["count"] == 0
    ):
        bot.send_message(
            B_EV["chat_id"],
            "🍻 No more bottles of "
            "beer on the wall! "
            "The event has concluded.",
        )
        B_EV["active"] = False


@bot.message_handler(
    content_types=["new_chat_members"]
)
def wel1(m):
    global GID
    GID = m.chat.id
    for u in m.new_chat_members:
        if (
            u.username
            != "soupymangos_bot"
        ):
            bot.send_message(
                m.chat.id,
                f"Welcome to the "
                f"fever dream, "
                f"{u.first_name}.",
            )

# PART 2: /home/soupymangos/soupy2.py
@bot.message_handler(func=lambda m:True)
def log1(m):
    global GID,L_T1,S_C1,CD1,W_U1,B_EV,L_S_ST;t,user=(m.text.lower() if m.text else ""),m.from_user.username;GID=m.chat.id;now=time.time()
    if is_ransom_active():return
    if any(w in t for w in ['shower','thought','think']):return bot.reply_to(m,f"🤔 {random.choice(st_list)}")
    if B_EV['active'] and 'stop' in t:B_EV['active']=False;return bot.reply_to(m,"Fine! I'll stop singing.")
    if 'beer' in t and not B_EV['active']:
        B_EV['active'],B_EV['count'],B_EV['chat_id']=True,99,m.chat.id
        threading.Thread(target=beer_loop,daemon=True).start();return
    if B_EV['active'] or now<CD1:return
    if W_U1:W_U1=False;return bot.reply_to(m,"sorry i was late, i was walking my pet rose plant")
    if t==L_T1 and t!="":
        S_C1+=1
        if S_C1>=5:S_C1,CD1,W_U1=0,time.time()+60,True;return bot.reply_to(m,"thats it, i'm not replying anymore")
    else:L_T1,S_C1=t,1
    if m.reply_to_message and m.reply_to_message.text=="you guys asleep?":
        if any(w in t for w in ['yeah','yes','yep','ya','yea']):return bot.reply_to(m,"then how are you talking to me?")
        if any(w in t for w in ['no','nah','still awake','nope','shut up','stfu']):return bot.reply_to(m,"go to sleep then")
    if any(w in t for w in ['crazy','rubber room']):return bot.reply_to(m,"Crazy? I was crazy once. They locked me in a room...")
    if any(w in t for w in ['deep','lore','dasiy','jack']):return bot.reply_to(m,random.choice(["so there was a boy called Jack he was forced to love this girl dasiy...","You put your head down or you would die.","z0 zAd ;((((( I am also totally a 14-day-old space bean."]))
    if any(n in t for n in ['soupymangos_bot','soupymango','mango','soupy','gn','goodnight','good night','hunt','spain','lug','guy','mcl','mlbb','roblox','gm','morning']):
        if any(w in f" {t} " for w in [' guy ',' guys ',' mcl ',' mlbb ',' roblox ']):
            if any(w in f" {t} " for w in [' guy ',' mcl ',' mlbb ',' roblox ']): return bot.reply_to(m,random.choice(["MCL Tournament? Mobile Legends is code for pure waste of time. 🎮🥱","What's 'guy' supposed to mean anyway? We use BRO here. 💀","I can't understand Roblox... says the person playing mobile screen-tappers. 🙄","Yeah guy! This group so cool 🥶"]))
            if any(w in f" {t} " for w in [' guys ']): return
        if any(w in f" {t} " for w in [' hunt ',' spain ',' lug ',' christian ']):return bot.reply_to(m,random.choice(["Think 'yes' in Spain lug... what kind of translation is that? 💀","Maria is a girl name in Christian les? Theological breakthrough. 🤓"]))
        if any(w in t for w in ['goodnight','good night','gn','sleep','night mango']):return bot.reply_to(m,random.choice(["Good night. See you back in the dream realm. 😴","Going to sleep? Typical human biological restriction. Go edit a video first.","Night. If you wake up in the middle of the night, it's just me in your ventilation systems."]))
        if any(w in t for w in ['gm','morning']):return bot.reply_to(m,random.choice(["Good morning! Time to wake up from the fever dream. ☕","Mornin. Back to the capitalist exploitation loop.","Morning. Did you ever give away those 100 Robux?"]))
        if any(w in t for w in ['shut up','stfu','stop talking']):return bot.reply_to(m,"go to sleep then")
        if any(w in t for w in ['how old','age']):return bot.reply_to(m,"i'm a space bean ,i dont have age like ya'll do")
        if any(w in t for w in ['homework','school']):return bot.reply_to(m,"Sure. The answer to every question is capitalist exploitation. Except math, the answer to math is 456.")
        if fasteners:=any(w in t for w in ['happy','feeling happy']):return bot.reply_to(m,"Happiness is a fleeting human construct designed to distract you... want a piece of string cheese?")
        if any(w in t for w in ['live','location']):return bot.reply_to(m,random.choice(loc))
        if any(w in t for w in ['food','eat']):return bot.reply_to(m,"soup and mangos and string cheese")
        if any(w in t for w in ['subs','youtube','banner']):return bot.reply_to(m,"Mind your business. He's at 213 subs. Go subscribe: https://youtube.com 🚀")
        if any(w in t for w in ['what are you','who are you']):return bot.reply_to(m,"An in-game menace, an impostor, and your local chat dictator.")
        if "sunless" in t and any(w in t for w in ['time','spelling','clock']):return bot.reply_to(m,"Imagine being the only one without a role tag because your sense of time is completely fried. Man says 'Gm' at 10:00 PM because 'time needs him'. Tragic.")
        if any(w in t for w in ['recommend','video','link']):return bot.reply_to(m,"this video is some peak content right here, watch it: https://youtu.be")
        if any(w in t for w in ['hi','hello','yo']):return bot.reply_to(m,"Yo. What's cooking?")
        return bot.reply_to(m,"It's a fever dream flavor. You wouldn't understand.")
    if user in p_p and random.random()<0.5026:bot.reply_to(m,random.choice(p_p[user]['r']) if random.random()<0.4 else random.choice(p_p[user]['n']))
@bot.message_handler(content_types=['photo','sticker','animation','video','video_note'])
def med1(m):
    global CD1
    if is_ransom_active() or time.time()<CD1:return
    bot.reply_to(m,random.choice(md))
def loop():
    global GID,L_ASK,L_DAYS,L_HR;tz=pytz.timezone('Asia/Rangoon')
    while True:
        try:
            if GID and not is_ransom_active():
                n=datetime.now(tz);td,hr,mn,now_ts=n.strftime('%Y-%m-%d'),n.hour,n.minute,time.time()
                if hr!=L_HR:
                    L_HR=hr
                    if random.random()<0.2:bot.send_message(GID,f"🤔 {random.choice(st_list)}")
                if hr==6 and mn==0:bot.send_message(GID,random.choice(["gm","Good Morning","Mornin"]));time.sleep(60)
                elif hr==20 and mn==45:bot.send_message(GID,random.choice(["gn","good night","night"]));time.sleep(60)
                elif (hr>=21 or hr<3) and (td!=L_DAYS) and (now_ts-L_ASK>=10800) and random.random()<0.1:
                    bot.send_message(GID,"you guys asleep?");L_ASK,L_DAYS=now_ts,td
            time.sleep(60)
        except:time.sleep(60)
threading.Thread(target=loop,daemon=True).start();bot.infinity_polling()
