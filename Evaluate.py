import fileio
import regex

def Check(substr1, substr2):
    if regex.match(substr1, substr2) != None:
        return 1
    else:
        return 0

def DB(dataNum):
    if dataNum==1:
        pos=fileio.readFile("positive1.txt")
        neg=fileio.readFile("negative1.txt")
    else:
        pos=fileio.readFile("positive2.txt")
        neg=fileio.readFile("negative2.txt")
    return [pos, neg]


def LOOCV1(func,dataNum):
    #Create result counts
    TruePos=0.0
    TrueNeg=0.0
    FalseNeg=0.0
    FalsePos=0.0

    #load correct dataset
    data=DB(dataNum)
    pos=data[0]
    neg=data[1]
    total=pos+neg

    #Run function on everything but Xi to get subsequence and cross check it against the dataset
    for i in range(len(pos)):
        substr=func(i, pos, neg)
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

    substr=func(len(pos), pos, neg)
    for i in range(len(neg)):
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

def LOOCV2(func,dataNum):
    #Create result counts
    TruePos=0.0
    TrueNeg=0.0
    FalseNeg=0.0
    FalsePos=0.0

    #load correct dataset
    data=DB(dataNum)
    pos=data[0]
    neg=data[1]
    total=pos+neg

    #Run function on everything but Xi to get subsequence and cross check it against the dataset
    for i in range(len(pos)):
        retList=func(i, pos, neg)
        substr=retList[0]
        fPos=retList[1]
        FalsePos+=fPos
        fNeg=retList[2]
        FalseNeg+=fNeg
        for j in range(len(pos)):
            if Check(substr, pos[j])==1:
                TruePos+=1
        for j in range(len(neg)):
            if Check(substr, neg[j])==0:
                TrueNeg+=1
                
    retList=func(len(pos), pos, neg)
    substr=retList[0]
    fPos=retList[1]
    fNeg=retList[2]
    for i in range(len(neg)):
        FalsePos+=fPos
        FalseNeg+=fNeg
        for j in range(len(pos)):
            if Check(substr, pos[j])==1:
                TruePos+=1
        for j in range(len(neg)):
            if Check(substr, neg[j])==0:
                TrueNeg+=1
    
    #Calculate sensitivity and specificity
    Sens=TruePos/(TruePos+FalseNeg)
    Spec=TrueNeg/(TrueNeg+FalsePos)

    return [Sens, Spec]


def NumError(substr, pos, neg):
    #Create result counts
    FalseNeg=0.0
    FalsePos=0.0

    #load correct dataset
    data=DB(dataNum)
    total=pos+neg

    #Calculate false positives and false negatives
    for j in range(len(pos)):
        if Check(substr, pos[j])==0:
            FalseNeg+=1
    for j in range(len(neg)):
        if Check(substr, neg[j])==1:
            FalsePos+=1

    return [FalsePos, FalseNeg]
    
