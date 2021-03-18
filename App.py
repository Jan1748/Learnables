import random

import wx

from Controller import *
from Database import Database
from Test import *


class MainFrame(wx.Frame):
    def __init__(self):
        self.database = Database('Learnables.db')
        self.database.create_tables()
        wx.Frame.__init__(self, None, title="Learnables", size=(1200, 800))
        menubar = wx.MenuBar()
        navigation = wx.Menu()
        learning_button = navigation.Append(1, "Start Learning")
        create_button = navigation.Append(2, "Create Dataset/Questions")
        manage_button = navigation.Append(3, "Manage Questions and Datasets")
        self.Bind(wx.EVT_MENU, self.switch_to_learning_panel, learning_button)
        self.Bind(wx.EVT_MENU, self.switch_to_create_panel, create_button)
        self.Bind(wx.EVT_MENU, self.switch_to_manage_panel, manage_button)
        self.learning_panel = LearningPanel(self, self.database)
        self.create_panel = CreatePanel(self, self.database)
        self.manage_panel = ManagePanel(self, self.database)
        menubar.Append(navigation, 'Navigation')
        self.SetMenuBar(menubar)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.learning_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.create_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.manage_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)
        self.Show()
        self.switch_to_learning_panel(wx.EVT_MENU)

    def switch_to_learning_panel(self, event):
        self.learning_panel.Show()
        self.learning_panel.refresh_datasets()
        self.create_panel.Hide()
        self.manage_panel.Hide()
        self.Layout()

    def switch_to_create_panel(self, event):
        self.learning_panel.Hide()
        self.create_panel.Show()
        self.create_panel.refresh_datasets()
        self.manage_panel.Hide()
        self.Layout()

    def switch_to_manage_panel(self, event):
        self.learning_panel.Hide()
        self.create_panel.Hide()
        self.manage_panel.Show()
        self.manage_panel.refresh_datasets()
        self.Layout()


class ManagePanel(wx.Panel):
    def __init__(self, parent, database):
        wx.Panel.__init__(self, parent=parent)
        self.database = database
        self.choices = get_all_datasets(self.database, True)
        self.ch = wx.Choice(self, -1, choices=self.choices, size=(275, -1), pos=(15, 15))
        self.ch.SetSelection(0)
        self.button = wx.Button(self, label="Show Questions", pos=(300, 15))
        self.Bind(wx.EVT_BUTTON, self.show_questions, self.button)
        self.question_list = wx.ListCtrl(self, size=(1150, 650), pos=(15, 50), style=wx.LC_REPORT)
        self.question_list.InsertColumn(0, 'ID', width=100)
        self.question_list.InsertColumn(1, 'Dataset', width=150)
        self.question_list.InsertColumn(2, 'Question', width=400)
        self.question_list.InsertColumn(3, 'Answer', width=400)
        self.question_list.InsertColumn(4, 'Answered Right', width=100)
        # self.add_line()
        self.delete_button = wx.Button(self, label="Delete Question", pos=(1000, 15))
        self.Bind(wx.EVT_BUTTON, self.delete_question, self.delete_button)
        self.delete_id = wx.TextCtrl(self, size=(250, -1), pos=(730, 15))
        self.delete_id.SetHint('Input the ID of the deleting question here')
        self.delete_dataset_button = wx.Button(self, label="Delete Dataset", pos=(420, 15))
        self.Bind(wx.EVT_BUTTON, self.delete_dataset_and_question, self.delete_dataset_button)
        # self.question_list.Hide()

    def show_questions(self, event):
        self.index = 0
        dataset = self.ch.GetString(self.ch.GetSelection())
        questions = get_questions(self.database, dataset)
        self.question_list.DeleteAllItems()
        for question in questions:
            self.add_line(question[0], question[1], question[2], question[3], question[4])

    def add_line(self, question_id, dataset_name, question, answer, right_answered):
        self.question_list.InsertItem(self.index, str(question_id))
        self.question_list.SetItem(self.index, 1, str(dataset_name))
        self.question_list.SetItem(self.index, 2, str(question))
        self.question_list.SetItem(self.index, 3, str(answer))
        self.question_list.SetItem(self.index, 4, str(right_answered))
        self.index += 1

    def refresh_datasets(self):
        self.choices = get_all_datasets(self.database, True)
        self.ch.SetItems(self.choices)
        self.ch.SetSelection(0)

    def delete_question(self, event):
        id_to_delete = self.delete_id.GetValue()
        delete_question(self.database, id_to_delete)
        self.show_questions(0)

    def delete_dataset_and_question(self, event):
        dataset = self.ch.GetString(self.ch.GetSelection())
        delete_dataset_and_questions(self.database, dataset)
        self.refresh_datasets()
        self.show_questions(0)

class CreatePanel(wx.Panel):
    def __init__(self, parent, database):
        wx.Panel.__init__(self, parent=parent)
        self.database = database
        text = wx.StaticText(self, -1, 'Create Question', size=(20, 100), pos=(15, 100))
        font = wx.Font(18, wx.DECORATIVE, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        text.SetFont(font)

        # Question Form
        self.choices = self.datasets = get_all_datasets(self.database, False)
        wx.StaticText(self, -1, "Choose a dataset to which the question should be assigned", size=(600, -1), pos=(15, 180))
        self.ch = wx.Choice(self, -1, choices=self.choices, size=(600, 200), pos=(15, 200))
        self.ch.SetSelection(0)
        wx.StaticText(self, -1, "Question", size=(100, -1), pos=(15, 250))
        self.question = wx.TextCtrl(self, size=(600, 50), pos=(15, 270))
        self.question.SetHint('Input your Question here')
        wx.StaticText(self, -1, "Answer", size=(100, -1), pos=(15, 350))
        self.answer = wx.TextCtrl(self, size=(600, 50), pos=(15, 370))
        self.answer.SetHint('Input your Answer here')
        self.create_question_button = wx.Button(self, label="Create Question", size=(600, 60), pos=(15, 440))
        self.Bind(wx.EVT_BUTTON, self.create_question, self.create_question_button)

        # Dataset Form
        text2 = wx.StaticText(self, -1, 'Create Dataset', size=(20, 100), pos=(700, 100))
        text2.SetFont(font)
        wx.StaticText(self, -1, "Dataset Name", size=(200, -1), pos=(700, 180))
        self.dataset_name = wx.TextCtrl(self, size=(400, -1), pos=(700, 200))
        self.dataset_name.SetHint('Input new Dataset name here')
        self.create_dataset_button = wx.Button(self, label="Create Dataset", size=(400, 60), pos=(700, 250))
        self.Bind(wx.EVT_BUTTON, self.create_dataset, self.create_dataset_button)

    def create_question(self, event):
        dataset = self.ch.GetString(self.ch.GetSelection())
        question = self.question.GetValue()
        answer = self.answer.GetValue()
        create_question(self.database, dataset, question, answer)
        self.question.Clear()
        self.answer.Clear()

    def create_dataset(self, event):
        dataset_name = self.dataset_name.GetValue()
        self.dataset_name.Clear()
        create_dataset(self.database, dataset_name)
        self.refresh_datasets()

    def refresh_datasets(self):
        self.choices = get_all_datasets(self.database, False)
        self.ch.SetItems(self.choices)
        self.ch.SetSelection(0)


class LearningPanel(wx.Panel):
    def __init__(self, parent, database):
        wx.Panel.__init__(self, parent=parent)
        self.database = database
        self.questions = None
        self.question_index = 0
        self.choices = self.datasets = get_all_datasets(self.database, True)
        self.ch = wx.Choice(self, -1, choices=self.choices, size=(275, -1), pos=(15, 15))
        self.ch.SetSelection(0)
        self.button = wx.Button(self, label="Start Learning", pos=(300, 15))
        self.Bind(wx.EVT_BUTTON, self.select_dataset, self.button)
        self.st = wx.StaticText(self, -1, "Question", (150, 200), (400, 200), wx.ALIGN_CENTER)
        self.answer_button = wx.Button(self, label="Show Answer", size=(400, 200), pos=(620, 200))
        self.Bind(wx.EVT_BUTTON, self.show_answer, self.answer_button)
        self.right_button = wx.Button(self, label="Answered Right", size=(200, 100), pos=(220, 450))
        self.Bind(wx.EVT_BUTTON, self.right_button_counter, self.right_button)
        self.right_button.Hide()
        self.next_button = wx.Button(self, label="Next", size=(1000, 100), pos=(80, 600))
        self.Bind(wx.EVT_BUTTON, self.next, self.next_button)

    def right_button_counter(self, event):
        right_counter(self.database, self.questions[self.question_index][0])
        self.right_button.Hide()

    def show_answer(self, event):
        self.st.SetLabel(str(self.questions[self.question_index][3]))
        self.right_button.Show()

    def next(self, event):
        self.question_index += 1
        if len(self.questions) <= self.question_index:
            self.question_index = 0
        self.st.SetLabel(str(self.questions[self.question_index][2]))
        self.right_button.Hide()

    def select_dataset(self, event):
        dataset_name = self.ch.GetString(self.ch.GetSelection())
        self.questions = get_questions(self.database, dataset_name)
        self.question_index = 0
        if self.questions is None or len(self.questions) == 0:
            self.st.SetLabel('No Questions Available')
        else:
            random.shuffle(self.questions)
        self.st.SetLabel(str(self.questions[self.question_index][2]))

    def refresh_datasets(self):
        self.choices = get_all_datasets(self.database, True)
        self.ch.SetItems(self.choices)
        self.ch.SetSelection(0)


app = wx.App()
frame = MainFrame()
frame.Show()
app.MainLoop()
