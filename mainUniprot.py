# coding: utf8
'''
Created on 27 janv. 2021

@author: Sarah Cohen Boulakia
'''

import cx_Oracle
import xml.etree.ElementTree as ET
import sys
import configparser
from uniprotLoadDB import UniprotParser, UniprotOracle
from builtins import Exception
from uniprotLoadDB.Comment import Comment
from uniprotLoadDB.DbRef import DbRef
from uniprotLoadDB.Entry import Entry
from uniprotLoadDB.GeneName import GeneName
from uniprotLoadDB.Keyword import Keyword
from uniprotLoadDB.Protein import Protein
from uniprotLoadDB.ProtName import ProtName

# Nous sommes dans le programme principal de l'appli 
if __name__ == '__main__':

    # Variable qui contiendra la connexion à Oracle
    con = None
    # On fait un try global pour s'assurer de fermer proprement la connexion à
    # Oracle si elle a pu être ouverte (éviter d'avoir des sessions fantomes 
    # sous Oracle est important)
    try:

        # Lecture du fichier de configuration qui contient les paramètres du programme
        # On charge en mémoire via le package standard python ConfigParser
        config = configparser.ConfigParser()
        config.read('resources/config.txt')

        # Connexion base de données, on récupère les infos dans le fichier de config
        dns = cx_Oracle.makedsn("tp-oracle.ups.u-psud.fr", 1522, sid=config.get('ORACLE', 'SID'))
        con = cx_Oracle.connect(config.get('ORACLE', 'USER'), config.get('ORACLE', 'PASSWD'), dns)

        # Création de la liste d'entrées dans laquelle on stockera les
        # objets représentant les entrées uniprot au fil de la lecture XML
        entList = []

        # Pour faciliter vos tests, des paramètres permettent de dire quels objets 
        # doivent être insérés en base ou non.
        if config.get('PERSIST', 'Comment') == 'FALSE':
            Comment.DEBUG_INSERT_DB = False
        if config.get('PERSIST', 'DbRef') == 'FALSE':
            DbRef.DEBUG_INSERT_DB = False
        if config.get('PERSIST', 'Entry') == 'FALSE':
            Entry.DEBUG_INSERT_DB = False
        if config.get('PERSIST', 'GeneName') == 'FALSE':
            GeneName.DEBUG_INSERT_DB = False
        if config.get('PERSIST', 'Keyword') == 'FALSE':
            Keyword.DEBUG_INSERT_DB = False
        if config.get('PERSIST', 'Protein') == 'FALSE':
            Protein.DEBUG_INSERT_DB = False
        if config.get('PERSIST', 'ProtName') == 'FALSE':
            ProtName.DEBUG_INSERT_DB = False

        # On boucle sur les options de la section LOADFILES du fichier de
        # configuration pour avoir la liste des fichiers à charger
        # (Option vaudra donc par exemple FILE1, puis FILE2 ...)
        for option in config.options("LOADFILES"):
            # On récupère le nom de fichier associé à cette option
            fileName = config.get("LOADFILES", option)
            # On parse le fichier XML en utilisant ElementTree, package standard
            # de python (renomme "ET" dans les imports)
            tree = ET.parse(fileName)
            # print("Option: ", option, ", fileName: ", fileName, ", tree: ", tree, "\n")
            # On ajoute la liste d'objets entrees obtenues en lisant l'ElementTree
            # par notre procedure parseTree (importee de UniprotParser.py)       
            entList = entList + UniprotParser.tree_2_uniprot_objects(tree)

        # On a maintenant la liste des entrees, on appelle notre fonction
        # qui les sauvegarde en base de donnees
        UniprotOracle.save2Oracle(con, entList)

    except Exception as err:
        sys.stderr.write('ERROR: %s' % str(err))
        # raise err

    finally:
        con.close()
