from iplot.source.go.goGrafico import goGrafico

class buscaIntercambio():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor, string, tipoGrafico):
        if(mneumonico == "interc"):
            if(len(string.split('-')) == 2):
                sbmDE = string.split('-')[0]
                sbmPARA = string.split('-')[1]
                return goGrafico(classe.intercambio(sbmDE, sbmPARA), classe.estagio, "MW", None, cor, legenda, tipoGrafico)
            elif(len(string.split('-')) == 1):
                return goGrafico(classe.intercambioTotalSubmercado(string), classe.estagio, "MW", None, cor, legenda, tipoGrafico)

        else:
            return 0
    