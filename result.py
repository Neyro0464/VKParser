import psycopg2
import pandas as pd

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

def result1():
    conn = connection()
    with conn.cursor() as cursor:
        query = f'''SELECT city, 
                    gr.name || ' ' || gr.addres as info, 
                    cat.name, 
                    COUNT(post_id) OVER (PARTITION BY city, gr.name, gr.addres, cat.name), 
                    posts.addres  
                    FROM posts
                    LEFT JOIN category cat ON cat.post_id = posts.id
                    LEFT JOIN vk_group gr ON gr.id = posts.group_id
                    WHERE comments_count>=20'''
        cursor.execute(query)
        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        excel_file = 'results.xlsx'
        df = pd.DataFrame(rows, columns=colnames)
        df.to_excel(excel_file, index=False)
        print(f"Data successfully written to {excel_file}")



def result2():
    conn = connection()
    with conn.cursor() as cursor:
        query = f'''SELECT posts.id, posts.posted_at, 
                    posts.comments_count, gr.name 
                    FROM posts
                    LEFT JOIN vk_group gr ON gr.id = posts.group_id'''
        cursor.execute(query)
        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        excel_file = 'results2.xlsx'
        df = pd.DataFrame(rows, columns=colnames)
        df.to_excel(excel_file, index=False)
        print(f"Data successfully written to {excel_file}")

