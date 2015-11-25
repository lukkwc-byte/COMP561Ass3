import fileio
import Evaluate
import time
from itertools import product, repeat

pos=""
neg=""

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

def probd(seq,M):
    p = 1
    for i in range(6):
        p *= sum((M[int(x)][i]+1)/(len(pos)+4) for x in str(BPtoI(seq[i])))
    return p
  
def prob(seq,M):
    p = 1
    for i in range(6):
        p *= sum(M[int(x)][i]/len(pos) for x in str(BPtoI(seq[i])))
    return p

def haskellMasterRace(M, index, t):
  print(index, len(pos))
  x = pos[index]
  retseqs = []
  seqs = Permute()
  for i in range(6):
    M[BPtoI(x[i])][i] -= 1
  for cand in seqs:
    seq = "".join(cand)
    if prob(seq, M) > t:
        retseqs.append(seq)
  return retseqs

def haskellMasterRaced(M, index, t):
  x = pos[index]
  retseqs = []
  seqs = Permute()
  for i in range(6):
    M[BPtoI(x[i])][i] -= 1
  for cand in seqs:
    seq = "".join(cand)
    if prob(seq, M) > t:
        retseqs.append(seq)
  return retseqs
  
def train(index, pos1, neg1, M):
  global pos
  global neg
  pos = pos1
  neg = neg1
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
      print(T)
      seqList=haskellMasterRace(M, index, T)
      for j in range(len(seqList)):
          evalList=Evaluate.NumError(j)
          E=evalList[0]+evalList[1]
          if E < bestE:
            bestE=E
            bestSeq=j
            fPos=evalList[0]
            fNeg=evalList[1]
  return [bestSeq, fPos, fNeg]

def ROC(index, pos1, neg1, M):
  global pos
  global neg
  pos = pos1
  neg = neg1
  tot = pos+neg
  tot = tot[:index]+tot[index+1:]
  sensL, specL = [],[]
  t0 = time.time()
  for i in range(20):
    t1 = t0
    print(t1-t0)
    t0 = time.time()
    T=0.00001*i
    seqList=haskellMasterRace(M, index, T)
    slist = [Evaluate.SS(x) for x in seqList]
    print(slist)
    top = sorted(slist, key = lambda x: x[0]*x[1])[0]
    sensL.append(top[0])
    specL.append(top[1])
  print("sensL: {}".format(sensL))
  print("specL: {}".format(specL))
  return [sensL, specL]

Evaluate.LOOCV2(ROC, 1)
