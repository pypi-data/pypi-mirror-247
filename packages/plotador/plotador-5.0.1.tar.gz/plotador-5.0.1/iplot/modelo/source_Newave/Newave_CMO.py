
from iplot.modelo.source_Newave.Newave_Estruturadores import estruturas
from iplot.modelo.EstruturasGerais import estruturasGerais


class dadosNewave_CMO(estruturas, estruturasGerais):

    def __init__(self, caminhoNewave):
        self.caminhoNewave = caminhoNewave
        estruturas.__init__(self, caminhoNewave)
        estruturasGerais.__init__(self)

    def cmo(self, identificador):
        if(identificador is None):
            return 0
        if(identificador in self.listaSubmercados):
            return self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "CMO_SBM_EST.parquet.gzip")
        else:
            return 0