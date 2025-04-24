# SELECT
import re

# Vem depois do FROM
class Tabela:
    def __init__(self,condicao):
        self.condicao = condicao # Nome da Tabela
        self.ordem = 1
# Vem depois do SELECT
class Projecao:
    def __init__(self,condicao, filhos):
        self.condicao = condicao # Nome da(s) coluna(s) separadas por vírgulas
        self.filhos = filhos # Próximo(s) nó(s)
        self.ordem = 4
# Vem depois do WHERE
class Restricao:
    def __init__(self,condicao, filhos):
        self.condicao = condicao # Condição da Filtragem
        self.filhos = filhos # Próximo(s) nó(s)
        self.ordem = 2
# JOIN e ON
class Juncao:
    def __init__(self,condicao,tabelaEsq,tabelaDir):
        self.condicao = condicao # Condição do Join
        self.tabela1 = tabelaEsq # Tabela da Esquerda
        self.tabela2 = tabelaDir # Tabela da Direita     
        self.ordem = 3  
# Função para localizar palavras reservadas
def stringReservada(elemento):
    if elemento.upper() == "FROM" or  elemento.upper() == "INNER JOIN" or elemento.upper() == "JOIN" or elemento.upper() == "WHERE" or elemento.upper() == "SELECT":
        return True
    else:
        return False
def expressao(arrayCondicao):
    comparadores = ["<=",">=","<>","=",">","<"]
    for comparador in comparadores:
        if comparador in arrayCondicao:
            index = arrayCondicao.index(comparador)
            if len(arrayCondicao[:index])>0 and len(arrayCondicao[index+1:])>0:
                return True
            else:
                return False
    return False
def agruparConsulta(comandoSql):
    # Padrões que queremos capturar
    padrao = r"""(?i)              # ignore case
        \bSELECT\b|\bFROM\b|\bWHERE\b|\bINNER?\s*JOIN\b|\bON\b|\bAND\b|   # palavras-chave
        <=|>=|<>|=|<|>|                                    # operadores
        \(|\)|                                            # parênteses
        '[^']*'|                                          # strings entre aspas simples
        \*|                                               # asterisco(Todas as colunas)
        [a-zA-Z_][a-zA-Z0-9_]*|                           # identificadores (nome de colunas ou tabelas)
        \d+                                               # números inteiros
    """
    # Vetor de consulta
    vetorConsulta = re.findall(padrao, comandoSql, re.IGNORECASE | re.VERBOSE)
    print(vetorConsulta)
    # Operações
    operacoes = []
    i = 0
    while i < len(vetorConsulta):
        # Pesquiso uma operação
        # Armazenando a operação
        op = vetorConsulta[i]
        i+=1
        # Pesquiso a condição no próximo elemento
        condicao = []
        # Percorre até o fim buscando as operações
        while i<len(vetorConsulta) and stringReservada(vetorConsulta[i]) == False:
            condicao.append(vetorConsulta[i])
            i+=1
        if op.upper() == "SELECT":
            if len(condicao)>0:
                projecao = Projecao(condicao,None)
                operacoes.append(projecao)
            else:
                print("Erro de Sintaxe")
                return
        elif op.upper() == "FROM":
            if len(condicao)==1:
                tabela = Tabela(condicao)
                operacoes.append(tabela)
            else:
                print("Erro de Sintaxe")
                return
        elif op.upper() == "INNER JOIN" or op.upper() == "JOIN":
            # Separando os dados (No caso do Join)
            if "ON" or "On" or "oN" or "on" in condicao:
                index = condicao.index("ON" or "On" or "oN" or "on")
                tabela2 = condicao[:index]
                nova_condicao = condicao[index+1:]
                if(tabela2 != None and nova_condicao!=None and tabela.condicao!=None):
                    juncao = Juncao(nova_condicao,tabela.condicao,tabela2)
                    operacoes.append(juncao)
                else:
                    print("Erro de Sintaxe")
                    return
            else:
                print("Erro de Sintaxe")
                return
        elif op.upper() == "WHERE":
            while i<len(vetorConsulta):
                i+=1
                condicao.append(vetorConsulta[i])
            condicoesParciais = []
            parte = []
            for elemento in condicao:
                if elemento.upper() == "AND":
                    condicoesParciais.append(parte)
                    parte = []
                else:
                    parte.append(elemento)
            condicoesParciais.append(parte)    
            for cond in condicoesParciais:
                restricao = Restricao(cond,None)
                operacoes.append(restricao)
    operacoesOrdenadas = sorted(operacoes, key=lambda op: op.ordem)
    return operacoesOrdenadas
def processarConsulta(comandoSql):
    operacoes = agruparConsulta(comandoSql)