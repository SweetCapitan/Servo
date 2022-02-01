import os

import mysql.connector
import mysqlx.errorcode as err_code
from .booleanconverter import boolean_converter


class ServoMySQL:

    def __init__(self):
        self.config = {
            'user': f'{os.environ.get("DATABASE_USER")}',
            'passwd': f'{os.environ.get("DATABASE_PASSWORD")}',
            'host': 'host.docker.internal',
            'db': 'servo',
            'port': '3306'
        }

    def get_setting(self, name, **boolean):
        cnx = mysql.connector.Connect(**self.config)
        cursor = cnx.cursor()
        try:
            if boolean:
                cursor.execute(f"SELECT boolean FROM settings WHERE name = '{name}'")
                for boolean in cursor:
                    return boolean_converter(boolean[0])
            elif not boolean:
                cursor.execute(f'SELECT value FROM settings WHERE name = "{name}"')
                for value in cursor:
                    return value[0]
        except mysql.connector.Error as E:
            return E
        finally:
            cursor.close()
            cnx.close()

    def create_table_setting(self):
        cnx = mysql.connector.Connect(**self.config)
        cursor = cnx.cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS `settings` ("
                           "    `name` VARCHAR(32),    "
                           "    `value` VARCHAR(32),    "
                           "    `boolean` INT(1))  ")
        except mysql.connector.Error as E:
            if E.errno == err_code.ER_TABLE_EXISTS_ERROR:
                return 'Table already exist'
            else:
                return E
        else:
            return 'Done! Table created.'
        finally:
            cursor.close()
            cnx.close()

    def fill_settings(self):
        cnx = mysql.connector.connect(**self.config)
        cursor = cnx.cursor()
        try:
            settings = ("INSERT INTO settings "
                        "(name, value, boolean)"
                        "VALUES (%(name)s, %(value)s, %(boolean)s)")
            null = None
            settings_data = [
                {'name': 'covid_time', 'value': 1643703600, 'boolean': null},
                {'name': 'streaming_status_text', 'value': 'MYSQL-POWER!', 'boolean': null},
                {'name': 'role_rainbow', 'value': 'Rainbow', 'boolean': null},
                {'name': 'role_rainbow_status', 'value': null, 'boolean': 0},
                {'name': 'kgb_mode', 'value': null, 'boolean': 0}]
            '''
            
            Это список настроек необходимых для стабильной работы бота, добавьте сюда массив, если необходимо добавить 
            новую настройку {'name': 'имя параметра', 'value' 'его значение': , 'boolean': 0 or 1}. Если необходимо 
            оставить поле пустым, то укажите None или null. 
            
            '''
            for i in settings_data:
                cursor.execute(settings, i)
        except mysql.connector.Error as E:
            return E
        else:
            print('Done! Settings has been filled!')
        finally:
            cnx.commit()
            cursor.close()
            cnx.close()

    def remove(self):
        pass  # Зарезервированно до востребованности

    def update_setting(self, name, value):
        if not isinstance(value, int):
            value = boolean_converter(value)
        try:
            with mysql.connector.Connect(**self.config) as cnx:
                with cnx.cursor() as cursor:
                    if isinstance(value, (str, int)):
                        cursor.execute(f'UPDATE settings SET settings.value = "{value}" WHERE name = "{name}"')
                        cnx.commit()
                        return f'Done! Value {value} Inserted into {name}'
                    elif isinstance(value, bool):
                        cursor.execute(f'UPDATE settings SET settings.boolean = "{value}" WHERE name = "{name}"')
                        cnx.commit()
                        return f'Done! Value {value} Inserted into {name}'

        except Exception as E:
            return E

    def init(self):

        self.create_table_setting()
        try:
            with mysql.connector.Connect(**self.config) as cnx:
                with cnx.cursor(buffered=True) as cursor:

                    cursor.execute('SELECT * FROM settings')
                    if cursor.rowcount == 0:
                        self.fill_settings()
                        return 'Migration successfully completed'
                    else:
                        return "DB already exist"

        except Exception as E:
            return f'Error: {E}'
