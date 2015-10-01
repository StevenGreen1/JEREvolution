#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <sstream>
#include <stdio.h>
#include <cstdlib>

using namespace std;

int main () 
{
    int pdgNumber(0);
    float energy(0.f), evtNumber(0.f), jobSize(0);

    std::cout << "Which single particle events would you like to simulate? (Kaon = 130, Photon = 22, Muon = 13)" << std::endl;
    std::cin >> pdgNumber;

    std::cout << "What Energy (in GeV) Kaons do you want to make?" << std::endl;
    std::cin >> energy;

    std::cout << "How many events would you like to simulate in total?" << std::endl;
    std::cin >> evtNumber;

    std::cout << "How many events do you want to run per condor job?" << std::endl;
    std::cin >> jobSize;

    std::ostringstream strBufPdgNumber;
    strBufPdgNumber << pdgNumber;
    std::string strPdgNumber(strBufPdgNumber.str());

    std::ostringstream strBufEnergy;
    strBufEnergy << energy;
    std::string strEnergy(strBufEnergy.str());

    std::ostringstream strBufnumber;
    strBufnumber << evtNumber;
    std::string strNumber(strBufnumber.str());

    std::ostringstream strBufJobSize;
    strBufJobSize << jobSize;
    std::string strJobSize(strBufJobSize.str());

    std::string prefixRunfile = strEnergy + "_GeV_Energy_" + strPdgNumber + "_pdg";

    std::string runfileFilenameMokka = "/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage2/MokkaSteering/MokkaRunfiles/Mokka_Runfile_" + prefixRunfile + ".txt";
    ofstream runfileMokka;
    runfileMokka.open (runfileFilenameMokka.c_str());

    std::srand(1234576);

    float mass(0.f), pTot(std::sqrt((energy*energy)-(mass*mass))), pi(std::acos(0)*2), numberJobs(evtNumber/jobSize);

    if (130==pdgNumber)
        mass = 0.497614; // PDG 29-9-14

    else if (22==pdgNumber)
        mass = 0;

    else if (13==pdgNumber)
        mass =  0.1056583715; // PDG 29-9-14

    else
        std::cout << "Please select from the avaliable particles." << std::endl;

    for (int z = 1; z <= numberJobs; z++)
    {
        std::ostringstream strBufZ;
        strBufZ << z;
        std::string strZ(strBufZ.str());

        ofstream jobZFile;
        string jobZFilename = "/usera/sg568/ilcsoft_v01_17_07/JEREvolution/Stage2/MokkaSteering/CalibrationHEPEvtFiles/" + prefixRunfile+ "_SN_" + strZ + ".HEPEvt"; 
        jobZFile.open (jobZFilename.c_str());

        for (int  i = 0 ; i < jobSize ; i++)
        {
            const float sign(((static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX)) > 0.5f) ? 1.f : -1.f);
            float cosTheta = sign * (static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX));
            float phi = 2 * pi * (static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX));

            float pX = pTot * std::sin(std::acos(cosTheta)) * std::cos(phi);
            float pY = pTot * std::sin(std::acos(cosTheta)) * std::sin(phi);
            float pZ = pTot * cosTheta;

            jobZFile << "\t" << 1 << "\n";
            jobZFile << "\t\t" << 1 << "\t" << strPdgNumber << "\t\t" << 0 << "\t\t" << 0 << "\t" << pX << "\t\t" << pY << "\t\t" << pZ << "\t\t" << mass << "\n";
        }
        runfileMokka << jobZFilename << " " << prefixRunfile+ "_SN_" + strZ << " 0 " << strJobSize << "\n";
        jobZFile.close();
    }
    runfileMokka.close();
    return 0;
}
