import json
import requests
import time
import urllib
import io

TOKEN = "1706103491:AAGVdKBTjb7-t2sGNvBhOJYOIYrvF0p049w"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        change = False
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        if text=="FASS":
            text = "FASS has several wheelchair ramps and elevator access to all floors. \nIf you wish to provide additional information about this location type /feedback"
            send_message(text, chat)
            change = True
            send_message("https://nus.edu.sg/osa/docs/default-source/osa-doc/services/disability-support/fass-schematic-map.pdf", chat)
        if text=="Utown":
            text = "Utown has wheelchair access for all buildings. \nIf you wish to provide additional information about this location type /feedback"
            send_message(text, chat)
            change = True
            send_message("https://lh3.googleusercontent.com/proxy/ZM6WKTRN8D0GglGHM3jIFbRMtFT2FzwUDCDu61hwupmJOJB3yzNLZQBR0C54i7PrWkWXlTSFYnlDXXCLPRXQwz6rPCEDSZMkQ3tyWSq2fdtNNGnn7zzcxILj--KSS44", chat)
        if text=="/buddy" :
            text="Welcome to the the NUS Connects buddy system. Please enter the location to which you would like to travel. Your options are \nFASS \nUtown"
            send_message(text, chat)
            text="Unfortunately no buddies are available right now!"
            send_message(text, chat)
        if text=="/feedback" :
            text = "Thank you for choosing to provide feedback! User generated information is the key to ensuring that our bot provides more accurate information than a simple web search!"
            send_message(text, chat)
            text = "###This part of the system has not been implemented yet###"
            send_message(text, chat)
        if not (change):
            text ="""Hi! Welcome to NUS Connect Bot! \nTo use the buddy system and request for a buddy enter:\n/buddy To get collated information about NUS locations, simply type in the name. Your options are:
Utown
FASS
Thanks for using our bot! We hope it has been useful to you!"""
            send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
