#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

- Should encase workflow in a "with driver as driver" block
- Wait for page to load: http://www.seleniumhq.org/docs/04_webdriver_advanced.jsp
'''

import requests, sys
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

# load html from Selenium, file, or requests
if True:
    fpath = '/Users/herman/Documents/kaGrader/Assign content | Khan Academy.html'
    with open(fpath, 'r') as f:
        html = f.read()
elif False:
    r = requests.get(URL, headers = Headers)
    html = r.text

# Run functions
d = makeTree(html)
printTree(d)

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
