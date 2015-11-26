import Evaluate
import time
from itertools import product, repeat

#Global Variables
pos=""
neg=""

#generate a lists for or regex with all combos with special bp for combination bp
def Permute():          
    bp=["A","G","C","T","l","m","n","o","p","q","r"]
    return product(bp, repeat=6)

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

#returns list of BP for each index
def ItoBP(i):
  if i==0: return 'A','l','m','n','r'
  if i==1: return 'G','l','o','p','r'
  if i==2: return 'C','m','o','q','r'
  if i==3: return 'T','n','p','q','r'
  
#generates probability of a sequence given M
def prob(seq,M):
    p = 1
    for i in range(6):
        p *= sum(M[int(x)][i] for x in str(BPtoI(seq[i])))
    return p/tc

#returns the base pair equivalent of special characters
def SpecCharToBPChar(char):
  if char==l: return "[A|C]"
  if char==m: return "[A|G]"
  if char==n: return "[A|T]"
  if char==o: return "[C|G]"
  if char==p: return "[C|T]"
  if char==q: return "[G|T]"
  if char==r: return "[A|G|C|T]"

#takes consensus sequences and makes them regex'able
def Transmute(Cseq):
  newCSeq=""
  for i in range(len(Cseq)):
    if Cseq[i]=="l" or Cseq[i]=="m" or Cseq[i]=="n" or Cseq[i]=="o" or Cseq[i]=="p" or Cseq[i]=="q" or Cseq[i]=="r":
          newCSeq+=SpecCharToBP(Cseq[i])
    else: newCSeq+=Cseq[i]
    return newCSeq

#training function
def train(D, Ppos, Pneg, index):
  
  #load dataset
  global pos, neg, tc, lp
  pos = Ppos
  neg = Pneg
  tc= len(pos)**6
  lp = len(pos)
  
  #local variables
  bestE=99999999999
  
  #loops through t's and generates a 
  for i in range(100):
      T=0.000002*i
      for Cseq, prob in D:
          newCseq=Transmute(Cseq)
          if prob < T: break
          E=Evaluate.NumFalse(index, newCseq, pos, neg)
          if E < bestE:
              bestE=E
              bestSeq=Cseq
  return bestSeq 

"""
def getSeqs(M, index, t):
  x = pos[index]
  retseqs = []
  seqs = Permute()
  for i in range(6):
    M[BPtoI(x[i])][i] -= 1
  for cand in seqs:
    seq = "".join(cand)
    if valid(seq) and prob(seq, M) > t:
      retseqs.append(seq)
  return retseqs

def ROC(index, pos1, neg1, M):
  global pos
  global neg
  pos = pos1
  neg = neg1
  tot = pos+neg
  tot = tot[:index]+tot[index+1:]
  sensL, specL = [],[]
  t0 = time.time()
  seqList = pls(M, index)
  for i in range(20):
    t1 = t0
    print(t1-t0)
    t0 = time.time()
    T=0.00001*i
    slist = [Evaluate.SS("".join(x)) for x in seqList]
    top = sorted(slist, key = lambda x: x[0]*x[1])[0]
    sensL.append(top[0])
    specL.append(top[1])
  print("sensL: {}".format(sensL))
  print("specL: {}".format(specL))
  return [sensL, specL]

def pls(M, index):
  print(index, len(pos))
  x = pos[index]
  retseqs = []
  seqs = Permute()
  for i in range(6):
    M[BPtoI(x[i])][i] -= 1
  return seqs
""" 
