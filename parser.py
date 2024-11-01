import vk_api
import requests
from datetime import datetime 
from dateutil.relativedelta import relativedelta


# Укажите ваши данные для авторизации
VK_TOKEN = '19ff385f19ff385f19ff385f901ade7549119ff19ff385f7eea6b22f6bc857365e56efc'
VERSION = '5.199'
GROUP_ID = '76582630'
NEWS_ID = '4430'
# сдвиг по постам
OFFSET = 0
# Домен группы
DOMAIN = 'incident_nsk'
COUNT = 20
# Ключевые слова для поиска
#Определить ключевые слова путем обработки текста
wordFilt = {'Строительство': ['снос объекта', 'городская инфраструктура', 'городской инфраструктуры'], 
            'Экология': ['деревьв', 'мусор', 'загрязнен'],
            'Экономика':['бюджет', 'тариф', 'цен', 'доход'],
            'Городское хозяйство':['парк', 'площадки','сквер','дороги','парковочные места','шум'],
            'Социальная сфера':['больниц','поликлинник','роддом','школ'],
            'Соседство, среда проживания':['сосед','жител'],
            'Культура и общественные ценности':['защита прав','ценност','активисты против','активист против','поддержание традиц','культур'],
            'Этнические и религиозные отношения':['между диаспорами','мигрант','цыган','национальност','хиджаб','миграц','националист',''],
            'Управление городом':['назначен','уволен','отстранен','отстранён','власт','начальник','город'],
            'Безопасность и правопорядок':['безопасно','правопорядо','коррупцион','субкульт']}

counter_dict = {'Строительство': 0, 
            'Экология': 0,
            'Экономика':0,
            'Городское хозяйство':0,
             'Социальная сфера':0,
            'Соседство, среда проживания':0,
            'Культура и общественные ценности':0,
            'Этнические и религиозные отношения':0,
            'Управление городом':0,
            'Безопасность и правопорядок':0
            }

# Авторизация
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
# Получения сведений(id, name, screen_name) о сообществе по домену
group_info = vk.groups.getById(group_ids=DOMAIN)
# Получение id владельца сообщества
owner_id = -int(group_info[0]['id'])  # Указываем ID сообщества с минусом


# ------------||Работа с комментариями||----------------

# Получение комментариев к новости
def get_comments(owner_id, post_id, offset=0, count=100):
    response = vk.wall.getComments(owner_id=owner_id, post_id=post_id, offset=offset, count=count)
    return response

# Парсинг комментариев
def parse_comments(owner_id, post_id):
    comments = []
    offset = 0
    while True:
        response = get_comments(owner_id, post_id, offset)
        if not response['items']:
            break
        comments.extend(response['items'])
        offset += 100
    return comments
# ------------||Работа с комментариями||----------------


#Добавить цикл который будет делать смещение постов пока не дойдет до нужной даты
#(Возможно сделать через timestamp - year)

# Использование метода wall.get через запрос к странице, чтобы получить id постов.
def get_posts(VK_TOKEN, VERSION, DOMAIN, OFFSET, COUNT):
    response2 = requests.get('https://api.vk.com/method/wall.get',
    params={'access_token': VK_TOKEN,
            'v': VERSION,
            #'owner_id': owner_id,
            'domain': DOMAIN,
            'offset': OFFSET,
            'count': COUNT
            })
    data = response2.json()['response']['items']
    return data



#добавить запись в файл/ворд

# Для каждого поста выводим комментарии
def parse_wall(VK_TOKEN, VERSION, DOMAIN, OFFSET, COUNT):
    exitFlag = False
    while not exitFlag:
        data = get_posts(VK_TOKEN, VERSION, DOMAIN, OFFSET, COUNT)
        for post in data:
            if datetime.fromtimestamp(post['date']) > datetime.today() - relativedelta(days=3):
                #post_id = int(post['id'])
                print('ID поста: ', post['id'], ':::', group_info[0]['name'], ':::', f"https://vk.com/{group_info[0]['screen_name']}")
                print('Ссылка на пост: ',f"https://vk.com/wall-{group_info[0]['id']}_{post['id']}")
                print('Дата выхода поста: ',datetime.fromtimestamp(post['date']), 'по нск', '\n')
                #comments = parse_comments(owner_id, post_id)
                if wordFilt: #Если список ключевых слов не пуст, то ищем каждое ключевое слово в тексте КАЖДОГО поста
                    for key in wordFilt.keys():
                        for word in wordFilt[key]:
                            text = post['text'].casefold()
                            if word in text:
                                counter_dict[key] += 1
                                #print(post['text'])
                                break
                # else: #Если пуст, то выводим текст поста
                #     print(post['text'])
                print("-" * 40, '\n')
            else:
                exitFlag = True
                break
        OFFSET = OFFSET + COUNT
    print (counter_dict)
                
parse_wall(VK_TOKEN, VERSION, DOMAIN, OFFSET, COUNT)
# # Вывод комментариев
#     for comment in comments:
#         print(f"Comment ID: {comment['id']}")
#         print(f"Author: {comment['from_id']}")
#         print(f"Text: {comment['text']}")
#         print("-" * 40)
