import fileio
import Evaluate
from itertools import product, repeat

def DBSelector(num):
    if num==1:
        return ["positive1.txt", "negative1.txt"]
    if num==2:
        return ["positive2.txt", "negative2.txt"]

#generate a lists for or regex with all combos with possible bp
def Permute():          
    bp=["A","G","C","T","l","m","n","o","p","q","r"]
    return product(bp, repeat=6)

#Generate PWM
def GenerateM(Seqs):
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
    return M
                   
def BPtoI(BP):
    if BP=="A": return 0
    if BP=="G": return 1
    if BP=="C": return 2
    if BP=="T": return 3
    if BP=="l": return 0,1
    if BP=="m": return 0,2
    if BP=="n": return 0,3
    if BP=="o": return 1,2
    if BP=="p": return 1,3
    if BP=="q": return 2,3
    if BP=="r": return 0,1,2,3
    
def prob(seq,M):
    p = 1
    for i in range(6):
        p *= sum(x[i] for x in M[BPtoI(seq[i])])
    return p

def haskellMasterRace(M, pos, index, t):
  x = pos[index]
  retseqs = []
  seqs = Permute()
  for i in range(6):
    M[BPtoI(x[i])][i] -= 1
  for cand in seqs: 
    if prob(cand, M) > t/len(pos):
        retseqs.append(cand)
  return retseqs
  
def train(index, pos, neg, M):
  tot = pos+neg
  tot = tot[:index]+tot[index+1:]
  T=0
  bestT=0
  bestE=99999999999
  fPos=0
  fNeg=0
  bestSeq=""
  for i in range(20):
      T=0.00001*i
      seqList=haskellMasterRace(M, pos, index, T)
      for i in range(seqList):
          evalList=Evaluate.NumError(seqList[i], pos, neg)
          E=evalList[0]
          if E < bestE:
            bestE=E
            bestSeq=seqList[i]
            fPos=fList[0]
            fNeg=fList[1]
  return [bestSeq, fPos, fNeg]

print(Evaluate.LOOCV2(train, 1))
