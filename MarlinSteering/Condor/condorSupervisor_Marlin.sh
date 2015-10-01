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

# Get directory script is running in
directory=${PWD}
directory="${directory}"

JOBNAME="Marlin_ReviewJER"

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
        njobs=`condor_q -w | grep "${JOBNAME}" | wc -l | sed 's/ //g'`		
		
        if [ $njobs -lt $maxRuns ]; then
            rm -f temp.job
            touch temp.job
            echo "executable              = Marlin_ReviewJER.sh                                             " >> temp.job 
            echo "initial_dir             = ${directory}                                                    " >> temp.job
            echo "notification            = never                                                           " >> temp.job
            echo "Requirements            = (OSTYPE == \"SLC6\")                                            " >> temp.job
# echo "Requirements            = (POOL == \"GENERAL\") && (OSTYPE == \"SLC6\")                   " >> temp.job
            echo "Rank                    = memory                                                          " >> temp.job
            echo "output                  = \$ENV(HOME)/CondorLogs/${JOBNAME}.out.\$(Process)               " >> temp.job
            echo "error                   = \$ENV(HOME)/CondorLogs/${JOBNAME}.err.\$(Process)               " >> temp.job
            echo "log                     = \$ENV(HOME)/CondorLogs/${JOBNAME}.log.\$(Process)               " >> temp.job
            echo "environment             = CONDOR_JOB=true                                                 " >> temp.job
            echo "Universe                = vanilla                                                         " >> temp.job
            echo "getenv                  = false                                                           " >> temp.job
            echo "copy_to_spool           = true                                                            " >> temp.job
            echo "should_transfer_files   = yes                                                             " >> temp.job
            echo "when_to_transfer_output = on_exit_or_evict                                                " >> temp.job
        
            tmpfilename="/tmp/job.$$.tmp"
            thisjob=0
            n=0
            rm -f ${tmpfilename};
            touch $tmpfilename
            cat $myrunlist | while read line
            do
               if [ $n -eq 0 ]; then
                    echo "arguments = "${line}                                                     >> temp.job
               else
                    echo $line >> $tmpfilename;
               fi
                    let "n++"
            done
            cp ${tmpfilename} ${myrunlist}
            rm ${tmpfilename}
            echo "queue 1"                                                                         >> temp.job
            echo "submitted another job as there were only $njobs jobs in the queue and $nRun jobs left to be submitted"

            condor_submit temp.job
            usleep 500000
            nRun=`wc -l < $myrunlist | sed 's/ //g'`
            rm -f temp.job
        else
            usleep 500000
        fi
    done
fi
echo "$myrunlist is empty. Exiting..."
exit 0;
