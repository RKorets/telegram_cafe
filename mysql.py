import pymysql
import os
from config import host, user, password, db_name


class DBConnect:

    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=host,
                port=8888,
                user=user,
                unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as ex:
            print(f"Connection refused....{ex}")

    def customers(self):
        self.name = []
        with self.connection.cursor() as cursor:
            self.import_table_data = "SELECT id,name,email,bio FROM peope WHERE id<12"
            cursor.execute(self.import_table_data)
            for i in cursor:
                self.name.append((i["id"],i["name"],i["email"]))
        return self.name

def tableName():
    try:
        connection = pymysql.connect(
            host=host,
            port=8888,
            user=user,
            unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connecting succesful")
        name = []

        try:
            with connection.cursor() as cursor:
                import_table_data = "SELECT id,name,email,bio FROM peope WHERE id<12"
                cursor.execute(import_table_data)

                for i in cursor:
                    name.append(i["name"])
        finally:
            connection.close()
    except Exception as ex:
        print(f"Connection refused....{ex}")
    return name


if __name__ == "__main__":
    d = DBConnect()
    print(d.people())