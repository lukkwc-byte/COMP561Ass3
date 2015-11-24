import fileio
import time
import Evaluate

def DBSelector(num):
    if num==1:
        return ["positive1.txt", "negative1.txt"]
    if num==2:
        return ["positive2.txt", "negative2.txt"]

#generate a lists for or regex with all combos with possible bp
def Permute():          
    bp=["A","G","C","T","l","m","n","o","p","q","r"]
    nl=[]
    for i in range(len(bp)):
        for j in range(len(bp)):
            for k in range(len(bp)):
                for l in range(len(bp)):
                    for m in range(len(bp)):
                        for n in range(len(bp)):
                            altSeq=bp[i]+bp[j]+bp[k]+bp[l]+bp[m]+bp[n]
                            nl.append(altSeq)
    return nl

#Generate PWM
def GenerateM(fil):
    Seqs=fileio.readFile(fil)
    M=[[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0],[1.0,1.0,1.0,1.0,1.0,1.0]]
    for k in range(len(Seqs)):
        for j in range(len(Seqs[k])):
            if Seqs[k][j]=="A":
                M[0][j]+=1
                M[4][j]+=1
                M[5][j]+=1
                M[6][j]+=1
            if Seqs[k][j]=="G":
                M[1][j]+=1
                M[5][j]+=1
                M[7][j]+=1
                M[9][j]+=1
            if Seqs[k][j]=="C":
                M[2][j]+=1
                M[4][j]+=1
                M[7][j]+=1
                M[8][j]+=1
            if Seqs[k][j]=="T":
                M[3][j]+=1
                M[6][j]+=1
                M[8][j]+=1
                M[9][j]+=1
    numSeqs=len(Seqs)
    seqLen=len(Seqs[0])
    totalBP=numSeqs*numSeqs
    for i in range(len(M)-1):
        for j in range(len(M[i])):
            M[i][j]=M[i][j]/totalBP
    return M

def BPtoI(BP):
    if BP=="A": return 0
    if BP=="G": return 1
    if BP=="C": return 2
    if BP=="T": return 3
    if BP=="l": return 4
    if BP=="m": return 5
    if BP=="n": return 6
    if BP=="o": return 7
    if BP=="p": return 8
    if BP=="q": return 9
    if BP=="r": return 10
    

def GenerateProbOfSeq(seq,M):
    prob=1
    for i in range(len(seq)):
        prob=prob*M[BPtoI(seq[i])][i]
    return prob

def FindBestMotif(num):
    files=DBSelector(num)
    M=GenerateM(files[1])
    seqs=Permute()
    t=0
    bestT=0
    bestE=9999999
    bestSeq=""
    top=[]
    for j in range(10,1,-1):
        t0 = time.time()
        t=j*0.00002
        topE=0
        topSeq=""
        for i in range(len(seqs)):
            prob=GenerateProbOfSeq(seqs[i], M)
            if prob > t:
                e=Evaluate.NumError(seqs[i],num)
                if e < bestE:
                    bestE=e
                    bestT=t
                    bestSeq=seqs[i]
        t1 = time.time()
        print("t = {} took {}s".format(j*0.0002, t1-t0)
    return [bestSeq, bestT, bestE]

def GenerateROC(num):
    files=DBSelector(num)
    M=GenerateM(files[1])
    errorList=[]
    for i in range(50):
        T=0.02*i
        seq=GenerateMotif(M, T)
        errors=Evaluate.LOOCV(seq, num)
        errorList.append(errors)
    return errorList

def train(index, pos, neg):
    tot = pos+neg
    tot = tot[:index]+tot[index+1:]
    

print(FindBestMotif(1))

        
