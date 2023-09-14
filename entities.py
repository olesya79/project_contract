from datetime import date


class Contract: # Класс для создания договоров
    def __init__(self, name, status='Черновик'):
        self.name = name
        self.created_date = date.today()
        self.sign_date = date.today()
        self.status = status
        self.project_id = None


class Project: # Класс для создания проектов
    def __init__(self, name):
        self.name = name
        self.created_date = date.today()
        self.contract_id = None
