# coding: utf8
'''
Classe Comment : Commentaire de fiche Uniprot
   Attributs :
      - typeC : type de commentaire
      - text : texte du commentaire
@author: Sarah Cohen Boulakia
'''


class Comment:
    # Parametre de classe utilise pour dire si les Comment doivent etre inserees
    # en base quand insertDB est appele
    DEBUG_INSERT_DB = True

    def __init__(self, typeC, text):
        self._typeC = typeC
        self._text = text

    '''
    Insertion en base du commentaire
    @param curDB: curseur sur la base oracle
    @param accession: numero d'accession a l'entree Uniprot
    '''

    def insertDb(self, curDB, accession):
        if Comment.DEBUG_INSERT_DB:
            curDB.prepare(
                "INSERT INTO comments (comment_id, accession, type_c, txt_c) "
                "VALUES (seq_comment_id.NEXTVAL, :accession, :typeC, :txtC)")
            curDB.execute(None, {'accession': accession, 'typeC': self._typeC, 'txtC': self._text})
