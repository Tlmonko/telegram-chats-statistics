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

print(f'You picked {chat_name} chat, collecting statistics....')

messages = chat['messages']

USERNAME = ' '.join(
    [data['personal_information']['first_name'], data['personal_information']['last_name']])

# statistics collecting

messages_count = len(messages)

users_messages_count = {}

for msg in messages:
    if msg['type'] == 'service':
        continue
    user_from = msg['from']
    if user_from in users_messages_count.keys():
        users_messages_count[user_from] += 1
    else:
        users_messages_count[user_from] = 1

members = users_messages_count.keys()
print(f'Members: {", ".join(members)}')

print(f'Messages count (total {messages_count})')
print('\n'.join(
    [f'{index + 1}. {user} - {users_messages_count[user]} messages.' for index, user in enumerate(
        sorted(users_messages_count.keys(), key=lambda el: users_messages_count[el],
               reverse=True))]))
