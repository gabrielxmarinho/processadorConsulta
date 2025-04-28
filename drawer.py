import networkx as nx
import matplotlib.pyplot as plt
from parser import Tabela, Projecao, Restricao, Juncao

def desenharGrafo(raiz):
    if raiz is None:
        print("Nenhuma operação para desenhar.")
        return
        
    G = nx.DiGraph()
    
    # Dicionário para armazenar os nós já criados (evitando duplicatas)
    nodes_created = {}
    
    # Dicionário para armazenar o tipo de nó 
    node_types = {}
    
    # Função recursiva para adicionar nós ao grafo
    def adicionar_no(no, parent_id=None):
        if no is None:
            return None
            
        # Criar ID baseado na classe e conteúdo do nó para garantir unicidade
        if isinstance(no, Tabela):
            node_id = f"TABELA({no.condicao})"
            node_types[node_id] = "tabela"
        elif isinstance(no, Projecao):
            node_id = f"PROJEÇÃO({', '.join(no.condicao)})"
            node_types[node_id] = "projecao"
        elif isinstance(no, Restricao):
            # Formatar condições de restrição
            condicoes = []
            for cond in no.condicao:
                condicoes.append(' '.join(cond))
            node_id = f"RESTRIÇÃO({' AND '.join(condicoes)})"
            node_types[node_id] = "restricao"
        elif isinstance(no, Juncao):
            # Formatar condição de junção
            node_id = f"JUNÇÃO({no.tabela1.condicao} ⨝ {no.tabela2.condicao} ON {' '.join(no.condicao)})"
            node_types[node_id] = "juncao"
        else:
            node_id = str(no)
            node_types[node_id] = "outro"
            
        # Adicionar nó ao grafo (se ainda não existir)
        if node_id not in nodes_created:
            G.add_node(node_id)
            nodes_created[node_id] = True
            
        # Adicionar aresta para o pai (se houver)
        if parent_id is not None:
            G.add_edge(node_id, parent_id)  # Fluxo de dados de baixo para cima
            
        # Processar filhos
        if isinstance(no, Juncao):
            # Para junção, adicionar as duas tabelas como filhos
            adicionar_no(no.tabela1, node_id)
            adicionar_no(no.tabela2, node_id)
        
        # Adicionar outros filhos (se houver)
        if hasattr(no, 'filhos'):
            for filho in no.filhos:
                adicionar_no(filho, node_id)
        
        return node_id
    
    # Iniciar a construção do grafo pela raiz
    adicionar_no(raiz)
    
    # Definir posições hierárquicas manualmente para melhor visualização
    pos = {}
    
    # Determinar níveis para cada tipo de nó
    nivel_projecao = 4
    nivel_restricao = 3
    nivel_juncao = 2
    nivel_tabela = 1
    
    # Lista para rastrear nós de cada tipo
    projecoes = []
    restricoes = []
    juncoes = []
    tabelas = []
    
    # Classificar nós por tipo
    for node_id, tipo in node_types.items():
        if tipo == "projecao":
            projecoes.append(node_id)
        elif tipo == "restricao":
            restricoes.append(node_id)
        elif tipo == "juncao":
            juncoes.append(node_id)
        elif tipo == "tabela":
            tabelas.append(node_id)
    
    # Posicionar nós por nível
    for i, node_id in enumerate(projecoes):
        pos[node_id] = (0, nivel_projecao)
        
    for i, node_id in enumerate(restricoes):
        pos[node_id] = (0, nivel_restricao)
        
    for i, node_id in enumerate(juncoes):
        pos[node_id] = (0, nivel_juncao)
    
    # Posicionar tabelas lado a lado
    offset_x = 0
    if len(tabelas) == 2:
        pos[tabelas[0]] = (-1, nivel_tabela)  # Primeira tabela à esquerda
        pos[tabelas[1]] = (1, nivel_tabela)   # Segunda tabela à direita
    else:
        for i, node_id in enumerate(tabelas):
            pos[node_id] = (i - len(tabelas) / 2, nivel_tabela)
    
    # Tamanhos de nós e fontes
    node_sizes = []
    font_sizes = []
    for node in G.nodes():
        if node_types[node] == "juncao":
            node_sizes.append(6000)  # Junção precisa de mais espaço para o texto
            font_sizes.append(8)
        elif node_types[node] == "restricao":
            node_sizes.append(4000)
            font_sizes.append(9)
        else:
            node_sizes.append(3000)
            font_sizes.append(9)
    
    # Desenhar o grafo
    plt.figure(figsize=(12, 10))
    
    # Desenhar os nós com os tamanhos apropriados
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="skyblue", alpha=0.8)
    
    # Desenhar as arestas
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, arrowstyle='->', width=1.5)
    
    # Desenhar os rótulos
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")
    
    plt.title("Grafo de Operadores SQL", fontsize=16)
    plt.axis('off')  # Ocultar eixos
    plt.tight_layout()
    plt.show()