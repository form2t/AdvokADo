import mysql.connector
from mysql.connector import Error
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read("config.ini")
HOST = config['Telegram']['HOST']
DB = config['Telegram']['DB']
user_DB = config['Telegram']['user_DB']
psw_DB = config['Telegram']['psw_DB']


class DataBase:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host=HOST, database=DB, user=user_DB, password=psw_DB)
            self.cursor = self.conn.cursor()
            print("DataBase is connect")
        except Error as error:
            print("Error while connecting to database", error)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def create_table(self, table):
        if table == "users":
            # id INT AUTO_INCREMENT PRIMARY KEY,
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users ("
                                "ID INT(11) NOT NULL AUTO_INCREMENT, "
                                "UserID INT(45) NOT NULL, "
                                "userName VARCHAR(100) NULL, "
                                "userFromChart INT(45) NULL, "
                                "pingToBattle INT(1) NOT NULL DEFAULT '0'"
                                "PRIMARY KEY (`ID`), "
                                "ADD UNIQUE KEY `ID_UNIQUE` (`ID`) "
                                "ADD UNIQUE KEY `UserID` (`UserID`)) ENGINE=InnoDB DEFAULT CHARSET=utf8")

    def __insert_data__(self, table_name, data, add_txt=''):
        data.insert(0, 'DEFAULT')
        data.insert(len(data), 'DEFAULT')
        query = "INSERT INTO %s VALUES %r %s;" % (table_name, tuple(data), add_txt)

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as error:
            self.conn.rollback()
            print("don't  insert_data")

    def select_data_pin_battle(self):
        query = "SELECT userFromChart, userName FROM users WHERE pingToBattle = 1"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            self.conn.rollback()
            print("don't select_data_pin_battle")

    def select_data_fight_ambush(self, data):
        query = f'SELECT userFromChart, userName FROM fightAmbush where idUser = {data[0]!r} and idMessage = {data[1]!r}'

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_data_fight_ambush")

    def update_data_user(self, data, key='userName'):
        add_txt = ' ON DUPLICATE KEY UPDATE userName = %r' % (data[1])
        self.__insert_data__('users', data, add_txt)

    def insert_data_ambush(self, data):
        data.insert(0, 'DEFAULT')
        query = "INSERT INTO fightAmbush VALUES {0}".format(tuple(data))
        # [msg.message.message_id, msg.from_user.id, msg.from_user.username, msg.message.chat.id]

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as error:
            self.conn.rollback()
            print("don't insert_data_ambush")

    def select_user_fight_ambush(self, data):
        query = f'SELECT userName FROM fightAmbush where idMessage = {data}'

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_data_fight_ambush")

    def select_count_data_fight_ambush(self, data):
        query = f'SELECT count(*) FROM fightAmbush WHERE idMessage = {data}'

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_count_data_fight_ambush")

    def add_trigger(self, data):
        data.insert(0, 'DEFAULT')
        data[-1] = str(datetime.utcfromtimestamp(data[-1]))
        query = f"INSERT INTO triggers VALUES {tuple(data)!r}"
        # [msg.message.message_id, msg.from_user.id, msg.from_user.username, msg.message.chat.id]

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as error:
            self.conn.rollback()
            print("don't add_trigger")

    def delete_trigger(self, trigger_name, chart_id):
        query = f'DELETE FROM triggers WHERE triggerName = {trigger_name!r} and ' \
                f'userFromChart = {chart_id!r}'
        # [msg.message.message_id, msg.from_user.id, msg.from_user.username, msg.message.chat.id]

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as error:
            self.conn.rollback()
            print("don't delete_trigger")

    def is_trigger(self, trigger_name, chart_id):
        query = f'SELECT triggerType, triggerValue FROM triggers WHERE triggerName = {trigger_name!r} and ' \
                f'userFromChart = {chart_id!r}'
        print(query)
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't is_trigger" + str(Error))

    def get_trigger_list(self, chart_id):
        query = f'SELECT triggerName FROM triggers WHERE userFromChart = {chart_id!r}'

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't get_trigger_list" + str(Error))

    # [message.message_id, message.forward_date, message.from_user.id, message.from_user.username,
    # message.chat.id, exp, gold, stock, hp, last_hit, dateAdded]
    def select_data_fight_ambush_result(self, data):

        data[1] = str(datetime.utcfromtimestamp(data[1]))
        query = f'SELECT userFromChart, userName FROM fightAmbushResult where dateMessage = {data[1]!r} and ' \
                f'idUser = {data[2]!r} and exp = {data[5]!r} and gold = {data[6]!r} '
        # print(query)
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_data_fight_ambush_result")

    def insert_data_fight_ambush_result(self, data):
        data.insert(0, 'DEFAULT')
        # data[2] = str(datetime.utcfromtimestamp(data[1]))
        data[-1] = str(datetime.utcfromtimestamp(data[-1]))

        # print(data)
        query = "INSERT INTO fightAmbushResult VALUES {0}".format(tuple(data))
        # print(query)
        # [msg.message.message_id, msg.from_user.id, msg.from_user.username, msg.message.chat.id]

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as error:
            self.conn.rollback()
            print("don't insert_data_fight_ambush_result")

    def select_get_me(self, data):
        query = f'SELECT count(exp), sum(exp), sum(gold), sum(stock), sum(hp), sum(lastHit), sum(knockout) ' \
                f'FROM fightAmbushResult where idUser = {data[0]!r} group by idUser'

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_get_me")

    def select_get_all(self):
        query = 'SELECT  count(exp), sum(exp), sum(gold), sum(stock), sum(hp), sum(lastHit), sum(knockout), userName ' \
                'FROM fightAmbushResult group by idUser order by sum(lastHit) DESC'

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_get_all")

    def select_top_count_battle(self, value):
        query = f"SELECT  count(exp), userName FROM fightAmbushResult group by idUser order by count(exp) " \
                f"DESC limit {value!r}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_top_count_battle")

    def select_top_exp(self, value):
        query = f"SELECT  sum(exp), userName FROM fightAmbushResult group by idUser order by sum(exp) " \
                f"DESC limit {value!r}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_top_exp")

    def select_top_gold(self, value):
        query = f"SELECT  sum(gold), userName FROM fightAmbushResult group by idUser order by sum(gold) " \
                f"DESC limit {value!r}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_top_gold")

    def select_top_stock(self, value):
        query = f"SELECT  sum(stock), userName FROM fightAmbushResult group by idUser order by sum(stock) " \
                f"DESC limit {value!r}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_top_stock")

    def select_top_hp(self, value):
        query = f"SELECT  sum(hp), userName FROM fightAmbushResult group by idUser order by sum(hp) " \
                f"ASC limit {value!r}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_top_hp")

    def select_top_last_hit(self, value):
        query = f"SELECT  sum(lastHit), userName FROM fightAmbushResult group by idUser order by sum(lastHit) " \
                f"DESC limit {value!r}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_top_last_hit")

    def select_top_knockout(self, value):
        query = f"SELECT  sum(knockout), userName FROM fightAmbushResult group by idUser order by sum(knockout) " \
                f"DESC limit {value!r}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't select_top_last_hit")