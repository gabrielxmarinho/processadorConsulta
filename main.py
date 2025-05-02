from parser import analisarConsulta, processarConsulta
from drawer import desenharGrafo

# Consulta SQL de exemplo 
sql = "SELECT nome FROM alunos INNER JOIN enderecos ON pessoas.id=enderecos.aluno_id INNER JOIN matriculas ON matriculas.aluno_id = alunos.id WHERE idade = 18 AND aluno_id = 2"

# Processar a consulta e obter a raiz da árvore de operadores
raiz = processarConsulta(sql)

# Desenhar o grafo
if raiz:
    desenharGrafo(raiz)
else:
    print("Erro ao processar a consulta.")