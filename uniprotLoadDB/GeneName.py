# coding: utf8
"""
Classe GeneName : Noms de genes Uniprot
   Attributs :
      - name : nom du gène
      - kwLabel : keyword label
@author: Sarah Cohen Boulakia
"""
import cx_Oracle


class GeneName:
    # Parametre de classe utilise pour dire si les GeneName doivent etre inseres
    # en base quand insertDB est appele
    DEBUG_INSERT_DB = True

    def __init__(self, name, typeN):
        self._name = name
        self._typeN = typeN

    '''
    Si le nom de gene (couple nom/type) n'existe pas déjà, ajout en base
    @param curDb: Curseur sur la base de donnees oracle 
    @return identifiant du gene en base de donnees
    '''

    def insertDB(self, curDB):
        gene_name_id = -1

        if GeneName.DEBUG_INSERT_DB:
            # Vérifier s'il y a pas de répétition
            curDB.prepare(
                "SELECT GENE_NAME_ID FROM GENE_NAMES "
                "WHERE GENE_NAME=:gene_name AND NAME_TYPE=:name_type")
            curDB.execute(None, {'gene_name': self._name, 'name_type': self._typeN})
            raw = curDB.fetchone()
            if raw is not None:
                # Si oui, récupérer id
                gene_name_id = raw[0]
            else:
                # Si non, créer un nouveau
                idG = curDB.var(cx_Oracle.NUMBER)
                # Retourner un id de gene_name par la séquance dans la variable id
                curDB.prepare(
                    "INSERT INTO GENE_NAMES (GENE_NAME_ID, GENE_NAME, NAME_TYPE) "
                    "VALUES (SEQ_GENE_NAMES.NEXTVAL, :gene_name, :name_type) "
                    "RETURNING GENE_NAME_ID INTO :id")
                curDB.execute(None, {'gene_name': self._name, 'name_type': self._typeN, 'id': idG})
                gene_name_id = idG.getvalue()[0]
        return gene_name_id
