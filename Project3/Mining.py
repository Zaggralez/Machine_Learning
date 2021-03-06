#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from similarity import binarize
from writeapriorifile import WriteAprioriFile
import numpy as np
from subprocess import run
import re
import os
import time
from sys import platform
import dataSetup

X = dataSetup.numbersData.values
#X = stats.zscore(X)
N,M = X.shape

Binarized_data = binarize(X)
WriteAprioriFile(Binarized_data, filename='binarized_data.txt')
print(Binarized_data)




if platform.startswith('linux'): #== "linux" or platform == "linux2":
    ext = ''  # Linux
    dir_sep = '/'
elif platform.startswith('darwin'): #== "darwin":
    ext = 'MAC'  # OS X
    dir_sep = '/'
elif platform.startswith('win'): #== "win32":
    ext = '.exe'  # Windows
    dir_sep = '\\'
else:
    raise NotImplementedError()

filename = 'binarized_data.txt'
print(ext)
minSup = 80
minConf = 100
maxRule = 4

# Run Apriori Algorithm
print('Mining for frequent itemsets by the Apriori algorithm')
status1 = run('apriori{0} -f"," -s{1} -v"[Sup. %S]" {2} apriori_temp1.txt'
              .format(ext, minSup, filename ), shell=True)

if status1.returncode != 0:
    print('An error occurred while calling apriori, a likely cause is that minSup was set to high such that no '
          'frequent itemsets were generated or spaces are included in the path to the apriori files.')
    exit()
if minConf > 0:
    print('Mining for associations by the Apriori algorithm')
    status2 = run('apriori{0} -tr -f"," -n{1} -c{2} -s{3} -v"[Conf. %C,Sup. %S]" {4} apriori_temp2.txt'
                  .format(ext, maxRule, minConf, minSup, filename ), shell=True)

    if status2.returncode != 0:
        print('An error occurred while calling apriori')
        exit()
print('Apriori analysis done, extracting results')

# Extract information from stored files apriori_temp1.txt and apriori_temp2.txt
f = open('apriori_temp1.txt', 'r')
lines = f.readlines()
f.close()
# Extract Frequent Itemsets
FrequentItemsets = [''] * len(lines)
sup = np.zeros((len(lines), 1))
for i, line in enumerate(lines):
    FrequentItemsets[i] = line[0:-1]
    sup[i] = re.findall(' [-+]?\d*\.\d+|\d+]', line)[0][1:-1]
#os.remove('apriori_temp1.txt')

# Read the file
f = open('apriori_temp2.txt', 'r')
lines = f.readlines()
f.close()
# Extract Association rules
AssocRules = [''] * len(lines)
conf = np.zeros((len(lines), 1))
for i, line in enumerate(lines):
    AssocRules[i] = line[0:-1]
    conf[i] = re.findall(' [-+]?\d*\.\d+|\d+,', line)[0][1:-1]
os.remove('apriori_temp2.txt')

# sort (FrequentItemsets by support value, AssocRules by confidence value)
AssocRulesSorted = [AssocRules[item] for item in np.argsort(conf, axis=0).ravel()]
AssocRulesSorted.reverse()
FrequentItemsetsSorted = [FrequentItemsets[item] for item in np.argsort(sup, axis=0).ravel()]
FrequentItemsetsSorted.reverse()

# Print the results
time.sleep(.5)
print('\n')
print('RESULTS:\n')
print('Frequent itemsets:')
for i, item in enumerate(FrequentItemsetsSorted):
    print('Item: {0}'.format(item))
print('\n')
print('Association rules:')
for i, item in enumerate(AssocRulesSorted):
    print('Rule: {0}'.format(item))