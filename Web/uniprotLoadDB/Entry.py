# coding: utf8
"""
Classe entry : Entree fiche Uniprot
   Attributs :
      - _accession : Numero d'accession de la fiche uniprotLoadDB
      - _base : Base de reference
      - _dateCreat : Date de creation de la fiche uniprotLoadDB
      - _dateModif : Date de modification de la fiche uniprotLoadDB
      - _version : version de la fiche
      - _protein : proteine associee a la fiche (sequence, noms ...)
      - _gene : gene associe a la fiche
      - _ comments : liste des commentaires de la fiche
      - _dbRefsGO : references associees a la fiche dans la base GO
      - _keywords : liste des mots cles associes  la fiche
@author: Sarah Cohen Boulakia
"""
import time
from uniprotLoadDB.Keyword import Keyword
from uniprotLoadDB.GeneName import GeneName


class Entry:
    # Parametre de classe utilise pour dire si les entrees doivent etre inserees
    # en base quand insertDB est appele
    DEBUG_INSERT_DB = True

    def __init__(self, accession, dataset, dateCreat, dateModif, version):
        # Copie dans des attributs de classe des valeurs passees 
        self._accession = accession
        self._dataset = dataset
        self._dateCreat = dateCreat
        self._dateModif = dateModif
        self._version = version
        self._protein = None
        self._geneNames = []
        self._specieRefNCBITaxo = None
        self._comments = []
        self._dbRefs = []
        self._keywords = []

    '''
    Affectation de la proteine associee a la fiche 
    @param prot: Proteine associee (Protein)
    '''

    def setProt(self, prot):
        self._protein = prot

    '''
    Ajout d'un nom de gene associe a la fiche
    @param geneName: Nom de gene associe 
    '''

    def addGeneName(self, geneName):
        self._geneNames.append(geneName)

    '''
    Positionner la reference a l'espece dans la taxonomie NCBI
    @param ref reference taxonomie NCBI de l'espece
    '''

    def setSpecieRefNCBITaxo(self, ref):
        self._specieRefNCBITaxo = ref

    '''
    Ajout d'un commentaire à la fiche
    @param comment : commentaire (Commentaire)
    '''

    def addComment(self, comment):
        self._comments.append(comment)

    '''
    Ajout d'une reference a une base tierce
    @param ref: reference  a ajouter (DbRef)
    '''

    def addDbRef(self, ref):
        self._dbRefs.append(ref)

    '''
    Ajout d'un nouveau mot cle 
    @kw: Mot cle (Keyword)
    '''

    def addKeyword(self, kw):
        self._keywords.append(kw)

    ''' 
    Stockage de l'entree et de toutes ses caracteristiques dans la base oracle
    @param curDB: Curseur sur la base Oracle
    @param accession: Numero d'accession de la fiche uniprotLoadDB
    '''

    def insertDB(self, curDB):

        if Entry.DEBUG_INSERT_DB:
            curDB.prepare(
                "INSERT INTO entries  (ACCESSION, DATASET, DATECREAT, DATEUPD, ENTRYVERSION, SPECIE)  "
                "VALUES  (:accession, :dataset,"
                "TO_DATE(:dateCreat,\'DD/MM/YYYY\'),  TO_DATE(:updDate, \'DD/MM/YYYY\'), :vers, :specie)")
            curDB.execute(None, {'accession': self._accession,
                                 'dataset': self._dataset,
                                 'dateCreat': time.strftime("%d/%m/%Y", self._dateCreat),
                                 'updDate': time.strftime("%d/%m/%Y", self._dateModif),
                                 'vers': self._version,
                                 'specie': self._specieRefNCBITaxo})
            ## version non optimisee 
            # curDB.execute("INSERT INTO entries " \
            #                + " (accession, base, dateCreat, dateUpd, " \
            #                + " entryVersion, specie) " \
            #                + " values " \
            #                + " ('" + self._accession + "', " \
            #                +       + "'" + self._base + "', " \
            #                    + " TO_DATE('" + time.strftime("%d/%m/%Y",self._dateCreat) + "','DD/MM/YYYY'), " \
            #                    + " TO_DATE('" + time.strftime("%d/%m/%Y",self._dateModif) + "', 'DD/MM/YYYY'), " \
            #                    + "'" + self._version + "', " \
            #                    + "'" +  self._specieRefNCBITaxo + "')")        

        # Ajout des commentaires en base
        for c in self._comments:
            c.insertDb(curDB, self._accession)

        # Ajout des noms de genes et leurs references 
        for geneName in self._geneNames:
            geneNameId = geneName.insertDB(curDB)
            if GeneName.DEBUG_INSERT_DB:
                curDB.prepare(
                    "INSERT INTO ENTRY_2_GENE_NAME (ACCESSION, GENE_NAME_ID) VALUES (:accession, :gene_name_id)")
                curDB.execute(None, {'accession': self._accession, 'gene_name_id': geneNameId})
                pass

        # Ajout des mots cles 
        for kw in self._keywords:
            kw.insertDB(curDB)
            if Keyword.DEBUG_INSERT_DB:
                curDB.prepare("INSERT INTO ENTRIES_2_KEYWORDS (ACCESSION, KW_ID) VALUES (:accession, :kw_id)")
                curDB.execute(None, {'accession': self._accession, 'kw_id': kw._kwId})
                pass

        # Ajout des references a des bases tierces
        for go in self._dbRefs:
            go.insertDB(curDB, self._accession)

        # Ajout des porteines (sequence, noms ...)
        self._protein.insertDB(curDB, self._accession)
