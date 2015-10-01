#!/bin/bash

cd Condor 

for runfiles in 'Mokka_Runfile_10_GeV_Energy_13_pdg.txt' 'Mokka_Runfile_10_GeV_Energy_22_pdg.txt' 'Mokka_Runfile_20_GeV_Energy_130_pdg.txt';
do
    for mokksSteeringFile in "mokka_15x15_30x30.sh"  "mokka_3x3_30x30.sh" "mokka_5x5_10x10.sh" "mokka_5x5_30x30.sh" "mokka_5x5_50x50.sh" "mokka_10x10_30x30.sh" "mokka_20x20_30x30.sh" "mokka_5x5_100x100.sh" "mokka_5x5_20x20.sh" "mokka_5x5_40x40.sh" "mokka_7x7_30x30.sh"
    do
        ./condorSupervisor.sh "/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage2/MokkaSteering/MokkaRunfiles/${runfiles}" 500 "/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage2/MokkaSteering/MokkaSteeringScripts/${mokksSteeringFile}"
    done
done
