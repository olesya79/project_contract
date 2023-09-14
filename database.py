import sqlite3


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor() # Подключаемся к базе данных

    def create_contract(self, contract):
        query = "INSERT INTO contracts (name, created_date, status) VALUES (?, ?, ?)" # Запрос к базе данных
        values = (contract.name, contract.created_date, contract.status)
        self.cursor.execute(query, values)
        self.connection.commit()


    def create_project(self, project):
        query = "INSERT INTO projects (name, created_date) VALUES (?, ?)" # Запрос к базе данных
        values = (project.name, project.created_date)
        self.cursor.execute(query, values)
        self.connection.commit()







