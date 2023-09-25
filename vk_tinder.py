
'''Данный модуль создает три таблицы photos, people, tinder_user.
Для создания таблиц необходимо :
- создать базу данных с именем vk_tinder
- установить psycopg2
- в переменную your_password записать свой пароль от postgres
- вызвать функцию create_tables() (раскоментировать её)'''

import psycopg2

your_password = 'maxim12345'



def create_tables() :
    conn = psycopg2.connect(host='localhost', database='vk_tinder', user='postgres', password= your_password)

    '''функция создает три таблицы. Перед этим удаляет ранее созданные'''
    with conn.cursor() as cur :

        cur.execute('''
        DROP TABLE IF EXISTS photos, people, tinder_user; 
        
        CREATE TABLE tinder_user (
                    user_id SERIAL PRIMARY KEY, 
                    user_name VARCHAR(30) NOT NULL, 
                    user_surname VARCHAR(30) NOT NULL);
                     
        CREATE TABLE people (
                    human_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES tinder_user(user_id),
                    human_name VARCHAR(30) NOT NULL,
                    human_surname VARCHAR(30) NOT NULL,
                    page_link VARCHAR(70) NOT NULL,
                    favourites BOOLEAN);

        CREATE TABLE IF NOT EXISTS photos (
                    photo_id SERIAL PRIMARY KEY,
                    human_id INTEGER NOT NULL REFERENCES people(human_id),
                    photo_data VARCHAR(70) NOT NULL);''')
    
        conn.commit()
    conn.close()

# create_tables()


                    




    