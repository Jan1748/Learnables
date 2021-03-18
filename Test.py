from Database import Database


def insert_example_data(database):
    database.create_tables()
    database.connect()
    dataset_id = database.get_dataset_id_by_name('Example Dataset')
    if len(dataset_id) > 0:
        print('Example data already there')
        return
    database.insert_dataset('Example Dataset')
    example_data = ['Mensch:human being', 'Männlich:male', 'Weiblich:female', 'Körper:body', 'Haare:hair', 'Kopf:head', 'Gesicht:face', 'Stirn:forehead', 'Auge, Augen:eye, eyes', 'Nase:nose', 'Mund:mouth', 'Ohr, Ohren:ear, ears', 'Wange, Wangen:cheek, cheeks']
    dataset_id = database.get_dataset_id_by_name('Example Dataset')
    print('Dataset_id:', dataset_id)
    for data in example_data:
        data = data.split(':')
        question = data[0]
        answer = data[1]
        database.insert_question(dataset_id[0][0], question, answer)
    database.close_connection()


d = Database('Learnables.db')
insert_example_data(d)
