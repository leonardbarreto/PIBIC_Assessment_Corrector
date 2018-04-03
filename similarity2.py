import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

#from __future__ import division
import itertools
import re
from fuzzywuzzy import fuzz, process
import jellyfish
import numpy

#docs=corpus_respostas#['o teste de jellyfish','jellyfish, o teste' ]

#Retorna a matriz com as distâncias entre os documentos
def sim(measure,documents):
    N = len(documents)

    mtx=numpy.empty((N,N,))
    mtx[:]=numpy.nan
    
    comb = list(itertools.combinations([x for x in range(len(documents))],2))
    
    for d in comb:
        i1 = d[0]
        i2 = d[1]
        mtx[d[0]][d[1]]=measure(documents[i1],documents[i2])
    
    return mtx 
    
def levenshtein(d1,d2):
    return jellyfish.levenshtein_distance(d1,d2)

def jaro(d1,d2):
    return jellyfish.jaro_distance(d1,d2)

def damerau(d1,d2):
    return jellyfish.damerau_levenshtein_distance(d1,d2)

def jaro_winkler(d1,d2):
    return jellyfish.jaro_winkler(d1,d2)

def hamming(d1,d2):
    return jellyfish.hamming_distance(d1,d2)

def match_rating_comparison(d1,d2):
    return jellyfish.match_rating_comparison(d1,d2)

def grafico_similaridade(mtx,title):
    #AJUSTAR ESCALA PARA CADA UMA DAS MEDIDAS
    mtx=numpy.tril(mtx.T,1) #tranforma matriz diagonal superior em inferior para a plotagem
    
    sns.set(style="white")

    mask = numpy.zeros_like(mtx, dtype=numpy.bool)
    mask[numpy.triu_indices_from(mask)] = True

    fig,ax = plt.subplots(figsize=(10,10))
    ax.set_title(title)


    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    sns.heatmap(mtx, mask=mask, cmap=cmap, vmax=numpy.nanmax(mtx), center=0,square=True, linewidths=.5, cbar_kws={"shrink": .5})

    plt.show()