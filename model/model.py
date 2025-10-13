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
        self.fornitori=DAO.getFornitori()
        self.negozio=Fornitore(0,"negozio","negozio@gmail.com",0.0,0.0)
        self.prodottiFornitori=DAO.getProdottiFornitori()
        self.setGrafo()



    def getProdotti(self):
        return self.prodotti,self.idMap

    def getFornitori(self):
        return self.fornitori

    def setGrafo(self):
        self.grafo.add_node(self.negozio)
        self.grafo.add_nodes_from(self.getFornitori())
        for f1 in self.fornitori:
            for f2 in self.fornitori:
                if f1!=f2:
                    self.grafo.add_edge(f1,f2)
                    peso=math.sqrt((f2.CoordinataX-f1.CoordinataX)*(f2.CoordinataX-f1.CoordinataX)+(f2.CoordinataY-f1.CoordinataY)*(f2.CoordinataY-f1.CoordinataY))
                    self.grafo.add_edge(f2,f1,weight=peso)

    def getGrafo(self):
        return self.grafo


    def aggiornaPr(self,prodotti):
        for id,pz in prodotti.items():
            for prodotto in self.prodotti:
                if prodotto.id_Prodotto == id:
                    prodotto.disponibilita=prodotto.disponibilita-pz


    def getStoricoV(self,prV,i):
        self.storicoV[copy.deepcopy(i)] = copy.deepcopy(prV)

    def getMiglioriFornitori(self):
        pass

    def ricorsione(self):
        pass



