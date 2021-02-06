import sqlite3


class Database:
    def __init__(self, database_name: str):
        self.__conn = None
        self.__cur = None
        self.__database_name = database_name

    def connect(self):
        self.__conn = sqlite3.connect(self.__database_name)
        self.__cur = self.__conn.cursor()

    def close_connection(self):
        self.__cur.close()
        self.__conn.close()

    def db_execute(self, sql_string: str, values=None):
        if values is None:
            self.__cur.execute(sql_string)
        else:
            self.__cur.execute(sql_string, values)
        self.__conn.commit()

    def db_select(self, sql_string: str, values=None):
        if values is None:
            self.__cur.execute(sql_string)
        else:
            self.__cur.execute(sql_string, values)
        self.__conn.commit()
        return self.__cur.fetchall()

    def create_tables(self):
        sql_dataset = """CREATE TABLE IF NOT EXISTS Datasets (DatasetID INTEGER PRIMARY KEY, DatasetName String NOT NULL);"""
        sql_question = """CREATE TABLE IF NOT EXISTS Questions (QuestionID INTEGER PRIMARY KEY, DatasetID INTEGER NOT NULL, Question String NOT NULL, Answer String NOT NULL, CorrectAnswers INTEGER DEFAULT 0, FOREIGN KEY (DatasetID) REFERENCES Datasets(DatasetID) ON DELETE CASCADE);"""
        #TODO Fix Foreign Key
        self.connect()
        self.db_execute(sql_dataset)
        self.db_execute(sql_question)
        self.close_connection()

    def insert_dataset(self, name: str):
        sql_string = "Insert Into Datasets (DatasetName) values (?)"
        values = (name,)
        self.db_execute(sql_string, values)

    def insert_question(self, dataset_id, question, answer):
        sql_string = "Insert Into Questions (DatasetID, Question, Answer) values (?,?,?)"
        values = (dataset_id, question, answer)
        self.db_execute(sql_string, values)

    def get_all_datasets(self):
        sql_string = "Select * From Datasets"
        datasets = self.db_select(sql_string)
        return datasets

    def get_all_questions(self, dataset_id: int):
        sql_string = "Select * From Questions WHERE DatasetID = ?"
        values = (dataset_id,)
        rows = self.db_select(sql_string, values)
        return rows


d = Database('Test.db')
d.create_tables()
d.connect()
d.insert_dataset('Spanisch')
d.insert_question(1, 'Are you there?', 'No...')
rows = d.get_all_questions(1)
print(rows)
d.close_connection()
