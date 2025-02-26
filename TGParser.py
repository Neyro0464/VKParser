from config import API_ID, API_HASH, PHONE
from tools import input_dates
from DBconn import connection, insert_post_info, disconnect, insert_group_info
from preset import TG_DOMAINS, WORDFILT, COUNT

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

#'kazan_smi' - Нету такого канала

# Категории постов и счетчик по каждому из постов
counter_dict = {'Строительство': 0, 
            'Экология': 0,
            'Экономика':0,
            'Городское хозяйство':0,
            'Социальная сфера':0,
            'Соседство, среда проживания':0,
            'Культура и общественные ценности':0,
            'Этнические и религиозные отношения':0,
            'Управление городом':0
            }


async def parse_channel(conn,client, channel_username):
    # Получаем объект канала
    channel = await client.get_entity(channel_username)
    group_addres = f"t.me/{channel_username}"
    insert_group_info(conn, channel.id, channel_username, group_addres, None)
    startdate, enddate = input_dates('01.10.2024','01.01.2025')
    exitFlag = 0
    OFFSET = 0
    limit = COUNT
    # Получаем историю постов
    while(exitFlag == 0):
        posts = await client(GetHistoryRequest(
            peer=channel,
            limit=limit,  # Количество постов, которые хотим получить
            offset_date=enddate,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=OFFSET,
            hash=0
        ))
        # Проходим по каждому посту
        for post in posts.messages:
            date = post.date.replace(tzinfo=None)
            if date > startdate:
                text = post.message
                if text:  # Проверяем, есть ли текст в посте
                     for key in WORDFILT.keys():
                            for word in WORDFILT[key]:
                                if word in text:
                                    counter_dict[key] += 1
                                    #------------блок вывода информации в консоль------------
                                    print(channel_username,'::', date)
                                    print(word)
                                    #print(f"Текст поста: {post.message}")
                                    print("#"*40)
                                    post_aaddres = f"t.me/{channel_username}/{post.id}"
                                    # Получаем количество комментариев
                                    if post.replies and post.replies.comments:
                                        print(f"Количество комментариев: {post.replies.replies}")
                                        comments = post.replies.replies
                                    else:
                                        print("Комментариев нет")
                                        comments = 0
                                    print("-" * 40)
                                    #------------блок вывода информации в консоль------------

                                    insert_post_info(conn, post.id, key, date,
                                                channel.id, post_aaddres, word, comments)
                                    break
            else:
                exitFlag = 1
        OFFSET += limit


async def main(client):
    await client.start()
    conn = connection()
    with conn:
        for domain in TG_DOMAINS:
            await parse_channel(conn,client, domain)  # Замените на username канала, который хотите парсить
    disconnect(conn)

def parse():
    # Создаем клиент
    client = TelegramClient(PHONE, API_ID, API_HASH)
    with client:
        client.loop.run_until_complete(main(client))


