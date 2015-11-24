import fileio
import Evaluate

def CalFreqHelper(lis, index):           #loop through and count base pairs and divide by total with special characters representing multiple bases
    freq={}
    freq['A']=0
    freq['G']=0
    freq['C']=0
    freq['T']=0
    for i in range(len(lis)):
        freq[lis[i][index]]+=1
    freq['A']=freq['A']/len(lis)
    freq['G']=freq['G']/len(lis)
    freq['C']=freq['C']/len(lis)
    freq['T']=freq['T']/len(lis)

    return freq

def CalcFreq(length, seq):
    freqAtPos=[]
    for i in range(length):
        freqAtPos.append(CalFreqHelper(seq, i))
    return freqAtPos

def train(index,pos,neg):
    seq = ""
    if not index < len(pos): return 0
    pos = pos[:index]+pos[index+1:]
    l = CalcFreq(6,pos)
    for d in l:
        j = sorted(list(d.items()), key=lambda x: x[1], reverse=True)
        k = 0
        while sum([x[1] for x in j[0:k]]) < 0.9: k+=1
        seq += "[{}]".format("|".join([x[0] for x in j[0:k]]))
    return seq

print(Evaluate.LOOCV(train, 1))
