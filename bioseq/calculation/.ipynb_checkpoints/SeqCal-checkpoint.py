from bioseq.sharefn.reverse import reverseSeq, complementSeq,reverseComplementSeq
def gcContent(seq):
    '''To calculate G+C/(A+T+G+C)''' 
    return (countBase(seq, 'G') + countBase(seq, 'C'))/len(seq)
def gcContent2(seq):
    '''To calculate G+C/(A+T+G+C)''' 
    return seq

def countBase(seq, base):
    '''Count specific base in the input sequence''' 
    return seq.count(base.upper())

def countBasesDict(seq):
    '''Count number of each base'''
    basesM = {}
    for base in seq:
        basesM[base] = basesM.get(base, 0)+1
    return basesM
def countBasesDict_re(seq):
    '''Count number of each base reverse'''
    return countBasesDict(reverseComplementSeq(seq))


