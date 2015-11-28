#returns the possible nucleotides in a list given the special character
def DoubleBP(char):
    if char=="l": return ["A","C"]
    if char=="m": return ["A","G"]
    if char=="n": return ["A","T"]
    if char=="o": return ["C","G"]
    if char=="p": return ["C","T"]
    if char=="q": return ["G","T"]
    if char=="r": return ["A","C","G","T"]
    
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

def GiveSeqsHelper(char,ret):
    copy=list(ret)
    alt=DoubleBP(char)
    for i in range(len(ret)):
        ret[i]=ret[i]+alt[0]
    for i in range(len(ret)):
        copy[i]=copy[i]+alt[1]
    return copy+ret

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

print(GiveSeqs("AGlmT"))
