import asyncio, time, os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Wired directly with your provided token string
TOKEN = "8924063665:AAFgHgip7nD9Z_Gg7tKa390yAvaYIXKQ2RE"
S = {}  # Game sessions storage

def get_s(cid):
    if cid not in S:
        S[cid] = {"status": "IDLE", "players": {}, "next_t": 10, "room": 0, "target": 0, "chased": None, "task": None, "stage": 0, "ts": []}
    return S[cid]

def get_hud(s):
    if s["status"] == "QUEUE":
        return "🤖 **TELLER UNIT INTRUSION** 🤖\n\n👉 Click below to pull a ticket.\nSend 🎫 to initialize launch!"
    if s["status"] in ["PROGRESSION", "RED_ALERT", "CHASE"]:
        ui = "".join(["🟥" if i < s["stage"] else "⬜" for i in range(5)])
        return f"📟 **TELLER DASHBOARD** 📟\n\nSCREEN: [{ui}]\nDOOR READOUT: [{s['room']}]\n\n⚠️ *Messages advance room count.*"
    return ""

async def alert_timer(ctx, cid):
    s = S[cid]
    for i in range(1, 6):
        await asyncio.sleep(1.4)
        if s["status"] != "RED_ALERT": return
        s["stage"] = i
        try: await s["msg"].edit_text(get_hud(s))
        except: pass
    s["status"] = "CHASE"
    await ctx.bot.send_message(cid, f"🚨 **PURSUIT MODE** 🚨\nTeller targets @{s['players'][s['chased']]['name']}!\n\n🏃‍♂️ Type 'hide'/'closet' to live, or chat to dodge!")

async def btn_click(update, ctx):
    q = update.callback_query; await q.answer()
    cid, u = q.message.chat_id, q.from_user
    s = get_s(cid)
    if s["status"] != "QUEUE": return
    if u.id in s["players"]:
        await ctx.bot.send_message(cid, f"❌ Already holding 🎫 #{s['players'][u.id]['ticket']}")
        return
    s["players"][u.id] = {"name": u.username or u.first_name, "ticket": s["next_t"]}
    await ctx.bot.send_message(cid, f"🎫 Ticket #{s['next_t']} taken by @{s['players'][u.id]['name']}.")
    s["next_t"] += random.randint(3, 8)

async def monitor_chat(update, ctx):
    if not update.message or not update.message.text: return
    cid, u, txt, now = update.effective_chat.id, update.effective_user, update.message.text.strip().lower(), time.time()
    s = get_s(cid)

    if s["status"] == "IDLE":
        s["ts"] = [t for t in s["ts"] + [now] if now - t <= 10]
        if f"@{ctx.bot.username}" in update.message.text or len(s["ts"]) >= 6:
            s.update({"status": "QUEUE", "players": {}, "next_t": random.randint(10, 30), "room": 0, "stage": 0})
            s["msg"] = await update.message.reply_text(get_hud(s), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📇 Pull Ticket", callback_data="get_t")]]))

    elif s["status"] == "QUEUE" and "🎫" in txt:
        if u.id not in s["players"]: return
        s["status"] = "PROGRESSION"
        s["target"] = random.choice([p["ticket"] for p in s["players"].values()])
        s["room"] = s["target"] - random.randint(4, 7)
        await update.message.reply_text("⚡ Bulkheads lifted. Teller moving.")
        s["msg"] = await ctx.bot.send_message(cid, get_hud(s))

    elif s["status"] == "PROGRESSION":
        s["room"] += 1
        try: await s["msg"].edit_text(get_hud(s))
        except: pass
        if s["room"] == s["target"]:
            for uid, p in s["players"].items():
                if p["ticket"] == s["room"]:
                    s.update({"chased": uid, "status": "RED_ALERT"})
                    await ctx.bot.send_message(cid, f"⚠️ **LOCKDOWN** ⚠️\nTeller blocking door [{s['room']}].\n🚨 @{p['name']} send 🎫 emoji immediately!")
                    s["task"] = asyncio.create_task(alert_timer(ctx, cid))
                    break

    elif s["status"] == "RED_ALERT" and "🎫" in txt and u.id == s["chased"]:
        if s["task"]: s["task"].cancel()
        s["status"] = "IDLE"
        await update.message.reply_text("✅ **PASSED.** Ticket verified. Teller powered down.")

    elif s["status"] == "CHASE" and u.id == s["chased"]:
        s["status"] = "IDLE"
        if any(w in txt for w in ["hide", "closet"]):
            await update.message.reply_text("🚪💨 Hiding successful. Teller took ticket and shutdown safely.")
        elif random.choice([True, False]):
            s.update({"status": "PROGRESSION", "target": s["target"] + random.randint(4, 8)})
            await update.message.reply_text("🤸‍♂️ Dodged! Teller missed tracking. Keep chatting to escape!")
        else:
            await update.message.reply_text("💀 **TERMINATED.** Teller caught you. Game over.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CallbackQueryHandler(btn_click, pattern="get_t"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, monitor_chat))
    app.run_polling()

if __name__ == "__main__": main()

