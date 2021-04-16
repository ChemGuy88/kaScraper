#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Contains workspace for analyzing data from KhanAcademy.org. See funcs.py for project notes.
'''

import argparse
import os
import sys
# from funcs import gradeKAScores
from pathlib import Path

########################################################################
### Import method for troubleshooting ##################################
########################################################################

from importlib import reload
try:
    import funcs
    reload(funcs)
    from funcs import gradeKAScores
except NameError as err:
    exceptionVal = err.args[0]
    if exceptionVal == "name 'funcs' is not defined":
        import funcs
        reload(funcs)
        from funcs import gradeKAScores
        print('reloading module "funcs".')
    else:
        raise

########################################################################
### Universal variables ################################################
########################################################################

userDir = str(Path.home())
workDir = os.path.join(userDir, 'Documents', 'kaGrader')

########################################################################
#### Functions #########################################################
########################################################################

# See funcs.py

########################################################################
#### Workspace #########################################################
########################################################################


def grader(kaScoresDir):
    print(f'Grading scores from {kaScoresDir}')
    _, hwGrade = gradeKAScores(kaScoresDir)
    kaGradespath = "/Users/herman/Documents/stemple 02 21Spring/kaGrades.csv"
    hwGrade.to_csv(kaGradespath, sep=',', header='hwAverage')
    print(f'Homework grade has been saved in {kaGradespath}')


########################################################################
#### boilerplate #######################################################
########################################################################


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--verbosity", help="increase output verbosity")

    parser.add_argument("--gradehw", help="Grade the homework located in a given directory.", metavar='kaScoresFolder')

    args = parser.parse_args()

    if args.verbosity:
        print("verbosity turned on")

    if args.gradehw:
        kaScoresDir = args.gradehw
        grader(kaScoresDir)

    if not len(sys.argv) > 1:
        parser.print_usage()

########################################################################
### End of File ########################################################
########################################################################
