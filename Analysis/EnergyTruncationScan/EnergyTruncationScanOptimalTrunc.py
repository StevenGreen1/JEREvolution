#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import math

#===========================================

def OptimalTruncation( detector ):
    #optimalTruncationDetector = [0.75,0.75,0.75,1.50,1.50,5.00] # Realistic HCal
    #optimalTruncationDetector = [0.50,0.75,1.00,1.50,1.50,5.00] # No Truncation
    #optimalTruncationDetector = [0.50,0.50,1.50,1.50,1.50,5.00] # Realistic HCal and ECal
    optimalTruncationDetector = [0.50,0.75,1.50,1.50,1.50,5.00] # Realistic HCal and ECal 10 ns TC

    regex = re.compile("(\d+)x(\d+)_(\d+)x(\d+)")
    searchResults = regex.search(detector)

    ECalCellSize = ''
    HCalCellSize = ''

    if searchResults is not None:
        ECalCellSize = searchResults.group(1)
        HCalCellSize = searchResults.group(3)

    optimalTruncation = ''

    if int(HCalCellSize) is 10:
        optimalTruncation = optimalTruncationDetector[0]
    elif int(HCalCellSize) is 20:
        optimalTruncation = optimalTruncationDetector[1]
    elif int(HCalCellSize) is 30:
        optimalTruncation = optimalTruncationDetector[2]
    elif int(HCalCellSize) is 40:
        optimalTruncation = optimalTruncationDetector[3]
    elif int(HCalCellSize) is 50:
        optimalTruncation = optimalTruncationDetector[4]
    elif int(HCalCellSize) is 100:
        optimalTruncation = optimalTruncationDetector[5]
    return optimalTruncation

#===========================================

thisFile = sys.argv[0]

# ILDCaloDigi
#stageList = [14,15,4,16,17,18,19,5]
#stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00, NewCalibration,}{ ILDCaloDigi (10^{6}ns Timing Cuts in ECal and HCal)}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

# NewLCDCaloDigi
#stageList = [8,9,2,10,11,12,13,3]
#stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00,}{NewCalibration, NewLDCCaloDigi}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

# ILDCaloDigi Realistic HCal
#stageList = [20,21,22,23,24,25,26,27]
#stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00,}{NewCalibration, ILDCaloDigi_RealisticHCal}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

# ILDCaloDigi No Truncation
#stageList = [28,29,30,31,32,33,34,35]
#stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00,}{NewCalibration, ILDCaloDigi_NoTruncation}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

# ILDCaloDigi Realistic HCal and ECal
#stageList = [36,37,38,39,40,41,42,43]
#stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00, NewCalibration,}{ILDCaloDigi_RealisticHCal_RealisticECal}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

# ILDCaloDigi Realistic HCal and ECal 10 ns timing cut
stageList = [44,45,46,47,48,49,50,51]
stageDescription = ['#splitline{ILD_o1_v06, ilcsoft v01_17_07 inc. PandoraPFA v02-00-00, NewCalibration,}{ILDCaloDigi_RealisticHCal_RealisticECal 10 ns Timing Cut}', 'MHHHE = 0.75 GeV','MHHHE = 1 GeV','MHHHE = 1.5 GeV','MHHHE = 2 GeV','MHHHE = 5.0 GeV','MHHHE = 10 GeV','MHHHE = 10^{6} GeV']

energyTruncation = [0.50, 0.75, 1.00, 1.50, 2.00, 5.00, 10.00, 1000000.00]
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

JERRefined = defaultdict(dict)
JERRefinedEnergyTruncation = defaultdict(dict)
JERErrorRefined = defaultdict(dict)

EnergyFOT = []

fullPandoraList = ['Default','Perfect_Photon','Perfect_Photon_Neutron_K0L','Perfect_PFA','Muon','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']

for key, value in JER.iteritems():
    for detector in detectorList:
        for energy in jetEnergyList:
            if 'Default' in key and detector in key and energy in key:
                JERRefinedEnergyTruncation[(energy,detector)] = OptimalTruncation(detector)
                for pandora in fullPandoraList:
                    stage = stageList[energyTruncation.index(OptimalTruncation(detector))]
                    JERRefined[(pandora,energy,detector)] = JER[(pandora,energy,detector,stage)]
                    JERErrorRefined[(pandora,energy,detector)] = JERError[(pandora,energy,detector,stage)]

#sys.exit()

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
    printString += 'TPad *pTPad = (TPad*)pCanvasEj->GetPad(1);'
    printString += 'pTPad->SetPad(0.0, 0.0, 1.0, 1.0);'
    printString += 'pTPad->SaveAs("JER_vs_Ej_EnergyTruncation_' + detector + '_Default.pdf");'
    printString += '}\n'

    text_file = open('JER_vs_Ej_EnergyTruncation_' + detector + '.C', 'w')
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

for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
    for energy in jetEnergyList:
        printStringECal += 'float ' + pandoraSettings + '_' + energy + '_JER[6] = {'
        for detector in ecalCellDetectorList:
            printStringECal += str(JERRefined[(pandoraSettings,energy,detector)])
            if detector is not ecalCellDetectorList[-1]:
                printStringECal += ','
        printStringECal += '};\n'
        printStringECal += 'float ' + pandoraSettings + '_' + energy + '_JERError[6] = {'
        for detector in ecalCellDetectorList:
            printStringECal += str(JERErrorRefined[(pandoraSettings,energy,detector)])
            if detector is not ecalCellDetectorList[-1]:
                printStringECal += ','
        printStringECal += '};\n'

rootLineColor = ['kBlue','kRed','kMagenta','kBlack']
rootLineStyle = ['1','2','3','4','5','6','7','8']

energyCounter = 0
for energy in jetEnergyList:
    settingsCounter = 1
    for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
        printStringECal += 'pCanvas->cd(' + str(settingsCounter) + ');\n'
        printStringECal += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + energy + ' = new TGraphErrors(6,ecalCellSize,' + pandoraSettings + '_' + energy + '_JER,ecalCellSizeError,' + pandoraSettings + '_' + energy + '_JERError);\n'
        printStringECal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '->SetLineStyle(1);\n'
        printStringECal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '->SetLineColor(' + rootLineColor[energyCounter] + ');\n'

        if energy is jetEnergyList[0]:
            printStringECal += 'TH2F *pAxes' + str(settingsCounter) + ' = new TH2F("axesEc","' + pandoraSettings + '",1200,0,25,12000,0,6);\n'
            printStringECal += 'pAxes' + str(settingsCounter) + '->GetXaxis()->SetTitle("ECAL Cell Size [mm]");\n'
            printStringECal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
            printStringECal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetRangeUser(0., 5.);\n'
            printStringECal += 'pAxes' + str(settingsCounter) + '->Draw();\n'

        printStringECal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '->Draw("lp,same");\n'
        settingsCounter = settingsCounter + 1
    energyCounter = energyCounter + 1

printStringECal += 'pCanvas->cd(1);\n'
printStringECal += 'TLegend *pLegend = new TLegend(0.1, 0.15, 0.7, 0.35);\n'
printStringECal += 'pLegend->AddEntry(pTGraphErrors_Default_500, "' + stageDescription[0] + '", "l");\n'
printStringECal += 'pLegend->Draw();\n'

printStringECal += 'TLegend *pLegend2 = new TLegend(0.7, 0.15, 0.9, 0.35);'
for energy in jetEnergyList:
    printStringECal += 'pLegend2->AddEntry(pTGraphErrors_Default_' + energy + ', " ' + energy + ' GeV Jets", "l");'
printStringECal += 'pLegend2->Draw();'

printStringECal += 'pCanvas->SaveAs("JER_vs_ECAL_Cell_Size.pdf");\n'
printStringECal += 'TPad *pTPad = (TPad*)pCanvas->GetPad(1);'
printStringECal += 'pTPad->SetPad(0.0, 0.0, 1.0, 1.0);'
printStringECal += 'pTPad->SaveAs("JER_vs_ECAL_Cell_Size_Default.pdf");'
printStringECal += '}'

text_file = open("JER_vs_ECAL_Cell_Size.C", "w")
text_file.write(printStringECal)
text_file.close()

#print printStringECal

#sys.exit()

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

for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
    for energy in jetEnergyList:
        printStringHCal += 'float ' + pandoraSettings + '_' + energy + '_JER[6] = {'
        for detector in hcalCellDetectorList:
            printStringHCal += str(JERRefined[(pandoraSettings,energy,detector)])
            if detector is not hcalCellDetectorList[-1]:
                printStringHCal += ','
        printStringHCal += '};\n'
        printStringHCal += 'float ' + pandoraSettings + '_' + energy + '_JERError[6] = {'
        for detector in hcalCellDetectorList:
            printStringHCal += str(JERErrorRefined[(pandoraSettings,energy,detector)])
            if detector is not hcalCellDetectorList[-1]:
                printStringHCal += ','
        printStringHCal += '};\n'

rootLineColor = ['kBlue','kRed','kMagenta','kBlack']
rootLineStyle = ['1','2','3','4','5','6','7','8']

energyCounter = 0
for energy in jetEnergyList:
    settingsCounter = 1
    for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
        printStringHCal += 'pCanvas->cd(' + str(settingsCounter) + ');\n'
        printStringHCal += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + energy + ' = new TGraphErrors(6,hcalCellSize,' + pandoraSettings + '_' + energy + '_JER,hcalCellSizeError,' + pandoraSettings + '_' + energy + '_JERError);\n'
        printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '->SetLineStyle(1);\n'
        printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '->SetLineColor(' + rootLineColor[energyCounter] + ');\n'

        if energy is jetEnergyList[0]:
            printStringHCal += 'TH2F *pAxes' + str(settingsCounter) + ' = new TH2F("axesHc","' + pandoraSettings + '",1200,0,120,12000,0,6);\n'
            printStringHCal += 'pAxes' + str(settingsCounter) + '->GetXaxis()->SetTitle("HCAL Cell Size [mm]");\n'
            printStringHCal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
            printStringHCal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetRangeUser(0., 5.);\n'
            printStringHCal += 'pAxes' + str(settingsCounter) + '->Draw();\n'

        printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '->Draw("lp,same");\n'
        settingsCounter = settingsCounter + 1
    energyCounter = energyCounter + 1

printStringHCal += 'pCanvas->cd(1);\n'
printStringHCal += 'TLegend *pLegend = new TLegend(0.1, 0.15, 0.7, 0.35);\n'
printStringHCal += 'pLegend->AddEntry(pTGraphErrors_Default_500, "' + stageDescription[0] + '", "l");\n'
printStringHCal += 'pLegend->Draw();\n'

printStringHCal += 'TLegend *pLegend2 = new TLegend(0.7, 0.15, 0.9, 0.35);'
for energy in jetEnergyList:
    printStringHCal += 'pLegend2->AddEntry(pTGraphErrors_Default_' + energy + ', " ' + energy + ' GeV Jets", "l");'
printStringHCal += 'pLegend2->Draw();'

printStringHCal += 'pCanvas->SaveAs("JER_vs_HCAL_Cell_Size.pdf");\n'
printStringHCal += 'TPad *pTPad = (TPad*)pCanvas->GetPad(1);'
printStringHCal += 'pTPad->SetPad(0.0, 0.0, 1.0, 1.0);'
printStringHCal += 'pTPad->SaveAs("JER_vs_HCAL_Cell_Size_Default.pdf");'
printStringHCal += '}'

text_file = open("JER_vs_HCAL_Cell_Size.C", "w")
text_file.write(printStringHCal)
text_file.close()

#print printStringHCal

#sys.exit()

#================================
# JER_vs_HCal_Cell_Size 250 GeV Jets
#================================

#printStringHCal = '{\n'
#printStringHCal += 'gStyle->SetOptStat(0);\n'

#printStringHCal += 'TCanvas *pCanvas = new TCanvas();\n'
#printStringHCal += 'pCanvas->cd();\n'
#printStringHCal += 'pCanvas->Divide(3,2);\n'

#hcalCellSizeList = ['10','20','30','40','50','100']
#printStringHCal += 'float hcalCellSize[6] = {'
#for hcalCellSize in hcalCellSizeList:
#    printStringHCal += hcalCellSize
#    if hcalCellSize is not hcalCellSizeList[-1]:
#        printStringHCal += ','
#printStringHCal += '};\n'
#printStringHCal += 'float hcalCellSizeError[6] = {0,0,0,0,0,0};\n'

#hcalCellDetectorList = ['5x5_10x10','5x5_20x20','5x5_30x30','5x5_40x40','5x5_50x50','5x5_100x100']

#for stage in stageList:
#    for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
#        for energy in ['500']:
#            printStringHCal += 'float ' + pandoraSettings + '_' + energy + '_JER' + str(stage) + '[6] = {'
#            for detector in hcalCellDetectorList:
#                printStringHCal += str(JER[(pandoraSettings,energy,detector,stage)])
#                if detector is not hcalCellDetectorList[-1]:
#                    printStringHCal += ','
#            printStringHCal += '};\n'
#            printStringHCal += 'float ' + pandoraSettings + '_' + energy + '_JERError' + str(stage) + '[6] = {'
#            for detector in hcalCellDetectorList:
#                printStringHCal += str(JERError[(pandoraSettings,energy,detector,stage)])
#                if detector is not hcalCellDetectorList[-1]:
#                    printStringHCal += ','
#            printStringHCal += '};\n'

#rootLineColor = ['kRed','kMagenta','kOrange','kYellow','kGreen','kCyan','kAzure','kBlue']
#rootLineStyle = ['1','2','3','4','5','6','7','8']

#stageCounter = 0

#maxOnGraph = ['6','2.5','4.5','2','3','3']
#minOnGraph = ['0','1.5','1.5','0','0','0']

#for stage in stageList:
#    energyCounter = 0
#    for energy in ['500']:
#        settingsCounter = 1
#        for pandoraSettings in ['Default','Perfect_PFA','Total_Confusion','Photon_Confusion','Neutral_Hadron_Confusion','Other_Confusion']:
#            printStringHCal += 'pCanvas->cd(' + str(settingsCounter) + ');\n'
#            printStringHCal += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + ' = new TGraphErrors(6,hcalCellSize,' + pandoraSettings + '_' + energy + '_JER' + str(stage) + ',hcalCellSizeError,' + pandoraSettings + '_' + energy + '_JERError' + str(stage) + ');\n'
#            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->SetLineStyle(1);\n'
#            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->SetLineColor(' + rootLineColor[stageCounter] + ');\n'

#            if energy is '500' and stage is stageList[0]:
#                printStringHCal += 'TH2F *pAxes' + str(settingsCounter) + ' = new TH2F("axesHc","' + pandoraSettings + '",1200,0,120,12000,0,6);\n'
#                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetXaxis()->SetTitle("HCAL Cell Size [mm]");\n'
#                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
#                printStringHCal += 'pAxes' + str(settingsCounter) + '->GetYaxis()->SetRangeUser(' + minOnGraph[settingsCounter-1] + ', ' + maxOnGraph[settingsCounter-1] + ');\n'
#                printStringHCal += 'pAxes' + str(settingsCounter) + '->Draw();\n'

#            printStringHCal += 'pTGraphErrors_' + pandoraSettings + '_' + energy + '_' + str(stage) + '->Draw("lp,same");\n'
#            settingsCounter = settingsCounter + 1
#        energyCounter = energyCounter + 1
#    stageCounter = stageCounter + 1

#printStringHCal += 'pCanvas->cd(1);\n'
#printStringHCal += 'TLegend *pLegend = new TLegend(0.1, 0.15, 0.4, 0.35);\n'
#stageCounter = 0
#for stage in stageList:
#    printStringHCal += 'pLegend->AddEntry(pTGraphErrors_Default_500_' + str(stage) + ', "' + briefStageDescription[stageCounter] + '", "l");\n'
#    stageCounter = stageCounter + 1
#printStringHCal += 'pLegend->Draw();\n'

#printStringHCal += 'TLegend *pLegend2 = new TLegend(0.4, 0.15, 0.9, 0.35);'
#for energy in ['500']:
#    printStringHCal += 'pLegend2->AddEntry(pTGraphErrors_Default_' + energy + '_' + str(stageList[0]) + ', " ' + stageDescription[0] + '", "l");'
#    printStringHCal += 'pLegend2->AddEntry((TObject*)0, "250 GeV Jets", "");'
#printStringHCal += 'pLegend2->Draw();'

#printStringHCal += 'pCanvas->SaveAs("JER_vs_HCAL_Cell_Size_EnergyTruncation_250GeVJets.pdf");\n'
#printStringHCal += '}'

#text_file = open("JER_vs_HCAL_Cell_Size_EnergyTruncation_250GeVJets.C", "w")
#text_file.write(printStringHCal)
#text_file.close()

