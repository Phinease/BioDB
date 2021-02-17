# coding: utf8
"""
Classe ProtName : Noms de proteines Uniprot
   Attributs :
      - name : nom de la proteine
      - name_kind : categorie de nom ('alternativeName', 'recommendedName', 'submittedName')
      - name_type : Type de nom ('fullName', 'shortName', 'ecNumber')
@author: Sarah Cohen Boulakia
"""
import cx_Oracle


class ProtName:
    # Parametre de classe utilise pour dire si les ProtName doivent etre inseres
    # en base quand insertDB est appele
    DEBUG_INSERT_DB = True

    def __init__(self, name, name_kind, name_type):
        self._name = name
        self._name_kind = name_kind
        self._name_type = name_type

    '''
    Si le nom de proteine (couple nom/type/categorie) n'existe pas deja, 
    ajout en base
    @param curDb: Curseur sur la base de donnees oracle 
    @return identifiant du gene en base de donnees
    '''

    def insertDB(self, curDB):
        prot_name_id = -1

        curDB.prepare("SELECT PROT_NAME_ID FROM PROTEIN_NAMES "
                      "WHERE PROT_NAME=:prot_name AND NAME_KIND=:name_kind AND NAME_TYPE=:name_type")
        curDB.execute(None, {'prot_name': self._name, 'name_kind': self._name_type, 'name_type': self._name_kind})
        raw = curDB.fetchone()
        if raw is not None:
            prot_name_id = raw[0]
        else:
            if ProtName.DEBUG_INSERT_DB:
                idP = curDB.var(cx_Oracle.NUMBER)
                curDB.prepare(
                    "INSERT INTO PROTEIN_NAMES (PROT_NAME_ID, PROT_NAME, NAME_KIND, NAME_TYPE) "
                    "VALUES (SEQ_PROT_NAMES.NEXTVAL, :prot_name, :name_kind, :name_type) "
                    "RETURNING PROT_NAME_ID INTO :id")
                curDB.execute(None, {'prot_name': self._name, 'name_kind': self._name_kind,
                                     'name_type': self._name_type, 'id': idP})
                prot_name_id = idP.getvalue()[0]
        return prot_name_id
