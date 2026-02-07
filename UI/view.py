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
import flet as ft



class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "PreviStock - Previsione domanda e riordino intelligente per un negozio"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#ebf4f4"
        self._page.window_height = 800
        page.window_center()
        self._page.scroll="auto"
        self.id_mensilita = 0
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._startP=0
        self._flagP=False
        self.rows = []


    def setNavBar(self):
        pagHeight = self._page.window_height
        hNav = 0.0625
        coloreTxt = ft.colors.WHITE
        over = ft.colors.BLUE_GREY_700
        coloreBck = ft.colors.BLUE_GREY_900

        self._title = ft.Text("PreviStock - Previsione domanda e riordino intelligente per un negozio", color=coloreTxt,
                              size=16)

        self._btnNavVendite = ft.TextButton(text="Vendite",
                                        style=ft.ButtonStyle(
                                            color=coloreTxt,
                                            overlay_color=over, shape=ft.RoundedRectangleBorder(radius=0)),
                                        height=pagHeight * hNav,on_click=self._controller.paginaVendite)
        self._btnNavRiordina = ft.TextButton(text="Riordina",
                                        style=ft.ButtonStyle(
                                            color=coloreTxt,
                                            overlay_color=over, shape=ft.RoundedRectangleBorder(radius=0)),
                                        height=pagHeight * hNav,on_click=self._controller.paginaRiordina)

        self._btnNavStoricoV = ft.TextButton(text="StoricoVendite",
                                        style=ft.ButtonStyle(
                                            color=coloreTxt,
                                            overlay_color=over, shape=ft.RoundedRectangleBorder(radius=0)),
                                        height=pagHeight * hNav,on_click=self._controller.paginaStoricoV)


        self._navBar = ft.Container(ft.Row([ft.Row([self._btnNavVendite,self._btnNavRiordina,self._btnNavStoricoV]),self._title],alignment="spaceBetween"),
                                    bgcolor=coloreBck,height=self._page.window_height*0.0625,padding=8)
        self._page.controls.append(self._navBar)

#Caricamento pagina iniziale
    def load_interface(self):
        self.load_Vendite()
        self._page.update()

# Caricamento pagina vendite
    def load_Vendite(self):
        width =self._page.window_width
        ddw=0.35
        if self._flagP:
            self._flagP=False
            self._startP=self.id_mensilita

        self.setNavBar()
        self._mese=ft.Text(value=f"Mensilita {self.id_mensilita}", color="black",size=20)
        self._mensilita = ft.Container(self._mese,
                                       border=ft.border.all(1,ft.colors.BLUE_GREY_900),  # bordo di 2px blu
                                       border_radius=5,  # angoli arrotondati
                                       padding=20,  # spazio interno
                                       margin=5,
                                       alignment=ft.alignment.center,width=width*0.15)
        self._page.controls.append(self._mensilita)
        self._ddVProd1=ft.Dropdown(label="Prodotti",hint_text="Seleziona il prodotto venduto",width=width*ddw)
        self._controller.loadProdotti()#riempe il dropDown
        self._txtVIn1=ft.TextField(label="pz venduti",input_filter=ft.NumbersOnlyInputFilter(),
        keyboard_type=ft.KeyboardType.NUMBER)

        self._btnVAgg=ft.ElevatedButton(text="Aggiungi vendita",on_click=self._controller.aggiungiV,style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=0),color=ft.colors.WHITE,bgcolor=ft.colors.ORANGE_600,overlay_color=ft.colors.ORANGE_300))
        self._btnVFine = ft.ElevatedButton(text="Fine Mensilità", on_click=self._controller.fineMese,
                                           style=ft.ButtonStyle(
                                               shape=ft.RoundedRectangleBorder(radius=0), color=ft.colors.WHITE,
                                               bgcolor=ft.colors.ORANGE_600, overlay_color=ft.colors.ORANGE_300))
        self._rowV1 = ft.Row([self._ddVProd1, self._txtVIn1, self._btnVAgg, self._btnVFine])
        self._page.controls.append(self._rowV1)
        self._txtVOut1=ft.Text(value="",color="Red")
        self._rowV2=ft.Row([self._txtVOut1])
        self._page.controls.append(self._rowV2)
        self._txtVResult = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txtVResult)
        self._page.update()

# Caricamento pagina rioridna
    def load_Riordina(self):
        self.setNavBar()
        btnFine=ft.ElevatedButton(text="Seleziona Fornitori", on_click=self._controller.selezFornitori,
                                           style=ft.ButtonStyle(
                                               shape=ft.RoundedRectangleBorder(radius=0), color=ft.colors.WHITE,
                                               bgcolor=ft.colors.ORANGE_600, overlay_color=ft.colors.ORANGE_300))
        btnPrevisione=ft.ElevatedButton(text="Previsione Domanda per il mese successivo", on_click=self._controller.previsioneDomanda,
                                           style=ft.ButtonStyle(
                                               shape=ft.RoundedRectangleBorder(radius=0), color=ft.colors.WHITE,
                                               bgcolor=ft.colors.ORANGE_600, overlay_color=ft.colors.ORANGE_300))
        self._rowR2=ft.Row([btnPrevisione, btnFine])
        self._page.controls.append(self._rowR2)
        width=self._page.width
        txtInR1=ft.Text(value="Prodotto",weight="bold",size=20,width=width*0.22)
        txtInR2=ft.Text(value="Riordina",weight="bold",size=20,width=width*0.1)
        self.rowR1=ft.Row([txtInR1,txtInR2],spacing=20,alignment="center")
        self._page.controls.append(self.rowR1)
        self._page.update()


# Caricamento pagina fornitore
    def load_Fornitore(self):
        width=self._page.width
        self.NavFornitori=ft.Container(ft.Text("Seleziona Fornitori",weight="bold",size=24,color=ft.colors.WHITE,text_align="center"),
                                       bgcolor=ft.colors.BLUE_GREY_900, width=width*0.7, border_radius=5,height=60,alignment=ft.alignment.center)
        self._page.controls.append(self.NavFornitori)
        txtInF1 = ft.Text(value="Prodotto", weight="bold", size=20, width=width * 0.22)
        txtInF2 = ft.Text(value="Pz", weight="bold", size=20, width=width * 0.1)
        txtInF3 = ft.Text(value="Fornitore", weight="bold", size=20, width=width * 0.22)
        rowF1 = ft.Row([txtInF1, txtInF2,txtInF3], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=20,alignment="center")
        self.containerF1=ft.Container(rowF1,padding=ft.padding.all(4),
                                            margin=ft.margin.all(4),border_radius=5,width=width*0.6)
        self._page.controls.append(self.containerF1)
        self._page.update()

    def load_btn(self):
        btnFine = ft.ElevatedButton(text="Riordina", on_click=self._controller.fine,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=0), color=ft.colors.WHITE,
                                        bgcolor=ft.colors.ORANGE_600, overlay_color=ft.colors.ORANGE_300))
        btnSelez = ft.ElevatedButton(text="Selezione Automatica",
                                          on_click=self._controller.migliore,
                                          style=ft.ButtonStyle(
                                              shape=ft.RoundedRectangleBorder(radius=0), color=ft.colors.WHITE,
                                              bgcolor=ft.colors.ORANGE_600, overlay_color=ft.colors.ORANGE_300))
        btnCosto = ft.ElevatedButton(text="Mostra costo",
                                          on_click=self._controller.costoTotale,
                                          style=ft.ButtonStyle(
                                              shape=ft.RoundedRectangleBorder(radius=0), color=ft.colors.WHITE,
                                              bgcolor=ft.colors.ORANGE_600, overlay_color=ft.colors.ORANGE_300))

        self._rowPF=ft.Row([btnSelez,btnCosto, btnFine])
        self._page.controls.append(self._rowPF)
        self._rowPF2=ft.Row()
        self._page.controls.append(self._rowPF2)
        self._page.update()

# Caricamento pagina storicoV
    def load_StoricoVendite(self):
        width=self._page.window_width
        self.setNavBar()
        intestazione = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Periodo", color=ft.colors.WHITE, width=width*0.05, text_align="center", weight="bold"),
                    ft.Text("Id", color=ft.colors.WHITE, width=width*0.05, text_align="center", weight="bold"),
                    ft.Text("Nome", color=ft.colors.WHITE, width=width*0.2, text_align="center", weight="bold"),
                    ft.Text("quantità", color=ft.colors.WHITE, width=width*0.05, text_align="center", weight="bold"),
                    ft.Text("Lordo", color=ft.colors.WHITE, width=width*0.1, text_align="center", weight="bold"),

                ],
                alignment="spaceEvenly",
            ),
            bgcolor="orange",
            width=width*0.75,  # 60% della pagina
            padding=10,
            alignment=ft.alignment.center
        )
        self._page.controls.append(intestazione)
        self._controller.loadVendite()
        self._page.update()


# altre funzioni
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()