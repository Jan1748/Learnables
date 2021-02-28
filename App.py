import wx
from Test import *

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Learnables", size=(1200, 800))
        menubar = wx.MenuBar()
        navigation = wx.Menu()
        self.learning_button = navigation.Append(1, "Start Learning")
        self.create_button = navigation.Append(2, "Create Dataset/Questions")
        self.manage_button = navigation.Append(3, "Manage Questions and Datasets")
        self.Bind(wx.EVT_MENU, self.switch_to_learning_panel, self.learning_button)
        self.Bind(wx.EVT_MENU, self.switch_to_create_panel, self.create_button)
        self.Bind(wx.EVT_MENU, self.switch_to_manage_panel, self.manage_button)
        self.learning_panel = ManagePanel(self)
        menubar.Append(navigation, 'Navigation')
        self.SetMenuBar(menubar)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.learning_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Show()

    def switch_to_learning_panel(self, event):
        print('Switching to Learning Panel')

    def switch_to_create_panel(self, event):
        print('Switching to Create Panel')

    def switch_to_manage_panel(self, event):
        print('Switching to Manage Panel')

class ManagePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        choices = get_datasets()
        self.ch = wx.Choice(self, -1, choices=choices, size=(275, -1), pos=(15, 15))
        self.ch.SetSelection(0)
        self.button = wx.Button(self, label="Show Questions", pos=(300, 15))
        self.Bind(wx.EVT_BUTTON, self.show_questions, self.button)
        self.question_list = wx.ListCtrl(self, size=(1000, 900), pos=(15, 50), style=wx.LC_REPORT)
        self.question_list.InsertColumn(0, 'Question', width=400)
        self.question_list.InsertColumn(1, 'Answer',width=400)
        self.question_list.InsertColumn(2, 'Right Answered',width=100)
        #self.add_line()

        #self.question_list.Hide()

    def show_questions(self, event):
        print('Showing Question')
        self.index = 0
        dataset = self.ch.GetString(self.ch.GetSelection())
        questions = [('What is your name', 'Jan', '5'),('What is your name', 'Jules', '5')] #TODO
        self.question_list.DeleteAllItems()
        for question in questions:
            self.add_line(question[0], question[1], question[2])

    def add_line(self, question, answer, right_answered):
        self.question_list.InsertItem(self.index, question)
        self.question_list.SetStringItem(self.index, 1, answer)
        self.question_list.SetStringItem(self.index, 2, str(right_answered))
        self.index += 1

class CreatePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        text = wx.StaticText(self, -1, 'Create Question', size=(20, 100), pos=(15, 100))
        font = wx.Font(18, wx.DECORATIVE, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        text.SetFont(font)
        #self.button = wx.Button(self, label="Start Learning", pos=(300, 15))
        #self.Bind(wx.EVT_BUTTON, self.select_dataset, self.button)
        #self.right_button = wx.Button(self, label="I was knowing the Answer",size=(200, 100), pos=(15, 450))
        #self.Bind(wx.EVT_BUTTON, self.right_button_counter, self.right_button)

        #Question Form
        self.choices = get_datasets()
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

        #Dataset Form
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
        self.question.Clear()
        self.answer.Clear()
        print(dataset, question, answer)

    def create_dataset(self, event):
        dataset_name = self.dataset_name.GetValue()
        self.dataset_name.Clear()
        print('Creating Dataset:', dataset_name)

    def select_dataset(self, event):
        c = self.ch.GetString(self.ch.GetSelection())
        print('Dataset Selected Loading Questions', c)



class LearningPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        choices = get_datasets()
        self.ch = wx.Choice(self, -1, choices=choices, size=(275, -1), pos=(15, 15))
        self.ch.SetSelection(0)
        self.button = wx.Button(self, label="Start Learning", pos=(300, 15))
        self.Bind(wx.EVT_BUTTON, self.select_dataset, self.button)
        self.st = wx.StaticText(self, -1, "Question", (150, 200), (400, 200), wx.ALIGN_CENTER)
        self.answer_button = wx.Button(self, label="Show Answer", size=(400, 200), pos=(620, 200))
        self.Bind(wx.EVT_BUTTON, self.show_answer, self.answer_button)
        self.right_button = wx.Button(self, label="I was knowing the Answer",size=(200, 100), pos=(220, 450))
        self.Bind(wx.EVT_BUTTON, self.right_button_counter, self.right_button)
        self.right_button.Hide()
        #self.back_button = wx.Button(self, label="Back", size=(500, 100), pos=(50, 600))
        self.next_button = wx.Button(self, label="Next", size=(1000, 100), pos=(80, 600))
        self.Bind(wx.EVT_BUTTON, self.next, self.next_button)

    def right_button_counter(self, event):
        print('Right')
        self.right_button.Hide()


    def show_answer(self, event):
        print('Showing Answer')
        self.st.SetLabel('Answer') #TODO Set Answere
        self.right_button.Show()

    def next(self, event):
        print('Next')
        self.st.SetLabel('Question') #TODO Set Answere
        self.right_button.Hide()

    def select_dataset(self, event):
        c = self.ch.GetString(self.ch.GetSelection())
        print('Dataset Selected Loading Questions', c)


app = wx.App()
frame = MainFrame()
frame.Show()
app.MainLoop()
