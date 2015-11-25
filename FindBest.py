import fileio
import regex
import math
import time
from itertools import product

def CalFreq(fil):           #loop through and count base pairs and divide by total with special characters representing multiple bases
    freq={}
    freq['A']=0
    freq['G']=0
    freq['C']=0
    freq['T']=0
    totalbp=0
    lines=fileio.readFile(fil)
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            freq[lines[i][j]]+=1
            totalbp+=1
    bp=float(totalbp)
    freq['A']=freq['A']/bp
    freq['G']=freq['G']/bp
    freq['C']=freq['C']/bp
    freq['T']=freq['T']/bp
    return freq

def Permute():          #generate 2 lists. One for regex with all combos with bp and another with special characters representing the multi
    bp=["A","G","C","T"]
    ml = product(bp, repeat=6)
    return ml

def CreateSeqDict():          #generate 2 lists. One for regex with all combos with bp and another with special characters representing the multi
    bp=["A","G","C","T"]
    ml = product(bp, repeat=6)
    SeqDict={}
    for s in ml:
        t="".join(s)
        SeqDict[t]=0
    return SeqDict

def UpdateDict(SeqDict, text):
    for i in 
    for i in range(len(text)-5):
        SeqDict[text[i:i+6]]+=1
    return SeqDict

def FindMotif(b, nb, total):
    ml=Permute()
    bound=fileio.readFile(b)
    unbound=fileio.readFile(nb)
    emptyDict=CreateSeqDict()
    unboundDict=UpdateDict(emptyDict, unbound)
    boundDict=UpdateDict(emptyDict, bound)
    bestSeq=""
    bestRatio=0
    for s in ml:
        t="".join(s)
        a=boundDict[s]
        b=unboundDict[s]
        ratio = a/b if b > 0 else 0
        if ratio == 0:
                print(str(t))
        if ratio > bestRatio:
            bestRatio=ratio
            bestSeq=s
    return bestSeq    

print(FindMotif("b.fa", "n.fa", "total.fa"))

