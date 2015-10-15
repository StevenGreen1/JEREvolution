#!/bin/bash

echo "STARTING CONDOR SUPERVISOR";

if [ $1 ]; then
    myrunlistPre=$1
    myrunlist="/tmp/jobs.${myrunlistPre}.tmp"
    rm -f ${myrunlist}
    cp ${myrunlistPre} ${myrunlist}
    
else
    echo "Not given a runlist! exiting"
    exit 0;
fi

if [ $2 ]; then
    maxRuns=$2
else
    maxRuns=10
fi

directory=${PWD}
directory="${directory}/"

JOBNAME='MarlinCalibration' #mokka

echo "Supervisor will allow no more than $maxRuns jobs to be queued at any time."
nRun=0
nRun=`wc -l < $myrunlist | sed 's/ //g'`

if [ $nRun -le 0 ]; then
    echo "$myrunlist is empty. Exiting..."
    exit 0;
else
    echo "There are still $nRun jobs to be submitted"

    while  [ $nRun -gt 0 ]
    do
        njobs=`condor_q -w | grep "${JOBNAME}.sh" | wc -l | sed 's/ //g'`		
		
        if [ $njobs -lt $maxRuns ]; then
            rm -f temp_Calibration.job
            touch temp_Calibration.job
            echo "executable              = MarlinCalibration.sh                                            " >> temp_Calibration.job 
            echo "initial_dir             = ${directory}                                                    " >> temp_Calibration.job
            echo "notification            = never                                                           " >> temp_Calibration.job
            echo "Requirements            = (POOL == \"GENERAL\") && (OSTYPE == \"SLC6\")                   " >> temp_Calibration.job
            echo "Rank                    = memory                                                          " >> temp_Calibration.job
            echo "output                  = \$ENV(HOME)/CondorLogs/${JOBNAME}.out.\$(Process)               " >> temp_Calibration.job
            echo "error                   = \$ENV(HOME)/CondorLogs/${JOBNAME}.err.\$(Process)               " >> temp_Calibration.job
            echo "log                     = \$ENV(HOME)/CondorLogs/${JOBNAME}.log.\$(Process)               " >> temp_Calibration.job
            echo "environment             = CONDOR_JOB=true                                                 " >> temp_Calibration.job
            echo "Universe                = vanilla                                                         " >> temp_Calibration.job
            echo "getenv                  = false                                                           " >> temp_Calibration.job
            echo "copy_to_spool           = true                                                            " >> temp_Calibration.job
            echo "should_transfer_files   = yes                                                             " >> temp_Calibration.job
            echo "when_to_transfer_output = on_exit_or_evict                                                " >> temp_Calibration.job
        
            tmpfilename="/tmp/job.$$.tmp"
            thisjob=0
            n=0
            rm -f ${tmpfilename};
            touch $tmpfilename
            cat $myrunlist | while read line
            do
               if [ $n -eq 0 ]; then
                    echo "arguments = "${line}                                                     >> temp_Calibration.job
               else
                    echo $line >> $tmpfilename;
               fi
                    let "n++"
            done
            cp ${tmpfilename} ${myrunlist}
            rm ${tmpfilename}
            echo "queue 1"                                                                         >> temp_Calibration.job
            echo "submitted another job as there were only $njobs jobs in the queue and $nRun jobs left to be submitted"

            condor_submit temp_Calibration.job
            usleep 500000
            #condor_q -global -run
            nRun=`wc -l < $myrunlist | sed 's/ //g'`
            rm -f temp_Calibration.job
        else
            usleep 500000
        fi
    done
fi
echo "$myrunlist is empty. Exiting..."

echo "Checking the jobs are finished..."

njobs2=`condor_q -w | grep "${JOBNAME}.sh" | wc -l | sed 's/ //g'`

sleep_time=10

while [ $njobs2 -gt 0 ];
do
    echo "Not finished yet, come back later."
    sleep ${sleep_time}s
    njobs2=`condor_q -w | grep "${JOBNAME}.sh" | wc -l | sed 's/ //g'`
done
    
echo "Finished"

exit 0;
