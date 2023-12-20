
from iplot.modelo.source_Newave.Newave_Estruturadores import estruturas
from iplot.modelo.EstruturasGerais import estruturasGerais
import pandas as pd

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
        

    def custos(self, identificador):
        df = pd.read_parquet(self.caminhoNewave+"/CUSTOS.parquet.gzip", engine='pyarrow')
        value = df.loc[(df["parcela"] == identificador)]["mean"]
        if(value.empty):
            print("ENTRADA ERRADA, POR FAVOR TENTE UMA DAS SEGUINTES")
            print(df["parcela"])
            exit(1)

        else:
             df = pd.DataFrame({"valor": value.tolist()})
        return df["valor"]