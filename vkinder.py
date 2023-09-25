
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
                    page_link VARCHAR(70) UNIQUE NOT NULL,
                    favourites BOOLEAN);

        CREATE TABLE IF NOT EXISTS photos (
                    photo_id SERIAL PRIMARY KEY,
                    human_id INTEGER NOT NULL REFERENCES people(human_id),
                    photo_data VARCHAR(70) NOT NULL);''')
    
        conn.commit()
    conn.close()


def add_user(name: str, surname: str)-> None :
   '''Функция добавляет данные пользователя в таблицу tinder_user'''
   conn = psycopg2.connect(host = 'localhost', database = 'vk_tinder', user = 'postgres', password = your_password)
   with conn.cursor() as cur :


    cur.execute('''INSERT INTO tinder_user(user_name, user_surname)
                        VALUES (%s, %s);''', (name, surname))

    print('В таблицу tinder_user добавлен пользователь: ', name, surname)
    conn.commit()
   conn.close()


def add_people_photos(user_id: int, human_name: str, human_surname: str, page_link: str, photos_list: list)-> None :
    '''Функция добавляет данные пользователя в таблицу people и добавляет его фотографии в таблицу photos.
    Функция принимает на вход 5 аргументов :
    user_id: тип - int(), ай-ди пользователя который осуществляет поиск (поидее всегда равен = 1, т.к. после смены пользователя нужно очищать данные таблиц),
    human_name: тип str(), имя человека страницу которого открыля для просмотра, 
    human_surname: тип str(), фамилия человека страницу которого открыля для просмотра,
    page_link: тип str(), ссылка на страницу которую открыли для просмотра,
    photos_list: тип list(), список с фотографиями этого человека '''
    conn = psycopg2.connect(host = 'localhost', database = 'vk_tinder', user = 'postgres', password = your_password)
    
    # заполнение данных таблицы people
    with conn.cursor() as cur :

        cur.execute('''INSERT INTO people(user_id, human_name, human_surname, page_link)
                            VALUES (%s, %s, %s, %s);''', (user_id, human_name,  human_surname, page_link))

        print('В таблицу people добавлен пользователь: ', human_name, human_surname)
    
    # получаем id для таблицы photos
    with conn.cursor() as cur :
        cur.execute('''SELECT human_id
                        FROM people
                       WHERE human_name = %s AND human_surname = %s;''', (human_name, human_surname))
        res = cur.fetchone()
        id_human  = res[0]

    # заполнение данных таблицы photos
    with conn.cursor() as cur :
        for one_photo in photos_list :
            cur.execute('''INSERT INTO photos(human_id, photo_data)
                            VALUES (%s, %s);''', (id_human, one_photo))

    print('В таблицу photos добавлен фотграфии для пользователя: ', human_name, human_surname)

    conn.commit()
    conn.close()

def clean_tables()-> None :
    '''Функция удаляет все данные из таблиц photos, people, tinder_user'''
    conn = psycopg2.connect(host='localhost', database='vk_tinder', user='postgres', password= your_password)
    with conn.cursor() as cur :
        cur.execute('''DELETE FROM photos; 
                       DELETE FROM people;
                       DELETE FROM tinder_user;''')

        conn.commit()
    cur.close()




'''данные для проверки работы функций'''

# создаем таблицы 
# create_tables()

# вносим данные пользователя
# add_user(name='andrey', surname='andreev')

# вносим данные людей
# add_people_photos(1, 'sergey', 'badrov', 'ewq@37743', ['dasdasddads_1', 'sadasdsadasdasd_2', 'dsadasdasasdas_3'])
# print()
# add_people_photos(1, 'ira', 'belova', 'belova@37743', ['dadasddads_2', 'sadasdsadasdasd_2', 'dsadasdasasdas_2'])
# print()
# add_people_photos(1, 'lida', 'kirova', 'kirova@3743', ['dasdasddads_3', 'sadasdsadasdasd_3', 'dsadasdasasdas_3'])


# очищаем таблицы
# clean_tables()
    