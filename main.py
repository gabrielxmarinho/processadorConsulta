from parser import analisarConsulta, processarConsulta
from drawer import desenharGrafo

# Consulta SQL de exemplo 
sql = "SELECT Nome,Email FROM cliente INNER JOIN endereco ON Cliente_idCliente = idCliente WHERE Numero = 2371"

# Processar a consulta e obter a raiz da árvore de operadores
raiz = processarConsulta(sql)

# Desenhar o grafo
if raiz:
    desenharGrafo(raiz)
else:
    print("Erro ao processar a consulta.")
