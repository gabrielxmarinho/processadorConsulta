import networkx as nx
import matplotlib.pyplot as plt
from parser import Tabela, Projecao, Restricao, Juncao

def desenharGrafo(raiz):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()
    pos = {}
    labels = {}
    visited = set()

    def adicionarNo(grafo, no, pos, labels, nivel=0, x=0):
        if id(no) in visited:
            return x
        visited.add(id(no))

        # Nome legível para exibir
        if isinstance(no, Projecao):
            texto = f"π({','.join(no.condicao)})"
        elif isinstance(no, Restricao):
            # Formatar condições de restrição
            condicoes = []
            for cond in no.condicao:
                condicoes.append(' '.join(cond))
            texto = f"σ({' AND '.join(condicoes)})"
        elif isinstance(no, Juncao):
            # Formatar condição de junção
            if isinstance(no.tabela1,Tabela):
                texto = f"{no.tabela1.condicao} |X| {no.tabela2.condicao} ON {' '.join(no.condicao)}"
            else:
                # Não mostro a primeira tabela(Não tem nome)
                texto = f"|X| {no.tabela2.condicao} ON {' '.join(no.condicao)})"
        elif isinstance(no, Tabela):
            texto = f"TABELA({no.condicao})"
        else:
            texto = str(no)

        # ID interno exclusivo
        node_id = id(no)

        grafo.add_node(node_id)
        labels[node_id] = texto
        pos[node_id] = (x, -nivel)

        if hasattr(no, 'filhos'):
            for i, filho in enumerate(no.filhos):
                x = adicionarNo(grafo, filho, pos, labels, nivel + 1, x)
                grafo.add_edge(node_id, id(filho))
                x += 1

        return x

    adicionarNo(G, raiz, pos, labels)

    plt.figure(figsize=(12, 8))
    nx.draw(
        G, pos, labels=labels, with_labels=True,
        node_size=3000, node_color='lightblue',
        font_size=9, font_weight='bold', arrows=True
    )
    plt.title("Grafo de Operadores SQL")
    plt.axis('off')
    plt.show()
