# coding: utf8
"""
Procédures pour parser un fichier XML uniprot et preparer les
objets a utiliser pour stocker en base
@author: Sarah Cohen Boulakia
"""

from uniprotLoadDB.Entry import Entry
import time
from uniprotLoadDB.Protein import Protein
import re
from uniprotLoadDB.GeneName import GeneName
from uniprotLoadDB.ProtName import ProtName
from uniprotLoadDB.Comment import Comment
from uniprotLoadDB.Keyword import Keyword
from uniprotLoadDB.DbRef import DbRef

'''
parseTree : parser un ElementTree representant un doc XML Uniprot
@return liste d'entrees (Entry)
'''


def tree_2_uniprot_objects(tree):
    # On prépare la liste d'objets entree uniprot qui sera remplie
    # au fil du parsing XML et retournee en resultat de la fonction 
    entriesList = []

    # Récupération noeud racine
    root = tree.getroot()

    # récupération du namespace (ElementTree integre le 
    # namespace a chaque nom de noeud)
    namespace = re.match('{.*}', root.tag).group()

    # Boucle sur les entrées Uniprot 
    for nodeEntry in root.iter(namespace + 'entry'):
        # récupération de la base d'origine de l'entree
        # nodeEntry.get permet de recuperer un attribut, en l'occurence dataset 
        base = nodeEntry.get('dataset')
        # récupération du premier niveau d'accession
        # premier noeud sous le noeud entry 
        accession = nodeEntry[0].text
        # date creation : attribut XML "created"
        dateCreat = time.strptime(nodeEntry.get('created'), '%Y-%m-%d')
        # date modification, attribut xml "modidied"
        dateModif = time.strptime(nodeEntry.get('modified'), '%Y-%m-%d')
        # version, attribut
        version = nodeEntry.get('version')
        # Creation de l'objet Entry 
        en = Entry(accession, base, dateCreat, dateModif, version)

        # Noeud proteine -- un seul donc on fait semblant de boucler mais on 
        # considère qu'on en trouvera un seul
        protein = Protein()
        for nodeProt in nodeEntry.iter(namespace + 'protein'):

            # recuperation des noms pour les 3 categories 
            for protName in nodeProt.iter(namespace + 'recommendedName'):
                for kindName in protName:
                    # type de nom est le nom du noeud XML, on supprime le namespace
                    # vaudra fullName, shortName ou ecNumber
                    tagCourt = re.sub('{.*}', "", kindName.tag)
                    nomProt = ProtName(kindName.text, 'recommendedName', tagCourt)
                    protein.addName(nomProt)

            for protName in nodeProt.iter(namespace + 'alternativeName'):
                for kindName in protName:
                    # type de nom est le nom du noeud XML, on supprime le namespace
                    tagCourt = re.sub('{.*}', "", kindName.tag)
                    nomProt = ProtName(kindName.text, 'alternativeName', tagCourt)
                    protein.addName(nomProt)

            for protName in nodeProt.iter(namespace + 'submittedName'):
                for kindName in protName:
                    # type de nom est le nom du noeud XML, on supprime le namespace
                    tagCourt = re.sub('{.*}', "", kindName.tag)
                    nomProt = ProtName(kindName.text, 'submittedName', tagCourt)
                    protein.addName(nomProt)
            en.setProt(protein)

        # Noeud gene -- un seul donc on fait semblant de boucler mais on 
        # considère qu'on en trouvera un seul
        for nodeGene in nodeEntry.iter(namespace + 'gene'):
            for nodeName in nodeGene.iter(namespace + 'name'):
                nomGene = GeneName(nodeName.text, nodeName.get('type'))
                en.addGeneName(nomGene)

        # Noeud organisme -- un seul donc on fait semblant de boucler mais on
        # considère qu'on en trouvera un seul
        for nodeOrganism in nodeEntry.iter(namespace + 'organism'):
            for nodeRef in nodeOrganism.iter(namespace + 'dbReference'):
                # si l'attribut type du noeud dbReference est NCBITaxo c'est 
                # l'id qu'on cherchait (attribut id)
                if nodeRef.get('type') == 'NCBI Taxonomy':
                    en.setSpecieRefNCBITaxo(nodeRef.get('id'))

        # commentaires
        for nodeComment in nodeEntry.iter(namespace + 'comment'):
            if nodeComment.get('type') in ('disease', 'function'):
                for nodeText in nodeComment.iter(namespace + 'text'):
                    commentaire = Comment(nodeComment.get('type'),
                                          nodeText.text)
                    en.addComment(commentaire)

        # keywords
        for nodeKw in nodeEntry.iter(namespace + 'keyword'):
            kw = Keyword(nodeKw.get('id'), nodeKw.text)
            en.addKeyword(kw)

        # dbRef
        for nodeDbRef in nodeEntry.iter(namespace + 'dbReference'):
            if nodeDbRef.get('type') == 'GO':
                dbR = DbRef(nodeDbRef.get('type'), nodeDbRef.get('id'))
                en.addDbRef(dbR)

        # sequence (on considère qu'on ne trouve qu'un noeud)
        for nodeSequence in nodeEntry.iter(namespace + 'sequence'):
            protein.setSequence(nodeSequence.text, nodeSequence.get('length'), nodeSequence.get('mass'))

        entriesList.append(en)

    return entriesList
