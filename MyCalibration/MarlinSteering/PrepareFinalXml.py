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

#======================
# Calibration Constants
#======================
CalibrECal_Input = sys.argv[2]
CalibrECal_Input2 = 2 * float(CalibrECal_Input)
CalibrECal = str(CalibrECal_Input) + ' ' + str(CalibrECal_Input2)
CalibrHCalBarrel = sys.argv[3]
CalibrHCalEndcap = sys.argv[4]
CalibrHCalOther = sys.argv[5]
ECalBarrelTimeWindowMax = sys.argv[6]
HCalBarrelTimeWindowMax = sys.argv[7]
ECalEndcapTimeWindowMax = sys.argv[8]
HCalEndcapTimeWindowMax = sys.argv[9]
CalibrMuon = '56.7'
ECalGeVToMIP = sys.argv[10]
HCalGeVToMIP = sys.argv[11]
MuonGeVToMIP = sys.argv[12]
ECalMIPMPV= sys.argv[13]
HCalMIPMPV= sys.argv[14]
MHHHE = sys.argv[15]
ECalToEm = sys.argv[16]
HCalToEm = sys.argv[17]
ECalToHad = sys.argv[18]
HCalToHad = sys.argv[19]
#======================
# Output Path
#======================

outputPath = sys.argv[1]

#======================

baseFileName = 'FinalSteeringFileTemplate.xml'

jobList = ''

base = open(baseFileName,'r')
baseContent = base.read()
base.close()

newContent = baseContent

newContent = re.sub('CALIBRECAL_XXXX',CalibrECal,newContent)
newContent = re.sub('CALIBRHCALBARREL_XXXX',CalibrHCalBarrel,newContent)
newContent = re.sub('CALIBRHCALENDCAP_XXXX',CalibrHCalEndcap,newContent)
newContent = re.sub('CALIBRHCALOTHER_XXXX',CalibrHCalOther,newContent)
newContent = re.sub('ECALBARRELTIMEWINDOWMAX_XXXX',ECalBarrelTimeWindowMax,newContent)
newContent = re.sub('HCALBARRELTIMEWINDOWMAX_XXXX',HCalBarrelTimeWindowMax,newContent)
newContent = re.sub('ECALENDCAPTIMEWINDOWMAX_XXXX',ECalEndcapTimeWindowMax,newContent)
newContent = re.sub('HCALENDCAPTIMEWINDOWMAX_XXXX',HCalEndcapTimeWindowMax,newContent)
newContent = re.sub('CALIBRMUON_XXXX',CalibrMuon,newContent)
newContent = re.sub('ECALMIPMPV_XXXX',ECalMIPMPV,newContent)
newContent = re.sub('HCALMIPMPV_XXXX',HCalMIPMPV,newContent)
newContent = re.sub('ECALTOMIP_XXXX',ECalGeVToMIP,newContent)
newContent = re.sub('HCALTOMIP_XXXX',HCalGeVToMIP,newContent)
newContent = re.sub('MUONTOMIP_XXXX',MuonGeVToMIP,newContent)
newContent = re.sub('MHHHE_XXXX',MHHHE,newContent)
newContent = re.sub('ECALTOEM_XXXX',ECalToEm,newContent)
newContent = re.sub('HCALTOEM_XXXX',HCalToEm,newContent)
newContent = re.sub('ECALTOHAD_XXXX',ECalToHad,newContent)
newContent = re.sub('HCALTOHAD_XXXX',HCalToHad,newContent)

fullPath = os.path.join(outputPath, 'ILD_o1_v06_AAxAA_BBxBB_XX_YY.xml')

file = open(fullPath,'w')
file.write(newContent)
file.close()


