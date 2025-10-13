from dataclasses import dataclass


@dataclass
class Prodotto:
    id_Prodotto:int
    nome: str
    descrizione: str
    prezzo_Vendita: float
    disponibilita: int

    def __hash__(self):
        return hash(self.id_Prodotto)

    def __eq__(self, other):
        return self.id_Prodotto == other.id_Prodotto


