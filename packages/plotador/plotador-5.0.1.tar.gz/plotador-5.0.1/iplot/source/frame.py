
class frame():
    def __init__(self, formula, linha, coluna, grafico):
       self.formula = formula
       self.linha = linha
       self.coluna = coluna
       self.listaGO = []
       self.titulo = None
       self.grafico = grafico

    def addListaGO(self, GO):
        self.listaGO.append(GO)
    
    def setListaGO(self, listaGO):
        self.listaGO = listaGO

    def getListaGO(self):
        return self.listaGO
        
    def getTitulo(self):
        self.titulo = self.formula
        return self.titulo

    #def 