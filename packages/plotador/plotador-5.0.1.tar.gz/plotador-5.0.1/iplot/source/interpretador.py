from iplot.source.case.armazenamento import buscaArmazenamento
from iplot.source.case.cmo import buscaCMO
from iplot.source.case.convergencia import buscaConvergencia
from iplot.source.case.energia import buscaEnergia
from iplot.source.case.geracao import buscaGeracao
from iplot.source.case.intercambio import buscaIntercambio
from iplot.source.case.vazao import buscaVazao
from iplot.source.case.volume import buscaVolume
import re
import pandas as pd
class interpretador():

    def __init__(self):
        self.__mneumonicos = [
                "varmfu", "varmiu" , "varpf", "varpi",
                "vturb", "vvert", "vdef", "vafl", "vinc", "vinc_cen", "vagua", "vaguai"
                "qinc", "qafl", "qdef", "qturb", "qvert", "qinc_cen","qdefmin",
                "gh", "gt", "cmo", 
                "earm", "evert", "enaflu", "enaflu_cen",
                "zinf", "interc", "fph", "cpuTime" ]
         #cpuTime
    def help(self):
        print(self.__mneumonicos)

    
    def retornaListasGO(self, frame, gerenciadorArquivos):
        listaGO = []
        for caso in gerenciadorArquivos.mapaCasos:
            cor = gerenciadorArquivos.mapaCores[caso]
            #print(caso)
            listaGO.append(self.interpreta(gerenciadorArquivos.getClasse(caso), frame.formula, cor, frame.grafico))
            
        return listaGO
    

    def separaFormulaEmChaveIdentificador(self, listaFormula):

        listaParesChaveIdentificador  = []
        for elemento in listaFormula:
            if("[" in elemento):
                identificador = elemento[elemento.find("[")+1:elemento.find("]")].strip()
            else:
                identificador = None
            chave = elemento.split("[")[0].strip()
            print("chave: ", chave, " id: ", identificador)
            listaParesChaveIdentificador.append((chave.lower(),identificador))
        return listaParesChaveIdentificador

    def interpreta(self, classe, formula, cor, tipoGrafico):
        caminho = classe.caminho
        legenda = self.legenda(caminho)
        
        flag = 0
        flag_anterior = 0
        lista_ID =[]
        lista_chave = []
        chave = ""
        identificador = ""
        for i in range(len(formula)):
            flag_anterior = flag
            chave = chave + formula[i]
            if(formula[i] == "]"): 
                flag = 0
                chave = ""

            if(flag == 1):
                identificador = identificador + formula[i]
            if(flag_anterior == 1 and flag == 0):
                lista_ID.append(identificador)
                identificador = ""
            if(formula[i] == "["): 
                flag = 1
                lista_chave.append(chave.replace("[","").replace(" ",""))
            #print("flag ant ", flag_anterior , "flag ", flag, " formula[i] ", formula[i])

        lista_sinal = []
        lista_hash = []
        for i in range(len(lista_chave)):
            if(lista_chave[i][0] == "-"):
                lista_sinal.append("-")
                lista_chave[i] = lista_chave[i].replace("-","")
                
                lista_chave[i] = lista_chave[i].strip() 
            else:
                lista_chave[i] = lista_chave[i].replace("+","")
                lista_sinal.append("+")
            print(chave)
            lista_hash.append(str(hash(lista_sinal[i]+lista_chave[i]+"["+lista_ID[i]+"]")))


        mapaFormulaGO = {}
        for i in range(len(lista_hash)):
            mapaFormulaGO[lista_hash[i]]    = []
            if(lista_ID[i].upper() == "SIN"):
                lista_ID[i] = None

        for j in range(len(lista_hash)):
            mneumonico = lista_chave[j]
            string = lista_ID[j]
            string = None if string is None else string.upper()
            #print("mneumonico: ", mneumonico, " string: ", string)
            #GO_aux = self.retornaObjetoGO(classe, legenda, mneumonico, cor, string, tipoGrafico)
            #print("goAUX: ",GO_aux)
            mapaFormulaGO[lista_hash[j]] = self.retornaObjetoGO(classe, legenda, mneumonico, cor, string, tipoGrafico)


        print("ID: ", lista_ID)
        print("Chave: ", lista_chave)
        print("Sinal: ", lista_sinal)
        print("Hash: ", lista_hash)
        print(mapaFormulaGO)



        #listaFormula =  re.split(r"[-+/*]", formula.replace("(","").replace(")",""))
        #print(listaFormula)
        #formula_analise = formula.replace("(","").replace(")","")
        #listaFormula_analise = []
        #for i in range(len(formula_analise)):
        #    if(formula_analise[i] == "["): 
        #        print(True)
        #    if(formula_analise[i] == "]"): 
        #        print(False)

        #if("" in listaFormula): listaFormula.remove("") 

        #mapaFormulaGO = {}
        #listaParesChaveIdentificador = []
        #for i in range(len(listaFormula)):
        #    listaFormula[i] = listaFormula[i].strip()    
        #    mapaFormulaGO[listaFormula[i]]    = []
        #listaParesChaveIdentificador = self.separaFormulaEmChaveIdentificador(listaFormula)
        #contador = 0

        #for par in listaParesChaveIdentificador:
        #    mneumonico, string = par
        #    string = None if string is None else string.upper()
        #    #print("mneumonico: ", mneumonico, " string: ", string)
        #    GO_aux = self.retornaObjetoGO(classe, legenda, mneumonico, cor, string, tipoGrafico)
        #    #print("goAUX: ",GO_aux)
        #    mapaFormulaGO[listaFormula[contador]] = self.retornaObjetoGO(classe, legenda, mneumonico, cor, string, tipoGrafico)
        #    contador += 1

        print(mapaFormulaGO)
        #print(mapaFormulaGO[listaFormula[0]].y)
        for elemento in mapaFormulaGO:
            if(mapaFormulaGO[elemento] is None):
                print("MNEUMONICO ERRADO, REVISAR MNEUMONICOS OU CHAMAR O PROGRAMDOR")
                exit(1)


        if(len(mapaFormulaGO)> 1): 

            testeMais = formula.split("+")
            if(testeMais[0] != ""):
                testeMenos  = testeMais[0].split("-")
                if(testeMenos[0] != ""):
                    formula = "+"+formula

            todosMais = list(self.find_all_custom(formula, "+"))
            todosMenos =  list(self.find_all_custom(formula, "-"))
            todos = todosMais + todosMenos

            dfY = pd.DataFrame()
            for elemento in mapaFormulaGO:
                posicao =min(todos)    
                print("y: ", mapaFormulaGO[elemento].y)
                print("y_LIST: ", mapaFormulaGO[elemento].y.tolist())
                df_temp = pd.DataFrame({"valor":mapaFormulaGO[elemento].y.tolist()})
                if(posicao in todosMais):
                    dfY = pd.concat([dfY, df_temp["valor"]], axis = 1)
                if(posicao in todosMenos): 
                    dfY = pd.concat([dfY, df_temp["valor"]*-1], axis = 1)
                todos.remove(posicao)
            #print(dfY)
            GO = mapaFormulaGO[list(mapaFormulaGO.keys())[0]]
            GO.y = dfY.sum(axis = 1)
            return GO
        else:
            #print(mapaFormulaGO[list(mapaFormulaGO.keys())[0]])
            
            GO = mapaFormulaGO[list(mapaFormulaGO.keys())[0]]
            if(GO != 0 ): return GO
            

            if(GO == 0):
                print("MNEUMONICO ERRADO, POR FAVOR UTILIZE ALGUNS DOS MNEUMONICOS A SEGUIR:")
                print(self.__mneumonicos)
                exit(1)
                return 0

             



        #print(mapaFormulaGO)
        #  exit(1)


        #positionParenthesisBegin = list(self.find_all_custom(formula, "("))
        #positionParenthesisEnd = list(self.find_all_custom(formula, ")"))
        #if(len(positionParenthesisBegin) != len(positionParenthesisEnd) ):
        #     print("EXISTEM PARENTHESIS ERRADOS")
        #    exit(1)
        

        

            
       # GO = self.retornaObjetoGO(classe, legenda, mneumonico, cor, string)

        




    
    def legenda(self, caso):
        return caso.split("/")[-1]
    

    def retornaObjetoGO(self, classe, legenda, mneumonico, cor, string, tipoGrafico):
        GO = 0
        GO = buscaArmazenamento().interpreta(classe, legenda, mneumonico, cor, string, tipoGrafico)
        if(GO != 0 ): return GO
        GO = buscaCMO().interpreta(classe, legenda, mneumonico, cor, string, tipoGrafico)
        if(GO != 0 ): return GO
        GO = buscaConvergencia().interpreta(classe, legenda, mneumonico, cor, tipoGrafico)
        if(GO != 0 ): return GO
        GO = buscaEnergia().interpreta(classe, legenda, mneumonico, cor, string, tipoGrafico)
        if(GO != 0 ): return GO
        GO = buscaGeracao().interpreta(classe, legenda, mneumonico, cor, string, tipoGrafico)
        if(GO != 0 ): return GO
        GO = buscaIntercambio().interpreta(classe, legenda, mneumonico, cor, string, tipoGrafico)
        if(GO != 0 ): return GO
        GO = buscaVazao().interpreta(classe, legenda, mneumonico, cor, string, tipoGrafico)
        if(GO != 0 ): return GO
        GO = buscaVolume().interpreta(classe, legenda, mneumonico, cor, string, tipoGrafico)
        if(GO != 0 ): return GO
    


    def find_all_custom(self, a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches