# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 12:26:16 2018

@author: agraw066
"""


import Misc_Modules as MISC
import scipy.stats.mstats as statm
import os
import numpy as np
import scipy.io as sio
#import sys
import numpy.linalg as LA
import time
import pdb
#import bronk_kerb as bk
#import SignifTesterMultipole as SIG
#import levg_null_dist_expt3 as NULL3
#import CLIQUE_multipoles_algorithm as CLIQ
import itertools
import COMET_ADVANCED as COMETA 
import BruteForce_Climate as BRUT

def mkdirnotex(filename):
	folder=os.path.dirname(filename)
	if not os.path.exists(folder):
		os.makedirs(folder)


if __name__ == '__main__':
    
    loaddir = os.getcwd()
    State = 'Cartoon' # Cartoon
    State2 = 'Rest'
    scan_id = 7
    data  = sio.loadmat(loaddir+'/AllScanData'+State+'State.mat')    
    if State == 'Rest':
        InputTs = np.transpose(data['AllScansRest'][scan_id-1][0] )
    else:
        InputTs = np.transpose(data['AllScansCartoon'][scan_id-1][0])
        
    AllSigma = [0.6,0.5,0.4]
    AllDelta = [0.2,0.15,0.1]
    sigma = min(AllSigma)
    delta = min(AllDelta)
    t_beg = time.time()
    CorrMat = np.corrcoef(InputTs,rowvar=0)
    CorrMat = np.nan_to_num(CorrMat)
    t1 = time.time()
    [Brut3MPs,Brut3LEVs,Brut3LEVGs] = BRUT.brute_search_parallel2(CorrMat,3,sigma,delta)
    t2 = time.time()
    print("Time Elapsed for BruteSearch of size 3:"+str(t2-t1)+" seconds")
    print("Total 3Poles: "+str(len(Brut3MPs)))
    
    t1 = time.time()
    [Brut4MPs,Brut4LEVs,Brut4LEVGs] = BRUT.brute_search_parallel2(CorrMat,4,sigma,delta)
    t2 = time.time()
    print("Time Elapsed for BruteSearch of size 4:"+str(t2-t1)+" seconds")
    print("Total 4Poles: "+str(len(Brut4MPs)))
    
    t1 = time.time()
    [Brut5MPs,Brut5LEVs,Brut5LEVGs] = BRUT.brute_search_parallel2(CorrMat,5,sigma,delta)
    t2 = time.time()
    print("Time Elapsed for BruteSearch of size 5:"+str(t2-t1)+" seconds")
    print("Total 5Poles: "+str(len(Brut5MPs)))
#    [Brut5MPs,Brut5LEVs,Brut5LEVGs] = [[],[],[]]
    
    t1= time.time()
    MaxEdgWt3 = BRUT.get_maxedgewt_vec(CorrMat,Brut3MPs)
    t2 = time.time()
    print("Time Elapsed for IsNegCliq3:"+str(t2-t1)+" seconds")
    
    t1= time.time()
    MaxEdgWt4 = BRUT.get_maxedgewt_vec(CorrMat,Brut4MPs)
    t2 = time.time()
    print("Time Elapsed for IsNegCliq4:"+str(t2-t1)+" seconds")
    
    t1= time.time()
    MaxEdgWt5 = BRUT.get_maxedgewt_vec(CorrMat,Brut5MPs)
    t2 = time.time()
    print("Time Elapsed for IsNegCliq5:"+str(t2-t1)+" seconds")
    
    
    t1= time.time()
    BrutMPs = Brut3MPs + Brut4MPs + Brut5MPs
    BrutLEVs = Brut3LEVs + Brut4LEVs + Brut5LEVs
    BrutLEVGs = Brut3LEVGs + Brut4LEVGs + Brut5LEVGs
#    [BrutMPs,BrutLEVs,BrutLEVGs,BrutSzList] = MISC.remove_redundant_multipoles_alter_parallel(BrutMPs,BrutLEVs,BrutLEVGs)
#    [BrutMPs,BrutLEVs,BrutLEVGs,BrutSzList]= COMETA.remove_non_maximals(BrutMPs,BrutLEVs,BrutLEVGs,CorrMat,sigma,delta)

    t2= time.time()
    print("Time Elapsed i eliminating non-maximals:"+str(t2-t1)+" seconds")
    t_end = time.time()
    TotalTime = t_end - t_beg
    print("Total Time = {}".format(TotalTime))
#    [FinalBrutMPs,FinalBrutLEVs,FinalBrutLEVGs] = MISC.remove_redundant_multipoles_alter(BrutMPs,BrutLEVs,BrutLEVGs)
    NumBrutMPs = []
    ParamCombos = []
    for s in range(len(AllSigma)):
        sigma = AllSigma[s]
        for d in range(len(AllDelta)):
            delta = AllDelta[d]
            FinalBrutMPs = [BrutMPs[i] for i in range(len(BrutLEVs))  if (1-BrutLEVs[i]>=sigma and BrutLEVGs[i]>=delta)]
            FinalBrutLEVs = [BrutLEVs[i] for i in range(len(BrutLEVs))  if (1-BrutLEVs[i]>=sigma and BrutLEVGs[i]>=delta)]
            FinalBrutLEVGs = [BrutLEVGs[i] for i in range(len(BrutLEVs))  if (1-BrutLEVs[i]>=sigma and BrutLEVGs[i]>=delta)]
            [FinalBrutMPs,FinalBrutLEVs,FinalBrutLEVGs,FinalBrutSzList]= COMETA.remove_non_maximals(FinalBrutMPs,FinalBrutLEVs,FinalBrutLEVGs,CorrMat,sigma,delta)

            NumBrutMPs.append(len(FinalBrutMPs))
            ParamCombos.append([sigma,delta])
            savedir = os.getcwd()+'/MultipolesfMRI/'
            mkdirnotex(savedir)
            file_str1 = State + '_scanid_'+str(scan_id)
            file_str2 = '_sigma_'+str(sigma)+'_delta_'+str(delta) 
            saveData = {'Brut3MPs':Brut3MPs,'Brut3LEVs':Brut3LEVs,'Brut3LEVGs':Brut3LEVGs,
            'Brut4MPs':Brut4MPs,'Brut4LEVs':Brut4LEVs,'Brut4LEVGs':Brut4LEVGs,
            'Brut5MPs':Brut5MPs,'Brut5LEVs':Brut5LEVs,'Brut5LEVGs':Brut5LEVGs,
            'MaxEdgWt3':MaxEdgWt3,'MaxEdgWt4':MaxEdgWt4,'MaxEdgWt5':MaxEdgWt5,
            'FinalBrutMPs':FinalBrutMPs,'FinalBrutLEVs':FinalBrutLEVs,'FinalBrutLEVGs':FinalBrutLEVGs}            
            sio.savemat(savedir+'BRUTE_Multipoles_'+file_str1+file_str2,saveData,appendmat=True)
            