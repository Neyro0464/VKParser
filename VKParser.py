import vk_api
import requests
from datetime import datetime 
from config import VK_TOKEN, VERSION
from DBconn import connection, insert_post_info, disconnect, insert_group_info
from preset import VK_DOMAINS, WORDFILT, COUNT
from flashtext import KeywordProcessor

import time

# Укажите ваши данные для авторизации
limit = COUNT

# Авторизация
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api() # Ключевые слова для поиска

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

    # ------------||Работа с комментариями||----------------

    # Получение комментариев к новости
    # def get_comments(owner_id, post_id, offset=0, count=500):
    #     responseComm = vk.wall.getComments(owner_id=owner_id, post_id=post_id, offset=offset, count=count)
    #     return responseComm['count']

    # Парсинг комментариев
    # def parse_comments(owner_id, post_id):
    #     comments = []
    #     offset = 0
    #     while True:
    #         responseComm = get_comments(owner_id, post_id, offset)
    #         if not responseComm['items']:
    #             break
    #         comments.extend(responseComm['items'])
    #         offset += 100
    #     return comments
    # # ------------||Работа с комментариями||----------------


 #GROUPS
def parse_groups(DOMAIN_LIST):
    conn = connection()
    for domain in DOMAIN_LIST:
        group_info = vk.groups.getById(group_ids=domain, fields=['members_count', 'city'])
        print(group_info[0]['members_count'])
        if 'city' not in group_info[0]:
            group_info[0].setdefault('city', {}).setdefault('title', 'NULL')
        print(group_info[0]['city']['title'])
        #print(group_info[0]['counters'])
        insert_group_info(conn, group_info[0]['id'], group_info[0]['name'], 
                          f"https://vk.com/{group_info[0]['screen_name']}", group_info[0]['city']['title'])
    disconnect(conn)
#GROUPS

 # Использование метода wall.get через запрос к странице, чтобы получить id постов.
def get_posts(domain, OFFSET):
    responsePost = requests.get('https://api.vk.com/method/wall.get',
    params={'access_token': VK_TOKEN,
            'v': VERSION,
            'domain': domain,
            'offset': OFFSET,
            'count': limit
            })
    data = responsePost.json()['response']['items']
    return data


# Для каждого поста выводим комментарии
def parse_wall(conn, DOMAIN_LIST, STARTDATE, ENDDATE):
    start_time = 0
    end_time = 0
    for domain in DOMAIN_LIST:

        start_time = time.time()

        OFFSET = 0
        exitFlag = False
        while not exitFlag:
            # Получения сведений(id, name, screen_name) о сообществе по домену
            group_info = vk.groups.getById(group_ids=domain)            #Данные о постах
            data = get_posts(domain, OFFSET)
            if data == []:
                exitFlag = True
                break
            for post in data:
                date = datetime.fromtimestamp(post['date'])
                print(post['id'], '\t', date)
                if date <= ENDDATE:
                    if date > STARTDATE: # пока дата поста больше требуемой, продолжаем
                        text = post['text'].casefold()
                        for key in WORDFILT.keys():
                            word_list = WORDFILT[key]
                            keyword_processor = KeywordProcessor()
                            keyword_processor.add_keywords_from_list(word_list)
                            #for word in WORDFILT[key]:
                            word = keyword_processor.extract_keywords(text)
                                #if word in text:
                            if word:
                                counter_dict[key] += 1
                                 #------------блок вывода информации в консоль------------
                                print('ID поста: ', post['id'], ':::', group_info[0]['name'], ':::',
                                       f"https://vk.com/{group_info[0]['screen_name']}")
                                addres = f"https://vk.com/wall-{group_info[0]['id']}_{post['id']}"
                                print('Ссылка на пост: ', addres)
                                print('Дата выхода поста: ',date, 'по нск', '\n')
                                #------------блок вывода информации в консоль------------
                                # Подключение к базе и занос информации туда
                                insert_post_info(conn, post['id'], key, date,
                                        group_info[0]['id'], addres, word[0], post['comments']['count'])
                                break
                    else:
                        exitFlag = True
                        break
            OFFSET = OFFSET + limit

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Время выполнения: {elapsed_time:.6f} секунд")

    print(counter_dict)


def parse(STARTDATE, ENDDATE):
    parse_groups(VK_DOMAINS)
    conn = connection()  
    parse_wall(conn, VK_DOMAINS, STARTDATE, ENDDATE)
    disconnect(conn)