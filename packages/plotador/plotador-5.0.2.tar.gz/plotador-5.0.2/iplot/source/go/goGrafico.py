
import plotly.graph_objects as go
class goGrafico():
    def __init__(self, y, x, yaxis, xaxis, cor, legenda):
       self.y = y 
       self.x = x
       self.yaxis = yaxis
       self.xaxis = xaxis
       self.cor  = cor
       self.legenda = legenda
       self.GO = None

    def setGOObject(self, GO):
       self.GO = GO

    def returnGoObject(self):
       return self.GO

    #def __init__(self, y, x, yaxis, xaxis, cor, legenda, tipoGrafico):
    #   self.y = y 
    #   self.x = x
    #   self.yaxis = yaxis
    #   self.xaxis = xaxis
    #   self.cor  = cor
    #   self.legenda = legenda
#
    #   tipoGrafico = tipoGrafico.strip()
    #   listaPar = self.separaFormulaEmChaveIdentificador([tipoGrafico])
    #   chave, parametros = listaPar[0]
    #   self.tipoGrafico = chave
    #   self.listaParametros = parametros if parametros is None else parametros.split(",")
    #   print(self.tipoGrafico, " ", self.listaParametros)

    #def returnGoObject(self, show = False):
    #    if(self.tipoGrafico == "plot"):
    #        return go.Scatter(x = self.x, y = self.y , name = self.legenda, legendgroup= self.legenda,line=dict(color=self.cor), showlegend=show)
    #    elif(self.tipoGrafico == "box"):
    #        if(self.listaParametros is None):
    #            print("Nao foram escolhidos estagios para plotar o BOXPLOT")
    #            exit(1)
    #        if(self.listaParametros is not None):
    #            ylistaPlot = []
    #            xlistaPlot = []
    #            for estagio in self.listaParametros:
    #                df = self.y.loc[self.y["estagio"] == int(estagio)]
    #                ylistaPlot += df["valor"].tolist()
    #                xlistaPlot += df["estagio"].tolist()
#
#
    #            self.y = ylistaPlot
    #            self.x = xlistaPlot
    #            self.xaxis = "meses"
    #        return go.Box(x = self.x, y = self.y, text=self.y,     boxpoints= False, name = self.legenda, legendgroup = self.legenda, fillcolor = self.cor, marker_color = self.cor, showlegend=show) #, mode='lines+markers+text'
#
    #    
    #    elif(self.tipoGrafico == "boxaglut"):
    #        
    #        if(self.listaParametros is None):
    #            print("Aglutinacao BOXPLOT sem Parametros para aglutinar")
    #            exit(1)
    #        if(self.listaParametros is not None):
    #            ylistaPlot = []
    #            xlistaPlot = []
    #            for aglut in self.listaParametros:
    #                print(aglut)
    #                lista = self.mediaPeriodoSerie(self.y, int(aglut))
    #                ylistaPlot += lista
    #                xlistaPlot += [str(aglut)]*len(lista)
    #            self.y = ylistaPlot
    #            self.x = xlistaPlot
    #            self.xaxis = "meses"
    #            print(self.y)
    #            print(self.x)
    #        return go.Box(x = self.x, y = self.y, text=self.y,     boxpoints= False,  name = self.legenda, legendgroup = self.legenda, fillcolor = self.cor, marker_color = self.cor, showlegend=show) #, mode='lines+markers+text'
    #    elif(self.tipoGrafico == "max"):
    #        return go.Scatter(x = self.x, y = self.y, name = self.legenda, legendgroup=self.legenda, mode = "markers", marker=dict(color=self.cor, size = 3), showlegend=False)
    #    elif(self.tipoGrafico == "min"):
    #        return go.Scatter(x = self.x, y = self.y, name = self.legenda, legendgroup=self.legenda,line=dict(color=self.cor, width = 1, dash = 'dash'), showlegend=False)
    #    elif(self.tipoGrafico == "bar"):
    #        return go.Bar(x = self.x, y = self.y, showlegend=False)

    #def mediaPeriodoSerie(self, df, aglut):
    #    lista = []
    #    
    #    print(df)
    #    numeroCenarios = max([eval(i) for i in df["cenario"].tolist()]) if isinstance(df["cenario"].tolist()[0], str) else max(df["cenario"].tolist())
    #    print(numeroCenarios)
    #    for serie in range(1,(numeroCenarios+1)):
    #        serie = str(serie) if isinstance(df["cenario"].tolist()[0], str) else serie
    #        lista.append(df.loc[(df["cenario"]==serie) & (df["estagio"] <= aglut)]["valor"].mean())
    #    return lista
#
    #def separaFormulaEmChaveIdentificador(self, listaFormula):
#
    #    listaParesChaveIdentificador  = []
    #    for elemento in listaFormula:
    #        if("[" in elemento):
    #            identificador = elemento[elemento.find("[")+1:elemento.find("]")].strip()
    #        else:
    #            identificador = None
    #        chave = elemento.split("[")[0].strip()
    #        print("chave: ", chave, " id: ", identificador)
    #        listaParesChaveIdentificador.append((chave.lower(),identificador))
    #    return listaParesChaveIdentificador