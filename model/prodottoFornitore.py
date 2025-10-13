from dataclasses import dataclass

@dataclass
class ProdottoFornitore:
    idF:int
    idP:int
    costo:float
    disponibili:int

    def __hash__(self):
        return hash((self.idF,self.idP))
    def __eq__(self, other):
        return (self.idF,self.idP) == (other.idF,other.idP)
