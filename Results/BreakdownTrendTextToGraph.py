#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import math

thisFile = sys.argv[0]
fileName = sys.argv[1]
stage = sys.argv[2] 

fileNameList = []
stageList = []

for item in sys.argv:
    if '.txt' in item:
        fileNameList.append(item)
    elif item.isdigit():
        stageList.append(item)

stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00, NewCalibration,}{ MHHHE = 10^{6} GeV, ILDCaloDigi - 300 ns ECal and HCal Timing Cuts}','#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00, NewCalibration,}{ MHHHE = 10^{6} GeV, ILDCaloDigi - 10 ns ECal and HCal Timing Cuts}','#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00, NewCalibration,}{ MHHHE = 10^{6} GeV, ILDCaloDigi - 10^{6} ns ECal and HCal Timing Cuts}']

print 'fileNameList : '
print fileNameList
print 'stageList : '
print stageList

from collections import defaultdict
JER = defaultdict(dict)
JERError = defaultdict(dict)

pandoraSettings = ''
pandoraSettingsList = ['Default','Perfect_Photon','Perfect_Photon_Neutron_K0L','Perfect_PFA','Muon']
jetEnergyList = ['91','200','360','500']
detector = ''
detectorList = ['3x3_30x30','5x5_30x30','7x7_30x30','10x10_30x30','15x15_30x30','20x20_30x30','5x5_10x10','5x5_20x20','5x5_40x40','5x5_50x50','5x5_100x100']

fileCounter = 0
for fileName in fileNameList:
    file = open(fileName)
    allLines = file.readlines()
    search = False

    for line in allLines:
        if 'ILD_o1_v06_' in line:
            regex = re.compile("ILD_o1_v06_(.*?)\n")
            q = regex.search(line) 
            detector = q.group(1)

        if line.rstrip() in pandoraSettingsList:
            pandoraSettings = line.rstrip() 

        regex = re.compile("(\d+) GeV Di Jet Energy:fPFA_L7A(.*?)sE\/E: (\d\.\d+)\+\-(\d\.\d+)")
        r = regex.search(line)
        if r is not None:
            JER[(pandoraSettings,str(r.group(1)),detector,stageList[fileCounter])] = float(r.group(3))
            JERError[(pandoraSettings,str(r.group(1)),detector,stageList[fileCounter])] = float(r.group(4))
    fileCounter = fileCounter + 1

# Print dictionaries
#for x in JER.keys():print x,' : ',JER[x]
#for x in JERError.keys():print x,' : ',JERError[x]

for stage in stageList:
    for detector in detectorList:
        # Total Confusion
        for energy in jetEnergyList:    
            JER[('Total_Confusion',energy,detector,stage)] = math.sqrt( math.fabs( (JER[('Default',energy,detector,stage)] * JER[('Default',energy,detector,stage)]) - (JER[('Perfect_PFA',energy,detector,stage)] * JER[('Perfect_PFA',energy,detector,stage)]) ) )
            JERError[('Total_Confusion',energy,detector,stage)] = math.sqrt( math.fabs( ( (JERError[('Default',energy,detector,stage)] * JERError[('Default',energy,detector,stage)] * JER[('Default',energy,detector,stage)] * JER[('Default',energy,detector,stage)]) / (JER[('Total_Confusion',energy,detector,stage)] * JER[('Total_Confusion',energy,detector,stage)]) ) - ( (JERError[('Perfect_PFA',energy,detector,stage)] * JERError[('Perfect_PFA',energy,detector,stage)] * JER[('Perfect_PFA',energy,detector,stage)] * JER[('Perfect_PFA',energy,detector,stage)]) / (JER[('Total_Confusion',energy,detector,stage)] * JER[('Total_Confusion',energy,detector,stage)]) ) ) )

        # Photon Confusion
        for energy in jetEnergyList:    
            JER[('Photon_Confusion',energy,detector,stage)] = math.sqrt( math.fabs( (JER[('Default',energy,detector,stage)] * JER[('Default',energy,detector,stage)]) - (JER[('Perfect_Photon',energy,detector,stage)] * JER[('Perfect_Photon',energy,detector,stage)]) ) )
            JERError[('Photon_Confusion',energy,detector,stage)] = math.sqrt( math.fabs( ( (JERError[('Default',energy,detector,stage)] * JERError[('Default',energy,detector,stage)] * JER[('Default',energy,detector,stage)] * JER[('Default',energy,detector,stage)]) / (JER[('Photon_Confusion',energy,detector,stage)] * JER[('Photon_Confusion',energy,detector,stage)]) ) - ( (JERError[('Perfect_Photon',energy,detector,stage)] * JERError[('Perfect_Photon',energy,detector,stage)] * JER[('Perfect_Photon',energy,detector,stage)] * JER[('Perfect_Photon',energy,detector,stage)]) / (JER[('Photon_Confusion',energy,detector,stage)] * JER[('Photon_Confusion',energy,detector,stage)]) ) ) )

        # Neutral Hadron Confusion
        for energy in jetEnergyList:
            JER[('Neutral_Hadron_Confusion',energy,detector,stage)] = math.sqrt( math.fabs( (JER[('Perfect_Photon',energy,detector,stage)] * JER[('Perfect_Photon',energy,detector,stage)]) - (JER[('Perfect_Photon_Neutron_K0L',energy,detector,stage)] * JER[('Perfect_Photon_Neutron_K0L',energy,detector,stage)]) ) )    
            JERError[('Neutral_Hadron_Confusion',energy,detector,stage)] = math.sqrt( math.fabs( ( (JERError[('Perfect_Photon',energy,detector,stage)] * JERError[('Perfect_Photon',energy,detector,stage)] * JER[('Perfect_Photon',energy,detector,stage)] * JER[('Perfect_Photon',energy,detector,stage)]) / (JER[('Neutral_Hadron_Confusion',energy,detector,stage)] * JER[('Neutral_Hadron_Confusion',energy,detector,stage)]) ) - ( (JERError[('Perfect_Photon_Neutron_K0L',energy,detector,stage)] * JERError[('Perfect_Photon_Neutron_K0L',energy,detector,stage)] * JER[('Perfect_Photon_Neutron_K0L',energy,detector,stage)] * JER[('Perfect_Photon_Neutron_K0L',energy,detector,stage)]) / (JER[('Neutral_Hadron_Confusion',energy,detector,stage)] * JER[('Neutral_Hadron_Confusion',energy,detector,stage)]) ) ) )

        # Other Confusion
        for energy in jetEnergyList:
            JER[('Other_Confusion',energy,detector,stage)] = math.sqrt( math.fabs( (JER[('Perfect_Photon_Neutron_K0L',energy,detector,stage)] * JER[('Perfect_Photon_Neutron_K0L',energy,detector,stage)]) - (JER[('Perfect_PFA',energy,detector,stage)] * JER[('Perfect_PFA',energy,detector,stage)]) ) )    
            JERError[('Other_Confusion',energy,detector,stage)] = math.sqrt( math.fabs( ( (JERError[('Perfect_Photon_Neutron_K0L',energy,detector,stage)] * JERError[('Perfect_Photon_Neutron_K0L',energy,detector,stage)] * JER[('Perfect_Photon_Neutron_K0L',energy,detector,stage)] * JER[('Perfect_Photon_Neutron_K0L',energy,detector,stage)]) / (JER[('Other_Confusion',energy,detector,stage)] * JER[('Other_Confusion',energy,detector,stage)]) ) - ( (JERError[('Perfect_PFA',energy,detector,stage)] * JERError[('Perfect_PFA',energy,detector,stage)] * JER[('Perfect_PFA',energy,detector,stage)] * JER[('Perfect_PFA',energy,detector,stage)]) / (JER[('Other_Confusion',energy,detector,stage)] * JER[('Other_Confusion',energy,detector,stage)]) ) ) )

#================================
# JER_vs_Ej
#================================
detector = '5x5_30x30'

printString = '{\n'
printString += 'gStyle->SetOptStat(0);\n'
printString += 'TCanvas *pCanvasEj = new TCanvas();\n'
printString += 'pCanvasEj->cd();\n'

printString += 'TH2F *pAxesEj = new TH2F("axesEj","",1200,0,300,12000,0,5);\n'
printString += 'pAxesEj->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
printString += 'pAxesEj->GetXaxis()->SetTitle("E_{j} [GeV]");\n'
printString += 'pAxesEj->Draw();\n'

printString += 'float jetEnergy[4] = {'
for energy in jetEnergyList:
    printString += str(float(energy)/2.0)
    if energy is not '500':
        printString += ','
printString += '};\n'
printString += 'float jetEnergyError[4] = {0,0,0,0};\n'

for stage in stageList:
    for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
        printString += 'float ' + pandoraSettings + '_' + detector + '_JER' + stage + '[4] = {'
        for energy in jetEnergyList:
            printString += str(JER[(pandoraSettings,energy,detector,stage)])
            if energy is not jetEnergyList[-1]:
                printString += ','
        printString += '};\n'
        printString += 'float ' + pandoraSettings + '_' + detector + '_JERError' + stage + '[4] = {'
        for energy in jetEnergyList:
            printString += str(JERError[(pandoraSettings,energy,detector,stage)])
            if energy is not jetEnergyList[-1]:
                printString += ','
        printString += '};\n'

rootLineColor = ['1','4','2','kOrange','8','6']
rootLineStyle = ['1','2','3','4','5','6']

printString += 'TLegend *pLegend = new TLegend(0.1, 0.8, 0.4, 0.9);\n'
printString += 'TLegend *pLegend2 = new TLegend(0.4, 0.8, 0.9, 0.9);\n'

stageCounter = 0
for stage in stageList:
    settingsCounter = 0
    for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
        printString += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + stage + ' = new TGraphErrors(4,jetEnergy,' + pandoraSettings + '_' + detector + '_JER' + stage + ',jetEnergyError,' + pandoraSettings + '_' + detector + '_JERError' + stage + ');\n'
        printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + stage + '->SetLineStyle(' + rootLineStyle[stageCounter] + ');\n'
        printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + stage + '->SetLineColor(' + rootLineColor[settingsCounter] + ');\n'
        printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + stage + '->Draw("lp,same");\n'
        settingsCounter = settingsCounter + 1
    printString += 'pLegend2->AddEntry(pTGraphErrors_Default_' + detector + '_' + stage + ', "' + stageDescription[stageCounter] + '", "lp");\n'
    stageCounter = stageCounter + 1

for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
    printString += 'pLegend->AddEntry(pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + stageList[0] + ', "' + pandoraSettings + '", "lp");\n'

printString += 'pLegend->Draw();\n'
printString += 'pLegend2->Draw();\n'

printString += 'pCanvasEj->SaveAs("JER_vs_Ej.pdf");\n'
printString += '}\n'

text_file = open("JER_vs_Ej.C", "w")
text_file.write(printString)
text_file.close()

#================================
# JER_vs_ECal_Cell_Size
#================================

printStringECal = '{\n'
printStringECal += 'gStyle->SetOptStat(0);\n'

printStringECal += 'TCanvas *pCanvas = new TCanvas();\n'
printStringECal += 'pCanvas->cd();\n'
printStringECal += 'pCanvas->Divide(3,2);\n'

ecalCellSizeList = ['3','5','7.5','10','15','20']
printStringECal += 'float ecalCellSize[6] = {'
for ecalCellSize in ecalCellSizeList:
    printStringECal += ecalCellSize
    if energy is not '20':
        printStringECal += ','
printStringECal += '};\n'
printStringECal += 'float ecalCellSizeError[6] = {0,0,0,0,0,0};\n'

ecalCellDetectorList = ['3x3_30x30','5x5_30x30','7x7_30x30','10x10_30x30','15x15_30x30','20x20_30x30']

for stage in stageList:
    for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
        for energy in jetEnergyList:
            printStringECal += 'float ' + pandoraSettings + '_' + energy + '_JER' + stage + '[6] = {'
            for detector in ecalCellDetectorList:
                printStringECal += str(JER[(pandoraSettings,energy,detector,stage)])
                if detector is not ecalCellDetectorList[-1]:
                    printStringECal += ','
            printStringECal += '};\n'
            printStringECal += 'float ' + pandoraSettings + '_' + energy + '_JERError' + stage + '[6] = {'
            for detector in ecalCellDetectorList:
                printStringECal += str(JERError[(pandoraSettings,energy,detector,stage)])
                if detector is not ecalCellDetectorList[-1]:
                    printStringECal += ','
            printStringECal += '};\n'

rootLineColor = ['kBlue','kRed','kMagenta','kBlack']
rootLineStyle = ['1','2','3','4','5','6']

stageCounter = 0
for stage in stageList:
    energyCounter = 0
    for energy in jetEnergyList:
        settingsCounter = 1
        for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
            printStringECal += 'pCanvas->cd(' + str(settingsCounter) + ');\n'
            printStringECal += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + stage + ' = new TGraphErrors(6,ecalCellSize,' + pandoraSettings + '_' + energy + '_JER' + stage + ',ecalCellSizeError,' + pandoraSettings + '_' + energy + '_JERError' + stage + ');\n'
            printStringECal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + stage + '->SetLineStyle(' + rootLineStyle[stageCounter] + ');\n'
            printStringECal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + stage + '->SetLineColor(' + rootLineColor[energyCounter] + ');\n'

            if energy is jetEnergyList[0] and stage is stageList[0]:
                printStringECal += 'TH2F *pAxes' + str(settingsCounter) + ' = new TH2F("axesEc","' + pandoraSettings + '",1200,0,25,12000,0,6);\n'
                printStringECal += 'pAxes' + str(settingsCounter) + '->GetXaxis()->SetTitle("ECAL Cell Size [mm]");\n'
                printStringECal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
                printStringECal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetRangeUser(0., 5.);\n'
                printStringECal += 'pAxes' + str(settingsCounter) + '->Draw();\n'

            printStringECal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + stage + '->Draw("lp,same");\n'
            settingsCounter = settingsCounter + 1
        energyCounter = energyCounter + 1
    stageCounter = stageCounter + 1

printStringECal += 'pCanvas->cd(1);\n'
printStringECal += 'TLegend *pLegend = new TLegend(0.1, 0.15, 0.7, 0.35);\n'
stageCounter = 0
for stage in stageList:
    printStringECal += 'pLegend->AddEntry(pTGraphErrors_Default_500_' + stage + ', "' + stageDescription[stageCounter] + '", "l");\n'
    stageCounter = stageCounter + 1
printStringECal += 'pLegend->Draw();\n'

printStringECal += 'TLegend *pLegend2 = new TLegend(0.7, 0.15, 0.9, 0.35);'
for energy in jetEnergyList:
    printStringECal += 'pLegend2->AddEntry(pTGraphErrors_Default_' + energy + '_' + stageList[0] + ', " ' + energy + ' GeV Jets", "l");'
printStringECal += 'pLegend2->Draw();'

printStringECal += 'pCanvas->SaveAs("JER_vs_ECAL_Cell_Size.pdf");\n'
printStringECal += 'TPad *pTPad = (TPad*)pCanvas->GetPad(1);pTPad->SetPad(0.0, 0.0, 1.0, 1.0);pTPad->SaveAs("JER_vs_ECAL_Cell_Size_Default.pdf");\n'
printStringECal += '}'

text_file = open("JER_vs_ECAL_Cell_Size.C", "w")
text_file.write(printStringECal)
text_file.close()

#print printStringECal

#================================
# JER_vs_HCal_Cell_Size
#================================

printStringHCal = '{\n'
printStringHCal += 'gStyle->SetOptStat(0);\n'

printStringHCal += 'TCanvas *pCanvas = new TCanvas();\n'
printStringHCal += 'pCanvas->cd();\n'
printStringHCal += 'pCanvas->Divide(3,2);\n'

hcalCellSizeList = ['10','20','30','40','50','100']
printStringHCal += 'float hcalCellSize[6] = {'
for hcalCellSize in hcalCellSizeList:
    printStringHCal += hcalCellSize
    if hcalCellSize is not hcalCellSizeList[-1]:
        printStringHCal += ','
printStringHCal += '};\n'
printStringHCal += 'float hcalCellSizeError[6] = {0,0,0,0,0,0};\n'

hcalCellDetectorList = ['5x5_10x10','5x5_20x20','5x5_30x30','5x5_40x40','5x5_50x50','5x5_100x100']

for stage in stageList:
    for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
        for energy in jetEnergyList:
            printStringHCal += 'float ' + pandoraSettings + '_' + energy + '_JER' + stage + '[6] = {'
            for detector in hcalCellDetectorList:
                printStringHCal += str(JER[(pandoraSettings,energy,detector,stage)])
                if detector is not hcalCellDetectorList[-1]:
                    printStringHCal += ','
            printStringHCal += '};\n'
            printStringHCal += 'float ' + pandoraSettings + '_' + energy + '_JERError' + stage + '[6] = {'
            for detector in hcalCellDetectorList:
                printStringHCal += str(JERError[(pandoraSettings,energy,detector,stage)])
                if detector is not hcalCellDetectorList[-1]:
                    printStringHCal += ','
            printStringHCal += '};\n'

rootLineColor = ['kBlue','kRed','kMagenta','kBlack']
rootLineStyle = ['1','2','3','4','5','6']

stageCounter = 0

for stage in stageList:
    energyCounter = 0
    for energy in jetEnergyList:
        settingsCounter = 1
        for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
            printStringHCal += 'pCanvas->cd(' + str(settingsCounter) + ');\n'
            printStringHCal += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + stage + ' = new TGraphErrors(6,hcalCellSize,' + pandoraSettings + '_' + energy + '_JER' + stage + ',hcalCellSizeError,' + pandoraSettings + '_' + energy + '_JERError' + stage + ');\n'
            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + stage + '->SetLineStyle(' + rootLineStyle[stageCounter] + ');\n'
            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + stage + '->SetLineColor(' + rootLineColor[energyCounter] + ');\n'

            if energy is jetEnergyList[0] and stage is stageList[0]:
                printStringHCal += 'TH2F *pAxes' + str(settingsCounter) + ' = new TH2F("axesHc","' + pandoraSettings + '",1200,0,120,12000,0,6);\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetXaxis()->SetTitle("HCAL Cell Size [mm]");\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetRangeUser(0., 5.);\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->Draw();\n'

            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + stage + '->Draw("lp,same");\n'
            settingsCounter = settingsCounter + 1
        energyCounter = energyCounter + 1
    stageCounter = stageCounter + 1

printStringHCal += 'pCanvas->cd(1);\n'
printStringHCal += 'TLegend *pLegend = new TLegend(0.1, 0.15, 0.7, 0.35);\n'
stageCounter = 0
for stage in stageList:
    printStringHCal += 'pLegend->AddEntry(pTGraphErrors_Default_500_' + stage + ', "' + stageDescription[stageCounter] + '", "l");\n'
    stageCounter = stageCounter + 1
printStringHCal += 'pLegend->Draw();\n'

printStringHCal += 'TLegend *pLegend2 = new TLegend(0.7, 0.15, 0.9, 0.35);'
for energy in jetEnergyList:
    printStringHCal += 'pLegend2->AddEntry(pTGraphErrors_Default_' + energy + '_' + stageList[0] + ', " ' + energy + ' GeV Jets", "l");'
printStringHCal += 'pLegend2->Draw();'

printStringHCal += 'pCanvas->SaveAs("JER_vs_HCAL_Cell_Size.pdf");\n'
printStringHCal += 'TPad *pTPad = (TPad*)pCanvas->GetPad(1);pTPad->SetPad(0.0, 0.0, 1.0, 1.0);pTPad->SaveAs("JER_vs_HCAL_Cell_Size_Default.pdf");\n'
printStringHCal += '}'

text_file = open("JER_vs_HCAL_Cell_Size.C", "w")
text_file.write(printStringHCal)
text_file.close()

#print printStringHCal
