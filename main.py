import json
import os

file_name = input('Type your JSON telegram data file name (default: result.json): ')
if not file_name:
    file_name = 'result.json'

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

print(f'You picked {chat_name} chat, collecting statistics....\n')

messages = chat['messages']

USERNAME = ' '.join(
    [data['personal_information']['first_name'], data['personal_information']['last_name']])

# statistics collecting

messages_count = len(messages)

users_messages_count = {}

all_words = {}

dates = {}

for msg in messages:
    date, time = msg['date'].split('T')
    if date not in dates.keys():
        dates[date] = 0
    dates[date] += 1
    if msg['type'] == 'service':
        continue
    msg_text = msg['text']
    text = ''
    if isinstance(msg_text, list):
        for el in msg_text:
            if isinstance(el, str):
                text += el
            else:
                text += el['text'] + ' '
    else:
        text = msg_text
    words = text.lower().split()
    for word in words:
        if len(word) < 3:
            continue
        if word in all_words.keys():
            all_words[word] += 1
        else:
            all_words[word] = 1
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
print()

count_of_dates_to_display = int(input('Type count of most active days that you want to display: '))
print('Most active days:')
print('\n'.join([f'{el} - {dates[el]} messages' for el in
                 sorted(dates.keys(), key=lambda date: dates[date])[::-1][:count_of_dates_to_display]]))

count_of_words_to_display = int(input('Type count of most used words that you want to display: '))
if count_of_words_to_display >= len(all_words):
    count_of_words_to_display = len(all_words) - 1
print(f'{count_of_words_to_display} most used words:')
print('\n'.join(
    [f'{index + 1}. {word} - {all_words[word]} words.' for index, word in enumerate(
        sorted(all_words.keys(), key=lambda el: all_words[el],
               reverse=True)[:count_of_words_to_display])]))
