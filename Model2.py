import Evaluate
import regex
import time
from itertools import product, repeat

#returns index of a BP the position PWM                   
def BPtoI(BP):
    if BP=="A": return 0
    if BP=="G": return 1
    if BP=="C": return 2
    if BP=="T": return 3
  
#generates probability of a sequence
def prob(seq):
    p = 1
    for i in range(6):
        p *= sum(M[int(x)][i] for x in str(BPtoI(seq[i])))
    return p/tc

#training function
def train(t):
    global M
    
    tp, fn, fp , tn = 0,0,0,0
    total = pos+neg
    for i in range(lp+len(neg)):
        
        exc = total[:i] + total[i+1:]
        
        #perturb M
        for j in range(6):
            M[BPtoI(total[i][j])][j] -= 1
             
        for ind, j in enumerate(exc):
            p = prob(j)
            if p > t and ind < lp:
                tp += 1
            elif p < t and ind < lp:
                fn += 1
            elif p > t and ind >= lp:
                fp += 1
            else:
                tn += 1
                
        #return perturbation
        if i > 0:
            for j in range(6):
                M[BPtoI(pos[i-1][j])][j] += 1
    
    return tp, tn, fp, fn
