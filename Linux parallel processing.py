#Process level parallelism for shell commands
import glob
import subprocess as sp
import multiprocessing as mp
import numpy as np
import pandas as pd

# Run mne_start and initiatlize SUBJECTS_DIR before running

def work(in_file):
    """Defines the work unit on an input file"""
    log = open('/biotic/home/timb/data/camcan/analysis/subjects/bemLogs/' + in_file + 'bem_recon.log', 'w')
    sp.call(['/home/timb/bin/post_recon_steps', '{}'.format(in_file)], stdout=log, stderr=sp.STDOUT)
    return 0

if __name__ == '__main__':
    #Specify files to be worked with typical shell syntax and glob module
    goodSubjects = pd.read_csv('/biotic/home/timb/data/camcan/analysis/proc_data/demographics_goodSubjects.csv')
    goodSubjects = goodSubjects.loc[goodSubjects['DataReads']==1]
    subjectIDs = goodSubjects['SubjectID'].tolist()[2:]

    #Set up the parallel task pool to use all available processors
    count = np.round(mp.cpu_count()*3/4)
    pool = mp.Pool(processes=count)

    #Run the jobs
    print(subjectIDs)
    pool.map(work, subjectIDs)

