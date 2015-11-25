import fileio
import regex
import math
import time
import SciPy
from itertools import product

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

def Bin(s, t, p):
    


def FindMotif(b, nb):
    ml=Permute()
    bound=fileio.readFile(b)
    unbound=fileio.readFile(nb)
    boundDict=CreateSeqDict()
    unboundDict=boundDict.copy()
    unboundDict=UpdateDict(unboundDict, unbound)
    boundDict=UpdateDict(boundDict, bound)
    bestSeq=""
    bestRatio=0
    count=0
    for s in ml:
        count+=1
        conSeq="".join(s)
        possibleSeqs=GiveSeqs(conSeq)
        for seq in possibleSeqs:
            a=boundDict[seq]
            b=unboundDict[seq]
            ratio = a/b
            if ratio == 0:
                    print(str(t))
            if ratio > bestRatio:
                bestRatio=ratio
                bestSeq=conSeq
    return bestSeq    

print(FindMotif("b.fa", "n.fa"))

