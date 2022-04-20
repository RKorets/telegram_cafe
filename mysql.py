import pymysql
import os
from config import host, user, password, db_name


class DBConnect:

    def connect(self):
        try:
            print("Connect in db")
            self.connection = pymysql.connect(
                host=host,
                port=8888,
                user=user,
                unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            return self.connection
        except Exception as ex:
            print(f"Connection refused....{ex}")

    def product_id(self, product_name: str):
        self.product_id = []
        with self.connect().cursor() as cursor:
            self.import_table_data = "SELECT ProductID" \
                                  f" FROM Product WHERE ProductName = '{product_name}'"
            cursor.execute(self.import_table_data)
            for el in cursor:
                self.product_id.append(el["ProductID"])
        return self.product_id

    def product_hot(self):
        self.product = []
        with self.connect().cursor() as cursor:
            self.import_product = "SELECT ProductName,ProductLS,ProductPrice" \
                                  " FROM Product WHERE ProductLS LIKE 'hot_%'"
            cursor.execute(self.import_product)
            for el in cursor:
                self.product.append((el["ProductName"], el["ProductLS"], el["ProductPrice"]))
        return self.product

    def product_ice(self):
        self.product = []
        with self.connect().cursor() as cursor:
            self.import_product = "SELECT ProductName,ProductLS,ProductPrice" \
                                  " FROM Product WHERE ProductLS LIKE 'ice_%'"
            cursor.execute(self.import_product)
            for el in cursor:
                self.product.append((el["ProductName"], el["ProductLS"], el["ProductPrice"]))
        return self.product

    def product_taste(self):
        self.product = []
        with self.connect().cursor() as cursor:
            self.import_product = "SELECT ProductName,ProductLS,ProductPrice" \
                                  " FROM Product WHERE ProductLS LIKE 'taste_%'"
            cursor.execute(self.import_product)
            for el in cursor:
                self.product.append((el["ProductName"], el["ProductLS"], el["ProductPrice"]))
        return self.product

    def take_product_info(self, product_ls: str):
        self.product_info = []
        with self.connect().cursor() as cursor:
            self.import_product = "SELECT *" \
                                  f" FROM Product WHERE ProductLS = '{product_ls}'"
            cursor.execute(self.import_product)
            for el in cursor:
                self.product_info.append(el["ProductID"])
                self.product_info.append(el["ProductName"])
                self.product_info.append(el["ProductLS"])
                self.product_info.append(el["ProductPrice"])
        return self.product_info

    def create_order(self, order_number: int, customer_id: int):
        conn = self.connect()

        conn.cursor().execute("INSERT INTO Orders(OrderID, CustomerID)" \
                              f" VALUES ({order_number},{customer_id})")
        conn.commit()
        print("Succesful")


    def create_product_in_order(self,order_number: int, product_id: int):
        pass


if __name__ == "__main__":
    d = DBConnect()
    print(d.people())
