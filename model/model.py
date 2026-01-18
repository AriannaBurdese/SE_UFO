import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._nodes = []
        self._edges = []
        self.id_map = {}

        self._lista_states = []
        self._lista_neighbors = []
        self._lista_sighting = []
        self.load_states()


    def get_shapes(self, year):
        return DAO.get_shapes(year)
    def load_sighting(self):
        self._lista_sighting = DAO.get_sighting()
    def load_states(self):
        self._lista_states = DAO.get_states()

    def load_neighbors(self, year, shape):
        self._lista_neighbors = DAO.get_all_weighted_neighbors(year, shape)
        print("DEBUG neighbors:", self._lista_neighbors)


    def build_graph(self, year, shape):
        self.G.clear()

        self._nodes = []
        self._edges = []
        self.id_map = {}
        self.load_neighbors(year, shape)
        #vado a riempirmi e creari i miei nodi
        for state in self._lista_states:
            self._nodes.append(state)
            self.id_map[state.id] = state
        self.G.add_nodes_from(self._nodes)
        """
        
        for arco in self._lista_neighbors:
            self._edges.append((self.id_map[arco[0]], self.id_map[arco[1]], arco[2]))
        self.G.add_weighted_edges_from(self._edges)"""
        # ho calcolato il peso nel dao
        #creo i miei archi
        self._edges.clear()
        for s1,s2, peso in self._lista_neighbors:
            if s1 in self.id_map and s2 in self.id_map and peso>0:

                vicino1 = self.id_map[s1]
                vicino2 = self.id_map[s2]
                #peso = self._calcola_peso(vicino1, vicino2)
                #if peso > 0:
                self.G.add_edge(vicino1, vicino2, weight=peso)


    def get_sum_weight_per_node(self):
        pesi = []
        for nodo in self.G.nodes():
            sum_w = 0
            for arco in self.G.edges(nodo, data=True):
                sum_w += arco[2]['weight']
            pesi.append((nodo.id, sum_w))
        return pesi



    def get_num_of_nodes(self):
        return self.G.number_of_nodes()
    def get_num_of_edges(self):
        return self.G.number_of_edges()









