import fileio
import Model1
import Model2
import regex
import Evaluate
from random import randint
import time
from itertools import product, repeat

#global variables
pos = ""
neg = ""
M = []
tc , lp, tc0, tc1 = 0, 0, 0, 0

def DB(dataNum):
    global pos, neg, tc, lp, tc0, tc1, tc2
    if dataNum==1:
        pos=fileio.readFile("positive1.txt")
        neg=fileio.readFile("negative1.txt")
    else:
        pos=fileio.readFile("positive2.txt")
        neg=fileio.readFile("negative2.txt")
    lp = len(pos)
    tc = lp**6
    tc0 = (lp-1)**6
    tc1 = (lp+4)**6
    tc2 = (lp+3)**6
    

def Mod1(func,dataNum):
   
    #Create result counts
    TPos, TNeg, FPos, FNeg = 0.0, 0.0, 0.0, 0.0

    #load globals
    DB(dataNum)

    #Run function on everything but Xi to get subsequence and cross check it against the dataset
    for i in range(len(pos)):
        Cseq=func(i, pos, neg)
        if regex.match(Cseq, pos[i]):
          TPos+=1
        else:
          FNeg+=1
                   
    #after positive alterations
    Cseq=func(len(pos), pos, neg)
    for i in range(len(neg)):
        if regex.match(Cseq, neg[i]):
          FPos+=1
        else:
          TNeg+=1
    
    #Calculate sensitivity and specificity
    Sens=TPos/(TPos+FNeg)
    Spec=TNeg/(TNeg+FPos)

    return Sens, Spec

def GenerateM(Seqs):
    global M
    M = [list(repeat(0, 6)) for i in range(4)]
    for k in range(len(Seqs)):
        for j in range(6):
            if Seqs[k][j]=="A":
                M[0][j]+=1
            if Seqs[k][j]=="G":
                M[1][j]+=1
            if Seqs[k][j]=="C":
                M[2][j]+=1
            if Seqs[k][j]=="T":
                M[3][j]+=1
    

#returns index of a BP the position PWM                   
def BPtoI(BP):
    if BP=="A": return 0
    if BP=="G": return 1
    if BP=="C": return 2
    if BP=="T": return 3
  
def Mod2(func,dataNum):

    #Select correct database and make globals
    DB(dataNum)
    
    #set variables used to loop through and optimize
    t=0
    bestT=0
    Sens=None
    Spec=None
    minFalses=9999999

    #Generate PWM
    GenerateM(pos) 
    
    while t < 1:
        tpos, tneg, fpos, fneg = func(t)
        falses = fpos + fneg
        if falses < minFalses:
            minFalses=falses
            bestT=t
            Sens = tpos/(tpos + fneg)
            Spec = tneg/(tneg + fpos)
        t+=0.0001
    return Sens, Spec

#generates probability of a sequence
def prob(seq, mode='pos'):
    p = 1
    for i in range(6):
        p *= M[BPtoI(seq[i])][i]
    if mode == 'pos':
        return p/tc0
    if mode == 'neg':
        return p/tc
    if mode == 'neg2':
        return p/tc1
    if mode == 'pos2':
        return p/tc2


#training function
def train(t):
    global M
    tp, fn, fp, tn = 0,0,0,0

    for i in range(lp):
        #perturb M
        for j in range(6):
            M[BPtoI(pos[i][j])][j] -= 1
             
        p = prob(pos[i])
        if p > t:
            tp += 1
        else: 
            fn += 1

        #return perturbation
        for j in range(6):
            M[BPtoI(pos[i][j])][j] += 1

    for i in range(len(neg)):
        p = prob(neg[i], 'neg')
 
        if p > t: 
            fp += 1
        else: 
            tn += 1
    
    return tp, tn, fp, fn

#training function
def traind(t):
    global M
    
    tp, fn, fp, tn = 0,0,0,0

    for i in range(lp):
        dummy = "".join(["ACTG"[randint(0,3)] for x in range(6)])
        #perturb M
        for j in range(6):
            M[BPtoI(dummy[j])][j] += 1
            M[BPtoI(pos[i][j])][j] -= 1
            
        p = prob(pos[i], 'pos2')
        if p > t:
            tp += 1
        else: 
            fn += 1
                     
        #return perturbation
        for j in range(6):
            M[BPtoI(dummy[j])][j] -= 1
            M[BPtoI(pos[i][j])][j] += 1
            
        
    for i in range(len(neg)):
        dummy = "".join(["ACTG"[randint(0,3)] for x in range(6)])
        #perturb M
        for j in range(6):
            M[BPtoI(dummy[j])][j] += 1
            
        p = prob(neg[i], 'neg2')
        if p > t: 
            fp += 1
        else: 
            tn += 1
       
        for j in range(6):
            M[BPtoI(dummy[j])][j] -= 1
     
    return tp, tn, fp, fn
    
def ROC(func,dataNum):

    #Select correct database and make globals
    DB(dataNum)
    
    #set variables used to loop through and optimize
    t=0
    bestT=0
    Sens=None
    Spec=None
    minFalses=9999999

    #Generate PWM
    GenerateM(pos) 
    
    
    while t < 1:
        results=func(t)
        Sens=results[0]/(results[0]+results[3])
        Spec=results[1]/(results[1]+results[2])
        t+=0.001
        print(Sens, Spec)
    

  
#print(Mod1(Model1.train,1))
#print(Mod1(Model1.train,2))
#print(Mod2(train,1))
#print(Mod2(train,2))

ROC(traind,2)
