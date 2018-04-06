#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import datetime

token = "558253283:AAGsWj4xlW02_Ogfw3OtYwjYprxZBQ-ZPUk"

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = \
            'https://api.telegram.org/bot{}/'.format(token)

    def get_updates(self, offset=None, timeout=3):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result
        return last_update

greet_bot = BotHandler(token)
greetings = ('hello', 'hi', 'greetings', 'sup')
now = datetime.datetime.now()

def write_chats(filename, information, today):
    """
    Create a txt file for every user, who texts the bot.
    Write down the messages and time of chat in a txt file.
    """
    new = open(filename, "a")
    new.write(today+"\n")
    new.write(str(information) + "\n")

def main():
    new_offset = None
    today = now.day
    hour = now.hour
    while True:
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()
        print("LAST UPDATE: ", type(last_update), "\n", last_update)
        
        if type(last_update) != list:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            print(last_chat_text, len(last_chat_text), type(last_chat_text))

            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']
            
            try:
                first_chat_name = last_update['message']['chat']['last_name']
            except:
                first_chat_name = "none"
                
            if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
                greet_bot.send_message(last_chat_id, 'Good Morning  {}'.format(last_chat_name))
                today += 1
            elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
                greet_bot.send_message(last_chat_id, 'Good Afternoon {}'.format(last_chat_name))
                today += 1
            elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
                greet_bot.send_message(last_chat_id, 'Good Evening  {}'.format(last_chat_name))
                today += 1
            new_offset = last_update_id + 1
        else:
            print("No updates")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

			