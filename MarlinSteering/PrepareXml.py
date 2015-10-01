# -*- coding: utf-8 -*-
import os
import re
import random
import dircache
import sys

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ''


#===========================
# Input Variables
#===========================

ECalCellSize = sys.argv[1]
HCalCellSize = sys.argv[2]
Stage = sys.argv[3]
baseFile = sys.argv[4]

#===========================
# Read Calibration Constants
#===========================

Slcio_Path = '/r06/lc/marshall/Review/ILD_o1_v06_' + str(ECalCellSize) + 'x' + str(ECalCellSize) + '_' + str(HCalCellSize) + 'x' + str(HCalCellSize) + '/'

Slcio_Format = 'ILD_o1_v06_uds(.*?).slcio'

Gear_File_And_Path = '/usera/marshall/jobs/mokka/Review/gear/ILD_o1_v06_' + str(ECalCellSize) + 'x' + str(ECalCellSize) + '_' + str(HCalCellSize) + 'x' + str(HCalCellSize) + '.gear'

Output_Root_Path = '/r06/lc/sg568/ReviewJER/RootFiles/Stage' + str(Stage) + '/' + str(ECalCellSize) + 'x' + str(ECalCellSize) + '_' + str(HCalCellSize) + 'x' + str(HCalCellSize) + '/'

Pandora_Settings_Muon = '/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage' + str(Stage) + '/PandoraSettings/PandoraSettingsMuon.xml'
Pandora_Settings_Default = '/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage' + str(Stage) + '/PandoraSettings/PandoraSettingsDefault_SiW_' + str(ECalCellSize) + 'x' + str(ECalCellSize) + '.xml'
Pandora_Settings_Perfect_Photon = '/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage' + str(Stage) + '/PandoraSettings/PandoraSettingsPerfectPhoton.xml'
Pandora_Settings_Perfect_Photon_Neutron_K0L = '/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage' + str(Stage) + '/PandoraSettings/PandoraSettingsPerfectPhotonNeutronK0L.xml'
Pandora_Settings_Perfect_PFA = '/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage' + str(Stage) + '/PandoraSettings/PandoraSettingsPerfectPFA.xml'

#===========================

# Read in base file name with appropriate calibration variables
#baseFile = '/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage' + str(Stage) + '/MarlinSteering/ILD_o1_v06_AAxAA_BBxBB_XX_YY.xml'

jobList = ''

base = open(baseFile,'r')
baseContent = base.read()
base.close()

fileDirectory = Slcio_Path

allFilesInDirectory = dircache.listdir(fileDirectory)

inputFileExt = 'slcio'

allFiles = []
allFiles.extend(allFilesInDirectory)
allFiles[:] = [ item for item in allFiles if re.match('.*\.'+inputFileExt+'$',item.lower()) ]
allFiles.sort()

baseFileName = '/r06/lc/sg568/ReviewJER/MarlinXml/Stage' + str(Stage) + '/' + str(ECalCellSize) + 'x' + str(ECalCellSize) + '_' + str(HCalCellSize) + 'x' + str(HCalCellSize) + '/ILD_o1_v06_' + str(ECalCellSize) + 'x' + str(ECalCellSize) + '_' + str(HCalCellSize) + 'x' + str(HCalCellSize) + '_XX_YY.xml'

if allFiles:
    array_size=len(allFiles)
    
    for nfiles in range (array_size):
        
        newContent = baseContent
        nextFile = allFiles.pop(0)
        matchObj = re.match(Slcio_Format, nextFile, re.M|re.I)
        
        if matchObj:
            SN = matchObj.group(1)
            
            # Pandora Settings Files
            newContent = re.sub('PANDORA_SETTINGS_MUON_FILE',Pandora_Settings_Muon,newContent)
            newContent = re.sub('PANDORA_SETTINGS_DEFAULT_FILE',Pandora_Settings_Default,newContent)
            newContent = re.sub('PANDORA_SETTINGS_PERFECT_PHOTON_FILE',Pandora_Settings_Perfect_Photon,newContent)
            newContent = re.sub('PANDORA_SETTINGS_PERFECT_PHOTON_NEUTRON_K0L_FILE',Pandora_Settings_Perfect_Photon_Neutron_K0L,newContent)
            newContent = re.sub('PANDORA_SETTINGS_PERFECT_PFA_FILE',Pandora_Settings_Perfect_PFA,newContent)
 
            # Root Files
            Pandora_Settings_Muon_Root_File = Output_Root_Path + 'ILD_o1_v06_uds' + SN + '_Muon.root'
            newContent = re.sub('PANDORA_SETTINGS_MUON_ROOT_FILE',Pandora_Settings_Muon_Root_File,newContent)

            Pandora_Settings_Default_Root_File = Output_Root_Path + 'ILD_o1_v06_uds' + SN + '_Default.root'
            newContent = re.sub('PANDORA_SETTINGS_DEFAULT_ROOT_FILE',Pandora_Settings_Default_Root_File,newContent)

            Pandora_Settings_Perfect_Photon_Root_File = Output_Root_Path + 'ILD_o1_v06_uds' + SN + '_Perfect_Photon.root'
            newContent = re.sub('PANDORA_SETTINGS_PERFECT_PHOTON_ROOT_FILE',Pandora_Settings_Perfect_Photon_Root_File,newContent)

            Pandora_Settings_Perfect_Photon_Neutron_K0L_Root_File = Output_Root_Path + 'ILD_o1_v06_uds' + SN + '_Perfect_Photon_Neutron_K0L.root'
            newContent = re.sub('PANDORA_SETTINGS_PERFECT_PHOTON_NEUTRON_K0L_ROOT_FILE',Pandora_Settings_Perfect_Photon_Neutron_K0L_Root_File,newContent)

            Pandora_Settings_Perfect_PFA_Root_File = Output_Root_Path + 'ILD_o1_v06_uds' + SN + '_Perfect_PFA.root'
            newContent = re.sub('PANDORA_SETTINGS_PERFECT_PFA_ROOT_FILE',Pandora_Settings_Perfect_PFA_Root_File,newContent)

            # Slcio File
            newContent = re.sub('LCIO_INPUT_FILE',Slcio_Path + nextFile,newContent)

            # Gear File
            newContent = re.sub('GEAR_FILE',Gear_File_And_Path,newContent)
            
            # New File Name 
            newFileName = re.sub('XX_YY','uds' + str(SN),baseFileName)
            
            file = open(newFileName,'w')
            file.write(newContent)
            file.close()
            
            jobList += newFileName
            jobList += '\n'
            del newContent

file = open( '/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage' + str(Stage) + '/MarlinSteering/Condor/Marlin_Runfile_Detector' + str(ECalCellSize) + '_' + str(HCalCellSize) + '.txt','w')
file.write(jobList)
file.close()
