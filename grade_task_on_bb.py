# coding = utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys
#%%
user_name = '20349057'
password = '066842yhl'


driver = webdriver.Chrome()
driver.maximize_window()
#%%
driver.get('https://bb.suibe.edu.cn/')

# # switch to log page
# driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div[1]/div/div[1]/form/div[1]/div[2]').click()
#%%
# input the log info
driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div/div[3]/div/form/p[1]/input').send_keys(user_name)
driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div/div[3]/div/form/p[2]/input').send_keys(password)
#%%
# simulate click log
driver.find_element(By.XPATH,'//*[@id="casLoginForm"]/p[5]/button').click()
#%%
driver.find_element(By.XPATH,'//*[@id="login"]/table/tbody/tr[1]/td/img').click()
#%%
driver.find_element(By.XPATH,'//*[@id="_3_1termCourses_noterm"]/ul[2]/li[1]/a').click()
driver.find_element(By.XPATH,'//*[@id="menuPuller"]').click()
driver.find_element(By.XPATH,'//*[@id="controlpanel.grade.center_groupExpanderLink"]').click()
driver.find_element(By.XPATH,'//*[@id="controlpanel.grade.center_groupContents"]/li[4]/a').click()

#%%
Drag = driver.find_element(By.XPATH,'//*[@id="table1_container"]/div[2]')
ActionChains(driver).drag_and_drop_by_offset(Drag,0, 0.5).perform()
# for i in range(1):
#     Drag = driver.find_element_by_class_name("jspDrag") #找到滚动条
#     #控制滚动条的行为，每次向y轴(及向下)移动10个单位
#     ActionChains(driver).drag_and_drop_by_offset(Drag, 0, 50).perform()


#%%
score = 100
flag = 0
flag_1 = 0
for i in range(200):
    try:
        if i>=9:
            i = 9
        path0 = f'//*[@id="cell_{i}_8"]/div/div[1]/div[2]/a/img'
        path1 = f'//*[@id="cell_{i}_8"]'
        path2 = f'//*[@id="cell_{i}_8"]/div/div[2]/input'
        info = driver.find_element(By.XPATH,path0)
        if info.get_attribute('title') == '需要评分':
            print('scoring successful')
            if flag<10:
                time.sleep(0.5)
                driver.find_element(By.XPATH, path1).click()
            time.sleep(0.5)
            driver.find_element(By.XPATH,path2).send_keys(score)
            driver.find_element(By.XPATH,path2).send_keys(Keys.ENTER)
    except Exception as e:
        flag_1+=1
        print(i)
        print(e)
    if flag_1>=20:
        break
    flag += 1
