class DadoEixo():
    def __init__(self, chave, ID):
       self.dado = None
       self.eixo = None
       self.chave = chave
       self.ID = ID
       

    

    def interpreta(self, classe):


        #VAZAOself.dado, self.eixo = self.interpreta()

        PAR = 0

        print("self.chave: ", self.chave)
        if(self.chave == "qafl"):
            PAR =  (classe.vazaoAfluente(self.ID), "m3s")
        elif(self.chave == "custos"):
            PAR =  (classe.custos(self.ID), "R$")
        elif(self.chave == "qinc"):
            PAR =  (classe.vazaoIncremental(self.ID), "m3s")
        elif(self.chave == "qdef"):
            PAR =  (classe.vazaoDefluente(self.ID), "m3s")
        elif(self.chave == "qdefmin"):
            PAR =  (classe.vazaoDefluenteMinima(self.ID), "m3s")
        elif(self.chave == "qturb"):
            PAR =  (classe.vazaoTurbinada(self.ID), "m3s")
        elif(self.chave == "qvert"):
            PAR =  (classe.vazaoVertida(self.ID), "m3s")
        elif(self.chave == "qinc_cen"):
            print("ACHOU")
            PAR =  (classe.vazaoIncremental_Serie(self.ID), "m3s")
        #INTERCAMBIO
        elif(self.chave == "interc"):
            if(len(self.ID.split('-')) == 2):
                sbmDE = self.ID.split('-')[0]
                sbmPARA = self.ID.split('-')[1]
                PAR =  (classe.intercambio(sbmDE, sbmPARA), "MW")
            elif(len(self.ID.split('-')) == 1):
                PAR =  (classe.intercambioTotalSubmercado(self.ID), "MW")
        #ENERGIA
        elif(self.chave == "earm"):
            PAR =  (classe.earm(self.ID), "MW")
        elif(self.chave == "ever"):
            PAR =  (classe.enevert(self.ID), "MW")
        elif(self.chave == "eafl"):
            PAR =  (classe.enaflu(self.ID), "MW")
            #ADICIONAR MNEUMONICO DE VVER_SBM, VFIM_SBM, VAFL_SBM, VDEF_SBM
        elif(self.chave == "enaflu_cen"):
            PAR =  (classe.enaflu_Serie(self.ID), "MW")
        #CONVERGENCIA
        elif(self.chave == "zinf"):
            PAR =  (classe.zinf, "R$")
        elif(self.chave == "cpuTime"):
            
            PAR =  (classe.cpuTime, "1000R$")
        #CMO
        elif(self.chave == "cmo"):
            PAR =  (classe.cmo(self.ID), "MWh/R$")
        #ARMAZENAMENTO
        elif(self.chave == "varmfu"):
            est = classe.estagio
            PAR =  (classe.volumeUtilFinal(self.ID), "hm3")
        elif(self.chave == "varmiu"):

            PAR =  (classe.volumeUtilInicial(self.ID), "hm3")
        elif(self.chave == "varpf"):
            PAR =  (classe.volumeFinalPercentual(self.ID), "%")
        elif(self.chave == "varpi"):
            PAR =  (classe.volumeInicialPercentual(self.ID), "%")

        #GERACAO
        elif(self.chave == "gh"):
            PAR =  (classe.geracaoHidreletrica(self.ID), "MW")
        elif(self.chave == "gt"):
            PAR =  (classe.geracaoTermica(self.ID), "MW")
        elif(self.chave == "fph"):
            PAR =  (classe.fphaUtilizada(self.ID), "MW/m3/s")
        elif(self.chave == "est"):
            PAR =  (classe.estagio, "estagios")
        elif(self.chave == "legend"):
            PAR =  (classe.caminho.split("/")[-1], "casos")
        elif(self.chave == "caso"):
            PAR =  (classe.nome, "casos")
        elif(self.chave == "iter"):
            PAR =  (classe.iter, "iteracoes")
        #VOLUME
        elif(self.chave == "vturb"):
            PAR =  (classe.volumeTurbinado(self.ID), "hm3")
        elif(self.chave == "vvert"):
            PAR =  (classe.volumeVertido(self.ID), "hm3")
        elif(self.chave == "vafl"):
            PAR =  (classe.volumeAfluente(self.ID), "hm3")
        elif(self.chave == "vinc"):
            PAR =  (classe.volumeIncremental(self.ID), "hm3")
        elif(self.chave == "vdef"):
            PAR =  (classe.volumeDefluente(self.ID), "hm3")
        elif(self.chave == "vagua"):
            PAR =  (classe.valorAgua(self.ID), "unidade")
        elif(self.chave == "vaguai"):
            PAR =  (classe.valorAguaI(self.ID), "unidade")
        elif(self.chave == "vinc_cen"):
            PAR =  (classe.volumeIncremental_Serie(self.ID), "hm3")
        else:
            PAR =  0
        print("PAR: ", PAR)
        if(PAR != 0):
            self.dado, self.eixo = PAR
        else:
            print("ERRO, CHAVE NAO ENCONTRADA")
            exit(1)