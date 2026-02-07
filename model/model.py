# Copyright [2026] [Mattia Barbero]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import copy
import math
from operator import index

import networkx as nx
from flet_core.icons import PRINT_DISABLED

from database.DAO import DAO
from model.fornitore import Fornitore


class Model:
    def __init__(self):
        self.prodotti = []
        self.fornitori = []
        self.idMap = {}
        self.prodotti, self.idMap = DAO.getProdotti()
        self.storicoV = {}
        self.storicoR = {}
        self.grafo = nx.Graph()
        self.fornitori, self.idMapF = DAO.getFornitori()
        self.negozio = Fornitore(0, "negozio", "negozio@gmail.com", 0.0, 0.0)
        self.prodottiFornitori, self.prodottiFornitore, self.idMapP = DAO.getProdottiFornitori()
        self.getAssociazione()
        self.n = 0
        self.risultati = []
        self.riordina = {}
        self.risultatiAssociaz = []
        self.min = 999999999999
        self.bestF = []
        self.bestA = {}

    def getProdotti(self):
        return self.prodotti, self.idMap

    def getFornitori(self):
        return self.fornitori

    def provaSetGrafo(self, ddf):
        self.grafo.clear()
        self.grafo.add_node(self.negozio)
        for idP, f in ddf.items():
            for fornitore in f.options:
                idF = fornitore.key
                if self.idMapF[idF] not in self.grafo.nodes():
                    self.grafo.add_node(self.idMapF[idF])

        for f1 in self.grafo.nodes():
            for f2 in self.grafo.nodes():
                if f1 != f2:
                    peso = math.sqrt((f2.CoordinataX - f1.CoordinataX) * (f2.CoordinataX - f1.CoordinataX) + (
                            f2.CoordinataY - f1.CoordinataY) * (f2.CoordinataY - f1.CoordinataY))
                    self.grafo.add_edge(f2, f1, weight=peso*2)
                    #costo benzina *2(sto contando in linea d'aria)
    def getGrafo(self):
        return self.grafo

    def aggiornaPr(self, prodotti):
        for id, pz in prodotti.items():
            for prodotto in self.prodotti:
                if prodotto.id_Prodotto == id:
                    prodotto.disponibilita = prodotto.disponibilita - pz

    def riordinati(self, prodotti):
        for id, pz in prodotti.items():
            for prodotto in self.prodotti:
                if prodotto.id_Prodotto == id:
                    prodotto.disponibilita = prodotto.disponibilita + pz.value

    def getStoricoV(self, prV, i):
        self.storicoV[copy.deepcopy(i)] = copy.deepcopy(prV)

    def getAssociazione(self):
        self.associazione = DAO.getAssociazione()

    def getMiglioriFornitori(self, riordina):
        prodotti = []
        self.risultati = []
        self.risultatiAssociaz = []
        self.riordina = riordina
        for p in self.riordina:
            prodotti.append(p)
        negozio = copy.deepcopy(self.negozio)
        self.min=99999999999
        self.ricorsione([negozio], copy.deepcopy(prodotti), {})
        return self.bestF,self.min,self.bestA


    def getCosto(self,parziale,associaz):
        costo=0
        for i in range(len(parziale)):
            if i!=(len(parziale)-1):#forse -1
                costo+=self.grafo.get_edge_data(parziale[i], parziale[i + 1])['weight']
        for idF,idsP in associaz.items():
            for idP in idsP:
                for pf in self.prodottiFornitori:
                    if pf.idF == idF and pf.idP == idP:
                        for pr, val in self.riordina.items():
                            if pr == pf.idP:
                                costo += val.value * pf.costo
        if costo<self.min:
            self.min=costo
            self.bestF=copy.deepcopy(parziale)
            self.bestA=copy.deepcopy(associaz)

    def ricorsione(self, parziale, arrayP, associaz):
        if arrayP == []:
            self.getCosto(parziale,associaz)
        else:
            for fornitore in self.trovaCandidati(parziale, arrayP):
                # Creo una lista dei prodotti che questo fornitore può coprire,per backTrack.
                pCoperti = []
                for idP in self.prodottiFornitore[fornitore.id_Fornitore]:
                    if idP in arrayP:
                        pCoperti.append(idP)
                for idP in pCoperti:
                    arrayP.remove(idP)
                if fornitore.id_Fornitore not in associaz:
                    associaz[fornitore.id_Fornitore] = []
                associaz[fornitore.id_Fornitore].extend(pCoperti)
                # Aggiungo il fornitore al percorso se non c'è già
                fornitore_aggiunto_ora = False
                if fornitore not in parziale:
                    parziale.append(fornitore)
                    fornitore_aggiunto_ora = True
                self.ricorsione(parziale, arrayP, associaz)
                #BACKTRACKING
                if fornitore_aggiunto_ora:
                    parziale.pop()
                for idP in pCoperti:
                    associaz[fornitore.id_Fornitore].remove(idP)
                if not associaz[fornitore.id_Fornitore]:
                    del associaz[fornitore.id_Fornitore]
                arrayP.extend(pCoperti)

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