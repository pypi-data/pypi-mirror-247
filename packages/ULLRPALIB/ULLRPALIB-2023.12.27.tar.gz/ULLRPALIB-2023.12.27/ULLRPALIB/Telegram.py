from telegram import Bot
import asyncio

BOT_TOKEN = "Z:\\RPA\RPA23\\0000_Utils\\Ultrasecreto\\rparobi_bot_token.txt"

async def send_telegram_message(message,chat_id):
    token = get_bot_token()
    # Create the bot
    bot = Bot(token)

    # Send the message
    async with bot:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

def send_message(message,chat_id):
    asyncio.run(send_telegram_message(message,chat_id))
    # Cualquier cosa

# Read secret txt file and obtain the token
def get_bot_token(): 
    with open(BOT_TOKEN, "r") as f:
        token = f.readline().replace("\n", "")
    return token
    
    

"""
if __name__ == "__main__":
    send_message("Hello, world!")
    

"""