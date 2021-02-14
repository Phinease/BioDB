# coding: utf8
"""
Procédures pour stocker en base des objets representant la structure
XML Uniprot
@author: Sarah Cohen Boulakia
"""


def save2Oracle(conOracle, entList):
    global cur
    try:
        # On ouvre un "curseur" sur la connexion Oracle recue en parametre
        # il sera utilse a chaque requete par les objets
        cur = conOracle.cursor()

        # Boucle sur les objets entree pour les inserer en base 
        for en in entList:
            en.insertDB(cur)

        # On ferme le curseur
        cur.close()
        # on commit
        conOracle.commit()
    except:
        # en cas d'erreur on essaye quand meme de fermer le curseur
        cur.close()
        raise
