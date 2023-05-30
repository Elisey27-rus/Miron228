import sqlite3


#Получаем имя пользователя в ДБ
def get_users_name_from_users_id(user_id):
    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()

        sql = f"""
        SELECT user_name 
        FROM users 
        WHERE user_id={user_id}
        """

        users_name = cursor.execute(sql).fetchone()[0]
    return users_name
#================================================================
