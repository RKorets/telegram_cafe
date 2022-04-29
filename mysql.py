import pymysql
import os
import datetime
from config import host, user, password, db_name


class DBConnect:

    @property
    def connect(self):
        try:
            print("Connect in db")
            connection = pymysql.connect(
                host=host,
                port=8888,
                user=user,
                unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except Exception as ex:
            print(f"Connection refused....{ex}")

    def product_id(self, product_name: str):
        product = []
        with self.connect.cursor() as cursor:
            import_table_data = "SELECT ProductID" \
                                  f" FROM Product WHERE ProductName = '{product_name}'"
            cursor.execute(import_table_data)
            for el in cursor:
                product.append(el["ProductID"])
        return str(product[0])

    def product_hot(self):
        product = []
        with self.connect.cursor() as cursor:
            import_product = "SELECT ProductName,ProductLS,ProductPrice" \
                                  " FROM Product WHERE ProductLS LIKE 'hot_%'"
            cursor.execute(import_product)
            for el in cursor:
                product.append((el["ProductName"], el["ProductLS"], el["ProductPrice"]))
        return product

    def product_ice(self):
        product = []
        with self.connect.cursor() as cursor:
            import_product = "SELECT ProductName,ProductLS,ProductPrice" \
                                  " FROM Product WHERE ProductLS LIKE 'ice_%'"
            cursor.execute(import_product)
            for el in cursor:
                product.append((el["ProductName"], el["ProductLS"], el["ProductPrice"]))
        return product

    def product_taste(self):
        product = []
        with self.connect.cursor() as cursor:
            import_product = "SELECT ProductName,ProductLS,ProductPrice" \
                                  " FROM Product WHERE ProductLS LIKE 'taste_%'"
            cursor.execute(import_product)
            for el in cursor:
                product.append((el["ProductName"], el["ProductLS"], el["ProductPrice"]))
        return product

    def take_product_info(self, product_ls: str):
        product_info = []
        with self.connect.cursor() as cursor:
            import_product = "SELECT *" \
                                  f" FROM Product WHERE ProductLS = '{product_ls}'"
            cursor.execute(import_product)
            for el in cursor:
                product_info.append(el["ProductID"])
                product_info.append(el["ProductName"])
                product_info.append(el["ProductLS"])
                product_info.append(el["ProductPrice"])
        return product_info

    def create_customers(self, info: dict):
        conn = self.connect
        with conn.cursor() as cursor:
            import_product = "SELECT CustomerID" \
                                  f" FROM Customers WHERE CustomerID = {info['id']}"
            cursor.execute(import_product)
            if len(cursor.fetchall()) == 0:
                conn.cursor().execute("INSERT INTO Customers (CustomerID, CustomerFirstName,CustomerLastName,CustomerUsername)" \
                                      f" VALUES ({info['id']},'{info['first_name']}','{info['last_name']}','{info['username']}')")
                conn.commit()

    def create_order(self, order_number: str, customer_id: int):
        conn = self.connect
        conn.cursor().execute("INSERT INTO Orders(OrderID, CustomerID)" \
                              f" VALUES ('{order_number}',{customer_id})")
        conn.commit()
        print(f"New order customers {customer_id}")

    def create_product_in_order(self, order_number: int, product_id: int):
        conn = self.connect
        conn.cursor().execute("INSERT INTO ProductInOrder(OrderID, ProductID)" \
                              f" VALUES ({order_number},{product_id})")
        conn.commit()
        print(f"Add from {order_number} productId {product_id}")

    def create_reviews(self, customer_id: int, reviews_text: str):
        conn = self.connect
        conn.cursor().execute("INSERT INTO Reviews(CustomerID, ReviewsText)" \
                              f" VALUES ({customer_id},'{reviews_text}')")
        conn.commit()
        print(f"Add 1 new reviews")

    def admin(self, admin_id: int):
        with self.connect.cursor() as cursor:
            import_product = "SELECT FullName" \
                                  f" FROM Admin WHERE TelegramID = {admin_id}"
            cursor.execute(import_product)
            if len(cursor.fetchall()) == 0:
                return False
            else:
                return True

    def take_new_orders(self) -> list:
        order_id = []
        with self.connect.cursor() as cursor:
            import_product = "SELECT OrderID" \
                                  f" FROM Orders WHERE OrderStatus = 'new'"
            cursor.execute(import_product)
            for el in cursor:
                order_id.append(el["OrderID"])
        return order_id

    def take_order_info(self, order):
        product_info = []
        with self.connect.cursor() as cursor:
            import_product = "SELECT Orders.OrderID, Product.ProductName, ProductPrice, Customers.CustomerID FROM ProductInOrder "\
                                    " JOIN Product ON ProductInOrder.ProductID = Product.ProductID "\
                                    " JOIN Orders ON ProductInOrder.OrderID = Orders.OrderID "\
                                    " JOIN Customers ON Customers.CustomerID = Orders.CustomerID "\
                                    f" WHERE Orders.OrderID = {order}"
            cursor.execute(import_product)
            for el in cursor:
                product_info.append((el["ProductName"], el["ProductPrice"], el["CustomerID"], el["OrderID"]))
        return product_info  #список всіх замовлень з статусом new

    def edit_status(self, order_number: int, status: str):
        conn = self.connect
        conn.cursor().execute("UPDATE `Orders` SET "  
                             f"`OrderStatus`= '{status}' WHERE `OrderID` = {order_number}")
        conn.commit()
        print(f"Status edit")

    def take_user_id(self, order_id: int):
        product_info = []
        with self.connect.cursor() as cursor:
            import_product = "SELECT CustomerID FROM Orders " \
                                      f" WHERE OrderID = {order_id}"
            cursor.execute(import_product)
            for el in cursor:
                product_info.append(el["CustomerID"])
        return product_info[0]

    def take_statistics(self):
        product_info = []
        with self.connect.cursor() as cursor:
            import_product = "SELECT OrderID FROM Orders " \
                                     f"WHERE DATEDIFF(OrderDate, CURRENT_TIMESTAMP) = 0 AND OrderStatus = 'confirm'"
            cursor.execute(import_product)
            for el in cursor:
                product_info.append(el["OrderID"])
        return product_info


#
# if __name__ == "__main__":
#     d = DBConnect()
