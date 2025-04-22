# SELECT
import re

# Consulta SQL de exemplo
sql = "SELECT nome FROM pessoas JOIN enderecos ON pessoas.id=enderecos.pessoa_id WHERE idade > 18"

# Padrões que queremos capturar
padrao = r"""(?i)              # ignore case
    \bSELECT\b|\bFROM\b|\bWHERE\b|\bINNER?\s*JOIN\b|\bON\b|\bAND\b|   # palavras-chave
    <=|>=|<>|=|<|>|                                    # operadores
    \(|\)|                                            # parênteses
    '[^']*'|                                          # strings entre aspas simples
    [a-zA-Z_][a-zA-Z0-9_]*|                           # identificadores (nome de colunas ou tabelas)
    \d+                                               # números inteiros
"""
# Vetor de consulta
consulta = re.findall(padrao, sql, re.IGNORECASE | re.VERBOSE)
# Operações
operacoes = []
# Vem depois do FROM
class Tabela:
    def __init__(self,condicao):
        self.condicao = condicao # Nome da Tabela
        self.prioridade = 4
# Vem depois do SELECT
class Projecao:
    def __init__(self,condicao, filhos):
        self.condicao = condicao # Nome da(s) coluna(s) separadas por vírgulas
        self.filhos = filhos # Próximo(s) nó(s)
        self.prioridade = 1
# Vem depois do WHERE
class Restricao:
    def __init__(self,condicao, filhos):
        self.condicao = condicao # Condição da Filtragem
        self.filhos = filhos # Próximo(s) nó(s)
        self.prioridade = 3
# JOIN e ON
class Juncao:
    def __init__(self,condicao,tabelaEsq,tabelaDir):
        self.condicao = condicao # Condição do Join
        self.tabela1 = tabelaEsq # Tabela da Esquerda
        self.tabela2 = tabelaDir # Tabela da Direita     
        self.prioridade = 2  
# Função para localizar operações
def stringReservada(elemento):
    if elemento.upper() == "FROM" or  elemento.upper() == "INNER" or elemento.upper() == "JOIN" or elemento.upper() == "WHERE" or elemento.upper() == "SELECT":
        return True
    else:
        return False
def agruparConsulta(vetorConsulta):
    for i in range(0,len(vetorConsulta)):
        # Pesquiso uma operação
        if stringReservada(vetorConsulta[i]):
            # Armazenando a operação
            op = vetorConsulta[i].upper()
            # Pesquiso a condição no próximo elemento
            i+=1
            condicao = []
            # Percorre até o fim buscando as operações
            while i<len(vetorConsulta) and stringReservada(vetorConsulta[i]) == False:
                condicao.append(vetorConsulta[i])
                i+=1 
            if len(condicao) == 0:
                print("Erro de Sintaxe")
                return
            if op.upper() == "SELECT":
                projecao = Projecao(condicao,None)
                operacoes.append(projecao)
            elif op.upper() == "FROM":
                tabela = Tabela(condicao)
                operacoes.append(tabela)
            elif op.upper() == "JOIN":
                # Separando os dados (No caso do Join)
                if "ON" or "On" or "oN" or "on" in condicao:
                    index = condicao.index("ON" or "On" or "oN" or "on")
                    tabela2 = condicao[:index]
                    nova_condicao = condicao[index+1:]
                    if(tabela2 != None and nova_condicao!=None and tabela!=None):
                        juncao = Juncao(nova_condicao,tabela,tabela2)
                        operacoes.append(juncao)
                    else:
                        print("Erro de Sintaxe")
                        return
                else:
                    print("Erro de Sintaxe")
                    return
            elif op.upper() == "WHERE":
                restricao = Restricao(condicao,None)
                operacoes.append(restricao)
    operacoesOrdenadas = sorted(operacoes, key=lambda op: op.prioridade)
    print(operacoesOrdenadas)
agruparConsulta(consulta)