import tkinter.messagebox as tkmsgbox
import os
import json
import random
try:
    import xlwings as xw
except Exception as e:
    os.system('pip install xlwings')
    import xlwings as xw
try:
    import docx2txt
except Exception as e:
    os.system('pip install docx2txt')
    import docx2txt

def GetExtension(path):
    return path.split('.')[-1]

def GetFileName(path):
    return path.split('/')[-1]

def ImportFromExcelFile(source, dest):
    try:
        excel_app = xw.App(visible=False)
        ws = excel_app.books.open(source).sheets[0]
    except Exception as e:
        excel_app.quit()
        return 0, e
    try:
        i = 0
        ques = {'quantity': 0, 'collection': []}
        while True:
            datas = ws.range(f'A{i+1}:F{i+1}').value
            if datas == [None]*6:
                break
            ques['collection'].append(datas[:5])
            ques['collection'][i].append(int(datas[5]) - 1)
            i+=1
        excel_app.quit()
        ques['quantity'] = i
        with open(dest + '/' + GetFileName(source).split('.')[0], 'wt') as f:
            f.write(json.dumps(ques))
        return 1, GetFileName(source).split('.')[0]
    except Exception as e:
        excel_app.quit()
        return 0, e

def ImportFromDocFile(source, dest):
    try:
        datas = docx2txt.process(source).split('\n')
    except Exception as e:
        return 0, e
    try:
        i = 0
        ques = {'quantity': 0, 'collection': []}
        q = ''
        ans = ['']*4
        correctAns = -1
        while i<len(datas):
            while datas[i].strip()=='':
                i+=1
            q = datas[i].strip()
            # print(q)
            i+=1
            while datas[i].strip()=='':
                i+=1
            ans[0] = datas[i].strip()
            # print(ans[0])
            i+=1
            while datas[i].strip()=='':
                i+=1
            ans[1] = datas[i].strip()
            # print(ans[1])
            i+=1
            while datas[i].strip()=='':
                i+=1
            ans[2] = datas[i].strip()
            # print(ans[2])
            i+=1
            while datas[i].strip()=='':
                i+=1
            ans[3] = datas[i].strip()
            # print(ans[3])
            i+=1
            while datas[i].strip()=='':
                i+=1
            correctAns = int(datas[i].strip()) - 1
            # print(correctAns)
            i+=1

            ques['collection'].append([q, ans[0], ans[1], ans[2], ans[3], correctAns])
            q = ''
            ans = ['']*4
            correctAns = -1
        ques['quantity'] = len(ques['collection'])
        with open(dest + '/' + GetFileName(source).split('.')[0], 'wt') as f:
            f.write(json.dumps(ques))
        return 1, GetFileName(source).split('.')[0]
    except Exception as e:
        return 0, e

def ImportFromFile(source, dest):
    source = source.strip()
    if not os.path.exists(source):
        return 0, 'No such file or directory: \'' + source + '\''
    if GetExtension(source) == 'xlsx' or GetExtension(source) == 'csv' or GetExtension(source) == 'xls':
        return ImportFromExcelFile(source, dest)
    elif GetExtension(source) == 'docx':
        return ImportFromDocFile(source, dest)
    else:
        return 0, 'Extension .' + GetExtension(source) + ' does not supported'

# 1 part = <part index> * <number of question>
def GenStaticQuestion(loadFileName, part, maxQuestionQuiz):
    with open(loadFileName, 'rt') as f:
        datas = json.loads(f.read())
    # print(loadFileName, part, maxQuestionQuiz)
    ques = []
    for i, quesi in enumerate(range(part*maxQuestionQuiz, part*maxQuestionQuiz + maxQuestionQuiz)):
        if quesi>=len(datas['collection']):
            break
        ques.append([])
        for ele in datas['collection'][quesi]:
            ques[i].append(ele)
        ques[i].append(0)           # isSolved
        ques[i].append(-1)          # userAnswer
    return ques


# 1 part = <number of question random>
def GenDynamicQuestion(loadFileName, maxQuestionQuiz):
    with open(loadFileName, 'rt') as f:
        datas = json.loads(f.read())
    ques = []
    for _ in range(maxQuestionQuiz):
        if len(datas['collection']) == 0:
            break
        ques.append([])
        i = random.choice(range(len(datas['collection'])))
        for ele in datas['collection'][i]:
            ques[-1].append(ele)
        ques[-1].append(0)           # isSolved
        ques[-1].append(-1)          # userAnswer
        del datas['collection'][i]
    return ques