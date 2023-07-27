import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmsgbox
import os
import json
from threading import Thread
import time
import scripts.question as question
from PIL import Image, ImageTk
from update_check import isUpToDate

class GUIWINDOW:
    def __init__(self):
        self.check_update()
        # These var can be access by other class
        # Those var not in this __init__ func will be private
        self.correctAns = None
        self.maxQuestionQuiz = None
        self.question_quiz_num = None
        self.currentQuestionQuiz = None
        self.questionQuiz = None
        self.choice = None
        self.image_path = ''
        self.image_count = 1

        if not os.path.exists('layout.conf'):
            with open('layout.conf', 'wt') as f:
                f.write(json.dumps({
                    'winWidth': 900,
                    'winHeight': 500,
                    'quizFontSize': 13,
                    'genFontSize': 13,
                    'savePath': './data'
                    }))
            if not os.path.exists('data'):
                os.mkdir('data')
        with open('layout.conf', 'rt') as f:
            self.layout = json.loads(f.read())

    def check_update(self):
        print(isUpToDate(__file__, "https://github.com/nhtri2003gmail/QuizMaker/blob/master/scripts/guiwindow.py"))
        input()

    def GUI(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.layout['winWidth']}x{self.layout['winHeight']}+200+50")
        self.root.title('Quiz Maker')
        # self.root.resizable(False, False)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Create notebook for containing tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky='news')
        # Create tab "Load"
        self.frLoadTab = ttk.Frame(self.notebook)
        self.notebook.add(self.frLoadTab, text='Load')
        # Create tab "Quiz"
        self.frQuizTab = ttk.Frame(self.notebook)
        self.notebook.add(self.frQuizTab, text='Quiz')
        # Create tab "Setting"
        self.frSettingTab = ttk.Frame(self.notebook)
        self.notebook.add(self.frSettingTab, text='Setting')
        # Select default tab
        self.notebook.select(0)

        self.LoadTab()
        self.QuizTab()
        self.SettingTab()

        self.frQuizContent.bind("<Configure>", self.QuizOnResize)
        self.frSettingTab.bind("<Configure>", self.SettingOnResize)
        self.root.mainloop()
    
    def QuizOnResize(self, event):
        # 110 - 85
        self.lbQues.config(wraplength=event.width-75)

        if self.image_path != '':
            image = Image.open(self.image_path)
            ratio = (event.width - 85) / image.size[0]
            image_resized = image.resize( (int(image.size[0] * ratio), int(image.size[1] * ratio)) )
            img = ImageTk.PhotoImage(image_resized)
            self.lb_image.image = img
            self.lb_image.config(image=img)

        for i in range(4):
            self.rdBtnAns[i].config(wraplength=event.width-100)

    def SettingOnResize(self, event):
        self.etWinWidth.delete(0, tk.END)
        self.etWinWidth.insert(0, str(event.width + 4))
        self.etWinHeight.delete(0, tk.END)
        self.etWinHeight.insert(0, str(event.height + 26))


    ##############################################
    ### LOADTAB ##################################
    ##############################################
    def LoadTab(self):
        self.frLoadTab.rowconfigure(1, weight=1)
        self.frLoadTab.columnconfigure(0, weight=1)
        self.frLoadTab.columnconfigure(1, weight=1)

        self.frLoadImportFrom = tk.Frame(self.frLoadTab)
        self.frLoadImportFrom.columnconfigure(1, weight=1)
        self.frLoadImportFrom.grid(row=0, column=0, columnspan=2, sticky='news')
        self.lbImportFrom = tk.Label(self.frLoadImportFrom, text='Import from: ', font=('Arial', self.layout['genFontSize']))
        self.lbImportFrom.grid(row=0, column=0, pady=(20,10), padx=(30, 10), sticky='news')
        self.etImportFrom = tk.Entry(self.frLoadImportFrom, font=('Arial', self.layout['genFontSize']), width=20)
        self.etImportFrom.grid(row=0, column=1, pady=(20,10), sticky='news')
        self.btnImportFrom = tk.Button(self.frLoadImportFrom, text='   Browse...   ', font=('Arial', self.layout['genFontSize']), command=self.LoadGetImportFromPath)
        self.btnImportFrom.grid(row=0, column=2, pady=(20,10), padx=(10, 30), sticky='news')
        self.btnImport = tk.Button(self.frLoadImportFrom, text='IMPORT', font=('Arial', self.layout['genFontSize']), command=self.LoadImport)
        self.btnImport.grid(row=2, column=0, columnspan=3, pady=(0, 10), padx=50, sticky='we')

        self.frLoadFromFile = tk.Frame(self.frLoadTab)
        self.frLoadFromFile.rowconfigure(0, weight=1)
        self.frLoadFromFile.columnconfigure(0, weight=1)
        self.frLoadFromFile.grid(row=1, column=0, sticky='news')
        self.lsLoadedFile = tk.Listbox(self.frLoadFromFile, font=('Arial', self.layout['genFontSize']))
        self.lsLoadedFile.grid(row=0, column=0, pady=(20,5), padx=20, sticky='news')
        self.lsLoadedFile.bind('<Double-Button-1>', self.LoadFile)
        self.btnLoadFile = tk.Button(self.frLoadFromFile, text='LOAD', font=('Arial', self.layout['genFontSize']), command=lambda: self.LoadFile(None))
        self.btnLoadFile.grid(row=1, column=0, padx=20, pady=(0, 30), sticky='news')

        self.frLoadFunctionality = tk.Frame(self.frLoadTab)
        self.frLoadFunctionality.columnconfigure(1, weight=1)
        self.frLoadFunctionality.rowconfigure(0, weight=1)
        self.frLoadFunctionality.rowconfigure(1, weight=1)
        self.frLoadFunctionality.rowconfigure(2, weight=1)
        self.frLoadFunctionality.rowconfigure(3, weight=1)
        self.frLoadFunctionality.rowconfigure(4, weight=1)
        self.frLoadFunctionality.rowconfigure(5, weight=1)
        self.frLoadFunctionality.grid(row=1, column=1, sticky='news')

        self.lbLoadedFile = tk.Label(self.frLoadFunctionality, text='File loaded: ', font=('Arial', self.layout['genFontSize']))
        self.lbLoadedFile.grid(row=0, column=0, pady=(20, 5), padx=10, sticky='w')
        self.etLoadedFileName = tk.Entry(self.frLoadFunctionality, text='', font=('Arial', self.layout['genFontSize']), state='readonly')
        self.etLoadedFileName.grid(row=0, column=1, columnspan=2, padx=(0, 20), sticky='we')

        self.lbMode = tk.Label(self.frLoadFunctionality, text='Mode:', font=('Arial', self.layout['genFontSize']))
        self.lbMode.grid(row=1, column=0, pady=5, padx=10, sticky='w')
        self.varMode = tk.StringVar(value='Practice')
        self.cbbMode = ttk.Combobox(self.frLoadFunctionality, textvariable=self.varMode, values=['Practice', 'Quiz'], font=('Arial', self.layout['genFontSize']))
        self.cbbMode.grid(row=1, column=1, columnspan=2, pady=5, padx=(0, 20), sticky='we')
        self.cbbMode.bind("<<ComboboxSelected>>", self.ModeSelected)

        self.frRadioButtonFunction = tk.Label(self.frLoadFunctionality)
        self.frRadioButtonFunction.rowconfigure(0, weight=1)
        self.frRadioButtonFunction.rowconfigure(1, weight=1)
        self.frRadioButtonFunction.columnconfigure(1, weight=1)
        self.frRadioButtonFunction.columnconfigure(3, weight=1)
        self.frRadioButtonFunction.grid(row=2, column=0, columnspan=3, pady=5, sticky='news')
        # Show answer
        self.lbShowAnswer = tk.Label(self.frRadioButtonFunction, text='Show answer:', font=('Arial', self.layout['genFontSize']))
        self.lbShowAnswer.grid(row=0, column=0, rowspan=2, padx=10, sticky='w')
        self.varTmpShowAnswer = tk.StringVar(value='1')
        self.varShowAnswer = tk.StringVar(value='1')
        self.rdBtnShowAnswerYes = tk.Radiobutton(self.frRadioButtonFunction, text='Yes', font=('Arial', self.layout['genFontSize']), variable=self.varTmpShowAnswer, value='1')
        self.rdBtnShowAnswerYes.grid(row=0, column=1, sticky='w')
        self.rdBtnShowAnswerNo = tk.Radiobutton(self.frRadioButtonFunction, text='No', font=('Arial', self.layout['genFontSize']), variable=self.varTmpShowAnswer, value='0')
        self.rdBtnShowAnswerNo.grid(row=1, column=1, sticky='w')
        # Random order
        self.lbRandomOrder = tk.Label(self.frRadioButtonFunction, text='Random order:', font=('Arial', self.layout['genFontSize']))
        self.lbRandomOrder.grid(row=0, column=2, rowspan=2, padx=10, sticky='w')
        self.varRandomOrder = tk.StringVar(value='1')
        self.rdBtnRandomOrderYes = tk.Radiobutton(self.frRadioButtonFunction, text='Yes', font=('Arial', self.layout['genFontSize']), variable=self.varRandomOrder, value='1')
        self.rdBtnRandomOrderYes.grid(row=0, column=3, sticky='w')
        self.rdBtnRandomOrderNo = tk.Radiobutton(self.frRadioButtonFunction, text='No', font=('Arial', self.layout['genFontSize']), variable=self.varRandomOrder, value='0')
        self.rdBtnRandomOrderNo.grid(row=1, column=3, sticky='w')

        self.lbNumOfQues = tk.Label(self.frLoadFunctionality, text='Number of questions:', font=('Arial', self.layout['genFontSize']))
        self.lbNumOfQues.grid(row=3, column=0, pady=5, padx=10, sticky='w')
        self.etNumOfQues = tk.Entry(self.frLoadFunctionality, font=('Arial', self.layout['genFontSize']))
        self.etNumOfQues.grid(row=3, column=1, sticky='we')
        self.btnSetNumOfQues = tk.Button(self.frLoadFunctionality, text='   Set   ', font=('Arial', self.layout['genFontSize']), command=self.LoadSetNumberOfQues)
        self.btnSetNumOfQues.grid(row=3, column=2, padx=50, sticky='we')

        self.lbPart = tk.Label(self.frLoadFunctionality, text='Part:', font=('Arial', self.layout['genFontSize']))
        self.lbPart.grid(row=4, column=0, pady=5, padx=10, sticky='w')
        self.varPart = tk.StringVar(value='')
        self.cbbPart = ttk.Combobox(self.frLoadFunctionality, textvariable=self.varPart, values=[], font=('Arial', self.layout['genFontSize']))
        self.cbbPart.grid(row=4, column=1, columnspan=2, padx=(0, 20), sticky='we')

        self.btnStart = tk.Button(self.frLoadFunctionality, text='   START   ', font=('Arial', self.layout['genFontSize']), command=self.LoadStartQuiz)
        self.btnStart.grid(row=5, column=0, columnspan=3, pady=5, padx=50, sticky='we')
        
        self.btnSetNumOfQues.config(state='disabled')
        self.btnStart.config(state='disabled')

        self.LoadLoadedFile()
    
    def LoadStartQuiz(self):
        self.QuizResetAnswerButton()
        mode = self.cbbMode.get()
        if mode=='Practice':
            if self.cbbPart.current() == -1:
                tkmsgbox.showinfo('Info', 'You didn\'t choose which part to practice')
                return
            part = self.cbbPart.get()
            self.currentQuestionQuiz = 0
            if self.varRandomOrder.get() == '1':
                self.questionQuiz = question.GenStaticQuestionRandom(self.loadFileName, int(part.split(' ')[1]) - 1, self.maxQuestionQuiz)
            else:
                self.questionQuiz = question.GenStaticQuestionNoRandom(self.loadFileName, int(part.split(' ')[1]) - 1, self.maxQuestionQuiz)
        elif mode=='Quiz':
            self.currentQuestionQuiz = 0
            self.questionQuiz = question.GenDynamicQuestion(self.loadFileName, self.maxQuestionQuiz)
        self.question_quiz_num = len(self.questionQuiz)
        self.correctAns = int(self.questionQuiz[self.currentQuestionQuiz][5])
        self.QuizTabLoadContent()
        self.notebook.select(1)
        self.lsQuestion.delete(0, tk.END)
        for i in range(len(self.questionQuiz)):
            self.lsQuestion.insert('end', 'Question ' + str(i+1))
        self.varShowAnswer.set(self.varTmpShowAnswer.get())

    def LoadSetNumberOfQues(self):
        try:
            n = int(self.etNumOfQues.get())
            if n<1 or n>200:
                tkmsgbox.showinfo("Number of question", 'Number of question should be from 1 to 200')
                return
            mode = self.cbbMode.get()
            with open(self.loadFileName, 'rt') as f:
                ques = json.loads(f.read())
            quantity = ques['quantity']
            self.maxQuestionQuiz = n if n < quantity else quantity
            self.etNumOfQues.delete(0, tk.END)
            self.etNumOfQues.insert(0, str(self.maxQuestionQuiz))
            if mode=='Practice':
                parts = []
                if quantity % self.maxQuestionQuiz == 0:
                    partNum = quantity // self.maxQuestionQuiz
                else:
                    partNum = (quantity // self.maxQuestionQuiz) + 1
                for i in range(partNum):
                    if i==0:
                        self.varPart.set('Part ' + str(i+1))
                    parts.append('Part ' + str(i+1))
                self.cbbPart.config(values=parts)
            self.btnStart.config(state='normal')
        except Exception as e:
            tkmsgbox.showerror('Number of question', e)

    def ModeSelected(self, event):
        if self.cbbMode.get() == 'Quiz':
            self.rdBtnRandomOrderYes.config(state='disabled')
            self.rdBtnRandomOrderNo.config(state='disabled')
            self.varRandomOrder.set('1')
            self.varPart.set('Random')
            self.cbbPart.config(values=['Random'])
        else:
            self.rdBtnRandomOrderYes.config(state='normal')
            self.rdBtnRandomOrderNo.config(state='normal')
            self.varPart.set('')
            self.cbbPart.config(values=[])

    def LoadFile(self, event):
        if self.lsLoadedFile.size()==0 or self.lsLoadedFile.curselection()==():
            return
        index = self.lsLoadedFile.curselection()[0]
        self.loadFileName = self.layout['savePath'] + '/' + self.lsLoadedFile.get(index)
        with open(self.loadFileName, 'rt') as f:
            ques = json.loads(f.read())
        self.etLoadedFileName.config(state='normal')
        self.etLoadedFileName.delete(0, tk.END)
        self.etLoadedFileName.insert(0, f'[{ques["quantity"]}] ' + self.lsLoadedFile.get(index))
        self.etLoadedFileName.config(state='readonly')
        self.btnSetNumOfQues.config(state='normal')
        self.etNumOfQues.delete(0, tk.END)
        self.etNumOfQues.insert(0, '15')
        self.LoadSetNumberOfQues()

    def LoadLoadedFile(self):
        files = os.listdir(self.layout['savePath'])
        for file in files:
            if file[-4:] != '.img':
                self.lsLoadedFile.insert('end', file)

    def LoadGetImportFromPath(self):
        path = tkfiledialog.askopenfile()
        if path:
            self.etImportFrom.delete(0, tk.END)
            self.etImportFrom.insert(0, path.name)

    def LoadImport(self):
        self.btnImport.config(text='IMPORTING...')
        path = self.etImportFrom.get()
        if not path:
            tkmsgbox.showinfo('Import from path', "Invalid path")
            self.btnImport.config(text='Import')
            return
        res, msg = question.ImportFromFile(self.etImportFrom.get(), self.etSavePath.get())
        if res == 1:
            tkmsgbox.showinfo("Import from", 'File ' + self.etImportFrom.get() + ' imported successfully')
            isExisted = False
            for index in range(self.lsLoadedFile.size()):
                if self.lsLoadedFile.get(index) == msg:
                    isExisted = True
                    break
            if not isExisted:
                self.lsLoadedFile.insert('end', msg)
        else:
            tkmsgbox.showerror("Import from", msg)
        self.btnImport.config(text='IMPORT')
        


    ##############################################
    ### QUIZTAB ##################################
    ##############################################
    def QuizTab(self):
        self.frQuizTab.rowconfigure(0, weight=1)
        self.frQuizTab.rowconfigure(1, weight=1)
        self.frQuizTab.columnconfigure(0, weight=1)
        # self.frQuizTab.columnconfigure(1, weight=1)

        self.frQuizContent = tk.Frame(self.frQuizTab, width=self.layout['winWidth'], height=self.layout['winHeight'])
        self.frQuizContent.columnconfigure(0, weight=1)
        self.frQuizContent.grid(row=0, column=0, sticky='news')
        self.lbQues = tk.Label(self.frQuizContent, text='', font=('Arial', self.layout['quizFontSize']), justify='left', anchor='w', wraplength=self.layout['winWidth']-275)
        self.lb_image = tk.Label(self.frQuizContent)
        self.choice = tk.StringVar(value='-1')
        self.rdBtnAns = [None]*4
        for i in range(4):
            self.rdBtnAns[i] = tk.Radiobutton(
                self.frQuizContent, 
                text='',
                font=('Arial', self.layout['quizFontSize']), 
                variable=self.choice, 
                value=f'{i}',
                justify='left',
                anchor='w',
                wraplength=self.layout['winWidth']-300,
                disabledforeground='black',
                command=self.QuizSelectedAnswer
            )
        self.lbQues.grid(row=0, column=0, pady=(30, 0), padx=(40, 0), sticky='w')
        self.lb_image.grid(row=1, column=0, pady=(10, 30), padx=(40, 0), sticky='w')
        for i in range(4):
            self.rdBtnAns[i].grid(row=(2 + i), column=0, pady=5, padx=(40, 0), sticky='w')

        self.frQuizFooter = tk.Frame(self.frQuizTab)
        self.frQuizFooter.columnconfigure(0, weight=1)
        self.frQuizFooter.columnconfigure(1, weight=1)
        self.frQuizFooter.columnconfigure(2, weight=1)
        self.frQuizFooter.grid(row=1, column=0, pady=30, sticky='swe')
        self.left_btn = tk.Button(self.frQuizFooter, text='   <   ', font=('Arial', self.layout['genFontSize']), command=self.QuizPreviousQuestion)
        self.right_btn = tk.Button(self.frQuizFooter, text='   >   ', font=('Arial', self.layout['genFontSize']), command=self.QuizNextQuestion)
        self.submit_btn = tk.Button(self.frQuizFooter, text='     Submit     ', font=('Arial', self.layout['genFontSize']), command=self.QuizSubmit)
        self.left_btn.grid(row=0, column=0, padx=(0, 5), sticky='e')
        self.right_btn.grid(row=0, column=1, padx=(5, 0), sticky='w')
        self.submit_btn.grid(row=0, column=2, sticky='w')

        self.frQuestionList = tk.Frame(self.frQuizTab)
        self.frQuestionList.rowconfigure(0, weight=1)
        self.frQuestionList.columnconfigure(0, weight=1)
        self.frQuestionList.grid(row=0, column=1, rowspan=2, sticky='news')
        self.lsQuestion = tk.Listbox(self.frQuestionList, font=('Arial', self.layout['genFontSize']))
        self.lsQuestion.grid(row=0, column=0, rowspan=7, sticky='ns')
        self.lsQuestion.bind('<Double-Button-1>', self.QuizJumpQuestionWithList)

    def QuizTabLoadContent(self):
        self.QuizResetAnswerButton()
        self.correctAns = self.questionQuiz[self.currentQuestionQuiz][5]
        self.choice.set(str(self.questionQuiz[self.currentQuestionQuiz][7]))
        if '<image>' in ''.join(self.questionQuiz[self.currentQuestionQuiz][0].lower().split()):
            self.image_path = f'{ self.etSavePath.get() }/{ self.etLoadedFileName.get().split("] ")[1] }.img/image{ self.image_count }.png'
            image = Image.open(self.image_path)
            ratio = (int(self.etWinWidth.get()) - 275) / image.size[0]
            image_resized = image.resize( (int(image.size[0] * ratio), int(image.size[1] * ratio)) )
            img = ImageTk.PhotoImage(image_resized)
            self.lb_image.image = img
            self.lb_image.config(image=img)
            self.lbQues.config(text=f'[{self.currentQuestionQuiz + 1}/{self.question_quiz_num}] ' + self.questionQuiz[self.currentQuestionQuiz][0].split('>')[1])
        else:
            self.image_path = ''
            self.lb_image.config(image='')
            self.lbQues.config(text=f'[{self.currentQuestionQuiz + 1}/{self.question_quiz_num}] ' + self.questionQuiz[self.currentQuestionQuiz][0])
        for i in range(4):
            self.rdBtnAns[i].config(text=self.questionQuiz[self.currentQuestionQuiz][i+1])

        # If question is solved then disable it
        if self.questionQuiz[self.currentQuestionQuiz][6]:
            # Disable all radio button first
            for i in range(4):
                self.rdBtnAns[i].config(state='disable')
            if self.varShowAnswer.get() == '1':
                # If answer is correct
                if int(self.choice.get()) == self.correctAns:
                    self.rdBtnAns[self.correctAns].config(disabledforeground='green')
                # If not
                else:
                    self.rdBtnAns[self.correctAns].config(disabledforeground='green')
                    self.rdBtnAns[int(self.choice.get())].config(disabledforeground='red')

    def QuizSelectedAnswer(self):
        if self.correctAns == None:
            return
        self.questionQuiz[self.currentQuestionQuiz][6] = 1          # solved
        self.questionQuiz[self.currentQuestionQuiz][7] = int(self.choice.get())
        # In case last question, it will be update immediately without changing question
        for i in range(4):
            self.rdBtnAns[i].config(state='disable')
        if self.varShowAnswer.get() == '1':
            # If answer is correct
            if (int(self.choice.get()) == self.correctAns):
                self.rdBtnAns[self.correctAns].config(disabledforeground='green')
                self.lsQuestion.itemconfig(self.currentQuestionQuiz,{'bg':'green', 'fg': 'white'})
            # If not
            else:
                self.rdBtnAns[self.correctAns].config(disabledforeground='green')
                self.rdBtnAns[int(self.choice.get())].config(disabledforeground='red')
                self.lsQuestion.itemconfig(self.currentQuestionQuiz,{'bg':'red', 'fg': 'white'})
        else:
            self.lsQuestion.itemconfig(self.currentQuestionQuiz,{'bg':'light blue', 'fg': 'white'})
        self.QuizNextQuestion()

    def QuizResetAnswerButton(self):
        for i in range(4):
            self.rdBtnAns[i].config(disabledforeground='black')
            self.rdBtnAns[i].config(state='normal')
            self.choice.set('-1')
            self.correctAns = -1

    def QuizPreviousQuestion(self):
        if self.currentQuestionQuiz==None or self.currentQuestionQuiz == 0:
            return
        self.currentQuestionQuiz-=1
        image_path_tmp = f'{ self.etSavePath.get() }/{ self.etLoadedFileName.get().split("] ")[1] }.img/image{ self.image_count - 1 }.png'
        if os.path.exists(image_path_tmp):
            if '<image>' in ''.join(self.questionQuiz[self.currentQuestionQuiz][0].lower().split()):
                self.image_count -= 1
        self.QuizTabLoadContent()

    def QuizNextQuestion(self):
        if (self.currentQuestionQuiz==None) or (self.currentQuestionQuiz == self.question_quiz_num - 1):
            return
        self.currentQuestionQuiz+=1
        image_path_tmp = f'{ self.etSavePath.get() }/{ self.etLoadedFileName.get().split("] ")[1] }.img/image{ self.image_count + 1 }.png'
        if os.path.exists(image_path_tmp):
            if '<image>' in ''.join(self.questionQuiz[self.currentQuestionQuiz][0].lower().split()):
                self.image_count += 1
        self.QuizTabLoadContent()

    def QuizJumpQuestionWithList(self, event):
        self.currentQuestionQuiz = self.lsQuestion.curselection()[0]
        self.QuizTabLoadContent()

    def QuizSubmit(self):
        count = 0
        for i, ques in enumerate(self.questionQuiz):
            if ques[6] == 0:
                self.lsQuestion.itemconfig(i,{'bg':'yellow', 'fg': 'black'})
                continue
            if ques[5] == ques[7]:
                count+=1
                self.lsQuestion.itemconfig(i,{'bg':'green', 'fg': 'white'})
            else:
                self.lsQuestion.itemconfig(i,{'bg':'red', 'fg': 'white'})
        self.varShowAnswer.set('1')
        # If answer is correct
        if (int(self.choice.get()) == self.correctAns):
            self.rdBtnAns[self.correctAns].config(disabledforeground='green')
        # If not
        else:
            self.rdBtnAns[self.correctAns].config(disabledforeground='green')
            self.rdBtnAns[int(self.choice.get())].config(disabledforeground='red')
        tkmsgbox.showinfo('Score', f'{count}/{self.maxQuestionQuiz}')

    ##############################################
    ### SETTING TAB ##############################
    ##############################################
    def SettingTab(self):
        self.frSetting = tk.Frame(self.frSettingTab, width=self.layout['winWidth'], height=self.layout['winHeight'])
        self.frSetting.grid(row=0, column=0, sticky='news')

        self.btnDefaultSave = tk.Button(self.frSetting, text='  Default  ', font=('Arial', self.layout['genFontSize']), command=self.SettingTabDefaultSave)
        self.btnDefaultSave.grid(row=0, column=0, padx=40, pady=(30, 50))
        self.btnSave = tk.Button(self.frSetting, text='    Save    ', font=('Arial', self.layout['genFontSize']), command=self.SettingTabSave)
        self.btnSave.grid(row=0, column=1, padx=40, pady=(30, 50))
        self.btnRefresh = tk.Button(self.frSetting, text='  Refresh  ', font=('Arial', self.layout['genFontSize']), command=self.SettingTabRefresh)
        self.btnRefresh.grid(row=0, column=2, padx=(10, 40), pady=(30, 50), sticky='e')

        self.lbWinWidth = tk.Label(self.frSetting, text='Window width: ', font=('Arial', self.layout['genFontSize']))
        self.lbWinWidth.grid(row=1, column=0, padx=(40, 10), pady=10, sticky='w')
        self.etWinWidth = tk.Entry(self.frSetting, font=('Arial', self.layout['genFontSize']))
        self.etWinWidth.grid(row=1, column=1, padx=10)
        self.etWinWidth.insert(0, str(self.layout['winWidth']))
        self.lbWinHeight = tk.Label(self.frSetting, text='Window height: ', font=('Arial', self.layout['genFontSize']))
        self.lbWinHeight.grid(row=2, column=0, padx=(40, 10), pady=10, sticky='w')
        self.etWinHeight = tk.Entry(self.frSetting, font=('Arial', self.layout['genFontSize']))
        self.etWinHeight.grid(row=2, column=1, padx=10)
        self.etWinHeight.insert(0, str(self.layout['winHeight']))

        self.lbQuizFontSize = tk.Label(self.frSetting, text='Quiz font size: ', font=('Arial', self.layout['genFontSize']))
        self.lbQuizFontSize.grid(row=3, column=0, padx=(40, 10), pady=10, sticky='w')
        self.etQuizFontSize = tk.Entry(self.frSetting, font=('Arial', self.layout['genFontSize']))
        self.etQuizFontSize.grid(row=3,column=1, padx=10)
        self.etQuizFontSize.insert(0, str(self.layout['quizFontSize']))

        self.lbGenFontSize = tk.Label(self.frSetting, text='General font size: ', font=('Arial', self.layout['genFontSize']))
        self.lbGenFontSize.grid(row=4, column=0, padx=(40, 10), pady=10, sticky='w')
        self.etGenFontSize = tk.Entry(self.frSetting, font=('Arial', self.layout['genFontSize']))
        self.etGenFontSize.grid(row=4,column=1, padx=10)
        self.etGenFontSize.insert(0, str(self.layout['genFontSize']))

        self.lbSavePath = tk.Label(self.frSetting, text='Save path: ', font=('Arial', self.layout['genFontSize']))
        self.lbSavePath.grid(row=5, column=0, padx=(40, 10), pady=10, sticky='w')
        self.etSavePath = tk.Entry(self.frSetting, font=('Arial', self.layout['genFontSize']))
        self.etSavePath.grid(row=5, column=1, padx=10)
        self.etSavePath.insert(0, self.layout['savePath'])
        self.btnSavePath = tk.Button(self.frSetting, text='  Browse...  ', font=('Arial', self.layout['genFontSize']), command=self.SettingTabSetSavePath)
        self.btnSavePath.grid(row=5, column=2, padx=(10, 40), sticky='e')

        self.lbResult = tk.Label(self.frSetting, text='', font=('Arial', self.layout['genFontSize']))
        self.lbResult.grid(row=6, column=0, columnspan=2, pady=30)

    def SettingTabDefaultSave(self):
        self.etWinWidth.delete(0, tk.END)
        self.etWinWidth.insert(0, str(900))
        self.etWinHeight.delete(0, tk.END)
        self.etWinHeight.insert(0, str(500))
        self.etQuizFontSize.delete(0, tk.END)
        self.etQuizFontSize.insert(0, str(13))
        self.etGenFontSize.delete(0, tk.END)
        self.etGenFontSize.insert(0, str(13))
        self.etSavePath.delete(0, tk.END)
        self.etSavePath.insert(0, './data')


    def SettingTabSave(self):
        t = Thread(target=self.SettingTabSaveInternal)
        t.setDaemon(True)
        t.start()

    def SettingTabSaveInternal(self):
        self.SettingTabChangeSavePath()
        self.SettingTabChangeWindowSize()
        self.SettingTabChangeQuizFontSize()
        self.SettingTabChangeGenFontSize()
        with open('layout.conf', 'wt') as f:
            f.write(json.dumps(self.layout))
        self.lbResult.config(text='Saved!')
        time.sleep(3)
        self.lbResult.config(text='')
        exit(0)

    def SettingTabRefresh(self):
        t = Thread(target=self.SettingTabRefreshInternal)
        t.setDaemon(True)
        t.start()

    def SettingTabRefreshInternal(self):
        self.etWinWidth.delete(0, tk.END)
        self.etWinWidth.insert(0, str(self.layout['winWidth']))
        self.etWinHeight.delete(0, tk.END)
        self.etWinHeight.insert(0, str(self.layout['winHeight']))
        self.etQuizFontSize.delete(0, tk.END)
        self.etQuizFontSize.insert(0, str(self.layout['quizFontSize']))
        self.etGenFontSize.delete(0, tk.END)
        self.etGenFontSize.insert(0, str(self.layout['genFontSize']))
        self.etSavePath.delete(0, tk.END)
        self.etSavePath.insert(0, str(self.layout['savePath']))
        self.lbResult.config(text='Refreshed!')
        time.sleep(3)
        self.lbResult.config(text='')
        exit(0)

    def SettingTabChangeWindowSize(self):
        try:
            self.layout['winWidth'] = int(self.etWinWidth.get())
        except:
            tkmsgbox.showerror(title='Window width', message=f'Cannot convert "{self.etWinWidth.get()}" to number')
            return
        try:
            self.layout['winHeight'] = int(self.etWinHeight.get())
        except:
            tkmsgbox.showerror(title='Window height', message=f'Cannot convert "{self.etWinHeight.get()}" to number')
            return
        self.root.geometry(f"{self.layout['winWidth']}x{self.layout['winHeight']}")

    def SettingTabChangeQuizFontSize(self):
        try:
            self.layout['quizFontSize'] = int(self.etQuizFontSize.get())
        except:
            tkmsgbox.showerror(title='Quiz font size', message=f'Cannot convert "{self.etQuizFontSize.get()}" to number')
            return
        self.lbQues.config(font=('Arial', self.layout['quizFontSize']))
        for i in range(4):
            self.rdBtnAns[i].config(font=('Arial', self.layout['quizFontSize']))

    def SettingTabChangeGenFontSize(self):
        try:
            self.layout['genFontSize'] = int(self.etGenFontSize.get())
        except:
            tkmsgbox.showerror(title='General font size', message=f'Cannot convert "{self.etGenFontSize.get()}" to number')
            return
        self.lbImportFrom.config(font=('Arial', self.layout['genFontSize']))
        self.etImportFrom.config(font=('Arial', self.layout['genFontSize']))
        self.btnImportFrom.config(font=('Arial', self.layout['genFontSize']))
        self.btnImport.config(font=('Arial', self.layout['genFontSize']))
        self.lsLoadedFile.config(font=('Arial', self.layout['genFontSize']))
        self.btnLoadFile.config(font=('Arial', self.layout['genFontSize']))
        self.lbLoadedFile.config(font=('Arial', self.layout['genFontSize']))
        self.etLoadedFileName.config(font=('Arial', self.layout['genFontSize']))
        self.lbShowAnswer.config(font=('Arial', self.layout['genFontSize']))
        self.rdBtnShowAnswerYes.config(font=('Arial', self.layout['genFontSize']))
        self.rdBtnShowAnswerNo.config(font=('Arial', self.layout['genFontSize']))
        self.lbRandomOrder.config(font=('Arial', self.layout['genFontSize']))
        self.rdBtnRandomOrderNo.config(font=('Arial', self.layout['genFontSize']))
        self.rdBtnRandomOrderYes.config(font=('Arial', self.layout['genFontSize']))
        self.lbMode.config(font=('Arial', self.layout['genFontSize']))
        self.cbbMode.config(font=('Arial', self.layout['genFontSize']))
        self.lbNumOfQues.config(font=('Arial', self.layout['genFontSize']))
        self.etNumOfQues.config(font=('Arial', self.layout['genFontSize']))
        self.lbPart.config(font=('Arial', self.layout['genFontSize']))
        self.cbbPart.config(font=('Arial', self.layout['genFontSize']))
        self.btnStart.config(font=('Arial', self.layout['genFontSize']))
        self.btnSetNumOfQues.config(font=('Arial', self.layout['genFontSize']))

        self.btnDefaultSave.config(font=('Arial', self.layout['genFontSize']))
        self.btnSave.config(font=('Arial', self.layout['genFontSize']))
        self.btnRefresh.config(font=('Arial', self.layout['genFontSize']))
        self.lbWinWidth.config(font=('Arial', self.layout['genFontSize']))
        self.etWinWidth.config(font=('Arial', self.layout['genFontSize']))
        self.lbWinHeight.config(font=('Arial', self.layout['genFontSize']))
        self.etWinHeight.config(font=('Arial', self.layout['genFontSize']))
        self.lbQuizFontSize.config(font=('Arial', self.layout['genFontSize']))
        self.etQuizFontSize.config(font=('Arial', self.layout['genFontSize']))
        self.lbGenFontSize.config(font=('Arial', self.layout['genFontSize']))
        self.etGenFontSize.config(font=('Arial', self.layout['genFontSize']))
        self.lbSavePath.config(font=('Arial', self.layout['genFontSize']))
        self.etSavePath.config(font=('Arial', self.layout['genFontSize']))
        self.btnSavePath.config(font=('Arial', self.layout['genFontSize']))

        self.left_btn.config(font=('Arial', self.layout['genFontSize']))
        self.right_btn.config(font=('Arial', self.layout['genFontSize']))
        self.submit_btn.config(font=('Arial', self.layout['genFontSize']))

        self.lbResult.config(font=('Arial', self.layout['genFontSize']))
        self.lsQuestion.config(font=('Arial', self.layout['genFontSize']))

    def SettingTabChangeSavePath(self):
        path = self.etSavePath.get()
        if not path:
            self.etSavePath.delete(0, tk.END)
            self.etSavePath.insert(0, self.layout['savePath'])
            tkmsgbox.showerror('Save path', 'Invalid path')
            return
        if not os.path.exists(path):
            tkmsgbox.showerror("Save path", 'Folder does not exist ' + path)
            self.etSavePath.delete(0, tk.END)
            self.etSavePath.insert(0, self.layout['savePath'])
            return
        self.layout['savePath'] = path

    def SettingTabSetSavePath(self):
        new_path = tkfiledialog.askdirectory()
        if new_path:
            self.etSavePath.delete(0, tk.END)
            self.etSavePath.insert(0, new_path)


