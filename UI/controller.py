import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._list_year = []
        self._list_shape = []

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        self._model.load_sighting()
        sighting_list = self._model._lista_sighting


        #popola lista anni unici
        for n in sighting_list:
            if n.s_datetime.year not in self._list_year:
                self._list_year.append(n.s_datetime.year)

        #popola dropdown anni
        self._view.dd_year.options.clear()
        for year in self._list_year:
            self._view.dd_year.options.append(ft.dropdown.Option(year))
        self._view.update()

    def change_option_year(self,e):
        #handler di dd_year associato all'evento on_change
        self.populate_dd_shape()

    def populate_dd_shape(self):
        #metodo per popolare il dropdown dd_shape con le forme filtrate in base all'anno
        self._list_shape = self._model.get_shapes(self._view.dd_year.value)


        #popola dropdown shapes
        #se avessi dovuto prendere tutte le shapes, a prescindere dall'anno, bastava chiaaìmarli le shape nel model dal dao, e poi richiamarlo qui (self._list_shape = self._model.list:shape)
        self._view.dd_shape.options.clear()
        for shape in self._list_shape:
            self._view.dd_shape.options.append(ft.dropdown.Option(shape))
        self._view.update()


    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """

        selected_year = self._view.dd_year.value
        selected_shape = self._view.dd_shape.value

        #pulire area risultato
        self._view.lista_visualizzazione_1.controls.clear()
        #costruisce grafo con i parametri selezionati
        self._model.build_graph(int(selected_year), selected_shape)
        self._view.lista_visualizzazione_1.controls.append(ft.Text(
            f"Numero di vertici: {self._model.get_num_of_nodes()} Numero di archi: {self._model.get_num_of_edges()}"))
        #mostra somma pesi per nodo
        for nodo in self._model.get_sum_weight_per_node():
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Nodo {nodo[0]}, somma pesi su archi = {nodo[1]}")
            )

        self._view.update()


    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
