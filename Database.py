import random
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
        sql_string = "Select DatasetName From Datasets"
        datasets = self.db_select(sql_string)
        return datasets

    def get_dataset_id_by_name(self, dataset_name):
        sql_string = "Select DatasetID From Datasets WHERE DatasetName == (?)"
        values = (dataset_name,)
        datasets = self.db_select(sql_string, values)
        return datasets

    def get_all_questions(self, dataset_id: int):
        values = None
        if dataset_id == -1:
            sql_string = "Select QuestionID, DatasetName, Question, Answer, CorrectAnswers FROM Questions Left JOIN Datasets D on Questions.DatasetID = D.DatasetID"
        else:
            sql_string = "Select QuestionID, DatasetName, Question, Answer, CorrectAnswers FROM Questions Left JOIN Datasets D on Questions.DatasetID = D.DatasetID WHERE D.DatasetID = (?)"
            values = (dataset_id,)
        return self.db_select(sql_string, values)

    def right_counter_up(self, question_id):
        sql_string = "Select CorrectAnswers FROM Questions WHERE QuestionID = (?)"
        values = (question_id,)
        correct_answers = int(self.db_select(sql_string, values)[0][0])
        correct_answers += 1
        sql_string = f"UPDATE Questions SET CorrectAnswers = {correct_answers} WHERE QuestionID = (?)"
        self.db_select(sql_string, values)
