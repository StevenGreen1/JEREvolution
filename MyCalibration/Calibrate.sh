#!/bin/bash

# Paths must end in a /
# The serial number in the slcio file must look like a wildcard (.*?) in python.
# Source root to begin with !!
# CalibMUON set to 70.1 in xml file as this is an improvment to a calibration constant but not set in fine detail.

#===============================================
# Input File Information
#===============================================

#echo $@
slcioPath="${1}"
slcioFormat="${2}"
gearFile="${3}"
outputPath="${4}"
pandoraSettingsFile="${5}"

# Hadronic Energy Truncation
MHHHE="${6}"

# Number of HCal layers, for Calibr HCal guess
numberHCalLayers="${7}"

#===============================================
# Default File Information
#===============================================
PandoraAnalysisPath="/usera/sg568/ilcsoft_v01_17_07/OptimisationStudies/PandoraAnalysis_OptimisationStudies/LCPandoraAnalysis/bin/"
#PandoraAnalysisPath="/cvmfs/ilc.desy.de/sw/x86_64_gcc44_sl6/v01-17-07/PandoraAnalysis/v01-00-01/bin/"
#PandoraAnalysisPath="/usera/sg568/ilcsoft_v01_17_07/PandoraAnalysis/bin/"

hadronicScaleSettingPandora="CSM" #TEM or CSM
sourceFile="/var/clus/usera/sg568/ilcsoft_v01_17_07/OptimisationStudies/init_ilcsoft_OptimisationStduies.sh"
useCondor="Yes"
maxNumCondorJobs=300

digitisationAccuracy=0.05                       # Fractional accuracy targetted by digitisation stage 
pandoraPFAAccuracy=0.005                        # Fractional accuracy targeted by PandoraPFA calibration stage 

#==============================================
# Calibration Information
#==============================================
# PandoraPFA Point To Calibration
#===================
kaonLEnergyCalibration=20
photonEnergyCalibration=10

#===================
# KaonL Points for non linearity corrections if implemented.
#===================
kaonLEnergies[0]=1
kaonLEnergies[1]=2
kaonLEnergies[2]=5
kaonLEnergies[3]=10
kaonLEnergies[4]=20
kaonLEnergies[5]=50
kaonLEnergies[6]=100

#===================
# Kaon Kinetic Energy - Used for calibration do not change
#===================
kaonLMass=0.497614
kaonLKineticEnergyCalibration=$(echo "scale=10; ${kaonLEnergyCalibration} -${kaonLMass}" | bc)

#===================
# MIP definition 
#===================
muonEnergyCalibration=10

#===============================================
# Initial Guesses For Calibration Parameters
#===============================================
# Digitisation (Inital Guesses = Defaults)
#===============================================
# This gets doubled in the code to become 42.91 85.82 as ECal thickness doubles in detector
CalibrECAL=42.77

CalibrHCALBarrel=43.58
CalibrHCALEndCap=50.26
CalibrHCALOther=26.76

CalibrHCALBarrel=$(echo "scale=10; ${CalibrHCALBarrel} * 48 / ${numberHCalLayers}" | bc)
CalibrHCALEndCap=$(echo "scale=10; ${CalibrHCALEndCap} * 48 / ${numberHCalLayers}" | bc)

ECalBarrelTimeWindowMax="${8}"
HCalBarrelTimeWindowMax="${9}"
ECalEndCapTimeWindowMax="${10}"
HCalEndCapTimeWindowMax="${11}"

#===============================================
# Pandora PFA
#===============================================
ECalToEm=0.9995
HCalToEm=1.075
ECalToHad=1.076
HCalToHad=1.075

#===============================================
# GeVToMIP
#===============================================
ECalGeVToMIP=160.0
HCalGeVToMIP=34.8
MuonGeVToMIP=10.0

ECalMIPMPV=0.00015
HCalMIPMPV=0.00004
#===============================================
# Clear previous files
#===============================================
rm -fr RootFiles
mkdir RootFiles
rm -fr MarlinXml
mkdir MarlinXml

#===============================================
# Output File Information
#===============================================
calibrationFile="${outputPath}Calibration.txt"
rm ${calibrationFile}
touch ${calibrationFile}
#===============================================
# Path To Root Files
#===============================================
path=$(pwd)

PythonReadScripts="${path}/PythonReadScripts/"
XmlGeneration="${path}/MarlinSteering/"
MarlinXml="${path}/MarlinXml/"
RootFileGeneration="${path}/MarlinSteering/Condor/"
RootFiles="${path}/RootFiles/"

kaonLPath="${path}/RootFiles/ILD_o1_v06_${kaonLEnergyCalibration}_GeV_KaonL_SN_*.root"
photonPath="${path}/RootFiles/ILD_o1_v06_${photonEnergyCalibration}_GeV_Photon_SN_*.root"
muonPath="${path}/RootFiles/ILD_o1_v06_${muonEnergyCalibration}_GeV_Muon_SN_*.root"

#==============================================
if [ "$useCondor" = "Yes" ];then
    cd ${RootFileGeneration}

    python Source.py ${sourceFile}
elif [ "$useCondor" = "No" ];then
    source ${sourceFile}

else
    echo "Please select whether you wish to use condor."
fi

#===============================================#
#===============================================#
#                 Digitisation                  #
#===============================================#
#===============================================#

# Set MIP scale for realistic ECal and HCal
cd ${XmlGeneration}
python PrepareXml.py "Muon" ${muonEnergyCalibration} ${slcioPath} ${slcioFormat} ${gearFile} ${pandoraSettingsFile} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

# Process steering files
cd ${RootFileGeneration}
Runfile="MarlinRunFile_${muonEnergyCalibration}_GeV_Muon.txt"

if [ "$useCondor" = "Yes" ];then
    ./CondorSupervisor.sh ${Runfile} ${maxNumCondorJobs}

elif [ "$useCondor" = "No" ];then
    ./DummyCondorSupervisor.sh ${Runfile} ${maxNumCondorJobs}

else
    echo "Please select whether you wish to use condor."
fi

${PandoraAnalysisPath}SimCaloHitEnergyDistribution -a "${muonPath}" -b "${muonEnergyCalibration}" -c "${outputPath}"

#===============================================#
#             GeV To MIP Constants              #
#===============================================#

cd ${PythonReadScripts}

ECalMIPMPV=$(python Extract_SimCaloHitMIPMPV.py ${calibrationFile} "ECal")
HCalMIPMPV=$(python Extract_SimCaloHitMIPMPV.py ${calibrationFile} "HCal")

#===============================================#
#          ECAL Digitisation Constants          #
#===============================================#

# Generate Marlin steering files with initial guesses
cd ${XmlGeneration}
python PrepareXml.py "Photon" ${photonEnergyCalibration} ${slcioPath} ${slcioFormat} ${gearFile} ${pandoraSettingsFile} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

#particle = sys.argv[1]
#energy = sys.argv[2]
#slcioPath = sys.argv[3]
#slcioFormat = sys.argv[4] #'ILD_o1_v06_ENERGY_GeV_energy_PARTICLE_pdg_SN_(.*?).slcio'
#gearFile = sys.argv[5]
#pandoraSettingsDefault = sys.argv[6]
#CalibrECal = sys.argv[7]
#CalibrHCalBarrel = sys.argv[8]
#CalibrHCalEndCap = sys.argv[9]
#CalibrHCalOther = sys.argv[10]
#ECalBarrelTimeWindowMax = sys.argv[11]
#HCalBarrelTimeWindowMax = sys.argv[12]
#ECalEndCapTimeWindowMax = sys.argv[13]
#HCalEndCapTimeWindowMax = sys.argv[14]
#ECalToMIP = sys.argv[15]
#HCalToMIP = sys.argv[16]
#MuonToMIP = sys.argv[17]
#MHHHE = sys.argv[18]
#ECalToEm = sys.argv[19]
#HCalToEm = sys.argv[20]
#ECalToHad = sys.argv[21]
#HCalToHad = sys.argv[22]

# Generate root files

cd ${RootFileGeneration}

chmod u+x CondorSupervisor.sh
chmod u+x DummyCondorSupervisor.sh
chmod u+x MarlinCalibration.sh

Runfile="MarlinRunFile_${photonEnergyCalibration}_GeV_Photon.txt"

if [ "$useCondor" = "Yes" ];then
    ./CondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 

elif [ "$useCondor" = "No" ];then
    ./DummyCondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 

else
    echo "Please select whether you wish to use condor."
fi

# Find and update CalibrECAL
${PandoraAnalysisPath}ECalDigitisation_ContainedEvents -a "${photonPath}" -b "${photonEnergyCalibration}" -c "${digitisationAccuracy}" -d "${outputPath}" -e 90 

cd ${PythonReadScripts}

CalibrECAL=$(python ECal_Digi_Extract.py ${calibrationFile} ${photonEnergyCalibration} ${CalibrECAL} "Calibration_Constant")
ECal_Mean=$(python ECal_Digi_Extract.py ${calibrationFile} ${photonEnergyCalibration} ${CalibrECAL} "Mean")
Fractional_Error_ECal_Mean=$(echo "scale=10; sqrt((${photonEnergyCalibration} -${ECal_Mean})^2)/${photonEnergyCalibration}" | bc)

# Loop until CalibrECAL acceptable
CheckECalDigi=$(echo "$Fractional_Error_ECal_Mean >= ${digitisationAccuracy}" | bc -l)

while [[ $CheckECalDigi -gt 0 ]] 
do
    cd ${XmlGeneration}
    python PrepareXml.py "Photon" ${photonEnergyCalibration} ${slcioPath} ${slcioFormat} ${gearFile} ${pandoraSettingsFile} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

    cd ${RootFileGeneration}
    Runfile="MarlinRunFile_${photonEnergyCalibration}_GeV_Photon.txt"

    if [ "$useCondor" = "Yes" ];then
        ./CondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 

    elif [ "$useCondor" = "No" ];then
        ./DummyCondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 

    else
        echo "Please select whether you wish to use condor."
    fi

    ${PandoraAnalysisPath}ECalDigitisation_ContainedEvents -a "${photonPath}" -b "${photonEnergyCalibration}" -c "${digitisationAccuracy}" -d "${outputPath}" -e 90

    cd ${PythonReadScripts}
    CalibrECAL=$(python ECal_Digi_Extract.py ${calibrationFile} ${photonEnergyCalibration} ${CalibrECAL} "Calibration_Constant")
    ECal_Mean=$(python ECal_Digi_Extract.py ${calibrationFile} ${photonEnergyCalibration} ${CalibrECAL} "Mean")

    Fractional_Error_ECal_Mean=$(echo "scale=10; sqrt((${photonEnergyCalibration} -${ECal_Mean})^2)/${photonEnergyCalibration}" | bc)

    CheckECalDigi=$(echo "$Fractional_Error_ECal_Mean >= ${digitisationAccuracy}" | bc -l)
done

#===============================================#
#          HCAL Digitisation Constants          #
#===============================================#
# Generate Marlin steering files with initial guesses

cd ${XmlGeneration}
python PrepareXml.py "KaonL" ${kaonLEnergyCalibration} ${slcioPath} ${slcioFormat} ${gearFile} ${pandoraSettingsFile} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

# Generate root files

cd ${RootFileGeneration}
Runfile="MarlinRunFile_${kaonLEnergyCalibration}_GeV_KaonL.txt"

if [ "$useCondor" = "Yes" ];then
    ./CondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 

elif [ "$useCondor" = "No" ];then
    ./DummyCondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 

else
    echo "Please select whether you wish to use condor."
fi

# Find and update CalibrHCALBarrel and CalibrHCALEndCap
${PandoraAnalysisPath}HCalDigitisation_ContainedEvents -a "${kaonLPath}" -b "${kaonLEnergyCalibration}" -c "${digitisationAccuracy}" -d "${outputPath}" -e "90" -f "${numberHCalLayers}" -g "Barrel" -i "0.2" -j "0.6"
${PandoraAnalysisPath}HCalDigitisation_ContainedEvents -a "${kaonLPath}" -b "${kaonLEnergyCalibration}" -c "${digitisationAccuracy}" -d "${outputPath}" -e "90" -f "${numberHCalLayers}" -g "EndCap" -i "0.8" -j "0.9"

cd ${PythonReadScripts}
CalibrHCALBarrel=$(python HCal_Digi_Extract.py ${calibrationFile} ${kaonLKineticEnergyCalibration} ${CalibrHCALBarrel} "Barrel" "Calibration_Constant")
CalibrHCALEndCap=$(python HCal_Digi_Extract.py ${calibrationFile} ${kaonLKineticEnergyCalibration} ${CalibrHCALEndCap} "EndCap" "Calibration_Constant")

HCal_Barrel_Mean=$(python HCal_Digi_Extract.py ${calibrationFile} ${kaonLKineticEnergyCalibration} ${CalibrHCALBarrel} "Barrel" "Mean")
HCal_EndCap_Mean=$(python HCal_Digi_Extract.py ${calibrationFile} ${kaonLKineticEnergyCalibration} ${CalibrHCALEndCap} "EndCap" "Mean")

Fractional_HCal_Barrel_Mean=$(echo "scale=10; sqrt((${kaonLKineticEnergyCalibration} -${HCal_Barrel_Mean})^2)/${kaonLKineticEnergyCalibration}" | bc)
Fractional_HCal_EndCap_Mean=$(echo "scale=10; sqrt((${kaonLKineticEnergyCalibration} -${HCal_EndCap_Mean})^2)/${kaonLKineticEnergyCalibration}" | bc)

# Loop until CalibrHCALBarrel and CalibrHCALEndCap acceptable
CheckHCalBarrelDigi=$(echo "$Fractional_HCal_Barrel_Mean >= ${digitisationAccuracy}" | bc -l)
CheckHCalEndCapDigi=$(echo "$Fractional_HCal_EndCap_Mean >= ${digitisationAccuracy}" | bc -l)


while [[ $CheckHCalBarrelDigi -gt 0 ]] || [[ $CheckHCalEndCapDigi -gt 0 ]]
do
    cd ${XmlGeneration}
    python PrepareXml.py "KaonL" ${kaonLEnergyCalibration} ${slcioPath} ${slcioFormat} ${gearFile} ${pandoraSettingsFile} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

    cd ${RootFileGeneration}
    Runfile="MarlinRunFile_${kaonLEnergyCalibration}_GeV_KaonL.txt"

    if [ "$useCondor" = "Yes" ];then
        ./CondorSupervisor.sh ${Runfile} ${maxNumCondorJobs}

    elif [ "$useCondor" = "No" ];then
        ./DummyCondorSupervisor.sh ${Runfile} ${maxNumCondorJobs}

    else
        echo "Please select whether you wish to use condor."
    fi

    ${PandoraAnalysisPath}HCalDigitisation_ContainedEvents -a "${kaonLPath}" -b "${kaonLEnergyCalibration}" -c "${digitisationAccuracy}" -d "${outputPath}" -e "90" -f "${numberHCalLayers}" -g "Barrel" -i "0.2" -j "0.6"
    ${PandoraAnalysisPath}HCalDigitisation_ContainedEvents -a "${kaonLPath}" -b "${kaonLEnergyCalibration}" -c "${digitisationAccuracy}" -d "${outputPath}" -e "90" -f "${numberHCalLayers}" -g "EndCap" -i "0.8" -j "0.9"

    cd ${PythonReadScripts}
    CalibrHCALBarrel=$(python HCal_Digi_Extract.py ${calibrationFile} ${kaonLKineticEnergyCalibration} ${CalibrHCALBarrel} "Barrel" "Calibration_Constant")
    CalibrHCALEndCap=$(python HCal_Digi_Extract.py ${calibrationFile} ${kaonLKineticEnergyCalibration} ${CalibrHCALEndCap} "EndCap" "Calibration_Constant")

    HCal_Barrel_Mean=$(python HCal_Digi_Extract.py ${calibrationFile} ${kaonLKineticEnergyCalibration} ${CalibrHCALBarrel} "Barrel" "Mean")
    HCal_EndCap_Mean=$(python HCal_Digi_Extract.py ${calibrationFile} ${kaonLKineticEnergyCalibration} ${CalibrHCALEndCap} "EndCap" "Mean")

    Fractional_HCal_Barrel_Mean=$(echo "scale=10; sqrt( (${kaonLKineticEnergyCalibration} -${HCal_Barrel_Mean})^2)/${kaonLKineticEnergyCalibration}" | bc)
    Fractional_HCal_EndCap_Mean=$(echo "scale=10; sqrt( (${kaonLKineticEnergyCalibration} -${HCal_EndCap_Mean})^2)/${kaonLKineticEnergyCalibration}" | bc)

    CheckHCalBarrelDigi=$(echo "$Fractional_HCal_Barrel_Mean >= ${digitisationAccuracy}" | bc -l)
    CheckHCalEndCapDigi=$(echo "$Fractional_HCal_EndCap_Mean >= ${digitisationAccuracy}" | bc -l)
done

# Generate Marlin steering files for muons, needed for HCal ring calibration
cd ${XmlGeneration}
python PrepareXml.py "Muon" ${muonEnergyCalibration} ${slcioPath} ${slcioFormat} ${gearFile} ${pandoraSettingsFile} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

# Process steering files
cd ${RootFileGeneration}
Runfile="MarlinRunFile_${muonEnergyCalibration}_GeV_Muon.txt"

if [ "$useCondor" = "Yes" ];then
    ./CondorSupervisor.sh ${Runfile} ${maxNumCondorJobs}

elif [ "$useCondor" = "No" ];then
    ./DummyCondorSupervisor.sh ${Runfile} ${maxNumCondorJobs}

else
    echo "Please select whether you wish to use condor."
fi

${PandoraAnalysisPath}HCalDigitisation_DirectionCorrectionDistribution -a "${kaonLPath}" -b "${kaonLEnergyCalibration}" -c "${outputPath}"
${PandoraAnalysisPath}SimCaloHitEnergyDistribution -a "${muonPath}" -b "${muonEnergyCalibration}" -c "${outputPath}"

cd ${PythonReadScripts}
# Ratio is (Ab_Ec*Sc_R)/(Ab_R*Sc_Ec)
Absorber_Scintillator_Ratio=$(python HCal_Ring_Gear_Information.py ${calibrationFile} ${gearFile} ${muonEnergyCalibration})

# Ratio is MIP_Peak_Ec/MIP_Peak_Ring
MIP_Peak_Ratio=$(python HCal_Ring_Digi_Extract.py ${calibrationFile} ${muonEnergyCalibration})

# Ratio is Dir_Corr_Ec/Dir_Corr_Ring
Direction_Correction_Ratio=$(python HCal_Direction_Corrections_Extract.py ${calibrationFile} ${kaonLEnergyCalibration})

CalibrHCALOther=$(echo "scale=10; " ${Direction_Correction_Ratio}*${MIP_Peak_Ratio}*${Absorber_Scintillator_Ratio}*${CalibrHCALEndCap}*${kaonLKineticEnergyCalibration}/${HCal_EndCap_Mean}| bc)

echo "_____________________________________________________________________________________" >> ${calibrationFile}
echo "CalibrHCALOther                                     : ${CalibrHCALOther} " >> ${calibrationFile}

#===============================================#
#             GeV To MIP Constants              #
#===============================================#
${PandoraAnalysisPath}PandoraPFACalibrate_MipResponse -a "${muonPath}" -b "${muonEnergyCalibration}" -c "${outputPath}" 

cd ${PythonReadScripts}
ECalGeVToMIP=$(python Extract_GeVToMIP.py ${calibrationFile} ${muonEnergyCalibration} "ECal")
HCalGeVToMIP=$(python Extract_GeVToMIP.py ${calibrationFile} ${muonEnergyCalibration} "HCal")
MuonGeVToMIP=$(python Extract_GeVToMIP.py ${calibrationFile} ${muonEnergyCalibration} "Muon")

ECalMIPMPV=$(python Extract_SimCaloHitMIPMPV.py ${calibrationFile} "ECal")
HCalMIPMPV=$(python Extract_SimCaloHitMIPMPV.py ${calibrationFile} "HCal")

#===============================================#
#===============================================#
#            PandoraPFA Calibration             #
#===============================================#
#===============================================#

#===============================================#
# Electromagnetic Energy Scale (Photon Events)  #
#===============================================#

# Generate Xml Files With Initial Guesses
cd ${XmlGeneration}
python PrepareXml.py "Photon" ${photonEnergyCalibration} ${slcioPath} ${slcioFormat} ${gearFile} ${pandoraSettingsFile} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

# Generate Root Files

cd ${RootFileGeneration}
Runfile="MarlinRunFile_${photonEnergyCalibration}_GeV_Photon.txt"

if [ "$useCondor" = "Yes" ];then
    ./CondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 

elif [ "$useCondor" = "No" ];then
    ./DummyCondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 

else
    echo "Please select whether you wish to use condor."
fi

# ECalToEm Calibration 

${PandoraAnalysisPath}PandoraPFACalibrate_EMScale -a "${photonPath}" -b "${photonEnergyCalibration}" -c "${pandoraPFAAccuracy}" -d "${outputPath}" -e "90" 

cd ${PythonReadScripts}
ECalToEm=$(python EM_Extract.py ${calibrationFile} ${photonEnergyCalibration} ${ECalToEm} "Calibration_Constant")
EM_Mean=$(python EM_Extract.py ${calibrationFile} ${photonEnergyCalibration} ${ECalToEm} "Mean")
Fractional_EM_Error=$(echo "scale=10; sqrt( (${photonEnergyCalibration} -${EM_Mean})^2)/${photonEnergyCalibration}" | bc)
CheckECalToEMPandoraPFA=$(echo "$Fractional_EM_Error >= ${pandoraPFAAccuracy}" | bc -l)

while [ $CheckECalToEMPandoraPFA -gt 0 ]
do
    cd ${XmlGeneration}
    python PrepareXml.py "Photon" ${photonEnergyCalibration} ${slcioPath} ${slcioFormat} ${gearFile} ${pandoraSettingsFile} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

    cd ${RootFileGeneration}
    Runfile="MarlinRunFile_${photonEnergyCalibration}_GeV_Photon.txt"

    if [ "$useCondor" = "Yes" ];then
        ./CondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 

    elif [ "$useCondor" = "No" ];then
        ./DummyCondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 

    else
        echo "Please select whether you wish to use condor."
    fi

    ${PandoraAnalysisPath}PandoraPFACalibrate_EMScale -a "${photonPath}" -b "${photonEnergyCalibration}" -c "${pandoraPFAAccuracy}" -d "${outputPath}" -e "90" 

    cd ${PythonReadScripts}
    ECalToEm=$(python EM_Extract.py ${calibrationFile} ${photonEnergyCalibration} ${ECalToEm} "Calibration_Constant")

    EM_Mean=$(python EM_Extract.py ${calibrationFile} ${photonEnergyCalibration} ${ECalToEm} "Mean")
    Fractional_EM_Error=$(echo "scale=10; sqrt( (${photonEnergyCalibration} -${EM_Mean})^2)/${photonEnergyCalibration}" | bc)

    CheckECalToEMPandoraPFA=$(echo "$Fractional_EM_Error >= ${pandoraPFAAccuracy}" | bc -l)
done

#===============================================#
#      Hadronic Energy Scale (KaonL Events)     #
#===============================================#

# Generate Xml Files With Initial Guesses
cd ${XmlGeneration}
python PrepareXml.py "KaonL" ${kaonLEnergyCalibration} ${slcioPath} ${slcioFormat} ${gearFile} ${pandoraSettingsFile} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

# Generate Root Files
cd ${RootFileGeneration}
Runfile="MarlinRunFile_${kaonLEnergyCalibration}_GeV_KaonL.txt"

if [ "$useCondor" = "Yes" ];then
    ./CondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 
elif [ "$useCondor" = "No" ];then
    ./DummyCondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 
else
    echo "Please select whether you wish to use condor."
fi

# HCalToHad and ECalToHad Calibration 
#echo "${kaonLEnergyCalibration}"
#echo "${kaonLPath}"
#echo "${numberHCalLayers}"
#echo "${pandoraPFAAccuracy}"
#echo "${outputPath}" 

if [ "$hadronicScaleSettingPandora" = "CSM" ];then
    ${PandoraAnalysisPath}PandoraPFACalibrate_HadronicScale_ChiSquareMethod -a "${kaonLPath}" -b "${kaonLEnergyCalibration}" -c "${pandoraPFAAccuracy}" -d "${outputPath}" -e "${numberHCalLayers}" 
elif [ "$hadronicScaleSettingPandora" = "TEM" ];then
    ${PandoraAnalysisPath}PandoraPFACalibrate_HadronicScale_TotalEnergyMethod -a "${kaonLPath}" -b "${kaonLEnergyCalibration}" -c "${pandoraPFAAccuracy}" -d "${outputPath}" -e "90" -f "${numberHCalLayers}" 
else
    echo "Select a calibration method."
fi

# Update HCTH and ECTH
cd ${PythonReadScripts}

HCalToHad=$(python Had_Extract.py ${calibrationFile} ${kaonLEnergyCalibration} "HCTH" ${HCalToHad} "Calibration_Constant" ${hadronicScaleSettingPandora}) 
HCalToEm=${HCalToHad}
ECalToHad=$(python Had_Extract.py ${calibrationFile} ${kaonLEnergyCalibration} "ECTH" ${ECalToHad} "Calibration_Constant" ${hadronicScaleSettingPandora}) 
HCalToHad_Fom=$(python Had_Extract.py ${calibrationFile} ${kaonLEnergyCalibration} "HCTH" ${HCalToHad} "FOM" ${hadronicScaleSettingPandora}) 
ECalToHad_Fom=$(python Had_Extract.py ${calibrationFile} ${kaonLEnergyCalibration} "ECTH" ${ECalToHad} "FOM" ${hadronicScaleSettingPandora}) 

# Target Limits on recostruction
UpperLimit=$(echo "1 + ${pandoraPFAAccuracy}" | bc)
LowerLimit=$(echo "1 - ${pandoraPFAAccuracy}" | bc)

# Limits on reconstruction

if [ "$hadronicScaleSettingPandora" = "CSM" ];then
    HCalToHad_UL=$(echo "${kaonLKineticEnergyCalibration}*${UpperLimit}" | bc)
    HCalToHad_LL=$(echo "${kaonLKineticEnergyCalibration}*${LowerLimit}" | bc)
    ECalToHad_UL=$(echo "${kaonLKineticEnergyCalibration}*${UpperLimit}" | bc)
    ECalToHad_LL=$(echo "${kaonLKineticEnergyCalibration}*${LowerLimit}" | bc)

    CheckOne=$(echo "$HCalToHad_Fom >= $HCalToHad_UL" | bc -l)
    CheckTwo=$(echo "$HCalToHad_Fom <= $HCalToHad_LL" | bc -l)
    CheckThree=$(echo "$ECalToHad_Fom >= $ECalToHad_UL" | bc -l)
    CheckFour=$(echo "$ECalToHad_Fom <= $ECalToHad_LL" | bc -l)
elif [ "$hadronicScaleSettingPandora" = "TEM" ];then
    HCalToHad_UL=$(echo "${UpperLimit}" | bc)
    HCalToHad_LL=$(echo "${LowerLimit}" | bc)
    ECalToHad_UL=$(echo "${UpperLimit}" | bc)
    ECalToHad_LL=$(echo "${LowerLimit}" | bc)

    CheckOne=$(echo "$HCalToHad_Fom >= $HCalToHad_UL" | bc -l)
    CheckTwo=$(echo "$HCalToHad_Fom <= $HCalToHad_LL" | bc -l)
    CheckThree=$(echo "$ECalToHad_Fom >= $ECalToHad_UL" | bc -l)
    CheckFour=$(echo "$ECalToHad_Fom <= $ECalToHad_LL" | bc -l)
else
    echo "Select a calibration method."
fi

# Itterate ECTH and HCTH until they are within acceptable limits
while [[ $CheckOne -gt 0 ]] || [[ $CheckTwo -gt 0 ]] || [[ $CheckThree -gt 0 ]] || [[ $CheckFour -gt 0 ]] 
do
    cd ${XmlGeneration}
    python PrepareXml.py "KaonL" ${kaonLEnergyCalibration} ${slcioPath} ${slcioFormat} ${gearFile} ${pandoraSettingsFile} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad} 
 
    cd ${RootFileGeneration}
    Runfile="MarlinRunFile_${kaonLEnergyCalibration}_GeV_KaonL.txt"

    if [ "$useCondor" = "Yes" ];then
        ./CondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 
    elif [ "$useCondor" = "No" ];then
        ./DummyCondorSupervisor.sh ${Runfile} ${maxNumCondorJobs} 
    else
        echo "Please select whether you wish to use condor."
    fi

    if [ "$hadronicScaleSettingPandora" = "CSM" ];then
        ${PandoraAnalysisPath}PandoraPFACalibrate_HadronicScale_ChiSquareMethod -a "${kaonLPath}" -b "${kaonLEnergyCalibration}" -c "${pandoraPFAAccuracy}" -d "${outputPath}" -e "${numberHCalLayers}" 
    elif [ "$hadronicScaleSettingPandora" = "TEM" ];then
        ${PandoraAnalysisPath}PandoraPFACalibrate_HadronicScale_TotalEnergyMethod -a "${kaonLPath}" -b "${kaonLEnergyCalibration}" -c "${pandoraPFAAccuracy}" -d "${outputPath}" -e "90" -f "${numberHCalLayers}" 
    else
        echo "Select a calibration method."
    fi

    cd ${PythonReadScripts}
    HCalToHad=$(python Had_Extract.py ${calibrationFile} ${kaonLEnergyCalibration} "HCTH" ${HCalToHad} "Calibration_Constant" ${hadronicScaleSettingPandora}) 
    HCalToEm=${HCalToHad}
    ECalToHad=$(python Had_Extract.py ${calibrationFile} ${kaonLEnergyCalibration} "ECTH" ${ECalToHad} "Calibration_Constant" ${hadronicScaleSettingPandora}) 
    HCalToHad_Fom=$(python Had_Extract.py ${calibrationFile} ${kaonLEnergyCalibration} "HCTH" ${HCalToHad} "FOM" ${hadronicScaleSettingPandora}) 
    ECalToHad_Fom=$(python Had_Extract.py ${calibrationFile} ${kaonLEnergyCalibration} "ECTH" ${ECalToHad} "FOM" ${hadronicScaleSettingPandora}) 

    if [ "$hadronicScaleSettingPandora" = "CSM" ];then
        HCalToHad_UL=$(echo "${kaonLKineticEnergyCalibration}*${UpperLimit}" | bc) 
        HCalToHad_LL=$(echo "${kaonLKineticEnergyCalibration}*${LowerLimit}" | bc) 
        ECalToHad_UL=$(echo "${kaonLKineticEnergyCalibration}*${UpperLimit}" | bc) 
        ECalToHad_LL=$(echo "${kaonLKineticEnergyCalibration}*${LowerLimit}" | bc) 

        CheckOne=$(echo "$HCalToHad_Fom >= $HCalToHad_UL" | bc -l) 
        CheckTwo=$(echo "$HCalToHad_Fom <= $HCalToHad_LL" | bc -l) 
        CheckThree=$(echo "$ECalToHad_Fom >= $ECalToHad_UL" | bc -l) 
        CheckFour=$(echo "$ECalToHad_Fom <= $ECalToHad_LL" | bc -l) 

    elif [ "$hadronicScaleSettingPandora" = "TEM" ];then
        HCalToHad_UL=$(echo "${UpperLimit}" | bc) 
        HCalToHad_LL=$(echo "${LowerLimit}" | bc) 
        ECalToHad_UL=$(echo "${UpperLimit}" | bc) 
        ECalToHad_LL=$(echo "${LowerLimit}" | bc) 
        
        CheckOne=$(echo "$HCalToHad_Fom >= $HCalToHad_UL" | bc -l) 
        CheckTwo=$(echo "$HCalToHad_Fom <= $HCalToHad_LL" | bc -l) 
        CheckThree=$(echo "$ECalToHad_Fom >= $ECalToHad_UL" | bc -l) 
        CheckFour=$(echo "$ECalToHad_Fom <= $ECalToHad_LL" | bc -l) 

    else
        echo "Select a calibration method."
    fi
done

#===============================================#
#           Final Calibration Numbers           #
#===============================================#

cd ${PythonReadScripts}
python Final_Calibration.py ${outputPath} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

cd ${XmlGeneration}
python PrepareFinalXml.py ${outputPath} ${CalibrECAL} ${CalibrHCALBarrel} ${CalibrHCALEndCap} ${CalibrHCALOther} ${ECalBarrelTimeWindowMax} ${HCalBarrelTimeWindowMax} ${ECalEndCapTimeWindowMax} ${HCalEndCapTimeWindowMax} ${ECalGeVToMIP} ${HCalGeVToMIP} ${MuonGeVToMIP} ${ECalMIPMPV} ${HCalMIPMPV} ${MHHHE} ${ECalToEm} ${HCalToEm} ${ECalToHad} ${HCalToHad}

#===============================================#
#                      End                      #
#===============================================a
