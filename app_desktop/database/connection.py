import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sikost_kelompok3"
            )
            self.cursor = self.conn.cursor(dictionary=True, buffered=True)
        except Error as e:
            print(f"Koneksi gagal: {e}")

    def execute(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except Error as e:
            print(f"Query gagal: {e}")
            raise

    def fetchall(self):
        try:
            return self.cursor.fetchall()
        except Error as e:
            print(f"Fetchall gagal: {e}")
            return []

    def fetchone(self):
        try:
            return self.cursor.fetchone()
        except Error as e:
            print(f"Fetchone gagal: {e}")
            return None

    def commit(self):
        try:
            self.conn.commit()
        except Error as e:
            print(f"Commit gagal: {e}")

    def rollback(self):
        try:
            self.conn.rollback()
        except Error as e:
            print(f"Rollback gagal: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
