from Database import Database


def get_questions(database: Database, dataset_name):
    database.connect()
    if dataset_name == 'All':
        dataset_id = -1
    else:
        dataset_id = int(database.get_dataset_id_by_name(dataset_name)[0][0])
    database.connect()
    questions = database.get_all_questions(dataset_id)
    database.close_connection()
    return questions


def get_all_datasets(database: Database, with_all: bool):
    database.connect()
    datasets = ['All'] if with_all else []
    [datasets.append(x[0]) for x in database.get_all_datasets()]
    database.close_connection()
    return datasets


def create_question(database: Database, dataset_name, question, answer):
    database.connect()
    dataset_id = database.get_dataset_id_by_name(dataset_name)[0][0]
    database.insert_question(dataset_id, question, answer)
    database.close_connection()


def create_dataset(database: Database, dataset_name):
    database.connect()
    database.insert_dataset(dataset_name)
    database.close_connection()

def right_counter(database: Database, question_id):
    database.connect()
    database.right_counter_up(question_id)
    database.close_connection()

def delete_question(database: Database, question_id):
    database.connect()
    database.delete_question(question_id)
    database.close_connection()

def delete_dataset_and_questions(database: Database, dataset_name):
    database.connect()
    if dataset_name == 'All':
        return
    else:
        dataset_id = int(database.get_dataset_id_by_name(dataset_name)[0][0])
    database.delete_dataset(dataset_id)
    database.close_connection()