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
    def __init__(self,condicao,tabelaEsq,tabelaDir,filhos):
        self.condicao = condicao # Condição do Join
        self.tabela1 = tabelaEsq # Tabela da Esquerda
        self.tabela2 = tabelaDir # Tabela da Direita
        self.filhos = filhos     
        self.ordem = 3  
def palavrasChave(string):
    if string.upper() == "SELECT" or string.upper() == "FROM" or string.upper() == "JOIN" or string.upper() == "INNER JOIN" or string.upper() == "ON" or string.upper() == "AND":
        return True
    else:
        return False
def expressao(arrayCondicao):
    comparadores = ["<=", ">=", "<>", "=", ">", "<"]
    for i, item in enumerate(arrayCondicao):
        if item in comparadores:
            if i > 0 and i < len(arrayCondicao) - 1:
                return True
            else:
                return False
    return False
def analisarConsulta(comandoSql):
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
    # Operações
    operacoes = []
    i = 0
    # Variável que testa se a sintaxe está correta
    teste = True
    # Atributos
    colunas = []
    tabela1 = None
    tabela2 = None
    condicoesJuncao = []
    condicoesRestricao = []
    # Primeiro procuro o SELECT no começo
    if vetorConsulta[i]=="SELECT":
        # Depois,procuro o FROM após o SELECT
        i+=1
        if "FROM" in vetorConsulta[i:]:
            while i<len(vetorConsulta) and vetorConsulta[i].upper()!="FROM":
                colunas.append(vetorConsulta[i])
                i+=1
            if len(colunas) == 0 or True in map(palavrasChave,colunas):
                teste=False
        else:
            teste=False
        # Pulando o FROM
        if teste == True:
            i+=1
            # Primeiro elemento após o FROM é a tabela
            if len(vetorConsulta[i:])>0:
                tabela1 = vetorConsulta[i:][0]
                if palavrasChave(tabela1)==True:
                    teste = False
                else:
                    # Pulando a tabela
                    i+=1
                    # Verificando se há JOIN
                    if "JOIN" in vetorConsulta[i:] or "INNER JOIN" in vetorConsulta[i:]:
                        if vetorConsulta[i:][0] == "JOIN" or vetorConsulta[i:][0] == "INNER JOIN":
                            i+=1
                            # Segunda Tabela
                            tabela2 = vetorConsulta[i:][0]
                            if palavrasChave(tabela2) == True:
                                teste = False
                            else:
                                i+=1
                                if "ON" in vetorConsulta[i:]:
                                    if vetorConsulta[i:][0] == "ON":
                                        i+=1
                                        while i<len(vetorConsulta) and vetorConsulta[i].upper()!="WHERE":
                                            condicoesJuncao.append(vetorConsulta[i])
                                            i+=1
                                        if expressao(condicoesJuncao) == True:
                                            if True in map(palavrasChave,condicoesJuncao):
                                                teste = False
                                            else:
                                                if "WHERE" in vetorConsulta[i:]:
                                                    if "WHERE" == vetorConsulta[i:][0]:
                                                        i+=1
                                                        operacao = []
                                                        while i<len(vetorConsulta):
                                                            if vetorConsulta[i]=="AND":
                                                                condicoesRestricao.append(operacao)
                                                                operacao = []
                                                            else:
                                                                operacao.append(vetorConsulta[i])
                                                            i+=1
                                                        condicoesRestricao.append(operacao)
                                                        for cond in condicoesRestricao:
                                                            if True in map(palavrasChave,cond) or expressao(cond) == False:
                                                                teste = False
                                                                break
                                                    else:
                                                        teste = False
                                                else:
                                                    if len(vetorConsulta[i:])>0:
                                                        teste = False
                                        else:
                                            teste = False
                                    else:
                                        teste=False
                                else:
                                    teste = False
                        else:               
                            teste = False
                    else:
                        # Sem Junção
                        if "WHERE" in vetorConsulta[i:]:
                            if "WHERE" == vetorConsulta[i:][0]:
                                i+=1
                                operacao = []
                                while i<len(vetorConsulta):
                                    if vetorConsulta[i]=="AND":
                                        condicoesRestricao.append(operacao)
                                        operacao = []
                                    else:
                                        operacao.append(vetorConsulta[i])
                                    i+=1
                                condicoesRestricao.append(operacao)
                                for cond in condicoesRestricao:
                                    if True in map(palavrasChave,cond) or expressao(cond) == False:
                                        teste = False
                                        break
                            else:
                                teste = False
                        else:
                            if len(vetorConsulta[i:])>0:
                                teste = False
            else:
                teste = False
    else:
        teste = False
    if teste == False:
        print("Erro de Sintaxe!")
    else:
        # Processar
        projecao = Projecao(colunas,None)
        tabelaEsq = Tabela(tabela1)
        operacoes = [projecao,tabelaEsq]
        if tabela2 != None:
            tabelaDir = Tabela(tabela2)
            juncao = Juncao(condicoesJuncao,tabelaEsq,tabelaDir,None)
            operacoes.append(tabelaDir)
            operacoes.append(juncao)
        if len(condicoesRestricao)>0:
            restricao = Restricao(condicoesRestricao,None)
            operacoes.append(restricao)
        operacoesOrdenadas = sorted(operacoes, key=lambda op: op.ordem)
        return operacoesOrdenadas
def processarConsulta(comandoSql):
    operacoes = analisarConsulta(comandoSql)