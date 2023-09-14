import sqlite3 as sq
from datetime import date

from database import Database
from entities import Contract
from entities import Project

database = Database('cont_proj.db')
with sq.connect('cont_proj.db') as con:  # Подключаемся к базе данных
    cur = con.cursor()

contracts = []
projects = []


def main_menu():
    print("Добро пожаловать в приложение 'Система проектов и договоров'!")
    while True:
        print("Выберите действие:")
        print("1. Создать новый договор")
        print("2. Создать новый проект")
        print("3. Просмотреть список договоров")
        print("4. Просмотреть список проектов")
        print("0. Выйти")

        choice = input("Введите номер пункта меню: ")

        if choice == "1":
            create_contract() # Вызов функции для создания договора
        elif choice == "2":
            create_project()  # Вызов функции для создания проекта
        elif choice == "3":
            get_contracts()  # Вызов функции для получения списка договоров
        elif choice == "4":
            get_projects()   # Вызов функции для получения списка проектов
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неправильный выбор. Попробуйте еще раз.")


def create_contract(): # Функция для создания договора
    print("Создание нового договора")
    name = input("Введите название договора: ")

    contract = {"name": name}
    contract = Contract(name)
    database.create_contract(contract)

    contracts.append(contract)
    print("Договор успешно создан!")

    contract_menu(contract)


def contract_menu(contract): # Меню для действий с  договорами
    while True:
        print("Выберите действие:")
        print("1. Подтвердить договор")
        print("2. Завершить договор")
        print("3. Вернуться в главное меню")

        choice = input("Введите номер пункта меню:  ")

        if choice == "1":
            confirm_contract(contract)
        elif choice == "2":
            complete_contract(contract)
        elif choice == "3":
            break
        else:
            print("Неправильный выбор. Попробуйте еще раз.")


def confirm_contract(contract): # Функция подтверждения и подписания договора
    get_contracts()
    contract_id = int(input("Введите идентификатор договора для подтверждения: "))
    print(contract_id)
    cur.execute("SELECT status FROM contracts WHERE id = ?", (contract_id,))  # Запрос к базе данных
    result_status = cur.fetchone()
    print(result_status)
    status = result_status[0]
    if status != 'Черновик':  # Проверка статуса выбраного договора
        print("Ошибка: можно подтвердить только договор в статусе 'Черновик'!")
        return
    else:
        print("Статус успешно изменён на 'Активен'.")
        sign_date = date.today()
        upd_query = """UPDATE contracts SET sign_date = ?, status = ? WHERE id = ?"""  # Запрос к базе данных
        data = (date.today(), 'Активен', contract_id)
        cur.execute(upd_query, data)
        con.commit()
    print("Договор успешно подтвержден!")


def get_contracts(): # Функция получения списка договоров
    print("Список договоров:")
    cur.execute("SELECT * FROM contracts")
    contracts = cur.fetchall()
    for contract in contracts:
        print(f"id: {contract[0]}  name: {contract[1]} - status: {contract[4]}")


def complete_contract(contract): # Функция завершения договоров
    get_contracts()
    contract_id = int(input("Введите идентификатор договора для завершения: "))
    cur.execute("SELECT status FROM contracts WHERE id = ?", (contract_id,))  # Запрос к базе данных
    result_status = cur.fetchone()
    print(result_status)
    status = result_status[0]
    if status == 'Активен':  # Проверка статуса выбраного договора
        status = "Завершён"
        contract = Contract(status)
        cur.execute("""UPDATE contracts SET status = 'Завершён' WHERE id = ?""", (contract_id,))  # Запрос к базе данных
        con.commit()
        print("Договор успешно завершён!")
    else:
        print("Ошибка: можно завершить только активный договор.")


def create_project(): # Функция создания проектов
    print("Создание нового проекта")
    if not contracts: # Проверка на наличие договоров
        print("Невозможно начать проект без существующих договоров. Создайте сначала договор.")
        return

    name = input("Введите название проекта: ")

    project = {"name": name, "contracts": []}
    project = Project(name)
    database.create_project(project)

    projects.append(project)
    print("Проект успешно создан!")

    project_menu(project)


def project_menu(project): # Меню проекта
    while True:
        print("Выберите действие:")
        print("1. Добавить договор в проект")
        print("2. Удалить договор из проекта")
        print("3. Завершить договор (из проекта)")
        print("4. Вернуться в главное меню")

        choice = input("Введите номер пункта меню:  ")

        if choice == "1":
            add_contract_to_project(project) # Функция добавления договора в проект
        elif choice == "2":
            remove_contract_from_project(project) # Функция удаления договора из проекта
        elif choice == "3":
            complete_contract(project) # Функция завершения договора
        elif choice == "4":
            break
        else:
            print("Неправильный выбор. Попробуйте еще раз.")


def add_contract_to_project(project): # Функция добавления договора в проект
    get_projects() # Список проектов
    project_id = int(input("Введите идентификатор проекта для добавления: "))
    print(project_id)
    get_contracts() # Список договоров
    contract_id = int(input("Введите идентификатор договора для добавления: "))
    print(contract_id)
    cur.execute("SELECT * FROM contracts WHERE numer_proj = ?", (project_id,))  # Запрос к базе данных
    result_project = cur.fetchall()
    print(result_project)
    if len(result_project) == 0:  # Проверка наличия выбраного договора в проектах
        print('Договор не используется в проектах')
    else:
        print(f'Договор уже используется в проекте {project_id}!')
        return
    cur.execute("SELECT status FROM contracts WHERE id = ?", (contract_id,))  # Запрос к базе данных
    result_status = cur.fetchone()
    print(result_status)
    status = result_status[0]
    if status != 'Активен':  # Проверка статуса выбраного договора для добавления в проект
        print("Ошибка: можно добавить только активный договор в проект.")
        return
    else:
        print("Договор успешно добавлен в проект.")
        upd_query = """UPDATE contracts SET numer_proj= ? WHERE id = ?"""  # Запрос к базе данных
        data = (project_id, contract_id)
        cur.execute(upd_query, data)
        con.commit()
        return


def remove_contract_from_project(project): # Функция удаления договора из проекта
    get_contracts() # Список договоров
    contract_id = int(input("Введите идентификатор договора для удаления: "))
    result_con_id = contract_id
    print(result_con_id)
    cur.execute("DELETE FROM contracts WHERE id = ?", (contract_id,))  # Запрос к базе данных
    con.commit()
    print("Договор успешно удален из проекта!")


def get_projects(): # Функция получения списка проектов
    print("Список проектов:")
    cur.execute("SELECT * FROM projects")
    projects = cur.fetchall()
    for project in projects:
        print(f"id: {project[0]}, name: {project[1]}, creation_date {project[2]}")


main_menu()
