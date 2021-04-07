import json
import os

file_name = input('Type your JSON telegram data file name: ')

if not os.path.exists(file_name):
    print('File doesn\'t exist')
    exit()

with open(file_name, encoding='utf-8') as json_file:
    data = json.load(json_file)

chats = data['chats']['list']

chat_name = input('Type chat name: ')

chat = next(
    filter(lambda el: el['type'] != 'saved_messages' and el['name'] and el[
        'name'].lower() == chat_name.lower(), chats), None)

if not chat:
    print('Wrong chat name')
    exit()

print(chat['id'])
