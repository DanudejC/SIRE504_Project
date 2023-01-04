import re 
from bioseq.sharefn.reverse import reverseSeq, complementSeq,reverseComplementSeq
def cpgSearch(seq):
    '''Search CpG motif in the input sequence'''
    cpgs = []
    for m in re.finditer('CG', seq, re.I):
        cpgs.append((m.group(), m.start(), m.end()))
    return cpgs
def enzTargetsScan(seq, enz):
    resEnzyme = dict(EcoRI='GAATTC', BamHI='GGATCC', 
                 HindIII='AAGCTT',AccB2I='[AG]GCGC[CT]',
                 AasI='GAC[ATCG][ATCG][ATCG][ATCG][ATCG][ATCG]GTC',
                 AceI='GC[AT]GC')
    
    out = []
    if enz in resEnzyme:
        for m in re.finditer(resEnzyme.get(enz,),seq):
            out.append((m.group(0),m.start(),m.end()))
    return out
def enzTargetsScan_re(seq, enz):    
    return enzTargetsScan(reverseComplementSeq(seq),enz)

def transcription(seq):        
    return dna2rna(seq)

def transcription_re(seq):        
    return dna2rna(reverseComplementSeq(seq))

def translation(seq):        
    return dna2protein(seq)

def translation_re(seq):        
    return dna2protein(reverseComplementSeq(seq))



def dna2rna(seq):
    return seq.replace("T","U")

def dna2protein(seq):
    DNA_Codons = loadCodons()
    protein = ""
    for i in range(0,len(seq),3):
        dna = seq[i:i+3]
        protein += DNA_Codons.get(dna, "")
    return protein

def loadCodons():
    DNA_Codons = {
        # 'M' - START, '_' - STOP
        "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "TGT": "C", "TGC": "C",
        "GAT": "D", "GAC": "D",
        "GAA": "E", "GAG": "E",
        "TTT": "F", "TTC": "F",
        "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
        "CAT": "H", "CAC": "H",
        "ATA": "I", "ATT": "I", "ATC": "I",
        "AAA": "K", "AAG": "K",
        "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
        "ATG": "M",
        "AAT": "N", "AAC": "N",
        "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        "CAA": "Q", "CAG": "Q",
        "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
        "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
        "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
        "TGG": "W",
        "TAT": "Y", "TAC": "Y",
        "TAA": "_", "TAG": "_", "TGA": "_"
    }
    return DNA_Codons