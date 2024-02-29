import sqlite3
import random

db = sqlite3.connect("server.db")
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT, password TEXT, balance BIGINT
)""")

db.commit()
while True:

    def registration():
        new_user_login = input("Login =>").capitalize()
        new_user_password = input("Password =>")
        cur.execute(f"SELECT login FROM users WHERE login = '{new_user_login}'")
        if cur.fetchone() is None:
            cur.execute("INSERT INTO users VALUES (?, ?, ?)", (new_user_login, new_user_password, 0))
            db.commit()
            print("Вы успешно зарегистрированы")
        else:
            print(f"Пользователь с логином {new_user_login} уже существует")


    def game_num():
        deal = random.randint(1, 3)
        print("Добро пожаловать в игру 'Угадай число', здесь вам нужно угадать число от 1 до 3")
        answ_player = int(input("Введите число от 1 до 3\n"
                                "=>"))
        print(deal)
        if deal == answ_player:
            print("Поздравляю вы победили!")
        else:
            print("К сожалению вы проиграли. В следующий раз повезет")
        answ_player = input("Желаете сыиграть еще один раз?\n"
                            "1 - Да\n"
                            "2 - Нет\n"
                            "Введите ответ =>")
        if answ_player == "1":
            game_num()
        elif answ_player == "2":
            pass
        else:
            print("Нет такого ответа")
            play_casino()


    def game_slots(user):
        bet = int(input("Введите ставку =>"))
        cur.execute(f"UPDATE users SET balance = {1000 - bet} WHERE login = '{user}'")
        db.commit()
        emoji = ["🍎", "🍌", "🍒"]
        slot_1 = random.choice(emoji)
        slot_2 = random.choice(emoji)
        slot_3 = random.choice(emoji)
        print(slot_1, slot_2, slot_3)
        if slot_1 == slot_2 == slot_3:
            print("Поздравляю вы победили!")
            cur.execute(f"UPDATE users SET balance = {bet * 3} WHERE login = '{user}'")
            cur.execute(f"SELECT balance FROM users WHERE login = '{user}'")
            print(cur.fetchone())
            db.commit()
        else:
            print("К сожалению вы проиграли. В следующий раз повезет")
        answ_player = input("Желаете сыиграть еще один раз?\n"
                            "1 - Да\n"
                            "2 - Нет\n"
                            "Введите ответ =>")
        if answ_player == "1":
            game_slots(user)
        elif answ_player == "2":
            pass
        else:
            print("Нет такого ответа")
            play_casino()


    def play_casino():
        print("Добро пожаловать в казино. Для начала войдите в аккаунт или зарегистрируйтесь")
        user_login = input("Login =>").capitalize()
        user_password = input("Password =>")
        cur.execute(f"SELECT login, password FROM users WHERE login = '{user_login}' AND password = '{user_password}'")
        if cur.fetchone() is None:
            print("Такого пользователя не найдено. Желаете пройти регистрацию?")
            answ = input("1 - Да\n"
                         "2 - Нет\n"
                         "Введите ответ =>")
            if answ == "1":
                registration()
            elif answ == "2":
                pass
            else:
                print("Нет такого ответа")
                play_casino()
        else:
            cur.execute(f"UPDATE users SET balance = {1000} WHERE login = '{user_login}'")
            db.commit()
            cur.execute(f"SELECT balance FROM users WHERE login = '{user_login}'")
            print(f"На вашем балансе = {cur.fetchone()}")
            print("В какую игру хотите сыграть?")
            answ = input("1 - угадай число\n"
                         "2 - слоты\n"
                         "Введите ответ =>")
            if answ == "1":
                game_num()
            elif answ == "2":
                game_slots(user_login)
            else:
                print("Нет такого ответа")
                play_casino()


    play_casino()
