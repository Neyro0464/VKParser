import psycopg2

def connection(id, category, posted_at, group_id, addres, key_word):
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
        query = f'''SELECT DISTINCT id FROM posts WHERE id = {id}'''
        cursor.execute(query)
        check = cursor.fetchone()
        print(check)
        if (check == None):
            query = f'''INSERT INTO Posts(id, posted_at, group_id, addres) 
                        VALUES ({id},'{posted_at}',{group_id},'{addres}')'''
            cursor.execute(query)
        query = f'''INSERT INTO Category(post_id, name, key_word)
                    VALUES ('{id}','{category}','{key_word}')'''
        cursor.execute(query)
        print("SUCCESS")
