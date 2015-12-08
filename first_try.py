#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from time import sleep
import codecs

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

EMAIL = ''
PS = ''

# open firefox and jump to douban
driver = webdriver.Firefox()
driver.get('http://read.douban.com/reader/ebooks')

# this didn't work because everytime after login,
# douban will send a uuid back such that I can
# get whole artical.
# Need work this out.

# find email and password input
sleep(5)
form_email = driver.find_element_by_css_selector('input#email')
form_email.clear()
form_email.send_keys(EMAIL)

form_passwd = driver.find_element_by_css_selector('input#password')
form_passwd.clear()
form_passwd.send_keys(PS)
sleep(10)
form_passwd.send_keys(Keys.RETURN)

sleep(20)
# jump to target book
driver.get('http://read.douban.com/reader/ebooks')
sleep(20)
driver.get('http://read.douban.com/reader/ebook/9718059/')

# move to fist page
try:
    arkicon_list = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "arkicon-list"))
    )
    sleep(10)
    arkicon_list.click()
except Exception, e:
    print 1,e
    driver.close()
    sys.exit(-1)

try:
    page_1 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "page-173"))
    )
    sleep(10)
    page_1.click()
except Exception, e:
    print 2, e
    driver.close()
    sys.exit(-1)

while True:
    sleep(1.5)
    try:
        current_page = driver.find_element_by_class_name('curr-page')
        need_buy = current_page.find_element_by_class_name('rating-form')
        print 3,e
        break
    except NoSuchElementException, e:
        pass
    
    # Try to get element from each page
    try:
        one_page = []
        current_page = driver.find_element_by_class_name('curr-page')
        content = current_page.find_element_by_class_name('content')
        prs = content.find_elements_by_tag_name('p')
        for pr in prs:
            l = []
            for word in pr.find_elements_by_css_selector('span.word'):
                l.append(word.text)
            one_page.append(''.join(l))
        with codecs.open('text.txt', 'a+', 'utf-8') as f:
            print '\n'.join(one_page)
            f.write('\n'.join(one_page))
            
    except NoSuchElementException, e:
        print 4
        pass
    
    next_page = driver.find_element_by_class_name('page-next')
    sleep(0.5)
    next_page.click()

driver.close()
        
        
