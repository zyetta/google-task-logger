import datetime


class Tasks:
    id = ""
    task_id = ""
    title = ""
    task_list = ""
    completed = ""

    def __init__(self, title, task_list, completed, task_id):
        self.title = title
        self.task_list = task_list
        self.completed = completed
        self.task_id = task_id
        self.id = self.generate_id()

    def generate_id(self):
        a = self.task_id
        b = int(datetime.datetime.timestamp(datetime.datetime.strptime(self.completed, "%Y-%m-%dT%H:%M:%S.%f%z")))
        id_str = f'{a}-{b}'.encode('utf-8')
        return str(id_str.hex())

    def get_id(self):
        return self.id

    def get_task(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "title": self.title,
            "task_list": self.task_list,
            "completed": self.completed,
        }
