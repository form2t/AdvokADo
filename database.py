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

        #data.insert(len(data), )
        #data.insert(len(data), 'CURRENT_TIMESTAMP')
        #query = "INSERT INTO triggers VALUES {0}".format(tuple(data))
        query = f"INSERT INTO triggers VALUES {tuple(data)!r}"
        # [msg.message.message_id, msg.from_user.id, msg.from_user.username, msg.message.chat.id]

        print(query)
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as error:
            self.conn.rollback()
            print("don't add_trigger")

    def is_trigger(self, data):
        query = f'SELECT * FROM triggers WHERE triggerName = {data!r}'

        print(query)
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as error:
            print("don't is_trigger" + str(Error))
