from database.DB_connect import DBConnect
from model.fornitore import Fornitore
from model.prodotto import Prodotto
from model.prodottoFornitore import ProdottoFornitore


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getProdotti():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = '''select * from prodotti_magazzino pm order by pm.nome'''
        cursor.execute(query)
        returna=[]
        idmap={}
        for row in cursor:
            p=Prodotto(**row)
            returna.append(p)
            idmap[p.id_Prodotto]=p
        cursor.close()
        conn.close()
        return returna,idmap

    @staticmethod
    def getFornitori():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = '''select * from fornitori f  '''
        cursor.execute(query)
        returna = []

        for row in cursor:
            returna.append(Fornitore(**row))
        cursor.close()
        conn.close()
        return returna

    @staticmethod
    def getProdottiFornitori():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = '''select * \
                   from prodotti_fornitori pf  '''
        cursor.execute(query)
        returna = []

        for row in cursor:
            returna.append(ProdottoFornitore(idF=row["id_Fornitore"],idP=row["id_Prodotto"],costo=row["Prezzo_Acquisto"],disponibili=row["pezzi_Disponibili"]))
        cursor.close()
        conn.close()
        return returna





if __name__ == '__main__':
    DAO = DAO()
    print(DAO.getProdottiFornitori())


