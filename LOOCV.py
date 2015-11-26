import fileio
import Model1
import Model2
import Evaluate
from itertools import product, repeat

#global variables
pos = ""
neg = ""
M = []

def DB(dataNum):
    global pos, neg, tc, lp
    if dataNum==1:
        pos=fileio.readFile("positive1.txt")
        neg=fileio.readFile("negative1.txt")
    else:
        pos=fileio.readFile("positive2.txt")
        neg=fileio.readFile("negative2.txt")

def Mod1(func,dataNum):
   
    #Create result counts
    TPos, TNeg, FPos, FNeg = 0.0, 0.0, 0.0, 0.0

    #load globals
    DB(dataNum)

    #Run function on everything but Xi to get subsequence and cross check it against the dataset
    for i in range(len(pos)):
        Cseq=func(i, pos, neg)
        if Evaluate.Bind(Cseq, pos[i])==1:
          TPos+=1
        else:
          FPos+=1
                   
        #after positive alterations
    Cseq=func(len(pos), pos, neg)
    for i in range(len(neg)):
        if Evaluate.Bind(Cseq, neg[i])==0:
          TNeg[1]+=1
        else:
          FNeg[3]+=2
    
    #Calculate sensitivity and specificity
    Sens=TPos/(TPos+FNeg)
    Spec=TNeg/(TNeg+FPos)

    return [Sens, Spec]

def GenerateM(Seqs):
    global M
    M = [list(repeat(0.0, 6)) for i in range(4)]
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
    if BP=="l": return '01'
    if BP=="m": return '02'
    if BP=="n": return '03'
    if BP=="o": return '12'
    if BP=="p": return '13'
    if BP=="q": return "23"
    if BP=="r": return "0123"                

#generate a lists for or regex with all combos with special bp for combination bp
def Permute():          
    bp=["A","G","C","T","l","m","n","o","p","q","r"]
    return product(bp, repeat=6)    

#generates probability of a sequence
def prob(seq):
    p = 1
    for i in range(6):
        p *= sum(M[int(x)][i] for x in str(BPtoI(seq[i])))
    return p/tc
  
# generates dictionary
def generateD():
  retseqs = []
  seqs = Permute()
  for cand in seqs:
    seq = "".join(cand)
    retseqs.append(seq, prob(seq))
  return sorted(retseqs, reverse=True, key = lambda x: x[1])

def Mod2(func,dataNum):
    
    #Create result counts
    results=[0.0,0.0,0.0,0.0]

    #load globals
    DB(dataNum)
    GenerateM(pos)
    
    #Positive loop
    for i in range(len(pos)):
        
        #perturb M
        for j in range(6): 
          M[BPtoI(pos[i][j])][j] -= 1
            
        #M --> prob
        D = generateD() 
        substr = func(D, pos, neg, i)
        
        #Generates reults
        if Evaluate.Bind(substr, pos[i]):
            TruePos+=1
        else:
          FalseNeg+=1
        
        #return perturbation
        if i > 0:
          for j in range(6):
            M[BPtoI(pos[i-1][j])][j] += 1

    #Generate D and consensus that will be used for all negative sequences
    D = generateD()
    substr = func(D, pos, neg, lp)
    
    #Generates results
    for i in range(len(neg)):
        if Evaluate.Bind(substr, neg[i]):
          FalsePos+=1
        else:
          TrueNeg+=1
    
    if TruePos + FalseNeg != lp: print("TruePos + FalseNeg != lp \t {}+{}!={}".format(TruePos, FalseNeg, lp))
    if FalsePos + TrueNeg != len(neg): print("FalsePos + TrueNeg != len(neg) \t {}+{}!={}".format(FalsePos, TrueNeg, len(neg)))
    Sens=TruePos/(TruePos+FalseNeg)
    Spec=TrueNeg/(TrueNeg+FalsePos)

    return [Sens, Spec]
  
"""
def SS(substr):
#Create result counts
  TruePos = 0
  TrueNeg = 0
  FalseNeg = 0
  FalsePos = 0

  #Run function on everything but Xi to get subsequence and cross check it against the dataset
  for j in range(len(pos)):
    if Check(substr, pos[j])==1:
      TruePos+=1
    else:
      FalseNeg+=1
  for j in range(len(neg)):
    if Check(substr, neg[j])==1:
      FalsePos+=1
    else:
      TrueNeg+=1

  #Calculate sensitivity and specificity
  Sens=TruePos/(TruePos+FalseNeg)
  Spec=TrueNeg/(TrueNeg+FalsePos)

  return [Sens, Spec]
"""
