import regex

#determines if consensus sequence can bind to seq
def Bind(Cseq, seq):
    if regex.match(Cseq, seq) != None:
        return 1
    else:
        return 0

#calculates number of false pos/negs    
def NumFalse(index, substr, pos, neg):
    
    #Create result counts
    false=0.0

    #Calculate false positives and false negatives
    for j in range(len(pos)):
        if j != index and Bind(substr, pos[j])==0:
            false+=1
    for j in range(len(neg)):
        if j != index and Bind(substr, neg[j])==1:
            false+=1
    return false
