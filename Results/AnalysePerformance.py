#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

stage = '59'

executable = "/usera/sg568/ilcsoft_Mod_v01_17_07/PandoraAnalysis/bin/AnalysePerformance"
results = ''

# ECal Param Scan
for ECal in ['3', '5', '7', '10', '15', '20']:
    HCal = '30'

    print "Processing Results For Detector ECal: " + ECal + " and HCal: " + HCal + "\n"

    inputRootFileFolder = "/r06/lc/sg568/ReviewJER/RootFiles/Stage" + stage + "/" + ECal + "x" + ECal + "_" + HCal + "x" + HCal + "/"
    outputRootFileFolder = inputRootFileFolder

    results += '-----------------------------------------------------------------------------------------------------------------------------------\n'
    results += 'ILD_o1_v06_' + ECal + 'x' + ECal + '_' + HCal + 'x' + HCal + '\n'
    results += '-----------------------------------------------------------------------------------------------------------------------------------\n'   

    for pandoraSettings in ['Muon', 'Default', 'Perfect_Photon', 'Perfect_Photon_Neutron_K0L', 'Perfect_PFA']:
        results += pandoraSettings + '\n'

        for jetEnergy in ['91', '200', '360', '500']:
            inputRootFileFormat = "ILD_o1_v06_uds" + jetEnergy + "_*_" + pandoraSettings + ".root"
            outputRootFileName = "PfoAnalysisHistorgrams_ILD_o1_v06_" + ECal + "x" + ECal + "_" + HCal + "x" + HCal + "_uds" + jetEnergy + "GeV_PandoraSettings" + pandoraSettings + ".root"

            argsString = executable + ' ' + inputRootFileFolder + inputRootFileFormat + ' ' + outputRootFileFolder + outputRootFileName 
            args = argsString.split()
            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
            popen.wait()
            output = popen.stdout.read()

            resultsLine = ''
            for line in output.splitlines():
                if 'fPFA_L7A' in line:
                    resultsLine = line

            results += jetEnergy + ' GeV Di Jet Energy:' + resultsLine + '\n'
    results += '\n'

# HCal Param Scan
for HCal in ['10', '20', '40', '50', '100']:
    ECal = '5'
   
    print "Processing Results For Detector ECal: " + ECal + " and HCal: " + HCal + "\n"
 
    inputRootFileFolder = "/r06/lc/sg568/ReviewJER/RootFiles/Stage" + stage + "/" + ECal + "x" + ECal + "_" + HCal + "x" + HCal + "/"
    outputRootFileFolder = inputRootFileFolder

    results += '-----------------------------------------------------------------------------------------------------------------------------------\n'
    results += 'ILD_o1_v06_' + ECal + 'x' + ECal + '_' + HCal + 'x' + HCal + '\n'
    results += '-----------------------------------------------------------------------------------------------------------------------------------\n'   

    for pandoraSettings in ['Muon', 'Default', 'Perfect_Photon', 'Perfect_Photon_Neutron_K0L', 'Perfect_PFA']:
        results += pandoraSettings + '\n'

        for jetEnergy in ['91', '200', '360', '500']:
            inputRootFileFormat = "ILD_o1_v06_uds" + jetEnergy + "_*_" + pandoraSettings + ".root"
            outputRootFileName = "PfoAnalysisHistorgrams_ILD_o1_v06_" + ECal + "x" + ECal + "_" + HCal + "x" + HCal + "_uds" + jetEnergy + "GeV_PandoraSettings" + pandoraSettings + ".root"
            
            argsString = executable + ' ' + inputRootFileFolder + inputRootFileFormat + ' ' + outputRootFileFolder + outputRootFileName 
            args = argsString.split()
            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
            popen.wait()
            output = popen.stdout.read()

            resultsLine = ''
            for line in output.splitlines():
                if 'fPFA_L7A' in line:
                    resultsLine = line

            results += jetEnergy + ' GeV Di Jet Energy:' + resultsLine + '\n' 
    results += '\n'


text_file = open("Stage" + stage + "Results.txt", "w")
text_file.write(results)
text_file.close()

