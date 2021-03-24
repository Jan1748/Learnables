from Database import Database

class Controller:
    def __init__(self):
        self.__database = Database('Learnables.db')
        self.__database.create_tables()
    def get_questions(self, dataset_name: str):
        self.__database.connect()
        if dataset_name == 'All':
            dataset_id = -1
        else:
            dataset_id = int(self.__database.get_dataset_id_by_name(dataset_name)[0][0])
        self.__database.connect()
        questions = self.__database.get_all_questions(dataset_id)
        self.__database.close_connection()
        return questions


    def get_all_datasets(self, with_all: bool):
        self.__database.connect()
        datasets = ['All'] if with_all else []
        [datasets.append(x[0]) for x in self.__database.get_all_datasets()]
        self.__database.close_connection()
        return datasets


    def create_question(self, dataset_name, question, answer):
        self.__database.connect()
        dataset_id = self.__database.get_dataset_id_by_name(dataset_name)[0][0]
        self.__database.insert_question(dataset_id, question, answer)
        self.__database.close_connection()


    def create_dataset(self, dataset_name):
        self.__database.connect()
        self.__database.insert_dataset(dataset_name)
        self.__database.close_connection()


    def right_counter(self, question_id):
        self.__database.connect()
        self.__database.right_counter_up(question_id)
        self.__database.close_connection()


    def delete_question(self, question_id):
        self.__database.connect()
        self.__database.delete_question(question_id)
        self.__database.close_connection()


    def delete_dataset_and_questions(self, dataset_name):
        self.__database.connect()
        if dataset_name == 'All':
            return
        else:
            dataset_id = int(self.__database.get_dataset_id_by_name(dataset_name)[0][0])
        self.__database.delete_dataset(dataset_id)
        self.__database.close_connection()
