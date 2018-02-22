"""
ETAPA 1: Avaliar a qualidade das respostas, independente do gabarito, pautadas 
na ocorrência de:
	i) erros de grafia;
	ii) erros gramáticais; 

"""

respostas = ['Tais comandos devem ser colocados dentro de um bloco try. Porque no caso de ocorrer um exceção no bloco try, ela será lançado, os demais comandos da bloco serão suspensos, e o controle passará para o primeiro bloco catch que tenha um parâmetro de tipo compatível com a exceção lançada.','Tais comandos devem ser colocados dentro de um bloco try. Porque no caso de ocorrer um exceção no bloco try, ela será lançado, os demais comandos da bloco serão suspensos, e o controle passará para o primeiro bloco catch que tenha um parâmetro de tipo compatível com a exceção lançada.','Tais comandos devem ser colocados dentro de um bloco try. Porque no caso de ocorrer um exceção no bloco try, ela será lançado, os demais comandos da bloco serão suspensos, e o controle passará para o primeiro bloco catch que tenha um parâmetro de tipo compatível com a exceção lançada.','Tais comandos devem ser colocados dentro de um bloco try. Porque no caso de ocorrer um exceção no bloco try, ela será lançado, os demais comandos da bloco serão suspensos, e o controle passará para o primeiro bloco catch que tenha um parâmetro de tipo compatível com a exceção lançada.']
#################
# ETAPA 1.i) 
#################
import re
import SpellChecker as sc
# Fazer código para remover pontuação. Por exemplo, o "try," deve ser tratado sem
# a vírgula 

for r in respostas:
	words = r.lower().split()

# Verifica o número de erros entre os termos e a correção
errors = 0
doc_size = len(words)
for w in words:
	if w != sc.correction(w):
		print(w," ~> ",sc.correction(w))
		errors+=1
err_per=(errors/doc_size)*100
print(errors," erro(s)\n(%%): %.2f" %err_per)

#################
# ETAPA 1.ii)
#################

#Deve-se executar o arquivo cogroo4py.jar no console
# java -jar cogroo4py.jar &
# o "&" é para rodar em background

from cogroo_interface import Cogroo

cogroo = Cogroo.Instance()
# Avalia cada sentença de cada resposta, apresentando o(s) erro(s) da determinada 
#sentença
for r in respostas:
	sdoc = cogroo.grammar_check(r)
	for s in sdoc.sentences:
		str_sentences = str(s)
		d = cogroo.grammar_check(str_sentences)
		err = d.mistakes
		print("\n\n",str_sentences," ~ ",err, "\n\n")
	print("\n\nErros: ", len(sdoc.mistakes))
#num_err_doc = len(errors)
#print("Quantidade de erros: ",num_err_doc)
#print("Erros: ",errors)

#####################################################
# ETAPA 1.ii) Verificar Similaridade entre documentos
#####################################################
from similarity import calcula_similaridade
calcula_similaridade(respostas)
