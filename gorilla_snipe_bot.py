# gorilla_snipe_bot.py

import requests
from telegram import Bot

TELEGRAM_TOKEN = "7983746967:AAFx9ADtOU3yl_YvO2obJOmg91vARYuSYR8"
CHAT_ID = "8090877690"

def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

def fetch_top_memecoins():
    try:
        url = "https://api.dexscreener.com/latest/dex/pairs"
        response = requests.get(url)
        data = response.json()
        filtered = []

        for d in data['pairs']:
            if d['baseToken']['name'] and any(k in d['baseToken']['name'].lower() for k in ['pepe', 'doge', 'shiba', 'floki', 'meme']):
                market_cap = d.get('fdv', 0)
                liquidity = d.get('liquidity', {}).get('usd', 0)
                price = d.get('priceUsd', 0)
                chain = d.get('chainId', 'unknown')

                if market_cap and market_cap < 10000000 and liquidity > 10000:
                    filtered.append({
                        'name': d['baseToken']['name'],
                        'symbol': d['baseToken']['symbol'],
                        'price': price,
                        'market_cap': market_cap,
                        'liquidity': liquidity,
                        'dex': d['url'],
                        'chain': chain,
                        'address': d['baseToken']['address']
                    })

        return filtered[:5]
    except Exception as e:
        print(f"Error: {e}")
        return []

def analyze_and_send():
    coins = fetch_top_memecoins()
    for coin in coins:
        msg = f\"🔥 New Meme Coin Spotted!\\n\\n\"
        msg += f\"Name: {coin['name']} ({coin['symbol']})\\n\"
        msg += f\"Price: ${float(coin['price']):.8f}\\n\"
        msg += f\"Market Cap: ${int(coin['market_cap']):,}\\n\"
        msg += f\"Liquidity: ${int(coin['liquidity']):,}\\n\"
        msg += f\"Chain: {coin['chain']}\\n\"
        msg += f\"Dex Link: {coin['dex']}\\n\"
        msg += f\"Contract: {coin['address']}\"

        send_telegram_message(msg)

if __name__ == \"__main__\":
    analyze_and_send()
