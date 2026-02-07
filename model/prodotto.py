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


