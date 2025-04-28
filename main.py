from parser import analisarConsulta, processarConsulta
from drawer import desenharGrafo

# Consulta SQL de exemplo 
sql = "SELECT nome FROM pessoas INNER JOIN enderecos ON pessoas.id=enderecos.pessoa_id WHERE idade = 18 AND pessoa_id = 2"

# Processar a consulta e obter a raiz da árvore de operadores
raiz = processarConsulta(sql)

# Desenhar o grafo
if raiz:
    desenharGrafo(raiz)
else:
    print("Erro ao processar a consulta.")