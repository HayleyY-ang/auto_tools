#coding=utf-8
#%%
import os 
import re
import pandas as pd


# auto correct paper choise/gap
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
        student_grades = pd.DataFrame(columns=['student_id','student_name','student_computernum','test_id','choise_score','gap_score'])
        for ii in range(self.testnum):
            files = testfile[ii]
            choise_answer_right = self.answer_dict[self.testidlist[ii]]['choise_answer']
            gap_answer_right = self.answer_dict[self.testidlist[ii]]['gap_answer']
            for i in files:
                try:
                    print(i)
                    f = open(i,'r',encoding='gbk')
                    answers = ''.join(f.readlines()).split('==============================================')
                    if len(answers)==9:
                        pass
                    else:
                        f = open(i,'r',encoding='gbk')
                        answers = re.split('================+',''.join(f.readlines()))
                    student_id = re.findall('(\d+)\n',answers[0])[0]
                    student_name = re.findall('姓名：(.*?)\n',answers[0])[0]
                    student_computernum = re.findall('机号：(.*?)\n',answers[0])[0]
                    choise_answer = answers[3].strip().split('\n')
                    choise_score = 0
                    for choise in choise_answer:
                        q_num = int(re.findall('\d+',choise)[0])
                        q_ans = re.findall('[a-zA-Z]',choise)[0]
                        if q_ans.lower() ==choise_answer_right[q_num-1]:
                            choise_score+=2
                    # 填空题部分给分偏松
                    gap_answer = answers[5].strip().split('\n')
                    gap_score = 0
                    for gap in gap_answer:
                        q_num = int(re.findall('\d+',gap)[0])
                        q_ans = re.findall('\d+\.(.*)',gap)[0]
                        if q_ans.lower()==gap_answer_right[q_num] or gap_answer_right[q_num] in q_ans.lower():
                            gap_score+=3
                        elif len(set(q_ans.lower()).intersection(gap_answer_right[q_num]))/len(set(gap_answer_right[q_num]))>=0.8:
                            gap_score+=3
                        elif len(set(q_ans.lower()).intersection(gap_answer_right[q_num]))/len(set(gap_answer_right[q_num]))>=0.5:
                            gap_score+=1.5
                    stu_info = {'student_id':student_id,'student_name':student_name,'student_computernum':student_computernum,'test_id':self.testidlist[ii],'choise_score':choise_score,'gap_score':gap_score}
                    student_grades = student_grades.append(stu_info,ignore_index=True)
                except Exception as e:
                        wrong_files.append(i)
        student_grades['choise_gap_score'] = student_grades['choise_score']+student_grades['gap_score']
        return student_grades,wrong_files


if __name__ == '__main__':
    # 输入答案，文件地址
    # 答案全部小写
    answers_dict = {'3':{'choise_answer':'dbbcabbacbcbccdbcbba','gap_answer':{1:'count(*)',2:'datetime',3:'update',4:'after',5:'fulltext',6:'关系',7:'整数',8:'李%',9:'数据库',10:'rename'}},'4':{'choise_answer':'dcccccbbccbddbacbcbd','gap_answer':{1:'delete',2:'关系',3:'drop',4:'month(test_date) in (1,3,7)',5:'set price=price*1.2',6:'drop index',7:'modify',8:'非空',9:'max(price)',10:'limit'}}}
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
