from parser import analisarConsulta, processarConsulta
from drawer import desenharGrafo

# Consulta SQL de exemplo 
sql = "SELECT Descricao FROM cliente INNER JOIN endereco ON Cliente_idCliente = idCliente INNER JOIN tipoendereco ON idTipoEndereco = TipoEndereco_idTipoEndereco"

# Processar a consulta e obter a raiz da árvore de operadores
raiz = processarConsulta(sql)

# Desenhar o grafo
if raiz:
    desenharGrafo(raiz)
else:
    print("Erro ao processar a consulta.")