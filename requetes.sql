-- Quels sont les noms recommandés des protéines des entrées qui comportent le terme « cardiac » dans un champ commentaire (on veut le numéro d'accession et le nom de la protéine de ces entrées) ?

SELECT PN.prot_name, C.accession
FROM PROTEIN_NAMES PN, COMMENTS C, PROT_NAME_2_PROT PN2P
WHERE C.txt_c LIKE '%cardiac%'
AND C.accession = PN2P.accession
AND PN.name_kind = 'recommendedName'
AND PN2P.prot_name_id = PN.prot_name_id;


-- Quels sont les noms recommandés des protéines des entrées qui comportent le mot clé « Long QT syndrome » dans un champ mot-clé (on veut le numéro d'accession et le nom de la protéine de ces entrées)?

SELECT PN.prot_name, E2K.accession
FROM PROTEIN_NAMES PN, KEYWORDS K, ENTRIES_2_KEYWORDS E2K, PROT_NAME_2_PROT PN2P
WHERE PN.name_kind = 'recommendedName'
AND K.kw_label LIKE '%Long QT syndrome%'
AND E2K.kw_id = K.kw_id
AND PN2P.accession = E2K.accession
AND PN2P.prot_name_id = PN.prot_name_id;



--Quelle  est  l'entrée  qui  a  la  séquence  de  plus  grande  taille  (ou  les  entrées  si  plusieurs  entrées  atteignent  ce nombre maximal) ?

SELECT accession -- On suppose que par quel est l'entrée ils sous entendent le num d'accession (à modifier sinon)
FROM PROTEINS
WHERE seqLength =
                (SELECT MAX(seqLength) FROM PROTEINS)

--Quelle sont les entrées qui ont strictement plus de 2 noms de gène (on veut les accessions et le nombre de noms de gène) ?

SELECT E2GN.accession, GN.gene_name
FROM GENE_NAMES GN, ENTRY_2_GENE_NAME E2GN
WHERE GN.gene_name_id = E2GN.gene_name_id
AND E2GN.accession IN
(SELECT accession
FROM ENTRY_2_GENE_NAME
GROUP BY accession
HAVING COUNT(gene_name_id) > 2);

--Dans quelles entrées le terme «channel» est présent dans les noms de protéine (on veut l'accession, les noms et les sortes (kind) des noms) ?

SELECT PN2P.accession, PN.prot_name, PN.name_kind
FROM PROTEIN_NAMES PN, PROT_NAME_2_PROT PN2P
WHERE PN.prot_name_id = PN2P.prot_name_id
AND PN.prot_name LIKE '%channel%';


--Quelles sont les entrées et leur nom recommandé associées à la fois au mot clé « Long QT syndrome » et au mot clé « Short QT syndrome » ?

(SELECT e.accession, pn.prot_name
FROM KEYWORDS K1, ENTRIES E, ENTRIES_2_KEYWORDS E2K, PROTEIN_NAMES PN, PROT_NAME_2_PROT PN2P
WHERE PN.name_kind = 'recommendedName'
AND K1.kw_label LIKE '%Long QT syndrome%'
AND E2K.kw_id = K1.kw_id
AND PN.prot_name_id = PN2P.prot_name_id
AND PN2P.accession = E2K.accession)
INTERSECT
(SELECT e.accession, pn.prot_name
FROM KEYWORDS K2, ENTRIES E, ENTRIES_2_KEYWORDS E2K, PROTEIN_NAMES PN, PROT_NAME_2_PROT PN2P
WHERE PN.name_kind = 'recommendedName'
AND K2.kw_label LIKE '%Short QT syndrome%'
AND E2K.kw_id = K2.kw_id
AND PN.prot_name_id = PN2P.prot_name_id
AND PN2P.accession = E2K.accession);

--Quels sont les termes GOs des entrées qui possèdent un mot clé « Long QT syndrome » et qui sont communs à au moins 2 entrées ?

(SELECT db_ref
FROM DBREF, KEYWORDS
WHERE db_type LIKE '%GO%'
AND accession IN
(SELECT accession
FROM ENTRIES_2_KEYWORDS E2K, KEYWORDS K
WHERE K.kw_label LIKE '%Long QT syndrome%'
AND K.kw_id = E2K.kw_id))
INTERSECT
(SELECT db_ref
FROM DBREF
WHERE db_type LIKE '%GO%'
AND accession IN
(SELECT accession from DBREF
GROUP BY accession
HAVING COUNT(db_ref) >= 2));
