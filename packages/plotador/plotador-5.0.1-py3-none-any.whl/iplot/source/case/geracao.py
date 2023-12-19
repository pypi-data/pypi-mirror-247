from iplot.source.go.goGrafico import goGrafico

class buscaGeracao():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor, string, tipoGrafico):
        if(mneumonico == "gh"):
            return goGrafico(classe.geracaoHidreletrica(string), classe.estagio, "MW", None, cor, legenda, tipoGrafico)
        elif(mneumonico == "gt"):
            return goGrafico(classe.geracaoTermica(string), classe.estagio, "MW", None, cor, legenda, tipoGrafico)
        elif(mneumonico == "fph"):
            return goGrafico(classe.fphaUtilizada(string), classe.estagio, "MW/m3/s", None, cor, legenda, tipoGrafico)
        else:
            return 0
