# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 17:01:20 2017

@author: NAVER
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from operator import eq

import time

receiver = "test_lee3@naver.com"
sender = "test_lee2@naver.com"

receiverId  = "test_lee3"
senderId = "test_lee2"

receiverPw  = "naver!23"
senderPw = "naver!23"

tmpTime = ""

driver = webdriver.Chrome("C:\selenium\chromedriver.exe")

def logIn(Id, Pw):
    driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[1]/div/a/span").click()
    waitForIsElementPresent("//*[@id='id']")
    
    driver.find_element_by_xpath("//*[@id='id']").send_keys(Id)
    driver.find_element_by_xpath("//*[@id='pw']").send_keys(Pw)
    
    driver.find_element_by_xpath("//*[@id='frmNIDLogin']/fieldset/input").click();
    
    
def logOut():
    driver.find_element_by_xpath("//*[@id='gnb_name1']").click()
    driver.find_element_by_xpath("//*[@id='gnb_logout_button']/span[3]").click()
    
    
def waitForIsElementPresent(xpath):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        print(xpath, "가 존재하지 않습니다.")
        driver.close()
    
    
def basicWriting():
    driver.find_element_by_xpath("//*[@id='toInput']").send_keys(receiver)
    
    time.sleep(1)
    
    driver.find_element_by_xpath("//*[@id='atcp']/ul/li/div/a").click()       
    driver.find_element_by_xpath("//*[@id='subject']").click()  
        
    curTime = time.strftime("%Y%m%d %H%M%S", time.localtime())
    tmpTime = curTime
    
    driver.find_element_by_xpath("//*[@id='subject']").send_keys(curTime)    
    driver.switch_to_frame(driver.find_element_by_xpath("//*[@id='se2_iframe']"))    
    driver.find_element_by_xpath("/html/body").send_keys(curTime)
    
    driver.switch_to_default_content()

# 대화형 메일 만들기
def makeConversation(num):
            
    driver.find_element_by_xpath("//*[@id='nav_snb']/div[1]/a[1]/strong").click()
    waitForIsElementPresent("//*[@id='toInput']")
           
    basicWriting()           
       
    driver.find_element_by_xpath("//*[@id='sendBtn']").click()
    
    waitForIsElementPresent("//*[@id='sendresultDivContent']/div[2]/h4")
    comment = driver.find_element_by_xpath("//*[@id='sendresultDivContent']/div[2]/h4").text
       
    assert eq(comment, "메일을 성공적으로 보냈습니다.")
    
    i = 0
    
    while num > i:
       
        logOut()
        waitForIsElementPresent("//*[@id='container']/div/div[2]/div[1]/div/a/span")
        
        if i%2 == 0:
            logIn(receiverId, receiverPw)
        else:
            logIn(senderId, senderPw)
        
        driver.find_element_by_xpath("//*[@id='nav_snb']/div[3]/div/div[1]/ul/li[1]/span/a[1]").click()
        
        waitForIsElementPresent("//*[@id='list_for_view']/ol/li[1]/div/div[2]")        
        driver.find_element_by_xpath("//*[@id='list_for_view']/ol/li[1]/div/div[2]").click()
       
        waitForIsElementPresent("//*[@id='readBtnMenu']/div[1]/span[1]/button[1]")
        driver.find_element_by_xpath("//*[@id='readBtnMenu']/div[1]/span[1]/button[1]").click()
        
        time.sleep(1)   
        driver.find_element_by_xpath("//*[@id='sendBtn']").click()
        waitForIsElementPresent("//*[@id='sendresultDivContent']/div[2]/h4")
        comment = driver.find_element_by_xpath("//*[@id='sendresultDivContent']/div[2]/h4").text
        
        
        if eq(comment, "메일을 보내지 못했습니다."):
            driver.find_element_by_xpath("//*[@id='sendresultDivContent']/div[2]/p[2]/a").click()
            waitForIsElementPresent("//*[@id='list_for_view']/ol/li[1]/div/div[2]/a/span/strong")
            driver.find_element_by_xpath("//*[@id='list_for_view']/ol/li[1]/div/div[2]/a/span/strong").click()
            
            time.sleep(1)
            
            driver.find_element_by_xpath("//*[@id='sendBtn']").click()
            
        elif eq(comment, "메일을 성공적으로 보냈습니다."):
            assert eq(comment, "메일을 성공적으로 보냈습니다.")
                
        i = i+1
        time.sleep(1)
    

    
    
driver.get("http://mail.naver.com")  
    
logIn(senderId, senderPw)

makeConversation(10)


driver.close()


    