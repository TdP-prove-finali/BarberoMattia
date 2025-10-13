from dataclasses import dataclass


@dataclass
class Fornitore:
    id_Fornitore:int
    nome:str
    email:str
    CoordinataX:float
    CoordinataY:float

    def __hash__(self):
        return hash(self.id_Fornitore)
    def __eq__(self, other):
        return self.id_Fornitore == other.id_Fornitore
