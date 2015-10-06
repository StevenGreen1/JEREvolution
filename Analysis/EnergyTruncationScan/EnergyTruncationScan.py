#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import math

thisFile = sys.argv[0]

# ILDCaloDigi
#stageList = [14,15,4,16,17,18,19,5]
#stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00, NewCalibration,}{ MHHHE = 0.5 GeV, ILDCaloDigi (10^{6}ns Timing Cuts in ECal and HCal)}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

# NewLCDCaloDigi
#stageList = [8,9,2,10,11,12,13,3]
#stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00,}{NewCalibration, MHHHE = 0.5 GeV, NewLDCCaloDigi}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

# ILDCaloDigi Realistic HCal
#stageList = [20,21,22,23,24,25,26,27]
#stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00,}{NewCalibration, MHHHE = 0.5 GeV, ILDCaloDigi_RealisticHCal}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

# ILDCaloDigi No Truncation
#stageList = [28,29,30,31,32,33,34,35]
#stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00,}{NewCalibration, MHHHE = 0.5 GeV, ILDCaloDigi_NoTruncation}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

# ILDCaloDigi Realistic HCal Realistic ECal
stageList = [36,37,38,39,40,41,42,43]
stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00, NewCalibration}{ MHHHE = 0.5 GeV, ILDCaloDigi_RealisticHCal_RealisticECal}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

energyTruncation = [0.5, 0.75, 1.0, 1.5, 2.0, 5.0, 10.0, 1000000]
fileNameList = []

#stageList = [14,15,4,16,17,18,19,5]
#stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00, NewCalibration,}{ MHHHE = 0.5 GeV, ILDCaloDigi (10^{6}ns Timing Cuts in ECal and HCal)}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']
briefStageDescription = ['MHHHE = 0.5 GeV', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

for stage in stageList:
    fileNameList.append('/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage' + str(stage) + '/Results/Stage' + str(stage) + 'Results.txt')

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
# JER_vs_Ej_EnergyTruncation
#================================
#for detector in ['5x5_30x30', '5x5_10x10', '5x5_100x100']:
#    printString = '{\n'
#    printString += 'gStyle->SetOptStat(0);\n'
#    printString += 'TCanvas *pCanvasEj = new TCanvas();\n'
#    printString += 'pCanvasEj->cd();\n'
#    printString += 'pCanvasEj->Divide(3,2);\n'

#energyTruncation

#    printString += 'float jetEnergy[' + str(len(energyTruncation)) + '] = {'
#    for eT in energyTruncation:
#        printString += str(eT)
#        if eT is not energyTruncation[-1]:
#            printString += ','
#    printString += '};\n'
#    printString += 'float energyTruncationError[' + str(len(energyTruncation)) + '] = {'
#    for eT in energyTruncation:
#        printString += '0.f'
#        if eT is not energyTruncation[-1]:
#            printString += ','
#    printString += '};\n'

#    for energy in jetEnergyList:
#        for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
#            printString += 'float ' + pandoraSettings + '_' + detector + '_JER' + str(energy) + '[' + str(len(energyTruncation)) + '] = {'
#            for idx, eT in enumerate(energyTruncation):
#                printString += str(JER[(pandoraSettings,energy,detector,stageList(idx))])
#                if eT is not energyTruncation[-1]:
#                    printString += ','
#            printString += '};\n'
#            printString += 'float ' + pandoraSettings + '_' + detector + '_JERError' + str(energy) + '[' + str(len(energyTruncation)) + '] = {'
#            for idx, eT in enumerate(energyTruncation):
#                printString += str(JERError[(pandoraSettings,energy,detector,stageList(idx))])
#                if eT is not energyTruncation[-1]:
#                    printString += ','
#            printString += '};\n'

#    rootLineColor = ['kRed','kMagenta','kOrange','kYellow','kGreen','kCyan','kAzure','kBlue']
#    rootLineStyle = ['1','1','1','1','1','1','1','1']
#    maxOnGraph = ['4','3.0','3.0','2','2','2']
#    minOnGraph = ['2.5','1.5','1.5','0','0','0']

#    if detector is '5x5_100x100':
#        maxOnGraph = ['6','4','5','2','3','3']

#    printString += 'TLegend *pLegend = new TLegend(0.1, 0.8, 0.9, 0.9);\n'
#    printString += 'TLegend *pLegend2 = new TLegend(0.6, 0.6, 0.9, 0.9);\n'

#    stageCounter = 0
#    for stage in stageList:
#        settingsCounter = 0
#        for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
#            printString += 'pCanvasEj->cd(' + str(settingsCounter + 1) + ');\n'
#            printString += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + ' = new TGraphErrors(4,jetEnergy,' + pandoraSettings + '_' + detector + '_JER' + str(stage) + ',jetEnergyError,' + pandoraSettings + '_' + detector + '_JERError' + str(stage) + ');\n'
#            printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + '->SetLineStyle(' + rootLineStyle[settingsCounter] + ');\n'
#            printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + '->SetLineColor(' + rootLineColor[stageCounter] + ');\n'

#            if stage is stageList[0]:
#                printString += 'TH2F *pAxes' + str(settingsCounter) + ' = new TH2F("axesEc' + str(settingsCounter) + '","' + pandoraSettings + '",1200,0,300,12000,0,6);\n'
#                printString += 'pAxes' + str(settingsCounter) + '->GetXaxis()->SetTitle("E_{j} [GeV]");\n'
#                printString += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
#                printString += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetRangeUser(' + str(minOnGraph[settingsCounter]) + ', ' + str(maxOnGraph[settingsCounter]) + ');\n'
#                printString += 'pAxes' + str(settingsCounter) + '->Draw();\n'

#            printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + '->Draw("lp");\n'
#            settingsCounter = settingsCounter + 1
#        printString += 'pLegend2->AddEntry(pTGraphErrors_Default_' + detector + '_' + str(stage) + ', "' + briefStageDescription[stageCounter] + '", "lp");\n'
#        stageCounter = stageCounter + 1

#    printString += 'pCanvasEj->cd(1);\n'
#    printString += 'pLegend->AddEntry(pTGraphErrors_Default_' + detector + '_' + str(stageList[0]) + ', "' + stageDescription[0] + '", "lp");\n'
#    printString += 'pLegend->Draw("same");\n'

#    printString += 'pCanvasEj->cd(2);\n'
#    printString += 'pLegend2->Draw("same");\n'

#    printString += 'pCanvasEj->SaveAs("JER_vs_Ej_EnergyTruncation_' + detector + '.pdf");\n'
#    printString += '}\n'

#    text_file = open('JER_vs_Ej_EnergyTruncation_' + detector + '.C', 'w')
#    text_file.write(printString)
#    text_file.close()

#================================
# JER_vs_EnergyTruncation_Ej
#================================
for detector in ['5x5_30x30', '5x5_10x10', '5x5_100x100', '5x5_20x20', '5x5_40x40', '5x5_50x50']:
    printString = '{\n'
    printString += 'gStyle->SetOptStat(0);\n'
    printString += 'TCanvas *pCanvasEj = new TCanvas();\n'
    printString += 'pCanvasEj->cd();\n'
    printString += 'pCanvasEj->Divide(3,2);\n'

    printString += 'float jetEnergy[4] = {'

    for energy in jetEnergyList:
        printString += str(float(energy)/2.0)
        if energy is not jetEnergyList[-1]:
            printString += ','
    printString += '};\n'
    printString += 'float jetEnergyError[4] = {0,0,0,0};\n'

    for stage in stageList:
        for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
            printString += 'float ' + pandoraSettings + '_' + detector + '_JER' + str(stage) + '[4] = {'
            for energy in jetEnergyList:
                printString += str(JER[(pandoraSettings,energy,detector,stage)])
                if energy is not jetEnergyList[-1]:
                    printString += ','
            printString += '};\n'
            printString += 'float ' + pandoraSettings + '_' + detector + '_JERError' + str(stage) + '[4] = {'
            for energy in jetEnergyList:
                printString += str(JERError[(pandoraSettings,energy,detector,stage)])
                if energy is not jetEnergyList[-1]:
                    printString += ','
            printString += '};\n'

    rootLineColor = ['kRed','kMagenta','kOrange','kYellow','kGreen','kCyan','kAzure','kBlue']
    rootLineStyle = ['1','1','1','1','1','1','1','1']
    maxOnGraph = ['4','3.0','3.0','2','2','2']
    minOnGraph = ['2.5','1.5','1.5','0','0','0']

    if detector is '5x5_100x100':
        maxOnGraph = ['6','4','5','2','3','3']

    printString += 'TLegend *pLegend = new TLegend(0.1, 0.8, 0.9, 0.9);\n'
    printString += 'TLegend *pLegend2 = new TLegend(0.6, 0.6, 0.9, 0.9);\n'

    stageCounter = 0
    for stage in stageList:
        settingsCounter = 0
        for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
            printString += 'pCanvasEj->cd(' + str(settingsCounter + 1) + ');\n'
            printString += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + ' = new TGraphErrors(4,jetEnergy,' + pandoraSettings + '_' + detector + '_JER' + str(stage) + ',jetEnergyError,' + pandoraSettings + '_' + detector + '_JERError' + str(stage) + ');\n'
            printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + '->SetLineStyle(' + rootLineStyle[settingsCounter] + ');\n'
            printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + '->SetLineColor(' + rootLineColor[stageCounter] + ');\n'

            if stage is stageList[0]:
                printString += 'TH2F *pAxes' + str(settingsCounter) + ' = new TH2F("axesEc' + str(settingsCounter) + '","' + pandoraSettings + '",1200,0,300,12000,0,6);\n'
                printString += 'pAxes' + str(settingsCounter) + '->GetXaxis()->SetTitle("E_{j} [GeV]");\n'
                printString += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
                printString += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetRangeUser(' + str(minOnGraph[settingsCounter]) + ', ' + str(maxOnGraph[settingsCounter]) + ');\n'
                printString += 'pAxes' + str(settingsCounter) + '->Draw();\n'

            printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + '->Draw("lp");\n'
            settingsCounter = settingsCounter + 1
        printString += 'pLegend2->AddEntry(pTGraphErrors_Default_' + detector + '_' + str(stage) + ', "' + briefStageDescription[stageCounter] + '", "lp");\n'
        stageCounter = stageCounter + 1

    printString += 'pCanvasEj->cd(1);\n'
    printString += 'pLegend->AddEntry(pTGraphErrors_Default_' + detector + '_' + str(stageList[0]) + ', "' + stageDescription[0] + '", "lp");\n'
    printString += 'pLegend->Draw("same");\n'

    printString += 'pCanvasEj->cd(2);\n'
    printString += 'pLegend2->Draw("same");\n'

    printString += 'pCanvasEj->SaveAs("JER_vs_Ej_EnergyTruncation_' + detector + '.pdf");\n'
    printString += '}\n'

    text_file = open('JER_vs_Ej_EnergyTruncation_' + detector + '.C', 'w')
    text_file.write(printString)
    text_file.close()

#sys.exit()

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
    if energy is not jetEnergyList[-1]:
        printString += ','
printString += '};\n'
printString += 'float jetEnergyError[4] = {0,0,0,0};\n'

for stage in stageList:
    for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
        printString += 'float ' + pandoraSettings + '_' + detector + '_JER' + str(stage) + '[4] = {'
        for energy in jetEnergyList:
            printString += str(JER[(pandoraSettings,energy,detector,stage)])
            if energy is not jetEnergyList[-1]:
                printString += ','
        printString += '};\n'
        printString += 'float ' + pandoraSettings + '_' + detector + '_JERError' + str(stage) + '[4] = {'
        for energy in jetEnergyList:
            printString += str(JERError[(pandoraSettings,energy,detector,stage)])
            if energy is not jetEnergyList[-1]:
                printString += ','
        printString += '};\n'

rootLineColor = ['1','4','2','kOrange','8','6']
rootLineStyle = ['1','2','3','4','5','6','7','8']

printString += 'TLegend *pLegend = new TLegend(0.1, 0.8, 0.4, 0.9);\n'
printString += 'TLegend *pLegend2 = new TLegend(0.4, 0.8, 0.9, 0.9);\n'

stageCounter = 0
for stage in stageList:
    settingsCounter = 0
    for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
        printString += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + ' = new TGraphErrors(4,jetEnergy,' + pandoraSettings + '_' + detector + '_JER' + str(stage) + ',jetEnergyError,' + pandoraSettings + '_' + detector + '_JERError' + str(stage) + ');\n'
        printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + '->SetLineStyle(' + rootLineStyle[stageCounter] + ');\n'
        printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + '->SetLineColor(' + rootLineColor[settingsCounter] + ');\n'
        printString += 'pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stage) + '->Draw("lp,same");\n'
        settingsCounter = settingsCounter + 1
    printString += 'pLegend2->AddEntry(pTGraphErrors_Default_' + detector + '_' + str(stage) + ', "' + stageDescription[stageCounter] + '", "lp");\n'
    stageCounter = stageCounter + 1

for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
    printString += 'pLegend->AddEntry(pTGraphErrors_' + pandoraSettings + '_' + detector + '_' + str(stageList[0]) + ', "' + pandoraSettings + '", "lp");\n'

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
            printStringECal += 'float ' + pandoraSettings + '_' + energy + '_JER' + str(stage) + '[6] = {'
            for detector in ecalCellDetectorList:
                printStringECal += str(JER[(pandoraSettings,energy,detector,stage)])
                if detector is not ecalCellDetectorList[-1]:
                    printStringECal += ','
            printStringECal += '};\n'
            printStringECal += 'float ' + pandoraSettings + '_' + energy + '_JERError' + str(stage) + '[6] = {'
            for detector in ecalCellDetectorList:
                printStringECal += str(JERError[(pandoraSettings,energy,detector,stage)])
                if detector is not ecalCellDetectorList[-1]:
                    printStringECal += ','
            printStringECal += '};\n'

rootLineColor = ['kBlue','kRed','kMagenta','kBlack']
rootLineStyle = ['1','2','3','4','5','6','7','8']

stageCounter = 0
for stage in stageList:
    energyCounter = 0
    for energy in jetEnergyList:
        settingsCounter = 1
        for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
            printStringECal += 'pCanvas->cd(' + str(settingsCounter) + ');\n'
            printStringECal += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + ' = new TGraphErrors(6,ecalCellSize,' + pandoraSettings + '_' + energy + '_JER' + str(stage) + ',ecalCellSizeError,' + pandoraSettings + '_' + energy + '_JERError' + str(stage) + ');\n'
            printStringECal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->SetLineStyle(' + rootLineStyle[stageCounter] + ');\n'
            printStringECal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->SetLineColor(' + rootLineColor[energyCounter] + ');\n'

            if energy is jetEnergyList[0] and stage is stageList[0]:
                printStringECal += 'TH2F *pAxes' + str(settingsCounter) + ' = new TH2F("axesEc","' + pandoraSettings + '",1200,0,25,12000,0,6);\n'
                printStringECal += 'pAxes' + str(settingsCounter) + '->GetXaxis()->SetTitle("ECAL Cell Size [mm]");\n'
                printStringECal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
                printStringECal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetRangeUser(0., 5.);\n'
                printStringECal += 'pAxes' + str(settingsCounter) + '->Draw();\n'

            printStringECal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->Draw("lp,same");\n'
            settingsCounter = settingsCounter + 1
        energyCounter = energyCounter + 1
    stageCounter = stageCounter + 1

printStringECal += 'pCanvas->cd(1);\n'
printStringECal += 'TLegend *pLegend = new TLegend(0.1, 0.15, 0.7, 0.35);\n'
stageCounter = 0
for stage in stageList:
    printStringECal += 'pLegend->AddEntry(pTGraphErrors_Default_500_' + str(stage) + ', "' + stageDescription[stageCounter] + '", "l");\n'
    stageCounter = stageCounter + 1
printStringECal += 'pLegend->Draw();\n'

printStringECal += 'TLegend *pLegend2 = new TLegend(0.7, 0.15, 0.9, 0.35);'
for energy in jetEnergyList:
    printStringECal += 'pLegend2->AddEntry(pTGraphErrors_Default_' + energy + '_' + str(stageList[0]) + ', " ' + energy + ' GeV Jets", "l");'
printStringECal += 'pLegend2->Draw();'

printStringECal += 'pCanvas->SaveAs("JER_vs_ECAL_Cell_Size.pdf");\n'
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
            printStringHCal += 'float ' + pandoraSettings + '_' + energy + '_JER' + str(stage) + '[6] = {'
            for detector in hcalCellDetectorList:
                printStringHCal += str(JER[(pandoraSettings,energy,detector,stage)])
                if detector is not hcalCellDetectorList[-1]:
                    printStringHCal += ','
            printStringHCal += '};\n'
            printStringHCal += 'float ' + pandoraSettings + '_' + energy + '_JERError' + str(stage) + '[6] = {'
            for detector in hcalCellDetectorList:
                printStringHCal += str(JERError[(pandoraSettings,energy,detector,stage)])
                if detector is not hcalCellDetectorList[-1]:
                    printStringHCal += ','
            printStringHCal += '};\n'

rootLineColor = ['kBlue','kRed','kMagenta','kBlack']
rootLineStyle = ['1','2','3','4','5','6','7','8']

stageCounter = 0

for stage in stageList:
    energyCounter = 0
    for energy in jetEnergyList:
        settingsCounter = 1
        for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
            printStringHCal += 'pCanvas->cd(' + str(settingsCounter) + ');\n'
            printStringHCal += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + ' = new TGraphErrors(6,hcalCellSize,' + pandoraSettings + '_' + energy + '_JER' + str(stage) + ',hcalCellSizeError,' + pandoraSettings + '_' + energy + '_JERError' + str(stage) + ');\n'
            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->SetLineStyle(' + rootLineStyle[stageCounter] + ');\n'
            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->SetLineColor(' + rootLineColor[energyCounter] + ');\n'

            if energy is jetEnergyList[0] and stage is stageList[0]:
                printStringHCal += 'TH2F *pAxes' + str(settingsCounter) + ' = new TH2F("axesHc","' + pandoraSettings + '",1200,0,120,12000,0,6);\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetXaxis()->SetTitle("HCAL Cell Size [mm]");\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetRangeUser(0., 5.);\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->Draw();\n'

            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->Draw("lp,same");\n'
            settingsCounter = settingsCounter + 1
        energyCounter = energyCounter + 1
    stageCounter = stageCounter + 1

printStringHCal += 'pCanvas->cd(1);\n'
printStringHCal += 'TLegend *pLegend = new TLegend(0.1, 0.15, 0.7, 0.35);\n'
stageCounter = 0
for stage in stageList:
    printStringHCal += 'pLegend->AddEntry(pTGraphErrors_Default_500_' + str(stage) + ', "' + stageDescription[stageCounter] + '", "l");\n'
    stageCounter = stageCounter + 1
printStringHCal += 'pLegend->Draw();\n'

printStringHCal += 'TLegend *pLegend2 = new TLegend(0.7, 0.15, 0.9, 0.35);'
for energy in jetEnergyList:
    printStringHCal += 'pLegend2->AddEntry(pTGraphErrors_Default_' + energy + '_' + str(stageList[0]) + ', " ' + energy + ' GeV Jets", "l");'
printStringHCal += 'pLegend2->Draw();'

printStringHCal += 'pCanvas->SaveAs("JER_vs_HCAL_Cell_Size.pdf");\n'
printStringHCal += '}'

text_file = open("JER_vs_HCAL_Cell_Size.C", "w")
text_file.write(printStringHCal)
text_file.close()

#print printStringHCal

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
        for energy in ['500']:
            printStringHCal += 'float ' + pandoraSettings + '_' + energy + '_JER' + str(stage) + '[6] = {'
            for detector in hcalCellDetectorList:
                printStringHCal += str(JER[(pandoraSettings,energy,detector,stage)])
                if detector is not hcalCellDetectorList[-1]:
                    printStringHCal += ','
            printStringHCal += '};\n'
            printStringHCal += 'float ' + pandoraSettings + '_' + energy + '_JERError' + str(stage) + '[6] = {'
            for detector in hcalCellDetectorList:
                printStringHCal += str(JERError[(pandoraSettings,energy,detector,stage)])
                if detector is not hcalCellDetectorList[-1]:
                    printStringHCal += ','
            printStringHCal += '};\n'

rootLineColor = ['kRed','kMagenta','kOrange','kYellow','kGreen','kCyan','kAzure','kBlue']
rootLineStyle = ['1','2','3','4','5','6','7','8']

stageCounter = 0

maxOnGraph = ['6','2.5','4.5','2','3','3']
minOnGraph = ['0','1.5','1.5','0','0','0']

for stage in stageList:
    energyCounter = 0
    for energy in ['500']:
        settingsCounter = 1
        for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
            printStringHCal += 'pCanvas->cd(' + str(settingsCounter) + ');\n'
            printStringHCal += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + ' = new TGraphErrors(6,hcalCellSize,' + pandoraSettings + '_' + energy + '_JER' + str(stage) + ',hcalCellSizeError,' + pandoraSettings + '_' + energy + '_JERError' + str(stage) + ');\n'
            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->SetLineStyle(1);\n'
            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->SetLineColor(' + rootLineColor[stageCounter] + ');\n'

            if energy is '500' and stage is stageList[0]:
                printStringHCal += 'TH2F *pAxes' + str(settingsCounter) + ' = new TH2F("axesHc","' + pandoraSettings + '",1200,0,120,12000,0,6);\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetXaxis()->SetTitle("HCAL Cell Size [mm]");\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetRangeUser(' + minOnGraph[settingsCounter-1] + ', ' + maxOnGraph[settingsCounter-1] + ');\n'
                printStringHCal += 'pAxes' + str(settingsCounter) + '->Draw();\n'

            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->Draw("lp,same");\n'
            settingsCounter = settingsCounter + 1
        energyCounter = energyCounter + 1
    stageCounter = stageCounter + 1

printStringHCal += 'pCanvas->cd(1);\n'
printStringHCal += 'TLegend *pLegend = new TLegend(0.1, 0.15, 0.4, 0.35);\n'
stageCounter = 0
for stage in stageList:
    printStringHCal += 'pLegend->AddEntry(pTGraphErrors_Default_500_' + str(stage) + ', "' + briefStageDescription[stageCounter] + '", "l");\n'
    stageCounter = stageCounter + 1
printStringHCal += 'pLegend->Draw();\n'

printStringHCal += 'TLegend *pLegend2 = new TLegend(0.4, 0.15, 0.9, 0.35);'
for energy in ['500']:
    printStringHCal += 'pLegend2->AddEntry(pTGraphErrors_Default_' + energy + '_' + str(stageList[0]) + ', " ' + stageDescription[0] + '", "l");'
    printStringHCal += 'pLegend2->AddEntry((TObject*)0, "250 GeV Jets", "");'
printStringHCal += 'pLegend2->Draw();'

printStringHCal += 'pCanvas->SaveAs("JER_vs_HCAL_Cell_Size_EnergyTruncation_250GeVJets.pdf");\n'
printStringHCal += '}'

text_file = open("JER_vs_HCAL_Cell_Size_EnergyTruncation_250GeVJets.C", "w")
text_file.write(printStringHCal)
text_file.close()

