# -*- coding: utf-8 -*-
import os
import re
import random
import dircache
import sys

Mokka_Script_Format = 'mokka_(.*?)x(.*?)_(.*?)x(.*?).sh'
Gear_Path = '/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage2/MokkaSteering/MokkaGearFiles/'
LCIO_Path = '/r06/lc/sg568/ReviewJER/Slcio/Stage2/'
Init_Ilcsoft_Script = '/usera/sg568/ilcsoft_v01_17_07/init_ilcsoft.sh'

fileDirectory = '/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage2/MokkaSteering/MokkaSteeringScripts'
allFilesInDirectory = dircache.listdir(fileDirectory)
inputFileExt = 'sh'

allFiles = []
allFiles.extend(allFilesInDirectory)
allFiles[:] = [ item for item in allFiles if re.match('.*\.'+inputFileExt+'$',item.lower()) ]
allFiles.sort()

if allFiles:
    array_size=len(allFiles)
    for nfiles in range (array_size):
        nextFile = allFiles.pop(0)
        matchObj = re.match(Mokka_Script_Format, nextFile, re.M|re.I)
        if matchObj:
            ECal = matchObj.group(1)
            HCal = matchObj.group(3)
 
            base = open(nextFile,'r')
            baseContent = base.read()
            base.close()

            newContent = re.sub('/Mokka/init/MokkaGearFileName (.*?)\n','/Mokka/init/MokkaGearFileName ' + Gear_Path + 'ILD_o1_v06_' + ECal + 'x' + ECal + '_' + HCal + 'x' + HCal + '.gear' + '\n',baseContent)
            newContent = re.sub('/Mokka/init/lcioFilename (.*?)\n','/Mokka/init/lcioFilename ' + LCIO_Path + ECal + 'x' + ECal + '_' + HCal + 'x' + HCal + '/ILD_o1_v06_$2_$3.slcio' + '\n',newContent)
            newContent = re.sub('source (.*?)\n','source ' + Init_Ilcsoft_Script + '\n',newContent)

            file = open(nextFile,'w')
            file.write(newContent)
            file.close()
