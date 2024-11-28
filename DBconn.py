import psycopg2

def connection(post_id, category, posted_at, group_id, post_addres, key_word, group_name, group_addres, group_city):
    try:
        # пытаемся подключиться к базе данных
        conn = psycopg2.connect(dbname="postgres", 
                                user="postgres", 
                                password="postgres", 
                                host="localhost", 
                                port = 5432
                                )
        print('Connection succesful')
    except:
        # в случае сбоя подключения будет выведено сообщение в STDOUT
        print('Can`t establish connection to database')

    with conn.cursor() as cursor:
        conn.autocommit = True
        query = f'''SELECT DISTINCT id FROM VK_group WHERE id = {group_id}''' #ATTENTION!!!!
        cursor.execute(query)
        check = cursor.fetchone()
        if(check == None):
            query = f'''INSERT INTO Vk_group(id, name, addres, city) VALUES ({group_id},'{group_name}',{group_addres},'{group_city}')'''
        
        query = f'''SELECT DISTINCT id FROM posts WHERE id = {post_id}'''
        cursor.execute(query)
        check = cursor.fetchone()
        print(check)
        if (check == None):
            query = f'''INSERT INTO Posts(id, posted_at, group_id, addres) 
                        VALUES ({post_id},'{posted_at}',{group_id},'{post_addres}')'''
            cursor.execute(query)
        query = f'''INSERT INTO Category(post_id, name, key_word)
                    VALUES ('{post_id}','{category}','{key_word}')'''
        cursor.execute(query)
        print("SUCCESS")
