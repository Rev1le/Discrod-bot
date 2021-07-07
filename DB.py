import sqlite3

class DiscordIdDataBase:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                id_discord_user BIGINT PRIMARY KEY,
                name_user TEXT,
                total_messages INT,
                cash FLOAT)""")
        self.conn.commit()

    # Принимает массив в элементами [id_discord_user, user_name, total_message, total_cash]
    # ID человека в дисскорде, его имя в дисскорде, его количество сообщений, его деньги
    # Возвращает True или False
    def add_user(self, inf):
        def add():
            self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?)", inf)
            self.conn.commit()
            print('ID добавлен!')

        self.cur.execute("SELECT id_discord_user FROM users")
        id_discord_user_list = self.cur.fetchall()
        if id_discord_user_list:
            id_problem = False
            for user_id in id_discord_user_list:
                if user_id[0] == inf[0]:
                    id_problem = True
                    break
            if id_problem:
                print("Такой discord id уже есть в таблице!")
                return False
            else:
                add()
                return True
        else:
            add()
            return True

    # Принимает ID человека в дисскорде
    # Возвращает массив с информацией о человеке в формате [id, name, messages, cash]
    def get_info_on_id(self, id_discord):
        self.cur.execute(
            f"SELECT * FROM users WHERE id_discord_user={id_discord}")
        user_inf = self.cur.fetchone()  # [(),(),(),()]
        return user_inf

    # Принимает ID человека, изменяемый столбец и прибовляемое число (изначально +1)
    # Возвращает True или False
    def increase_column(self, id_discord, mode, increase=1):
        if not self.get_info_on_id(id_discord):
            print('Ошибка ввода ID Дискорда! Такого id нет!')
            return False

        if mode == 'total_messages':
            if isinstance(increase, int):
                self.cur.execute(
                    f"SELECT total_messages FROM users WHERE id_discord_user={id_discord}")
                old_total_messages = self.cur.fetchone()[0]
                self.cur.execute(
                    f"UPDATE users SET total_messages={old_total_messages + increase} WHERE id_discord_user={id_discord}")
                self.conn.commit()
                return True
            else:
                print('Ошибка ввода числа увеличения! Число не целое!')
                return False

        elif mode == 'cash':
            self.cur.execute(
                f"SELECT cash FROM users WHERE id_discord_user={id_discord}")
            old_cash = self.cur.fetchone()[0]
            self.cur.execute(
                f"UPDATE users SET cash={old_cash + increase} WHERE id_discord_user={id_discord}")
            self.conn.commit()
            return True
        else:
            print('Неверный ввод изменяемого столбца!')
            return False