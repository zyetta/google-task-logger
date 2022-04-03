import sqlite3


class SqliteController:
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                id TEXT NOT NULL UNIQUE PRIMARY KEY,
                task_id TEXT NOT NULL,
                title TEXT NOT NULL,
                task_list TEXT NOT NULL,
                completed DATETIME NOT NULL);
            """)
        except Exception as e:
            print(f"Could not successfully create database\n{e}")
        finally:
            if conn:
                conn.close()

    def insert_task(self, task_data):
        conn = None
        success = False;
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            sql_query = f"""
            INSERT INTO 
                tasks 
            VALUES (
                :id, 
                :task_id,
                :title,
                :task_list,
                :completed
            );""".format(table='tasks')
            c.execute(sql_query, task_data)
            conn.commit()
            success = True
        except Exception as e:
            print(e)
        finally:
            if conn:
                conn.close()
            return success

    def get_task(self, task_id):
        conn = None
        task = False
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(f"""SELECT * FROM tasks WHERE id = "{task_id}";""")
            task = c.fetchall()
            if not task:
                task = False
        except Exception as e:
            print(e)
        finally:
            if conn:
                conn.close()
            return task
