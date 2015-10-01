#!/bin/bash
#==================================
#==================================

Stage=59

# Same LCIO files (and gear file) used for calibation as in stage 2.

MHHHE="1000000.0"

ECalBarrelTimeWindowMax="300.0"
HCalBarrelTimeWindowMax="300.0"
ECalEndcapTimeWindowMax="300.0"
HCalEndcapTimeWindowMax="300.0"


for ECalCellSize in 3 5 7 10 15 20 
do
    # Calibration
    HCalCellSize="30"
    cd MyCalibration
    slcioFormat="ILD_o1_v06_ENERGY_GeV_Energy_PARTICLE_pdg_SN_(.*?).slcio"
    slcioPath="/r06/lc/sg568/ReviewJER/Slcio/Stage2/${ECalCellSize}x${ECalCellSize}_${HCalCellSize}x${HCalCellSize}/"
    gearFile="/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage2/MokkaSteering/MokkaGearFiles/ILD_o1_v06_${ECalCellSize}x${ECalCellSize}_${HCalCellSize}x${HCalCellSize}.gear"
    pandoraSettingsFile="/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage${Stage}/PandoraSettings/PandoraSettingsDefault_SiW_${ECalCellSize}x${ECalCellSize}.xml"
    calibrationResultsPath="/r06/lc/sg568/ReviewJER/CalibrationResults/Stage${Stage}/${ECalCellSize}x${ECalCellSize}_${HCalCellSize}x${HCalCellSize}/"
    numberOfHCalLayers="48"
    ./Calibrate.sh "${slcioPath}" "${slcioFormat}" "${gearFile}" "${calibrationResultsPath}" "${pandoraSettingsFile}" "${MHHHE}" "${numberOfHCalLayers}" "${ECalBarrelTimeWindowMax}" "${HCalBarrelTimeWindowMax}" "${ECalEndcapTimeWindowMax}" "${HCalEndcapTimeWindowMax}"
    cd ..
done

for HCalCellSize in 10 20 40 50 100
do
    # Calibration
    ECalCellSize="5"
    cd MyCalibration
    slcioFormat="ILD_o1_v06_ENERGY_GeV_Energy_PARTICLE_pdg_SN_(.*?).slcio"
    slcioPath="/r06/lc/sg568/ReviewJER/Slcio/Stage2/${ECalCellSize}x${ECalCellSize}_${HCalCellSize}x${HCalCellSize}/"
    gearFile="/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage2/MokkaSteering/MokkaGearFiles/ILD_o1_v06_${ECalCellSize}x${ECalCellSize}_${HCalCellSize}x${HCalCellSize}.gear"
    pandoraSettingsFile="/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage${Stage}/PandoraSettings/PandoraSettingsDefault_SiW_${ECalCellSize}x${ECalCellSize}.xml"
    calibrationResultsPath="/r06/lc/sg568/ReviewJER/CalibrationResults/Stage${Stage}/${ECalCellSize}x${ECalCellSize}_${HCalCellSize}x${HCalCellSize}/"
    numberOfHCalLayers="48"
    ./Calibrate.sh "${slcioPath}" "${slcioFormat}" "${gearFile}" "${calibrationResultsPath}" "${pandoraSettingsFile}" "${MHHHE}" "${numberOfHCalLayers}" "${ECalBarrelTimeWindowMax}" "${HCalBarrelTimeWindowMax}" "${ECalEndcapTimeWindowMax}" "${HCalEndcapTimeWindowMax}"
    cd ..
done

for ECalCellSize in 3 5 7 10 15 20
do
    # Run Jets
    HCalCellSize="30"
    calibrationResultsPath="/r06/lc/sg568/ReviewJER/CalibrationResults/Stage${Stage}/${ECalCellSize}x${ECalCellSize}_${HCalCellSize}x${HCalCellSize}/"
    marlinSteeringFile="${calibrationResultsPath}ILD_o1_v06_AAxAA_BBxBB_XX_YY.xml"
    cd MarlinSteering/
    python PrepareXml.py ${ECalCellSize} ${HCalCellSize} ${Stage} ${marlinSteeringFile}
    cd Condor
    ./condorSupervisor_Marlin.sh "Marlin_Runfile_Detector${ECalCellSize}_${HCalCellSize}.txt" 500
    cd ../../
done

for HCalCellSize in 10 20 40 50 100
do
    # Run Jets
    ECalCellSize="5"
    calibrationResultsPath="/r06/lc/sg568/ReviewJER/CalibrationResults/Stage${Stage}/${ECalCellSize}x${ECalCellSize}_${HCalCellSize}x${HCalCellSize}/"
    marlinSteeringFile="${calibrationResultsPath}ILD_o1_v06_AAxAA_BBxBB_XX_YY.xml"
    cd MarlinSteering/
    python PrepareXml.py ${ECalCellSize} ${HCalCellSize} ${Stage} ${marlinSteeringFile}
    cd Condor
    ./condorSupervisor_Marlin.sh "Marlin_Runfile_Detector${ECalCellSize}_${HCalCellSize}.txt" 500
    cd ../../
done
