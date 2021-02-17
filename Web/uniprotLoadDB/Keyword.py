# coding: utf8
"""
Classe Keyword : mots cles de la base uniprotLoadDB
   Attributs :
      - kwId : keyword id
      - kwLabel : keyword label
@author: Sarah Cohen Boulakia
"""


class Keyword:
    # Parametre de classe utilise pour dire si les Keyword doivent etre inseres
    # en base quand insertDB est appele
    DEBUG_INSERT_DB = True

    def __init__(self, kwId, kwLabel):
        self._kwId = kwId
        self._kwLabel = kwLabel

    '''
    Si le mot cle n'existe pas, ajout en base.
    @param curDb: Curseur sur la base de donnees oracle 
    @return N/A
    '''

    def insertDB(self, curDB):
        curDB.prepare("SELECT KW_ID FROM KEYWORDS WHERE KW_ID=:kwId")
        curDB.execute(None, {'kwId': self._kwId})
        raw = curDB.fetchone()
        if raw is None:
            if Keyword.DEBUG_INSERT_DB:
                curDB.prepare("INSERT INTO KEYWORDS (KW_ID, KW_LABEL) VALUES (:kwID, :kwLabel)")
                curDB.execute(None, {'kwID': self._kwId, 'kwLabel': self._kwLabel})
