#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Contains workspace for analyzing data from KhanAcademy.org. See funcs.py for project notes.
'''

import requests, sys
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from importlib import reload
try:
    reload(funcs)
except:
    t, v, cb = sys.exc_info()
    exceptionName = t.__name__
    exceptionVal = v.args[0]
    if exceptionName == 'NameError' and exceptionVal == "name 'funcs' is not defined":
        import funcs
        reload(funcs)
        from funcs import *
    else:
        raise


########################################################################
### Universal variables ################################################
########################################################################

rootUrl = u'https://www.khanacademy.org'
UserAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0)'+\
            ' Gecko/20100101 Firefox/56.0'
Headers = { 'User-Agent': UserAgent}

########################################################################
#### Workspace #########################################################
########################################################################

# Grade ka assignments via pasting
workDir = '/Users/herman/Documents/kaGrader'
l = []
for i in range(1,6):
    fpath = f'{workDir}/kaScores{i}.txt'
    df = tabText(fpath)
    l.append(df)

df = pd.concat(l, axis=1)

# Save scores as they appear on KA
fpath = f'{workDir}/kaScores.csv'
df.to_csv(fpath, sep=',')

# Mark late assignments as zero
cols = df.columns
late = cols[23:]
graded = df[late]
graded.replace(np.nan, 0, inplace=True)


# assignmentsMeans = df.mean(axis=0)
studentMeans = graded.mean(axis=1)

# Save scores after marking late
fpath = f'{workDir}/kaGrades.csv'
studentMeans.to_csv(fpath, sep=',', header='Average')

# Test
if False:
    student = 'Sealy, Justin'
    assignment = 'Create two-way frequency tables (9-Mar)'
    x = df.loc[student][assignment]
    print(f'Student "{student}" got a score of {x} on the assignment "{assignment}".')

# load html from Selenium, file, or requests
if False:
    fpath = '/Users/herman/Documents/kaGrader/Assign content | Khan Academy.html'
    with open(fpath, 'r') as f:
        html = f.read()
elif False:
    r = requests.get(URL, headers = Headers)
    html = r.text

# Some notes about the html tags
if False:
    soup = BeautifulSoup(html, 'html.parser')

    # Notes
    class3t1 = soup.findAll(attrs={'class' : '_1o605ie', 'data-test-id' : 'ap-statistics-topic-tree', 'role' : 'tree'}) # contains all horizontal bars
    class1k9 = soup.findAll(attrs={'class' : '_1k95g4y8'}) # contains the unit node and child nodes (i.e., lessons and video/exercises)
    classg20 = soup.findAll(attrs={'class' : '_g20yn58'}) # horizontal bar titles for units and lessons
    print(len(classg20)) # 74
    classm42 = soup.findAll(attrs={'class' : '_m42uf38'}) # subtitle for horizontal bars)
    print(len(classm42)) # 515
    classxu2 = soup.findAll(attrs={'role' : 'group', 'class' : '_xu2jcg'}) # Groups unit child nodes and lesson child nodes.
    print(len(classxu2)) # 70
    class14b = soup.findAll(attrs={'class' : '_14bmcy4r'}) # horizontal bar titles at video/exercise level
    print(len(class14b)) # 410
    class14b = soup.findAll(attrs={'class' : '_14bmcy4r'})


########################################################################
########################################################################
########################################################################

def main():
	return
	Arguments = sys.argv[1:]

if __name__ == '__main__':
	main()

########################################################################
### End of File ########################################################
########################################################################
