# SELECT
import re

# Vem depois do FROM
class Tabela:
    def __init__(self, condicao):
        self.condicao = condicao  # Nome da Tabela
        self.ordem = 1
        self.filhos = []  # Adicionei lista de filhos vazia por padrão

# Vem depois do SELECT
class Projecao:
    def __init__(self, condicao, filhos=None):
        self.condicao = condicao  # Nome da(s) coluna(s) separadas por vírgulas
        self.filhos = filhos if filhos else []  # Próximo(s) nó(s)
        self.ordem = 4

# Vem depois do WHERE
class Restricao:
    def __init__(self, condicao, filhos=None):
        self.condicao = condicao  # Condição da Filtragem
        self.filhos = filhos if filhos else []  # Próximo(s) nó(s)
        self.ordem = 2

# JOIN e ON
class Juncao:
    def __init__(self, condicao, tabelaEsq, tabelaDir):
        self.condicao = condicao  # Condição do Join
        self.tabela1 = tabelaEsq  # Tabela da Esquerda
        self.tabela2 = tabelaDir  # Tabela da Direita
        self.filhos = [tabelaEsq,tabelaDir]
        self.ordem = 3
def palavrasChave(string):
    if string.upper() == "SELECT" or string.upper() == "FROM" or string.upper() == "JOIN" or string.upper() == "INNER JOIN" or string.upper() == "ON" or string.upper() == "AND":
        return True
    else:
        return False
def expressao(arrayCondicao):
    cont = 0
    comparadores = ["<=", ">=", "<>", "=", ">", "<"]
    for i, item in enumerate(arrayCondicao):
        if item in comparadores:
            if i > 0 and i < len(arrayCondicao) - 1:
                cont+=1
            else:
                return False
    if cont == 1:
        return True
    else:
        return False
# Entidades do banco de dados
entidades = {
    "endereco":{"idEndereco":int,"EnderecoPadrao":int,"Logradouro":str,"Numero":str,"Complemento":str,"Bairro":str,"Cidade":str,"UF":str,"CEP":str,"TipoEndereco_idTipoEndereco":int,"Cliente_idCliente":int},
    "cliente":{"idCliente":int,"Nome":str,"Email":str,"Nascimento":str,"Senha":str,"TipoCliente_idTipoCliente":int,"DataRegistro":str},
    "pedido":{"idPedido":int,"Status_idStatus":int,"DataPedido":str,"ValorTotalPedido":float,"Cliente_idCliente":int},
    "produto":{"idProduto":int,"Nome":str,"Descricao":str,"Preco":float,"QuantEstoque":float,"Categoria_idCategoria":int},
    "tipoendereco":{"idTipoEndereco":int,"Descricao":str},
    "tipocliente":{"idTipoCliente":int,"Descricao":str},
    "telefone":{"Numero":str,"Cliente_idCliente":int},
    "status":{"idStatus":int,"Descricao":str},
    "pedido_das_produto":{"idPedidoProduto":int, "Pedido_idPedido":int,"Produto_idProduto":int,"Quantidade":float,"PrecoUnitario":float},
    "categoria":{"idCategoria":int,"Descricao":str}
}

def upper(string):
    return string.upper()
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
    tabelas = []
    condicoesJuncao = []
    condicoesRestricao = []
    # Primeiro procuro o SELECT no começo
    if vetorConsulta[i].upper()=="SELECT":
        # Depois,procuro o FROM após o SELECT
        i+=1
        if "FROM" in map(upper,vetorConsulta[i:]):
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
                tabelas.append(vetorConsulta[i:][0])
                if palavrasChave(tabelas[len(tabelas)-1])==True: 
                    teste = False
                else:
                    # Pulando a tabela
                    i+=1
                    # Verificando se há JOIN
                    if "JOIN" in map(upper,vetorConsulta[i:]) or "INNER JOIN" in map(upper,vetorConsulta[i:]):
                        while i<len(vetorConsulta) and ("JOIN" in map(upper,vetorConsulta[i:]) or "INNER JOIN" in map(upper,vetorConsulta[i:])):
                            if vetorConsulta[i:][0].upper() == "JOIN" or vetorConsulta[i:][0].upper() == "INNER JOIN":
                                i+=1
                                # Segunda Tabela
                                tabelas.append(vetorConsulta[i:][0])
                                if palavrasChave(tabelas[len(tabelas)-1]) == True:
                                    teste = False
                                    break
                                else:
                                    i+=1
                                    if "ON" in map(upper,vetorConsulta[i:]):
                                        if vetorConsulta[i:][0].upper() == "ON":
                                            i+=1
                                            condicao = []
                                            while i<len(vetorConsulta) and vetorConsulta[i].upper()!="WHERE" and vetorConsulta[i].upper()!="JOIN" and vetorConsulta[i].upper()!="INNER JOIN":
                                                condicao.append(vetorConsulta[i])
                                                i+=1
                                            
                                            condicoesJuncao.append(condicao)
                                        else:
                                            teste=False
                                            break
                                    else:
                                        teste = False
                                        break
                            else:
                                teste=False
                                break
                        if teste == True:
                            if False in map(expressao,condicoesJuncao):
                                teste = False
                            else:
                                for condicao in condicoesJuncao:
                                    if True in map(palavrasChave,condicao):
                                        teste = False
                                    else:
                                        if "WHERE" in map(upper,vetorConsulta[i:]):
                                            if "WHERE" == vetorConsulta[i:][0].upper():
                                                i+=1
                                                operacao = []
                                                while i<len(vetorConsulta):
                                                    if vetorConsulta[i].upper()=="AND":
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
                        # Sem Junção
                        if "WHERE" in map(upper,vetorConsulta[i:]):
                            if "WHERE" == vetorConsulta[i:][0].upper():
                                i+=1
                                operacao = []
                                while i<len(vetorConsulta):
                                    if vetorConsulta[i].upper()=="AND":
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
        # Verificação das entidades e colunas
        entidades_usadas = set(map(str.lower, tabelas))
        for tabela in entidades_usadas:
            if tabela not in entidades:
                print(f"Erro: entidade '{tabela}' não existe.")
                return

        # Função auxiliar para verificar se uma coluna pertence a alguma tabela usada
        def coluna_valida(col, entidades_usadas):
            if "." in col:
                tabela_nome, coluna_nome = col.split(".", 1)
                tabela_nome = tabela_nome.lower()
                if tabela_nome in entidades:
                    return coluna_nome in entidades[tabela_nome]
                return False
            else:
                # verificar se aparece em uma e somente uma tabela (sem ambiguidade)
                tabelas_com_coluna = [t for t in entidades_usadas if col in entidades[t]]
                return len(tabelas_com_coluna) == 1

        # Verificar colunas do SELECT
        for col in colunas:
            if col != "*" and not coluna_valida(col, entidades_usadas):
                print(f"Erro: coluna '{col}' não é válida ou é ambígua.")
                return

        # Verificar colunas nas condições de junção
        for cond in condicoesJuncao:
            for token in cond:
                if token not in ["=", "<", ">", "<=", ">=", "<>", "AND", "ON"] and not coluna_valida(token, entidades_usadas):
                    print(f"Erro: coluna '{token}' na cláusula ON não é válida.")
                    return

        # Verificar colunas nas condições de restrição
        for cond in condicoesRestricao:
            for token in cond:
                if token not in ["=", "<", ">", "<=", ">=", "<>", "AND"] and not coluna_valida(token, entidades_usadas):
                    print(f"Erro: coluna '{token}' na cláusula WHERE não é válida.")
                    return

        return processamentoNaoOtimizado(colunas,tabelas,condicoesJuncao,condicoesRestricao)
def processamentoNaoOtimizado(colunas,tabelas,condicoesJuncao,condicoesRestricao):
    # As restrições são feitas uma única vez (Não Otimizado)
    tabelaEsq = Tabela(tabelas[0])
    # Verificando se há mais de uma tabela(E consequentemente Junção)
    if len(tabelas)>1:
        # Junções
        # Contador i para a tabela da direita
        i = 0
        for condicao in reversed(condicoesJuncao):
            tabelaDir = Tabela(tabelas[i+1])
            juncao = Juncao(condicao,tabelaEsq,tabelaDir)
            tabelaEsq = juncao
            i+=1
        if len(condicoesRestricao)>0:
            restricao = Restricao(condicoesRestricao,[juncao])
            raiz = Projecao(colunas,[restricao])
        else:
            raiz = Projecao(colunas,[juncao])
    else:
        # Não há Junção
        if len(condicoesRestricao)>0:
            restricao = Restricao(condicoesRestricao,[tabelaEsq])
            raiz = Projecao(colunas,[restricao])
        else:
            raiz = Projecao(colunas,[tabelaEsq])
    return raiz
def processamentoOtimizado(colunas,tabela1,tabela2,condicoesJuncao,condicoesRestricao):
    # Criar objetos de nós
        tabelaEsq = Tabela(tabela1)
        raiz = None
        
        if tabela2 is not None:
            tabelaDir = Tabela(tabela2)
            juncao = Juncao(condicoesJuncao, tabelaEsq, tabelaDir)
            
            # A junção tem as duas tabelas como entrada
            if len(condicoesRestricao) > 0:
                restricao = Restricao(condicoesRestricao)
                restricao.filhos = [juncao]
                raiz = Projecao(colunas)
                raiz.filhos = [restricao]
            else:
                raiz = Projecao(colunas)
                raiz.filhos = [juncao]
        else:
            if len(condicoesRestricao) > 0:
                restricao = Restricao(condicoesRestricao)
                restricao.filhos = [tabelaEsq]
                raiz = Projecao(colunas)
                raiz.filhos = [restricao]
            else:
                raiz = Projecao(colunas)
                raiz.filhos = [tabelaEsq]
        
        return raiz

def processarConsulta(comandoSql):
    return analisarConsulta(comandoSql)