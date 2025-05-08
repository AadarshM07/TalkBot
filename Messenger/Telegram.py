import os
import json
import time
import requests
import traceback

class Telegram:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = "./Config/telegram_config.py"

        with open(config_path, 'r') as f:
            config = json.load(f)

        self.telegram_url = config['url']
        self.channels = config['channels']
        self.default_channel = self.channels[0]

        self.channel_info = {
            ch: {
                'bot_key': config[ch]['bot_key'],
                'chat_id': config[ch]['chat_id']
            } for ch in self.channels
        }

    def send_message(self, message, channel_name=None):
        if not message:
            return

        channel_name = channel_name or self.default_channel

        if channel_name not in self.channel_info:
            print(f"Channel '{channel_name}' not found in config.")
            return

        info = self.channel_info[channel_name]
        url = f"{self.telegram_url}{info['bot_key']}/sendMessage"
        data = {
            'chat_id': info['chat_id'],
            'text': message,
            'parse_mode': 'Markdown'
        }

        try:
            response = requests.post(url, params=data)
            if response.status_code != 200:
                print(f"Failed to send message: {response.text}")
        except Exception as e:
            print(f"Exception while sending message: {str(e)}")
            print(traceback.format_exc())

        time.sleep(1)  # Optional rate limit

if __name__=="__main__":
    tg = Telegram()
    tg.send_message("what color is your bugatti")