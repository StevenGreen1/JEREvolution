#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re

thisFile = sys.argv[0]
fileName = sys.argv[1]
stage = sys.argv[2]

resValues91 = []
eresValues91 = []

resValues200 = []
eresValues200 = []

resValues360 = []
eresValues360 = []

resValues500 = []
eresValues500 = []

look = False
count = 0

file = open(fileName)
allLines = file.readlines()
for line in allLines:
    if 'Default' in line:
        look = True

    if look:
        regex = re.compile("sE\/E: (\d\.\d+)\+\-(\d\.\d+)")
        r = regex.search(line)
        if r is not None:
            print line
            count +=1
            if count == 1:
                resValues91.append(r.group(1))
                eresValues91.append(r.group(2))
            if count == 2:
                resValues200.append(r.group(1))
                eresValues200.append(r.group(2))
            if count == 3:
                resValues360.append(r.group(1))
                eresValues360.append(r.group(2))
            if count == 4:
                resValues500.append(r.group(1))
                eresValues500.append(r.group(2))
                look = False
                count = 0
print 'ECal Scan :'

print 'float stage' + stage + '_91[6] = {' + resValues91[0] + ',' + resValues91[1] + ',' + resValues91[2] + ',' + resValues91[3] + ',' + resValues91[4] + ',' + resValues91[5] + '};'
print 'float estage' + stage + '_91[6] = {' + eresValues91[0] + ',' + eresValues91[1] + ',' + eresValues91[2] + ',' + eresValues91[3] + ',' + eresValues91[4] + ',' + eresValues91[5] + '};'
print 'TGraphErrors *pTGraphErrorsStage' + stage + 'ECalCS91 = new TGraphErrors(6,ecX,stage' + stage + '_91,eecX,estage' + stage + '_91);'
print 'pTGraphErrorsStage' + stage + 'ECalCS91->SetLineColor(kBlue); '
print 'pTGraphErrorsStage' + stage + 'ECalCS91->Draw("lp,same");'

print 'float stage' + stage + '_200[6] = {' + resValues200[0] + ',' + resValues200[1] + ',' + resValues200[2] + ',' + resValues200[3] + ',' + resValues200[4] + ',' + resValues200[5] + '};'
print 'float estage' + stage + '_200[6] = {' + eresValues200[0] + ',' + eresValues200[1] + ',' + eresValues200[2] + ',' + eresValues200[3] + ',' + eresValues200[4] + ',' + eresValues200[5] + '};'
print 'TGraphErrors *pTGraphErrorsStage' + stage + 'ECalCS200 = new TGraphErrors(6,ecX,stage' + stage + '_200,eecX,estage' + stage + '_200);'
print 'pTGraphErrorsStage' + stage + 'ECalCS200->SetLineColor(kRed); '
print 'pTGraphErrorsStage' + stage + 'ECalCS200->Draw("lp,same");'

print 'float stage' + stage + '_360[6] = {' + resValues360[0] + ',' + resValues360[1] + ',' + resValues360[2] + ',' + resValues360[3] + ',' + resValues360[4] + ',' + resValues360[5] + '};'
print 'float estage' + stage + '_360[6] = {' + eresValues360[0] + ',' + eresValues360[1] + ',' + eresValues360[2] + ',' + eresValues360[3] + ',' + eresValues360[4] + ',' + eresValues360[5] + '};'
print 'TGraphErrors *pTGraphErrorsStage' + stage + 'ECalCS360 = new TGraphErrors(6,ecX,stage' + stage + '_360,eecX,estage' + stage + '_360);'
print 'pTGraphErrorsStage' + stage + 'ECalCS360->SetLineColor(kMagenta); '
print 'pTGraphErrorsStage' + stage + 'ECalCS360->Draw("lp,same");'

print 'float stage' + stage + '_500[6] = {' + resValues500[0] + ',' + resValues500[1] + ',' + resValues500[2] + ',' + resValues500[3] + ',' + resValues500[4] + ',' + resValues500[5] + '};'
print 'float estage' + stage + '_500[6] = {' + eresValues500[0] + ',' + eresValues500[1] + ',' + eresValues500[2] + ',' + eresValues500[3] + ',' + eresValues500[4] + ',' + eresValues500[5] + '};'
print 'TGraphErrors *pTGraphErrorsStage' + stage + 'ECalCS500 = new TGraphErrors(6,ecX,stage' + stage + '_500,eecX,estage' + stage + '_500);'
print 'pTGraphErrorsStage' + stage + 'ECalCS500->SetLineColor(kBlack); '
print 'pTGraphErrorsStage' + stage + 'ECalCS500->Draw("lp,same");'



print '\n \n \n HCal Scan :'

print 'float stage' + stage + '_91[6] = {' + resValues91[6] + ',' + resValues91[7] + ',' + resValues91[1] + ',' + resValues91[8] + ',' + resValues91[9] + ',' + resValues91[10] + '};'
print 'float estage' + stage + '_91[6] = {' + eresValues91[6] + ',' + eresValues91[7] + ',' + eresValues91[1] + ',' + eresValues91[8] + ',' + eresValues91[9] + ',' + eresValues91[10] + '};'
print 'TGraphErrors *pTGraphErrorsStage' + stage + 'HCalCS91 = new TGraphErrors(6,hcX,stage' + stage + '_91,ehcX,estage' + stage + '_91);'
print 'pTGraphErrorsStage' + stage + 'HCalCS91->SetLineColor(kBlue); '
print 'pTGraphErrorsStage' + stage + 'HCalCS91->Draw("lp,same");'

print 'float stage' + stage + '_200[6] = {' + resValues200[6] + ',' + resValues200[7] + ',' + resValues200[1] + ',' + resValues200[8] + ',' + resValues200[9] + ',' + resValues200[10] + '};'
print 'float estage' + stage + '_200[6] = {' + eresValues200[6] + ',' + eresValues200[7] + ',' + eresValues200[1] + ',' + eresValues200[8] + ',' + eresValues200[9] + ',' + eresValues200[10] + '};'
print 'TGraphErrors *pTGraphErrorsStage' + stage + 'HCalCS200 = new TGraphErrors(6,hcX,stage' + stage + '_200,ehcX,estage' + stage + '_200);'
print 'pTGraphErrorsStage' + stage + 'HCalCS200->SetLineColor(kRed); '
print 'pTGraphErrorsStage' + stage + 'HCalCS200->Draw("lp,same");'

print 'float stage' + stage + '_360[6] = {' + resValues360[6] + ',' + resValues360[7] + ',' + resValues360[1] + ',' + resValues360[8] + ',' + resValues360[9] + ',' + resValues360[10] + '};'
print 'float estage' + stage + '_360[6] = {' + eresValues360[6] + ',' + eresValues360[7] + ',' + eresValues360[1] + ',' + eresValues360[8] + ',' + eresValues360[9] + ',' + eresValues360[10] + '};'
print 'TGraphErrors *pTGraphErrorsStage' + stage + 'HCalCS360 = new TGraphErrors(6,hcX,stage' + stage + '_360,ehcX,estage' + stage + '_360);'
print 'pTGraphErrorsStage' + stage + 'HCalCS360->SetLineColor(kMagenta); '
print 'pTGraphErrorsStage' + stage + 'HCalCS360->Draw("lp,same");'

print 'float stage' + stage + '_500[6] = {' + resValues500[6] + ',' + resValues500[7] + ',' + resValues500[1] + ',' + resValues500[8] + ',' + resValues500[9] + ',' + resValues500[10] + '};'
print 'float estage' + stage + '_500[6] = {' + eresValues500[6] + ',' + eresValues500[7] + ',' + eresValues500[1] + ',' + eresValues500[8] + ',' + eresValues500[9] + ',' + eresValues500[10] + '};'
print 'TGraphErrors *pTGraphErrorsStage' + stage + 'HCalCS500 = new TGraphErrors(6,hcX,stage' + stage + '_500,ehcX,estage' + stage + '_500);'
print 'pTGraphErrorsStage' + stage + 'HCalCS500->SetLineColor(kBlack); '
print 'pTGraphErrorsStage' + stage + 'HCalCS500->Draw("lp,same");'

print '\n \n \n ERes vs Ej :'
print 'float stage' + stage + '[4] = {' + resValues91[1] + ',' + resValues200[1] + ',' + resValues360[1] + ',' + resValues500[1] + '};'
print 'float estage' + stage + '[4] = {' + eresValues91[1] + ',' + eresValues200[1] + ',' + eresValues360[1] + ',' + eresValues500[1] + '};'
print 'TGraphErrors *pTGraphErrorsStage' + stage + ' = new TGraphErrors(4,ejX,stage' + stage + ',eejX,estage' + stage + ');' 
print 'pTGraphErrorsStage' + stage + '->Draw("lp,same");'


