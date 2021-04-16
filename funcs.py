#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Contains functions used in analyzing data from KhanAcademy.org

    There are two approaches to analyzing the data. The functions for both approaches are in this file.

    (1) This one works: Copy and paste scores to a text file. Because pasting produces text formatted in a consistent pattern, it can be converted into a table. Then the analysis is easy.
    (2) This one is not fully implemented. A totally programmatic approach is difficult because expanding certain webpage elements cannot be simulated. If this could be overcome, then scraping the site would be easy.
        2.1 This workflow should be encased in a "with driver as driver" block
        2.2 Expanding does not seem to be a function of page loading times. Wait for page to load: http://www.seleniumhq.org/docs/04_webdriver_advanced.jsp
'''

import os
import re
import numpy as np
import pandas as pd
from datetime import datetime as dt
from io import BytesIO
from lxml import etree
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait


########################################################################
### Universal variables ################################################
########################################################################

rootUrl = u'https://www.khanacademy.org'
UserAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0)' + \
            ' Gecko/20100101 Firefox/56.0'
Headers = {'User-Agent': UserAgent}
dxpaths = {'unitsxpath': '//span[contains(.,\'Unit\')]/../span[@class="_g20yn58"]/text()',
           'lessonsxpath': '//span[contains(.,\'Lesson\')]/../span[@class="_g20yn58"]/text()',
           'exercisesxpath': '//span[contains(.,\'Exercise\')]/../span[@class="_14bmcy4r"]/text()',
           'unitsNodexpath': '//span[contains(.,\'Unit\')]/../span[@class="_g20yn58"]'}
userDir = str(Path.home())
workDir = f'{userDir}/Documents/kaGrader'

########################################################################
### Functions ##########################################################
########################################################################


def expandHtml():
    '''
    Not working.

    This is hard to do, because sometimes if you do it too fast it won't expand, and sometimes the page needs ot be refreshed. It's hard to simulate real clicking behavior. It usually gets stuck after expanding the second unit.
    '''
    driver = webdriver.Safari()
    driver.maximize_window()  # has to do this first for some reason before resizing
    size = driver.get_window_size()
    wMax = size['width']
    hMax = size['height']
    wNew = int(wMax / 2)
    # hNew = int(hMax / 2)
    driver.set_window_size(wNew, hMax)  # half screen
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

    # coachBranch = '/coach/dashboard'
    # classBranch = '/coach/class/5816402088837120'
    assignBranch = '/coach/class/5816402088837120/create-assignments'
    url = rootUrl + assignBranch
    driver.get(url)
    # html length depends on if expandable elements are expanded. I will have to loop through everything and .click() them
    unitsxpath = '//span[contains(.,\'Unit\')]/../span[@class="_g20yn58"]/text()'
    wait.until(lambda driver: len(driver.find_elements_by_xpath(unitsxpath)) == 16)
    # html = driver.page_source  # fully loaded html length with all elements expanded should be approx. 173025

    # units = getUnits(html)  # Should do this natively in Selenium

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
    htmlasFile = BytesIO(bytes(html, 'utf-8'))
    htmlparser = etree.HTMLParser()
    tree = etree.parse(htmlasFile, htmlparser)

    # Find units
    unitsxpath = dxpaths['unitsxpath']
    units = tree.xpath(unitsxpath)

    return units


def getLessons(html, dxpaths=dxpaths):
    # Initialize xpath parser
    htmlasFile = BytesIO(bytes(html, 'utf-8'))
    htmlparser = etree.HTMLParser()
    tree = etree.parse(htmlasFile, htmlparser)

    # Find lessons
    lessonsxpath = dxpaths['lessonsxpath']
    lessons = tree.xpath(lessonsxpath)

    return lessons


def getExercises(html, dxpaths=dxpaths):
    # Initialize xpath parser
    htmlasFile = BytesIO(bytes(html, 'utf-8'))
    htmlparser = etree.HTMLParser()
    tree = etree.parse(htmlasFile, htmlparser)

    # Find list of exercises
    exercisesxpath = dxpaths['exercisesxpath']
    exercises = tree.xpath(exercisesxpath)

    return exercises


def makeTree(html, dxpaths=dxpaths):
    # Initialize xpath parser
    htmlasFile = BytesIO(bytes(html, 'utf-8'))
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
    for k, v in d.items():
        print(k)
        for lesson, exercises in v.items():
            print(f'\t{lesson}')
            for ex in exercises:
                print(f'\t\t{ex}')


def expTree(d, fpath):
    lines = []
    for k, v in d.items():
        lines.append([k, '', ''])
        for lesson, exercises in v.items():
            lines.append(['', lesson, ''])
            for ex in exercises:
                lines.append(['', '', ex])
    df = pd.DataFrame(lines)
    df.to_csv(fpath, sep=',', header=False, index=False)


def countDueDates(listOfLines):
    '''
    Counts the number of due dates on the assignment.
    '''

    pattern = '^[A-Z]{1}[a-z]{2} [0-9]{0,2}$'
    numColumns = [1 for el in listOfLines if re.search(pattern, el)]
    numColumns = np.array(numColumns).sum()

    return numColumns


def countCells(listOfLines):
    '''
    Counts how many of the values in the list are either ENDASHES or numeric strings. Assumes only cells contain EN DASHES and numeric strings.
    '''

    numCells = np.sum([1 for el in listOfLines if el == '\N{EN DASH}' or el.isnumeric()])

    return numCells


def tabText(fpath):
    '''
    Converts the pasted text from Khan Academy into a table.
    '''

    with open(fpath, 'r') as f:
        text = f.read()

    li = text.split('\n')

    li = [i for i in li if i]  # remove empty strings; This produces a bug when tabulating assignments that have a checkmark since the checkmark is pasted as an empty string. One way to fix it is to replace the "\n" with "\n\N{EN DASH}" in the file by using regex "^\n" after the column header lines. Note that countDueDates and countCells works independent of empty strings, so we can use thouse counts to find where to begin the regex.
    # 2021/03/11: I noticed the empty lines are only made when copying from Safari. Information pasted from Chrome skips the checkmark cells. Also, the regex is find: "^\n", replace: "100\n".
    li = li[1:]  # remove index column header, "Students"

    # Programmatically determine number of columns (assignments) and number of rows (students)
    numColumns = countDueDates(li)
    numCells = countCells(li)
    numColumnsx2 = numColumns * 2
    numStudents = len(li) - numCells - numColumnsx2

    # Create column names, the Khan Academy Assignments with Due Dates
    cols = li[:numColumnsx2]
    cols = np.array(cols)
    cols = cols.reshape((numColumns, 2))
    date = cols[:, 1]
    name = cols[:, 0]
    cols = [f'{x} ({y})' for x, y in zip(name, date)]

    # Create row/index names, the Khan Academy Students
    indx = li[numColumnsx2:numColumnsx2 + numStudents]

    # Create Pandas DataFrame
    data = np.array(li[numColumnsx2 + numStudents:])
    data = data.reshape((numStudents, numColumns))
    df = pd.DataFrame(data, columns=cols, index=indx, dtype='str')

    # Replace en dashes with NaNs
    endash = '\N{EN DASH}'
    df.replace(endash, '999', inplace=True)
    df = df.astype('float')
    df.replace(999.0, np.nan, inplace=True)

    return df


def gradeKAScores(dataPath):
    '''
    Reads text files in the folder "dataPath" and turns them into two tables. The first table contains the KA scores as they appear online, by student and assignment. The second one gives the students' mean score for all assignments that are due by the date the program is run.

    Assumptions:
        This function extracts the year from the raw scores folder and assumes the folder is named in the following format: "kaScores-YYYYmmdd".
    '''

    dirName = os.path.basename(dataPath)
    files = os.listdir(dataPath)
    if '.DS_Store' in files:
        files.pop(files.index('.DS_Store'))

    li = []
    for fname in files:
        fpath = f'{dataPath}/{fname}'
        df = tabText(fpath)
        li.append(df)

    df = pd.concat(li, axis=1)

    ## Sort by due date, because on KA it's sorted by date it was assigned
    cols = df.columns
    d = {}
    li = []
    pattern = r'kaScores-(\d{4})\d{4}'
    year = re.search(pattern, dataPath).groups()[0]
    for c in cols:
        date = re.search(r'\(([a-zA-Z]+ [0-9]+)\)', c).groups()[0]
        datetime = pd.to_datetime(f'{date} {year}', format='%b %d %Y').toordinal()
        d[c] = datetime
        li.append((c, datetime))

    li = sorted(li, key=lambda x: x[1])
    newCols = [t[0] for t in li]
    dates = [t[1] for t in li]
    kaScores = df[newCols]

    ## Save scores as they appear on KA
    fpath = f'{workDir}/kaScores-{dirName}.csv'
    kaScores.to_csv(fpath, sep=',')

    ## Determine indices for items that are due and therefore should be graded
    dates = np.array(dates)
    today = dt.today().toordinal()
    today = [today] * len(dates)
    today = np.array(today)
    dueIndices = np.argwhere(dates < today)

    ## New dataframe with missing assignments as zero
    dueCols = np.array(newCols)[dueIndices.ravel()]
    graded = kaScores[dueCols.ravel()]
    graded = graded.replace(np.nan, 0)

    ## Merge rows by student name, keep highest score.
    graded.loc[:, 'Student Name'] = graded.index
    graded = graded.groupby('Student Name').max()
    graded = graded.sort_index(key=lambda col: col.str.lower())

    ## Grade scores
    studentMeans = graded.mean(axis=1)

    ## If you're curious, the assignment means is given below
    # assignmentsMeans = kaScores.mean(axis=0)

    ## Save student means
    fpath = f'{workDir}/kaGrades-{dirName}.csv'
    studentMeans.to_csv(fpath, sep=',', header='Average')

    return kaScores, studentMeans

########################################################################
### End of File ########################################################
########################################################################
