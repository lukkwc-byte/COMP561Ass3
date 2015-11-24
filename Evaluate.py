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


def LOOCV(func,dataNum):
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
    for i in range(len(total)):
        substr=func(i, pos, neg)
        if substr != 0:
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
    
