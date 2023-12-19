from iplot.source.go.goGrafico import goGrafico
class buscaCMO():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor, string, tipoGrafico):
        if(mneumonico == "cmo"):
            return goGrafico(classe.cmo(string), classe.estagio, "MWh/R$", None, cor, legenda, tipoGrafico)
        else:
            return 0
