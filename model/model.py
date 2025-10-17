import copy
import math

import networkx as nx
from database.DAO import DAO
from model.fornitore import Fornitore


class Model:
    def __init__(self):
        self.prodotti=[]
        self.fornitori=[]
        self.idMap={}
        self.prodotti,self.idMap = DAO.getProdotti()
        self.storicoV={}
        self.storicoR={}
        self.grafo=nx.Graph()
        self.fornitori,self.idMapF=DAO.getFornitori()
        self.negozio=Fornitore(0,"negozio","negozio@gmail.com",0.0,0.0)
        self.prodottiFornitori,self.prodottiFornitore,self.idMapP=DAO.getProdottiFornitori()
        self.getAssociazione()
        self.n = 0

    

    def getProdotti(self):
        return self.prodotti,self.idMap

    def getFornitori(self):
        return self.fornitori

    def provaSetGrafo(self,ddf):
        self.grafo.clear()
        self.grafo.add_node(self.negozio)
        for idP,f in ddf.items():
            for fornitore in f.options:
                idF=fornitore.key
                if self.idMapF[idF] not in self.grafo.nodes():
                    self.grafo.add_node(self.idMapF[idF])

        for f1 in self.grafo.nodes():
            for f2 in self.grafo.nodes():
                if f1 != f2:
                    peso = math.sqrt((f2.CoordinataX - f1.CoordinataX) * (f2.CoordinataX - f1.CoordinataX) + (
                                f2.CoordinataY - f1.CoordinataY) * (f2.CoordinataY - f1.CoordinataY))
                    self.grafo.add_edge(f2, f1, weight=peso)


    def getGrafo(self):
        return self.grafo


    def aggiornaPr(self,prodotti):
        for id,pz in prodotti.items():
            for prodotto in self.prodotti:
                if prodotto.id_Prodotto == id:
                    prodotto.disponibilita=prodotto.disponibilita-pz


    def getStoricoV(self,prV,i):
        self.storicoV[copy.deepcopy(i)] = copy.deepcopy(prV)

    def getAssociazione(self):
        self.associazione=DAO.getAssociazione()

    def getMiglioriFornitori(self,prodotti):
        negozio=copy.deepcopy(self.negozio)
        self.ricorsione([negozio],prodotti,[],[])


    '''def ricorsione(self,parziale,prodotti,array):
        if array==prodotti:
            print(parziale)
        else:
            successori=self.trovaSuccessori(parziale,array,prodotti)
            for f in successori:
                for idP in self.prodottiFornitore[f.id_Fornitore]:
                    if idP in prodotti:
                        array.append(idP)
                parziale.append(f)
                self.ricorsione(parziale,prodotti,array)
                array.pop()
                parziale.pop()

    def trovaSuccessori(self,parziale,array,prodotti):
        if len(parziale) == 1:
            fornitori=self.grafo.neighbors(parziale[0])
            return fornitori
        else:
            returna=[]
            if len(array) < len(prodotti):
                for v in self.grafo.neighbors(parziale[-1]):
                    if v not in parziale:
                        for idP in self.prodottiFornitore[v.id_Fornitore]:
                            if idP not in array:
                                returna.append(v)
            return returna'''


    '''def ricorsione(self,parziale,prodotti,array,prec):
        if array==prodotti:
            print(parziale)
        else:
            successori,precedente=self.trovaSuccessori(parziale,array,prodotti,prec)
            for fornitore in successori:
                for idP in self.prodottiFornitore[fornitore.id_Fornitore]:
                    if idP in prodotti and idP not in array:
                        array.append(idP)
                        if fornitore not in parziale:
                            parziale.append(fornitore)
                self.ricorsione(parziale,prodotti,array,precedente)
                
                parziale.pop()
                array.pop()
                

    def trovaSuccessori(self,parziale,array,prodotti,prec):
        if len(parziale) == 1:
            return self.grafo.neighbors(parziale[0]),parziale[0]
        else:
            ritorna=[]
            
            if prec!=parziale[-1] and len(array) < len(prodotti):
                for vicino in self.grafo.neighbors(parziale[-1]):
                    if vicino not in parziale and vicino!=prec :
                        
                        ritorna.append(vicino)
                return ritorna,parziale[-1]
            else:
                
                return [],prec'''

    '''def ricorsione(self, parziale, prodotti, array):
        if array == prodotti:
            print(parziale)
        else:
            successori = self.trovaSuccessori(parziale, array, prodotti)
            for fornitore in successori:
                for idP in self.prodottiFornitore[fornitore.id_Fornitore]:
                    if idP in prodotti and idP not in array:
                        array.append(idP)
                        if fornitore not in parziale:
                            parziale.append(fornitore)
                self.ricorsione(parziale, prodotti, array)

                parziale.pop()
                array.pop()

    def trovaSuccessori(self, parziale, array, prodotti):
        if len(parziale) == 1:
            return self.grafo.neighbors(parziale[0])
        else:
            ritorna = []
            if len(array) < len(prodotti):
                for vicino in self.grafo.neighbors(parziale[-1]):
                    if vicino not in parziale :
                        for idP in self.prodottiFornitore[vicino.id_Fornitore]:
                            if idP in prodotti and idP not in array:
                                ritorna.append(vicino)
                return ritorna
            else:

                return []'''

    def ricorsione(self,parziale,prodotti,arrayP,arrayF):
        if arrayP == prodotti :
            print(parziale)
        else:
            vicini=self.trovaVicini(parziale,arrayF)
            for fornitore in vicini:
                for idP in self.prodottiFornitore[fornitore.id_Fornitore]:
                    if idP in prodotti and idP not in arrayP:
                        arrayP.append(idP)
                        arrayF.append(self.idMapP[idP])
                        if fornitore not in parziale:
                            parziale.append(fornitore)

                self.ricorsione(parziale,prodotti,arrayP,arrayF)
                parziale.pop()
                arrayF.pop()
                arrayP.pop()

    def trovaVicini(self,parziale,arrayF):
        if len(parziale)==0:
            return self.grafo.neighbors(parziale[0])
        else:
            ritorna=[]
            for vicino in self.grafo.neighbors(parziale[-1]):
                if vicino not in parziale and vicino.id_Fornitore not in arrayF:
                    ritorna.append(vicino)
            return ritorna