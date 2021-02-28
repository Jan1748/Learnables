import random


def get_datasets():
    return ['All', 'English', 'Spain', 'Math']

def get_next_question():
    questions = [(21, 2, 'Whos your Dady?', 'Your Mom', 0), (213, 2, 'Fucking?', 'Yes', 0)]
    return random.choice(questions)