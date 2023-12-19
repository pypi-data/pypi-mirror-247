from iplot.source.go.goGrafico import goGrafico

class buscaArmazenamento():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor, string, tipoGrafico):

        if(mneumonico == "varmfu"):
            est = classe.estagio
            #est.insert(0,0)
            return goGrafico(classe.volumeUtilFinal(string), est, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "varmiu"):

            return goGrafico(classe.volumeUtilInicial(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "varpf"):
            return goGrafico(classe.volumeFinalPercentual(string), classe.estagio, "%", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "varpi"):
            return goGrafico(classe.volumeInicialPercentual(string), classe.estagio, "%", "estagios", cor, legenda, tipoGrafico)
        else:
            return 0
    