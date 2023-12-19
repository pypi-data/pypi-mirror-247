
from isddp.sddp import LeituraPersonalizadaSDDP
from iplot.modelo.EstruturasGerais import estruturasGerais

class dadosSDDP_CMO(estruturasGerais):

    def __init__(self, caminhoSDDP):
        self.caminhoSDDP = caminhoSDDP
        estruturasGerais.__init__(self)

    def cmo(self, identificador):
        if(identificador is None):
            return 0
        if(identificador in self.listaSubmercados):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_cmgdem.csv").tabela[identificador]
        else:
            return 0