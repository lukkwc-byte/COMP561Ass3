import fileio
import regex
import math
import timeit
from itertools import product
from scipy.stats import binom

#Generate a list of possible sequences with special characters for double bp
def Permute():          
    bp=["A","G","C","T", "l", "m", "n", "o", "p", "q", "r"]
    ml = product(bp, repeat=6)
    return ml

#Create an empty dictionary of all possible 6bp
def CreateSeqDict():           
    bp=["A","G","C","T"]
    ml = product(bp, repeat=6)
    SeqDict={}
    for s in ml:
        t="".join(s)
        SeqDict[t]=0
    return SeqDict

#Sliding window dictionary
def UpdateDict(SeqDict, text): 
    for line in text:
        for i in range(len(line)-5):
            SeqDict[line[i:i+6]]+=1
    return SeqDict

#returns the possible nucleotides in a list given the special character
def DoubleBP(char):
    if char=="l": return ["A","C"]
    if char=="m": return ["A","G"]
    if char=="n": return ["A","T"]
    if char=="o": return ["C","G"]
    if char=="p": return ["C","T"]
    if char=="q": return ["G","T"]
    if char=="r": return ["A","C","G","T"]

#Returns a list of the possible sequences that can bind this consensus sequence
def GiveSeqs(substr):
    baseSeq=""
    ret=[baseSeq]
    for i in range(len(substr)):
        if substr[i]=="l" or substr[i]=="m" or substr[i]=="n" or substr[i]=="o" or substr[i]== "p" or substr[i]== "q":
            ret=GiveSeqsHelper(substr[i],ret)
        elif substr[i]=="r":
            ret=AnyBPHelper(ret)
        else:
            for j in range(len(ret)):
                ret[j]=ret[j]+substr[i]
    return ret

#Take current list of possible sequences and double number of possible sequences by adding possible bp
def GiveSeqsHelper(char,ret):
    copy=list(ret)
    alt=DoubleBP(char)
    for i in range(len(ret)):
        ret[i]=ret[i]+alt[0]
    for i in range(len(ret)):
        copy[i]=copy[i]+alt[1]
    return copy+ret

#In case of any bp double possible seqs by 4
def AnyBPHelper(ret):
    copy1=list(ret)
    copy2=list(ret)
    copy3=list(ret)
    for i in range(len(ret)):
        ret[i]=ret[i]+"A"
    for i in range(len(ret)):
        copy1[i]=copy1[i]+"G"
    for i in range(len(ret)):
        copy2[i]=copy2[i]+"C"
    for i in range(len(ret)):
        copy3[i]=copy3[i]+"T"
    return ret+copy1+copy2+copy3

def prob(i, D):
  p = 1
  for char in i:
    p *= D[char]
  return p

def allelefreqs(bound,unbound):
    freqd = {"A":0,"C":0,"T":0,"G":0,"l":0,"m":0,"n":0,"o":0,"p":0,"q":0,"r":0}
    for i in bound + unbound:
      freqd[i] += 1
    for i in 'lmnopqr':
      freqd[i] = sum(freqd[x] for x in DoubleBP(i))
    
    for i in "ACTGlmnopqr":
      freqd[i] = freqd[i]/len(bound+unbound)
    return freqd

def FindMotif(b, nb):
    ml=Permute()
    bound=fileio.readFile(b)[0]
    unbound=fileio.readFile(nb)[0]
    trials=len(bound)+len(unbound)
    aD=allelefreqs(bound,unbound)
    boundDict=CreateSeqDict()
    boundDict=UpdateDict(boundDict, fileio.readFile(b))
    bestSeq=""
    bestP=1
    count=0
    print(aD)
    for s in ml:
        start=timeit.default_timer()
        conSeq="".join(s)
        possibleSeqs=GiveSeqs(conSeq)
        t=0
        for seq in possibleSeqs:
            t+=boundDict[seq]
        if t == 5743:
            q=prob(conSeq, aD)
            p=binom.logpmf(t, trials, q, loc=trials*q)
            if p < bestP:
                bestSeq=conSeq
                bestP=p
        if count==1000000:
            print("""
────██──────▀▀▀██
──▄▀█▄▄▄─────▄▀█▄▄▄
▄▀──█▄▄──────█─█▄▄
─▄▄▄▀──▀▄───▄▄▄▀──▀▄
─▀───────▀▀─▀───────▀▀""")
            count=0
        count+=1
    return bestSeq

print(FindMotif("b0.fa", "n0.fa"))

