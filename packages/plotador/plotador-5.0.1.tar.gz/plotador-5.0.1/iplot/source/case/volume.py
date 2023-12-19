from iplot.source.go.goGrafico import goGrafico

class buscaVolume():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor, string, tipoGrafico):
        if(mneumonico == "vturb"):
            return goGrafico(classe.volumeTurbinado(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vvert"):
            return goGrafico(classe.volumeVertido(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vafl"):
            return goGrafico(classe.volumeAfluente(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vinc"):
            return goGrafico(classe.volumeIncremental(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vdef"):
            return goGrafico(classe.volumeDefluente(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vagua"):
            return goGrafico(classe.valorAgua(string), classe.estagio, "unidade", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vaguai"):
            return goGrafico(classe.valorAguaI(string), classe.estagio, "unidade", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vinc_cen"):
            return goGrafico(classe.volumeIncremental_Serie(string), None, "hm3", None, cor, legenda, tipoGrafico)
        else:
            return 0
    