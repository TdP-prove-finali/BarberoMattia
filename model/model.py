import copy
import math
from operator import index

import networkx as nx
from flet_core.icons import PRINT_DISABLED

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
        self.risultati=[]
        self.riordina={}
        self.risultatiAssociaz=[]
        self.costo_distanza = 2  # qui metti il tuo "costo x"


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
                    distanza = math.sqrt((f2.CoordinataX - f1.CoordinataX) * (f2.CoordinataX - f1.CoordinataX) + (
                                f2.CoordinataY - f1.CoordinataY) * (f2.CoordinataY - f1.CoordinataY))
                    peso = distanza * self.costo_distanza
                    self.grafo.add_edge(f2, f1, weight=peso)


    def getGrafo(self):
        return self.grafo


    def aggiornaPr(self,prodotti):
        for id,pz in prodotti.items():
            for prodotto in self.prodotti:
                if prodotto.id_Prodotto == id:
                    prodotto.disponibilita=prodotto.disponibilita-pz

    def riordinati(self,prodotti):
        for id,pz in prodotti.items():
            for prodotto in self.prodotti:
                if prodotto.id_Prodotto == id:
                    prodotto.disponibilita=prodotto.disponibilita+pz.value



    def getStoricoV(self,prV,i):
        self.storicoV[copy.deepcopy(i)] = copy.deepcopy(prV)

    def getAssociazione(self):
        self.associazione=DAO.getAssociazione()

    def getMiglioriFornitori(self,riordina):
        prodotti = []
        self.risultati=[]
        self.risultatiAssociaz=[]
        self.riordina=riordina
        for p in self.riordina:
            prodotti.append(p)
        negozio=copy.deepcopy(self.negozio)
        self.ricorsione([negozio],prodotti,copy.deepcopy(prodotti),{})


    def getCosto(self):
        min=99999999
        best=[]
        salva=0
        for ris in self.risultati:
            costo=0
            for i in range(len(ris)):
                if i < (len(ris)-1):
                    costo += self.grafo.get_edge_data(ris[i],ris[i+1])['weight']
                    for pf in self.prodottiFornitori:
                        if pf.idF==ris[i+1].id_Fornitore:
                            for pr,val in self.riordina.items():
                                if pr==pf.idP:
                                    costo+=val.value*pf.costo
                if costo < min:
                    salva=self.risultati.index(ris)
                    min=costo
                    best=ris
        return best,min,self.risultatiAssociaz[salva]

    def ricorsione(self, parziale, prodotti, da_coprire, associaz):
        # Caso base: tutti i prodotti sono coperti
        if not da_coprire:  # lista vuota
            self.risultati.append(copy.deepcopy(parziale))
            self.risultatiAssociaz.append(copy.deepcopy(associaz))
            return

        # Scelgo i fornitori candidati
        candidati = self.trovaCandidati(parziale, da_coprire)

        for fornitore in candidati:
            # Prodotti che questo fornitore può fornire tra quelli ancora da coprire
            prodotti_coperti = [
                idP
                for idP in self.prodottiFornitore[fornitore.id_Fornitore]
                if idP in da_coprire
            ]
            if not prodotti_coperti:
                continue  # questo fornitore in realtà non aiuta a coprire i rimanenti

            # --- SCELTA ---
            # salvo stato precedente per poter fare backtracking
            stato_precedente_da_coprire = da_coprire.copy()
            stato_precedente_assoc = associaz.get(fornitore.id_Fornitore, []).copy()
            aveva_gia = fornitore.id_Fornitore in associaz

            # aggiorno da_coprire togliendo i prodotti coperti da questo fornitore
            for p in prodotti_coperti:
                da_coprire.remove(p)

            # aggiorno associazioni fornitore -> prodotti
            if not aveva_gia:
                associaz[fornitore.id_Fornitore] = []
            associaz[fornitore.id_Fornitore].extend(prodotti_coperti)

            # aggiungo il fornitore al percorso (se non già presente)
            parziale.append(fornitore)

            # --- RICORSIONE ---
            self.ricorsione(parziale, prodotti, da_coprire, associaz)

            # --- BACKTRACKING ---
            parziale.pop()
            # ripristina lista prodotti da coprire
            da_coprire = stato_precedente_da_coprire
            # ripristina associazioni
            if aveva_gia:
                associaz[fornitore.id_Fornitore] = stato_precedente_assoc
            else:
                del associaz[fornitore.id_Fornitore]

    def trovaCandidati(self, parziale, arrayP):
        if len(parziale) == 1:
            return self.grafo.neighbors(parziale[0])
        else:
            ritorna = []
            if len(arrayP) >= 1:
                for vicino in self.grafo.neighbors(parziale[-1]):
                    if vicino not in parziale:
                        for idP in self.prodottiFornitore[vicino.id_Fornitore]:
                            if idP in arrayP:
                                if vicino not in ritorna:
                                    ritorna.append(vicino)
            return ritorna

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

    '''def ricorsione(self,parziale,prodotti,arrayP,arrayF):
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

    def ricorsione(self,parziale,prodotti,arrayP,associaz):
        if arrayP ==[]:
                self.risultati.append(copy.deepcopy(parziale))
                self.risultatiAssociaz.append(copy.deepcopy(associaz))
        else:
            for fornitore in self.trovaCandidati(parziale,arrayP):
                for idP in self.prodottiFornitore[fornitore.id_Fornitore]:
                    if idP in arrayP:
                        arrayP.remove(idP)
                        if fornitore.id_Fornitore not in associaz:
                            associaz[fornitore.id_Fornitore]=[]
                            associaz[fornitore.id_Fornitore].append(idP)
                        else:
                            associaz[fornitore.id_Fornitore].append(idP)
                        if fornitore not in parziale:
                            parziale.append(fornitore)
                self.ricorsione(parziale,prodotti,arrayP,associaz)
                parziale.pop()
                arrayP=copy.deepcopy(prodotti)


    def trovaCandidati(self,parziale,arrayP):
        if len(parziale)==1:
            return self.grafo.neighbors(parziale[0])
        else:
            ritorna=[]
            if len(arrayP)>=1:
                for vicino in self.grafo.neighbors(parziale[-1]):
                    if vicino not in parziale:
                        for idP in self.prodottiFornitore[vicino.id_Fornitore]:
                            if idP in arrayP:
                                if vicino not in ritorna:
                                    ritorna.append(vicino)
            return ritorna'''