import mysql.connector
import mysqlx.errorcode as err_code
from .booleanconverter import boolean_converter


class ServoMySQL:

    def __init__(self):
        self.config = {
            'user': 'root',
            'passwd': 'root',
            'host': 'host.docker.internal',
            'db': 'servo',
            'port': '3306'
        }

    def init(self):
        try:
            cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as E:
            if E.errno == err_code.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif E.errno == err_code.ER_BAD_DB_ERROR:
                return "Database does not exist"
            else:
                return E
        else:
            cnx.close()
            return "Succ"

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
            cursor.execute("CREATE TABLE `settings` ("
                           "    `name` VARCHAR(32),    "
                           "    `value` VARCHAR(32),    "
                           "    `boolean` INT(1))  ")
        except mysql.connector.Error as E:
            if E.errno == err_code.ER_TABLE_EXISTS_ERROR:
                return 'Already exist'
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
            data = None
            settings_data = [
                {'name': 'covid_time', 'value': 1636945200, 'boolean': data},
                {'name': 'streaming_status_text', 'value': 'MYSQL-POWER!', 'boolean': data},
                {'name': 'role_rainbow', 'value': 'Rainbow', 'boolean': data},
                {'name': 'role_rainbow_status', 'value': data, 'boolean': 0},
                {'name': 'kgb_mode', 'value': data, 'boolean': 0}]
            for i in settings_data:
                cursor.execute(settings, i)
        except mysql.connector.Error as E:
            return E
        else:
            return 'Done! Settings has been filled!'
        finally:
            cnx.commit()
            cursor.close()
            cnx.close()

    def remove(self):
        pass
        return data

    def update_setting(self, name, value):
        value = boolean_converter(value)
        try:
            with mysql.connector.Connect(**self.config) as cnx:
                with cnx.cursor() as cursor:
                    if isinstance(value, str):
                        cursor.execute(f'UPDATE settings SET settings.value = "{value}" WHERE name = "{name}"')
                        cnx.commit()
                        return f'Done! Value {value} Inserted into {name}'
                    elif isinstance(value, bool):
                        cursor.execute(f'UPDATE settings SET settings.boolean = "{value}" WHERE name = "{name}"')
                        cnx.commit()
                        return f'Done! Value {value} Inserted into {name}'

        except Exception as E:
            return E
