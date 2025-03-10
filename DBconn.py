import psycopg2

def connection():
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
    conn.autocommit = True
    return conn

def insert_post_info(conn, post_id, category, posted_at, group_id, post_addres, key_word, comment):
    with conn.cursor() as cursor:
        query = f'''SELECT DISTINCT id FROM posts WHERE id = {post_id}'''
        cursor.execute(query)
        check = cursor.fetchone()
        if (check == None):
            query = f'''INSERT INTO Posts(id, posted_at, group_id, addres, comments_count) 
                        VALUES ({post_id},'{posted_at}',{group_id},'{post_addres}', {comment})'''
            cursor.execute(query)
        query = f'''INSERT INTO Category(post_id, name, key_word)
                    VALUES ('{post_id}','{category}','{key_word}')'''
        cursor.execute(query)


def insert_group_info(conn, group_id, group_name, group_addres, group_city):
    with conn.cursor() as cursor:
        query = f'''SELECT DISTINCT id FROM SMGroups WHERE id = {group_id}''' #ATTENTION!!!!
        cursor.execute(query)
        check = cursor.fetchone()
        if(check == None):
            if group_city == 'NULL':
                query = f'''INSERT INTO SMGroups(id, name, addres, city) VALUES ({group_id},'{group_name}','{group_addres}', '')'''
            else: 
                query = f'''INSERT INTO SMGroups(id, name, addres, city) VALUES ({group_id},'{group_name}','{group_addres}','{group_city}')'''
            cursor.execute(query)
    cursor.close()


def disconnect(conn):
    if conn:
        conn.close()
        print("Disconnected succesfully")