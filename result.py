import pandas as pd
from DBconn import connection, disconnect

def result1():
    conn = connection()
    with conn.cursor() as cursor:
        query = f'''SELECT DISTINCT city, gr.name,
                    gr.name || ' ' || gr.addres as info, 
                    cat.name, 
                    COUNT(post_id) OVER (PARTITION BY city, gr.name, gr.addres, cat.name), 
                    posts.addres  
                    FROM posts
                    LEFT JOIN category cat ON cat.post_id = posts.id
                    LEFT JOIN smgroups gr ON gr.id = posts.group_id
                    WHERE comments_count>=200 
					AND posted_at BETWEEN '2024-01-01' AND '2025-01-01' 
                    '''
        cursor.execute(query)
        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        excel_file = 'results.xlsx'
        df = pd.DataFrame(rows, columns=colnames)
        df.to_excel(excel_file, index=False)
        print(f"Data successfully written to {excel_file}")
    disconnect(conn)



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
    disconnect(conn)
