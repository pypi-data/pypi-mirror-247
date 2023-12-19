from iplot.source.go.goGrafico import goGrafico
class buscaVazao():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor, string , tipoGrafico):
        if(mneumonico == "qafl"):
            return goGrafico(classe.vazaoAfluente(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qinc"):
            return goGrafico(classe.vazaoIncremental(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qdef"):
            return goGrafico(classe.vazaoDefluente(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qdefmin"):
            return goGrafico(classe.vazaoDefluenteMinima(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qturb"):
            return goGrafico(classe.vazaoTurbinada(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qvert"):
            return goGrafico(classe.vazaoVertida(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qinc_cen"):
            return goGrafico(classe.vazaoIncremental_Serie(string), None, "m3s", None, cor, legenda, tipoGrafico)
        
        else:
            return 0
