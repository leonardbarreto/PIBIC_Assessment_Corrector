"""
    Verificação de similaridade entre documentos por meio de 
    comparações entre termos e strings.
        entrada: lista de documentos
        saída: documentos com as respectivas métricas de similaridade
"""
from __future__ import division
import itertools
import re
from fuzzywuzzy import fuzz, process
import jellyfish
import numpy
# a shingle in this code is a string with K-words

K = 4

def jaccard_set(s1, s2):
    " takes two sets and returns Jaccard coefficient"
    u = s1.union(s2)
    i = s1.intersection(s2)
    return len(i)/len(u)

def make_a_set_of_tokens(doc):
    """makes a set of K-tokens"""

    # replace non-alphanumeric char with a space, and then split
    tokens = re.sub("[^\w]", " ",  doc).split()

    sh = set()
    for i in range(len(tokens)-K):
        t = tokens[i]
        for x in tokens[i+1:i+K]:
            t += ' ' + x 
        sh.add(t)
    return sh

def calcula_similaridade(documents):
    """
    documents = ["The legal system is made up of civil courts, criminal courts and specialty courts such as family law courts and bankruptcy court. Each court has its own jurisdiction, which refers to the cases that the court is allowed to hear. In some instances, a case can only be heard in one type of court. For example, a bankruptcy case must be heard in a bankruptcy court. In other instances, there may be several potential courts with jurisdiction. For example, a federal criminal court and a state criminal court would each have jurisdiction over a crime that is a federal drug offense but that is also an offense on the state level.",
      "The legal system is comprised of criminal and civil courts and specialty courts like bankruptcy and family law courts. Every one of the courts is vested with its own jurisdiction. Jurisdiction means the types of cases each court is permitted to rule on. Sometimes, only one type of court can hear a particular case. For instance, bankruptcy cases an be ruled on only in bankruptcy court. In other situations, it is possible for more than one court to have jurisdiction. For instance, both a state and federal criminal court could have authority over a criminal case that is illegal under federal and state drug laws.",
      "In many jurisdictions the judicial branch has the power to change laws through the process of judicial review. Courts with judicial review power may annul the laws and rules of the state when it finds them incompatible with a higher norm, such as primary legislation, the provisions of the constitution or international law. Judges constitute a critical force for interpretation and implementation of a constitution, thus de facto in common law countries creating the body of constitutional law."]
    """  
    shingles = []
    # handle documents one by one
    # makes a list of sets which are compresized of a list of K words string
    for doc in documents:
        # makes a set of tokens
        # sh = set([' ', ..., ' '])
        sh = make_a_set_of_tokens(doc)

        # shingles : list of sets (sh)
        shingles.append(sh)
        
    # print("shingles=%s") %(shingles)
    
    combinations = list( itertools.combinations([x for x in range(len(shingles))], 2) )
    #print("combinations=",combinations)

    # compare each pair in combinations tuple of shingles
    for c in combinations:
        i1 = c[0]
        i2 = c[1]
        jac = jaccard_set(shingles[i1], shingles[i2])
        #print(c,": jaccard=", jac)

    # Comparação de todo o documento (sem tokenizar) 
    N = len(documents)

    mtx_lv=numpy.empty((N,N,))
    mtx_lv[:]=numpy.nan
    mtx_jd=numpy.empty((N,N,))
    mtx_jd[:]=numpy.nan
    mtx_dlv=numpy.empty((N,N,))
    mtx_dlv[:]=numpy.nan
    mtx_jw=numpy.empty((N,N,))
    mtx_jw[:]=numpy.nan
    mtx_hd=numpy.empty((N,N,))
    mtx_hd[:]=numpy.nan
    mtx_mr=numpy.empty((N,N,))
    mtx_mr[:]=numpy.nan
    mtx_fuz=numpy.empty((N,N,))
    mtx_fuz[:]=numpy.nan
    

    comb = list(itertools.combinations([x for x in range(len(documents))],2))
    #print("comb=", comb)
    for d in comb:
        i1 = d[0]
        i2 = d[1]
        #lv = jellyfish.levenshtein_distance(documents[i1],documents[i2])
        mtx_lv[d[0]][d[1]]=jellyfish.levenshtein_distance(documents[i1],documents[i2])
        mtx_jd[d[0]][d[1]]=jellyfish.jaro_distance(documents[i1],documents[i2]) 
        mtx_dlv[d[0]][d[1]]=jellyfish.damerau_levenshtein_distance(documents[i1],documents[i2])
        mtx_jw[d[0]][d[1]]=jellyfish.jaro_winkler(documents[i1],documents[i2]) 
        mtx_hd[d[0]][d[1]]=jellyfish.hamming_distance(documents[i1],documents[i2]) 
        mtx_mr[d[0]][d[1]]=jellyfish.match_rating_comparison(documents[i1],documents[i2]) 
        mtx_fuz[d[0]][d[1]]= fuzz.ratio(documents[i1],documents[i2])
        """
        print("\n\nlv dist",d,":\t\t",lv )
        jd = jellyfish.jaro_distance(documents[i1],documents[i2])
        print("jaro dist",d,":\t\t",jd )
        dlv = jellyfish.damerau_levenshtein_distance(documents[i1],documents[i2])
        print("damerau dist",d,":\t\t",dlv )
        jw = jellyfish.jaro_winkler(documents[i1],documents[i2]) 
        print("jaro_wink dist",d,":\t\t",jw )
        hd = jellyfish.hamming_distance(documents[i1],documents[i2]) 
        print("hamming dist",d,":\t\t",hd )
        mr = jellyfish.match_rating_comparison(documents[i1],documents[i2]) 
        print("match_rat dist",d,":\t\t",mr )
        fuz = fuzz.ratio(documents[i1],documents[i2])
        print("fuzzy dist",d,":\t\t",fuz)
        """
    print("levenshtein_distance\n",mtx_lv)
    print("\n\njaro distance\n",mtx_jd)
    print("\n\ndemerau levenshtein distance\n",mtx_dlv)
    print("\n\njaro winkler\n",mtx_jw)
    print("\n\nhamming distance\n",mtx_hd)
    print("\n\nmatch_rating\n",mtx_mr)
    print("\n\nfuzz.ratio\n",mtx_fuz)
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt
    
    mtx_lv=numpy.tril(mtx_lv.T,1) #tranforma matriz diagonal superior em inferior para a plotagem

    sns.set(style="white")

    mask = numpy.zeros_like(mtx_lv, dtype=numpy.bool)
    mask[numpy.triu_indices_from(mask)] = True

    fig,ax = plt.subplots(figsize=(10,10))
    ax.set_title("levenshtein_distance")


    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    sns.heatmap(mtx_lv, mask=mask, cmap=cmap, vmax=500, center=0,square=True, linewidths=.5, cbar_kws={"shrink": .5})

    plt.show()         
    
"""   
#Módulo para a impressão dos gráficos
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

mtx_lv=np.tril(mtx_lv.T,1) #tranforma matriz diagonal superior em inferior para a plotagem

sns.set(style="white")

mask = numpy.zeros_like(mtx_lv, dtype=numpy.bool)
mask[numpy.triu_indices_from(mask)] = True

fig,ax = plt.subplots(figsize=(10,10))
ax.set_title("levenshtein_distance")


cmap = sns.diverging_palette(220, 10, as_cmap=True)

sns.heatmap(mtx_lv, mask=mask, cmap=cmap, vmax=500, center=0,square=True, linewidths=.5, cbar_kws={"shrink": .5})

plt.show()         
"""  