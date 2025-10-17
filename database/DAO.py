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
        idmap = {}
        for row in cursor:
            f=Fornitore(**row)
            returna.append(f)
            idmap[f.id_Fornitore]=f
        cursor.close()
        conn.close()
        return returna,idmap

    @staticmethod
    def getProdottiFornitori():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = '''select * \
                   from prodotti_fornitori pf  '''
        cursor.execute(query)
        returna = []
        idmap={}
        idmapP={}
        for row in cursor:
            if row["id_Fornitore"] in idmap.keys():
                idmap[row["id_Fornitore"]].append(row["id_Prodotto"])
            else:
                idmap[row["id_Fornitore"]] = []
                idmap[row["id_Fornitore"]].append(row["id_Prodotto"])
            if row["id_Prodotto"] in idmapP.keys():
                idmapP[row["id_Prodotto"]].append(row["id_Fornitore"])
            else:
                idmapP[row["id_Prodotto"]] = []
                idmapP[row["id_Prodotto"]].append(row["id_Fornitore"])
            returna.append(ProdottoFornitore(idF=row["id_Fornitore"],idP=row["id_Prodotto"],costo=row["Prezzo_Acquisto"],disponibili=row["pezzi_Disponibili"]))
        cursor.close()
        conn.close()
        return returna,idmap,idmapP

    @staticmethod
    def getAssociazione():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = '''select pf.id_Prodotto,f.id_Fornitore,f.nome  from fornitori f,prodotti_fornitori pf where pf.id_Fornitore=f.id_Fornitore order by pf.id_Prodotto  '''
        cursor.execute(query)
        returna = {}
        for row in cursor:
            if row['id_Prodotto'] in returna:
                returna[row['id_Prodotto']].append((row['id_Fornitore'],row['nome']))
            else:
                returna[row['id_Prodotto']] = []
                returna[row['id_Prodotto']].append((row['id_Fornitore'],row['nome']))
        cursor.close()
        conn.close()
        return returna




if __name__ == '__main__':
    DAO = DAO()
    print(DAO.getAssociazione())


