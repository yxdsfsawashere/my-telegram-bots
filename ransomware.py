import asyncio
import time
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "8748902297:AAGcGhn3mzO9MgZPJzz-UIQk6V2pV7C8QrU"

# Core database to manage chat metrics and active triggers
sessions = {}

def get_session(chat_id):
    if chat_id not in sessions:
        sessions[chat_id] = {
            "message_timestamps": [],
            "status": "IDLE",       # IDLE, WARNING, ACTIVE
            "warning_message": None,
            "alert_message": None,   # Stores the main encrypted alert panel
            "tracked_messages": [],  # Collects temporary notification messages to delete later
            "warning_task": None,
            "countdown_task": None,
            "balance_owed": 500,
            "time_left": 90          # 1 minute and 30 seconds (90 seconds total)
        }
    return sessions[chat_id]

async def clear_warning_after_delay(context: ContextTypes.DEFAULT_TYPE, chat_id: int, delay: int):
    """Deletes the warning message after 3 seconds if no further message triggers the payload."""
    await asyncio.sleep(delay)
    session = get_session(chat_id)
    if session["status"] == "WARNING" and session["warning_message"]:
        try:
            await session["warning_message"].delete()
        except Exception as e:
            print(f"Failed to delete warning message: {e}")
        session["status"] = "IDLE"
        session["warning_message"] = None

def generate_alert_text(balance, time_left):
    """Generates the live panel text showing real-time metrics with proper minutes:seconds notation."""
    minutes = time_left // 60
    seconds = time_left % 60
    return (
        "⚠️ CRITICAL SECURITY ALERT ⚠️\n\n"
        "YOUR CHAT LOGS HAVE BEEN ENCRYPTED\n"
        "If you do not pay this ransom in time your chat logs WILL BE ACCESSIBLE BY ANY MEANS\n\n"
        f"💰 REMAINING BALANCE OWED: {balance} GOLD\n"
        f"⏳ TIME REMAINING: {minutes:02d}:{seconds:02d}\n\n"
        "Accepted Currency Units (Mix & Match Any Order):\n"
        "🪙 Coin = 1 Gold\n"
        "💵 Bank Note = 10 Gold\n"
        "💰 Moneybag = 50 Gold\n"
        "💎 Diamond = 80 Gold\n"
        "🍯 Honeypot = 500 Gold"
    )

async def live_countdown_ticker(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """Updates the main message board live every 5 seconds until time runs out."""
    session = get_session(chat_id)
    try:
        while session["time_left"] > 0:
            await asyncio.sleep(5)
            if session["status"] != "ACTIVE":
                break
                
            session["time_left"] -= 5
            
            if session["time_left"] <= 0:
                break
                
            if session["alert_message"]:
                try:
                    await session["alert_message"].edit_text(
                        generate_alert_text(session["balance_owed"], session["time_left"])
                    )
                except Exception as e:
                    print(f"Failed to update dashboard text: {e}")
                    
        if session["status"] == "ACTIVE":
            await context.bot.send_message(
                chat_id=chat_id,
                text="TIME EXPIRED. DECRYPTION KEY DESTROYED.\nYOUR CHAT HISTORY IS PERMANENTLY UNRECOVERABLE. ⛔🔒"
            )
            await purge_session_messages(session)
            reset_session(session)
            
    except Exception as e:
        print(f"Ticker anomaly: {e}")

async def purge_session_messages(session):
    """Cleans up and purges all residual bot interactions cleanly from the timeline."""
    if session["alert_message"]:
        try:
            await session["alert_message"].delete()
        except Exception:
            pass
            
    for msg in session["tracked_messages"]:
        try:
            await msg.delete()
        except Exception:
            pass
            
    session["tracked_messages"] = []

def reset_session(session):
    if session["warning_task"]:
        session["warning_task"].cancel()
    if session["countdown_task"]:
        session["countdown_task"].cancel()
    session["status"] = "IDLE"
    session["warning_message"] = None
    session["alert_message"] = None
    session["balance_owed"] = 500
    session["time_left"] = 90

async def monitor_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_message = update.message
    if not user_message or not user_message.text:
        return

    session = get_session(chat_id)
    current_time = time.time()
    bot_username = (await context.bot.get_me()).username

    # --- MECHANIC 1: CHAT MONITORING & ACTIVATION ---
    if session["status"] == "IDLE":
        session["message_timestamps"].append(current_time)
        session["message_timestamps"] = [t for t in session["message_timestamps"] if current_time - t <= 10]

        is_mentioned = f"@{bot_username}" in user_message.text
        is_flooding = len(session["message_timestamps"]) >= 6

        if is_mentioned or is_flooding:
            session["status"] = "WARNING"
            session["warning_message"] = await user_message.reply_text("✋🛑STOP⛔️")
            session["warning_task"] = asyncio.create_task(clear_warning_after_delay(context, chat_id, 3))
            return

    elif session["status"] == "WARNING":
        if session["warning_task"]:
            session["warning_task"].cancel()
        
        session["status"] = "ACTIVE"
        session["balance_owed"] = 500
        session["time_left"] = 90
        session["tracked_messages"] = []
        
        session["alert_message"] = await user_message.reply_text(
            generate_alert_text(session["balance_owed"], session["time_left"])
        )
        session["countdown_task"] = asyncio.create_task(live_countdown_ticker(context, chat_id))
        return

    # --- MECHANIC 2 & 3: FLEXIBLE PAYMENT LOOP ---
    elif session["status"] == "ACTIVE":
        text = user_message.text
        
        coins = text.count("🪙")
        banknotes = text.count("💵")
        moneybags = text.count("💰")
        diamonds = text.count("💎")
        honeypots = text.count("🍯")
        
        total_paid = (coins * 1) + (banknotes * 10) + (moneybags * 50) + (diamonds * 80) + (honeypots * 500)
        
        if total_paid > 0:
            session["balance_owed"] -= total_paid
            
            if session["balance_owed"] <= 0:
                await purge_session_messages(session)
                await user_message.reply_text("👍🟩THANK YOU✅")
                reset_session(session)
            else:
                if session["alert_message"]:
                    try:
                        await session["alert_message"].edit_text(
                            generate_alert_text(session["balance_owed"], session["time_left"])
                        )
                    except Exception as e:
                        print(f"Error editing main text node: {e}")
                
                deficit_msg = await user_message.reply_text(
                    f"⚠️ DEFICIT NOTED. You have {session['balance_owed']} Gold left to pay!"
                )
                session["tracked_messages"].append(deficit_msg)

def main():
    """Starts the bot application without proxies for native cloud environments like Railway."""
    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, monitor_chat))
    
    print("Ransom simulator deployed and successfully running on Railway...")
    app.run_polling()

if __name__ == "__main__":
    main()

