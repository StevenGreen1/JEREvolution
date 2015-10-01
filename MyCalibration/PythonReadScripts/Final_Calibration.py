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
CalibrECal_Input = sys.argv[1]
CalibrECal_Input2 = 2 * float(CalibrECal_Input)
CalibrECal = str(CalibrECal_Input) + ' ' + str(CalibrECal_Input2)
CalibrHCalBarrel = sys.argv[2]
CalibrHCalEndCap = sys.argv[3]
CalibrHCalOther = sys.argv[4]
CalibrMuon = '56.7'
ECALBarrelTimeWindowMax = sys.argv[5]
HCALBarrelTimeWindowMax = sys.argv[6]
ECALEndcapTimeWindowMax = sys.argv[7]
HCALEndcapTimeWindowMax = sys.argv[8]

ECalGeVToMIP = sys.argv[9]
HCalGeVToMIP = sys.argv[10]
MuonGeVToMIP = sys.argv[11]
HCalMIPMPV = sys.argv[12]

MHHHE = sys.argv[13]

ECalToEm = sys.argv[14]
HCalToEm = sys.argv[15]
ECalToHad = sys.argv[16]
HCalToHad = sys.argv[17]

#======================
# Output Path
#======================

outputPath = sys.argv[18]

#======================

jobList = ''

jobList += 'CalibrECAL was found to be:                         '
jobList += str(CalibrECal) + '\n'

jobList += 'CalibrHCALBarrel was found to be:                   '
jobList += str(CalibrHCalBarrel) + '\n'

jobList += 'CalibrHCALEndcap was found to be:                   '
jobList += str(CalibrHCalEndCap) + '\n'

jobList += 'CalibrHCALOther was found to be:                    '
jobList += str(CalibrHCalOther) + '\n'

jobList += 'ECalGeVToMIP was found to be:                       '
jobList += str(ECalGeVToMIP) + '\n'

jobList += 'HCalGeVToMIP was found to be:                       '
jobList += str(HCalGeVToMIP) + '\n'

jobList += 'MuonGeVToMIP was found to be:                       '
jobList += str(MuonGeVToMIP) + '\n'

jobList += 'HCalMIPMPV (adc not calo hit) was found to be:      '
jobList += str(HCalMIPMPV) + '\n'

jobList += 'MaxHCalHitHadronicEnergy was found to be:           '
jobList += str(MHHHE) + '\n'

jobList += 'ECalToEMGeVCalibration was found to be:             '
jobList += str(ECalToEm) + '\n'

jobList += 'HCalToEMGeVCalibration was found to be:             '
jobList += str(HCalToEm) + '\n'

jobList += 'ECalToHadGeVCalibration was found to be:            '
jobList += str(ECalToHad) + '\n'

jobList += 'HCalToHadGeVCalibration was found to be:            '
jobList += str(HCalToHad) + '\n'

jobList += 'ECALBarrelTimeWindowMax is:                         '
jobList += ECALBarrelTimeWindowMax + '\n'

jobList += 'HCALBarrelTimeWindowMax is:                         '
jobList += HCALBarrelTimeWindowMax + '\n'

jobList += 'ECALEndcapTimeWindowMax is:                         '
jobList += ECALEndcapTimeWindowMax + '\n'

jobList += 'HCALEndcapTimeWindowMax is:                         '
jobList += HCALEndcapTimeWindowMax + '\n'

file = open( outputPath + 'Final_Calibration.txt','w')
file.write(jobList)
file.close()
