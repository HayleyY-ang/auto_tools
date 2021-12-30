#coding=utf-8
#%%
import os 
import re
import pandas as pd

#%%
# auto correct paper 
class ACPCG:

    def __init__(self,file,answer_dict):    
        self.file = file
        self.answer_dict = answer_dict
        self.testnum = len(answer_dict)
        self.testidlist = list(answers_dict.keys())


    def walkFile(self):
        testfile = [[] for i in range(self.testnum)]
        for root,dirs,files in os.walk(self.file):
            flag = 0
            for f in files:
                if flag !=0:
                    idx = self.testidlist.index(flag)
                    testfile[idx].append(os.path.join(root,f))     
                try:
                    flag = re.search('\d',f).group(0)
                except:
                    pass
        return testfile

    def correct_paper(self,testfile):
        wrong_files = []
        student_grades = pd.DataFrame(columns=['student_id','student_name','student_computernum','test_id','choise_score','judge_score','correct_score','choose_gap_score','query_score','total_score'])
        for ii in range(self.testnum):
            files = testfile[ii]
            choise_answer_right = self.answer_dict[self.testidlist[ii]]['choise_answer']
            judge_answer_right = self.answer_dict[self.testidlist[ii]]['judge']
            correct_answer_right = self.answer_dict[self.testidlist[ii]]['correct']
            choose_gap_answer_right = self.answer_dict[self.testidlist[ii]]['choose_gap']
            query_answer_right = self.answer_dict[self.testidlist[ii]]['query']
            for i in files:
                try:
                    print(i)
                    f = open(i,'r',encoding='gbk')
                    answers = ''.join(f.readlines()).split('==============================================')
                    if len(answers)==13:
                        pass
                    else:
                        f = open(i,'r',encoding='gbk')
                        answers = re.split('================+',''.join(f.readlines()))
                    try:
                        student_id = re.findall('(\d+)\n',answers[0])[0]
                        student_name = re.findall('姓名：(.*?)\n',answers[0])[0]
                        student_computernum = re.findall('B\d+',i)[0]
                    except:
                        student_id = None
                        student_name = None
                        student_computernum = re.findall('B\d+',i)[0]
                    # choise
                    choise_answer = answers[3].strip().split('\n')
                    choise_score = 0
                    for choise in choise_answer:
                        try:
                            q_num = int(re.findall('\d+',choise)[0])
                            q_ans = re.findall('[a-zA-Z]',choise)[0]
                            if q_ans.lower() ==choise_answer_right[q_num-1]:
                                choise_score+=2
                        except:
                            pass
                    
                    # judge
                    judge_answer = answers[5].strip().split('\n')
                    judge_score = 0
                    for ans in judge_answer:
                        try:
                            q_num = int(re.findall('\d+',ans)[0])
                            q_ans = re.findall('\d+\.(.*)',ans)[0]
                            if q_ans.lower()==judge_answer_right[q_num-1]:
                                judge_score+=3
                        except:
                            pass

                    # correct
                    correct_answer = answers[7].strip().split('\n')
                    correct_score = 0
                    for ans in correct_answer:
                        try:
                            q_num = int(re.findall('\d+',ans)[0])
                            q_ans = re.findall('\d+\.(.*)',ans)[0]
                            if q_num == 1:
                                correct_score+=2
                            else:
                                if  q_ans.lower()==correct_answer_right[q_num]:
                                    correct_score+=2
                        except:
                            pass
                    # choose_gap
                    choose_gap_answer = answers[9].strip().split('\n')
                    choose_gap_score = 0
                    for ans in choose_gap_answer:
                        try:
                            q_num = int(re.findall('\d+',ans)[0])
                            q_ans = re.findall('\d+\.(.*)',ans)[0]
                            if q_ans.lower()==choose_gap_answer_right[q_num-1]:
                                choose_gap_score+=2  
                        except:
                            pass
                    # query
                    query_answer = answers[11].strip().split('\n')
                    query_score = 0
                    for ans in query_answer:
                        try:
                            q_num = int(re.findall('\d+',ans)[0])
                            q_ans = re.findall('\d+\.(.*)',ans)[0]
                            if q_num ==3:
                                if q_ans.lower()==query_answer_right[q_num]:
                                    query_score+=3
                            else: 
                                if q_ans==query_answer_right[q_num]:
                                    query_score+=3  
                        except:
                            pass
                    
                    total_score = choise_score+judge_score+correct_score+choose_gap_score+query_score

                    stu_info = {'student_id':student_id,'student_name':student_name,'student_computernum':student_computernum,'test_id':self.testidlist[ii],'choise_score':choise_score,'judge_score':judge_score,'correct_score':correct_score,'choose_gap_score':choose_gap_score,'query_score':query_score,'total_score':total_score}
                    student_grades = student_grades.append(stu_info,ignore_index=True)
                except Exception as e:
                        wrong_files.append(i)
        return student_grades,wrong_files
# student_grade,wrong_files = auto_cor.correct_paper(testfile)


#%%
# if __name__ == '__main__':
    # 输入答案，文件地址
    # 答案全部小写
answers_dict = {'1':{'choise_answer':['b','c','b','d','d','d','b','b','c','c','b','c','c','b','c','abc','abd','abcd','bcd','acd'],'judge':'ttttft','correct':{1:'group',2:'modify',3:'drop',4:'root',5:'on',6:'exists'},'choose_gap':'kpfmjo','query':{1:48000,2:280,3:'浙江',4:6,5:13,6:14}}}
filepath = 'C:\\Users\HAYLEY\Desktop\批卷子'
# 初始化，支持计算超过两批试卷
auto_cor = ACPCG(filepath,answers_dict)
# 得到答题卡路径，不同批卷子分别存放在不同列表中
testfile = auto_cor.walkFile()

student_grade,wrong_files = auto_cor.correct_paper(testfile)
student_grade = student_grade.sort_values(by='student_id')
student_grade.to_excel(filepath+'\\student_grade.xlsx')
print('以下答题卡格式出错需要手动批阅：\n',wrong_files)













# %%
