import copy
import math

import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view:View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._prodVenduti={}
        self._idMap={}
        self._iPrec=0
        self.ddF={}
        self.venduti={}
        self.riordina={}
        self.periodo=0

#Sezione relativa pagina vendite
    def paginaVendite(self,e):
        self.clear()
        self._view.load_Vendite()
    def loadProdotti(self):
        prodotti,self._idMap=self._model.getProdotti()

        self._view._ddVProd1.options=[]
        for p in prodotti:
            self._view._ddVProd1.options.append(ft.dropdown.Option(key=p.id_Prodotto,text=p.nome))

    def aggiungiV(self,e):
        if self._view._ddVProd1.value !="" and self._view._txtVIn1.value !="":
            self._view._txtVOut1.value=""
            self._view.update_page()
            pezziRichiesti = int(self._view._txtVIn1.value)
            id = int(self._view._ddVProd1.value)
            p=self._idMap[id]
            if p.disponibilita<pezziRichiesti:
                self._view._txtVOut1.value=f"Errore, disponibilità massima: {p.disponibilita}"

            else:
                self._view._txtVResult.controls.append(ft.Text(f"Vendita inserita--> {p.nome}: {pezziRichiesti} pz"))
                if p.id_Prodotto in self._prodVenduti.keys():
                    self._prodVenduti[p.id_Prodotto]+=pezziRichiesti
                else:
                    self._prodVenduti[p.id_Prodotto]=pezziRichiesti

            self._view.update_page()
            #aggiorna db
    def fineMese(self,e):
        #aggiungere nel database vendite

        self._model.aggiornaPr(self._prodVenduti)
        self._model.getStoricoV(self._prodVenduti,self._view.id_mensilita)
        self._view.id_mensilita += 1
        self._view._mese.value = f"Mensilita {self._view.id_mensilita}"
        self._view._txtVResult.controls=[]
        self._prodVenduti={}
        self._view._ddVProd1.value=""
        self._view._txtVIn1.value=""
        self._view._txtVOut1.value=""
        self._view.update_page()


#Sezione relativa pagina riordina
    def paginaRiordina(self,e):
        self.clear()
        self._view.load_Riordina()
        self.periodo=self._view.id_mensilita-self._view._startP

        for t,v in self._model.storicoV.items():
                if t>=self._iPrec:
                    for id,qtn in v.items():
                       if id not in self.venduti.keys():
                           self.venduti[id]=qtn
                       else:
                            self.venduti[id]+=qtn
        width = self._view._page.width
        for pr,pz in self.venduti.items():
            nome=self._idMap[pr].nome

            self.riordina[pr]=ft.TextField(label="pezzi",width=width*0.1,input_filter=ft.NumbersOnlyInputFilter(),
                                            keyboard_type=ft.KeyboardType.NUMBER)

            self._view._page.controls.append(ft.Container(ft.Row([ft.Text(f"{nome}", size=16,width=width*0.22), self.riordina[pr]],
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=20,alignment="center"),padding=ft.padding.all(4),
                                            margin=ft.margin.all(4),border_radius=5,bgcolor=ft.colors.WHITE,width=width*0.36))

        self._view.update_page()

        self._iPrec = copy.deepcopy(self._view.id_mensilita)

    def selezFornitori(self,e):
        self.clear()
        self._view.load_Fornitore()
        width = self._view._page.width
        associazione=self._model.associazione
        for pr,pz in self.venduti.items():
            nome=self._idMap[pr].nome
            pezziRiordinati=self.riordina[pr].value
            if pezziRiordinati=="":
                self.riordina.pop(pr)
            else:
                self.ddF[pr]=ft.Dropdown(width=width*0.22)
                self.ddF[pr].options=[]
                for idP,idF_nome in associazione.items():
                    if idP==pr:
                        for idF,nomeF in idF_nome:
                            self.ddF[pr].options.append(ft.dropdown.Option(key=idF,text=nomeF))
                self._view._page.controls.append(ft.Container(ft.Row([ft.Text(f"{nome}", size=16,width=width*0.22),ft.Text(f"{pezziRiordinati}", size=16,width=width*0.1),self.ddF[pr] ],
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=20,alignment="center"),padding=ft.padding.all(4),
                                            margin=ft.margin.all(4),border_radius=5,bgcolor=ft.colors.WHITE,width=width*0.6))
        self._view.load_btn()
        self._model.provaSetGrafo(self.ddF)



    def migliore(self,e):
        prodotti=[]
        for p in self.riordina:
            prodotti.append(p)


        self._model.getMiglioriFornitori(prodotti)

    def costoTotale(self,e):
        flag=False
        for idP,f in self.ddF.items():

            if f.value!=None:
                flag=True
                break
        if flag:
            #funzione model costo totale
            testo=ft.Text()
        else:
            testo=ft.Text("Inserisci Tutti i fornitori!",color="red")
        self._view._rowPF2.controls.append(testo)
        self._view.update_page()


    def fine(self,e):
        self.ddF={}
        self.riordina={}
        self.venduti={}
        self.clear()
        self._view.load_Vendite()

    def previsioneDomanda(self,e):
        for id,pzV in self.venduti.items():
            self.riordina[id].value=math.ceil(pzV/self.periodo)
        self._view.update_page()

# Sezione relativa pagina storicoV
    def paginaStoricoV(self,e):
        self.clear()
        self._view.load_StoricoVendite()
        self.loadVendite()

    def loadVendite(self):
        width=self._view._page.width
        for i,v in self._model.storicoV.items():
            for id,qtn in v.items():
                nome=self._idMap[id].nome
                lordo=self._idMap[id].prezzo_Vendita*qtn
                riga = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(f"{i}", color=ft.colors.BLACK, width=width * 0.05, text_align="center"),
                            ft.Text(f"{id}", color=ft.colors.BLACK, width=width * 0.05, text_align="center" ),
                            ft.Text(f"{nome}", color=ft.colors.BLACK, width=width * 0.2, text_align="center" ),
                            ft.Text(f"{qtn}", color=ft.colors.BLACK, width=width * 0.05, text_align="center"),
                            ft.Text(f"{lordo}", color=ft.colors.BLACK, width=width * 0.1, text_align="center"),
                            ft.Text("Netto", color=ft.colors.BLACK, width=width * 0.1, text_align="center"),
                        ],
                        alignment="spaceEvenly",
                    ),
                    bgcolor="white",
                    width=width * 0.75,  # 60% della pagina
                    padding=10,
                    alignment=ft.alignment.center
                )
                self._view._page.controls.append(riga)

# Sezione relativa pagina storicoR
    def paginaStoricoR(self,e):
        self.clear()
        self._view.load_StoricoRiordina()

#altre funzioni
    def clear(self):
        self._view._page.controls=[]
