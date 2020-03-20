#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Contains functions used in analyzing data from KhanAcademy.org

    There are two approaches to analyzing the data. The functions for both approaches are in this file.

    (1) This one works: Copy and paste scores to a text file. Because pasting produces text formatted in a consistent pattern, it can be converted into a table. Then the analysis is easy.
    (2) This one is not fully implement. A totally programmatic approach is difficult because expanding certain webpage elements cannot be simulated. If this could be overcome, then scraping the site would be easy.
        2.1 This workflow should be encased in a "with driver as driver" block
        2.2 Expanding does not seem to be a function of page loading times. Wait for page to load: http://www.seleniumhq.org/docs/04_webdriver_advanced.jsp
'''

import requests, sys, time, webbrowser #, winsound
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from io import BytesIO
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait


########################################################################
### Universal variables ################################################
########################################################################

rootUrl = u'https://www.khanacademy.org'
UserAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0)'+\
            ' Gecko/20100101 Firefox/56.0'
Headers = { 'User-Agent': UserAgent}
dxpaths = {'unitsxpath' : '//span[contains(.,\'Unit\')]/../span[@class="_g20yn58"]/text()',\
           'lessonsxpath' : '//span[contains(.,\'Lesson\')]/../span[@class="_g20yn58"]/text()',\
           'exercisesxpath' : '//span[contains(.,\'Exercise\')]/../span[@class="_14bmcy4r"]/text()',\
           'unitsNodexpath' : '//span[contains(.,\'Unit\')]/../span[@class="_g20yn58"]'}

########################################################################
### Functions ##########################################################
########################################################################

def expandHtml():
    '''
    Not working.

    This is hard to do, because sometimes if you do it too fast it won't expand, and sometimes the page needs ot be refreshed. It's hard to simulate real clicking behavior. It usually gets stuck after expanding the second unit.
    '''
    driver = webdriver.Safari()
    driver.maximize_window() # has to do this first for some reason before resizing
    size = driver.get_window_size()
    wMax = size['width']
    hMax = size['height']
    wNew = int(wMax / 2)
    # hNew = int(hMax / 2)
    driver.set_window_size(wNew,hMax) # half screen
    height = 250
    driver.execute_script(f'window.scrollTo(0, {height})')

    loginBranch = '/login?continue=%2F'
    loginUrl = rootUrl + loginBranch

    driver.get(loginUrl)

    emailxpath = '//*[@id="uid-identity-text-field-0-email-or-username"]'
    email = driver.find_element_by_xpath(emailxpath)
    passwordxpath = '//*[@id="uid-identity-text-field-1-password"]'
    password = driver.find_element_by_xpath(passwordxpath)

    email.send_keys("hf.autore@gmail.com")
    if False:
        password.send_keys("fehxok-xicci1-vocRyx" + Keys.RETURN)
    elif True:
        wait = WebDriverWait(driver, 10)
        password.send_keys("fehxok-xicci1-vocRyx" + Keys.RETURN)
        xpathWait = '//div[@class="_o77ufew"]'
        wait.until(presence_of_element_located((By.XPATH, xpathWait)))

    coachBranch = '/coach/dashboard'
    classBranch = '/coach/class/5816402088837120'
    assignBranch = '/coach/class/5816402088837120/create-assignments'
    url = rootUrl + assignBranch
    driver.get(url)
    # html length depends on if expandable elements are expanded. I will have to loop through everything and .click() them
    unitsxpath = '//span[contains(.,\'Unit\')]/../span[@class="_g20yn58"]/text()'
    wait.until(lambda driver: len(driver.find_elements_by_xpath(unitsxpath)) == 16)
    html = driver.page_source # fully loaded html length with all elements expanded should be approx. 173025

    units = getUnits(html) # Should do this natively in Selenium

    # Expand each unit
    unitsNodexpath = dxpaths['unitsNodexpath']
    unitEls = driver.find_elements_by_xpath(unitsNodexpath)
    for elUnit in unitEls:
        elUnit.click()
        # gets stuck after expanding second unit
        # actions = ActionChains(driver)
        # actions.move_to_element(elUnit).perform()

    expandedHtml = driver.page_source

    return expandedHtml

def getUnits(html, dxpaths=dxpaths):
    # Initialize xpath parser
    htmlasFile = BytesIO(bytes(html,'utf-8'))
    htmlparser = etree.HTMLParser()
    tree = etree.parse(htmlasFile, htmlparser)

    # Find units
    unitsxpath = dxpaths['unitsxpath']
    units = tree.xpath(unitsxpath)

    return units

def getLessons(html, dxpaths=dxpaths):
    # Initialize xpath parser
    htmlasFile = BytesIO(bytes(html,'utf-8'))
    htmlparser = etree.HTMLParser()
    tree = etree.parse(htmlasFile, htmlparser)

    # Find lessons
    lessonsxpath = dxpaths['lessonsxpath']
    lessons = tree.xpath(lessonsxpath)

    return lessons

def getExercises(html, dxpaths=dxpaths):
    # Initialize xpath parser
    htmlasFile = BytesIO(bytes(html,'utf-8'))
    htmlparser = etree.HTMLParser()
    tree = etree.parse(htmlasFile, htmlparser)

    # Find list of exercises
    exercisesxpath = dxpaths['exercisesxpath']
    exercises = tree.xpath(exercisesxpath)

    return exercises

def makeTree(html, dxpaths=dxpaths):
    # Initialize xpath parser
    htmlasFile = BytesIO(bytes(html,'utf-8'))
    htmlparser = etree.HTMLParser()
    tree = etree.parse(htmlasFile, htmlparser)

    # Get units and lessons
    units = getUnits(html)
    lessons = getLessons(html)

    lessonsxpath = dxpaths['lessonsxpath']
    exercisesxpath = dxpaths['exercisesxpath']

    d = {}
    for unit in units:
        d1 = {}
        xpath = f'//span[text()=\"{unit}\"]/../../../div[@class="_xu2jcg"]{lessonsxpath}'
        lessons = tree.xpath(xpath)
        for lesson in lessons:
            xpath = f'//span[text()=\"{lesson}\"]/../../../div[@class="_xu2jcg"]{exercisesxpath}'
            exercises = tree.xpath(xpath)
            d1[lesson] = exercises
        d[unit] = d1

    return d

def printTree(d):
    for k,v in d.items():
        print(k)
        for lesson, exercises in v.items():
            print(f'\t{lesson}')
            for ex in exercises:
                print(f'\t\t{ex}')

def expTree(d, fpath):
    lines = []
    for k,v in d.items():
        lines.append([k,'',''])
        for lesson, exercises in v.items():
            lines.append(['',lesson,''])
            for ex in exercises:
                lines.append(['','',ex])
    df = pd.DataFrame(lines)
    df.to_csv(fpath, sep=',', header=False, index=False)

def tabText(fpath):
    '''
    '''

    with open(fpath, 'r') as f:
        text = f.read()

    l = text.split('\n')

    l = [i for i in l if i] # remove empty stirngs
    l = l[1:] # remove index column header, "Students"
    try:
        numCols = 15 # To-do: determine programmatically. I should find the numbes and endashes first
        # then cut those frmo the string, then, since the number of students is known ahead of time, cut n number of matches starting from the end. What's left are the columns.
        J = numCols*2

        # Create column names, the Khan Academy Assignments
        cols = l[:J]
        cols = np.array(cols)
        cols = cols.reshape((numCols,2))
        date = cols[:,1]
        name = cols[:,0]
        cols = [f'{x} ({y})' for x,y in zip(name,date)]
        I = 70 # To-do: determine programmatically

        # Create row/index names, the Khan Academy Students
        indx = l[J:J+I]

        # Create Pandas DataFrame
        data = np.array(l[J+I:])
        data = data.reshape((I,numCols))
    except ValueError:
        numCols = 13 # To-do: determine programmatically
        J = numCols*2

        # Create column names, the Khan Academy Assignments
        cols = l[:J]
        cols = np.array(cols)
        cols = cols.reshape((numCols,2))
        date = cols[:,1]
        name = cols[:,0]
        cols = [f'{x} ({y})' for x,y in zip(name,date)]
        I = 70 # To-do: determine programmatically

        # Create row/index names, the Khan Academy Students
        indx = l[J:J+I]

        # Create Pandas DataFrame
        data = np.array(l[J+I:])
        data = data.reshape((I,numCols))
    df = pd.DataFrame(data, columns= cols, index= indx, dtype='str')

    # Replace en dashes with NaNs
    endash = '\N{EN DASH}'
    df.replace(endash, '999', inplace=True)
    df = df.astype('float')
    df.replace(999.0, np.nan, inplace=True)

    return df

########################################################################
### End of File ########################################################
########################################################################
