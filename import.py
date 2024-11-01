import psycopg2

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

cursor = conn.cursor()
cursor.execute("SELECT * FROM products")
records = cursor.fetchall()
for row in records:
    print(row)
