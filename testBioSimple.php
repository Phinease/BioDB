<!DOCTYPE html>
<html lang="fr">
    <head>
        <link rel="stylesheet" href="styles.css" type="text/css" />
        <link rel="icon" type="image/png" href="protein.png"/>
        <title>Un exemple pour le projet PHP</title>
    </head>

    <body>

        <h1>Protéine Info </h1>
        <?php
            // Récupérer dans des variables locales les paramètres du formulaire
            $ac = $_REQUEST['accession'];
            /*
            $geneString = $_REQUEST['gene_string'];
            $protString = $_REQUEST['prot_string'];
            $commentString = $_REQUEST['comment_string'];
            */

            //TODO : Une fois les bases crées grace au parser python, changer le login
            $connexion = oci_connect('c##pandrie_a', 'pandrie_a', 'dbinfo');

            if (!$connexion){
                $msg = oci_error();
                trigger_error(htmlentities($msg['message']), E_USER_ERROR);
            }
            // Premiere requête : info sur la sequence
            $reqSeq = " select * from proteins p "
            . " where p.accession = :acces";
            // Et sur l'espece
            $reqSpecie = "select specie from entries e where e.accession = :acces";

            // Deuxième requête : les noms de protéines
            $reqProtName = " select prot_name, name_kind, name_type"
            . " from protein_names pn"
            . " where pn.prot_name_id = ("
                . "select prot_name_id from prot_name_2_prot pn2p"
                . " where pn2p.accession = :acces)";


            if (!empty($protString)){
                $reqProtName = $reqProtName . " and pn.prot_name like '%" . $protString . "%'";
            }

            // Troisème requête : les noms de gênes
            $reqGeneName = " select gene_name, name_type"
            . " from gene_names gn"
            . " where gn.gene_name_id = ("
                . "select gene_name_id from entry_2_gene_name e2gn"
                . " where e2gn.accession = :acces)";

            if (!empty($geneString)) {
                $reqGeneName = $reqGeneName . " and gn.gene_name like '%" . $geneString . "%'";
            }

            // Quatrième requête : commentaire et mots_clés
            // Commentaires:
            $reqComment = " select type_c, txt_c from comments c"
            . " where c.accession = :acces";

            if (!empty($commentString)) {
                $reqComment = $reqComment . " and c.txt_c like '%" . $commentString . "%'";
            }
            
            // Keywords
            $reqKw = " select kw_label from keywords kw"
            . " where kw.kw_id = ("
                . " select kw_id from entries_2_keywords e2kw "
                . " where e2kw.accession = :acces)";

            // Cinquième requête : info relatives aux termes GO
            $reqGO = " select db_ref from dbref db"
            . " where db.accession = :acces and db.db_type = 'GO' ";



            // Requete exemple
            $txtReq = " select dateCreat, dataset "
            . "from entries e "
            . "where e.accession = :acces ";
            // Pour débugger on affiche le texte de la requête:
            /*
             echo "<i>(debug : ".$txtReq.")</i><br>";
             echo "<i>(debug : ".$reqSeq.")</i><br>";
             echo "<i>(debug : ".$reqSpecie.")</i><br>";
             echo "<i>(debug : ".$reqProtName.")</i><br>";
             echo "<i>(debug : ".$reqGeneName.")</i><br>";
             echo "<i>(debug : ".$reqComment.")</i><br>";
             echo "<i>(debug : ".$reqKw.")</i><br>";
             echo "<i>(debug : ".$reqGO.")</i><br>";
            */


            $ordre0 = oci_parse($connexion, $txtReq);
            $ordre1 = oci_parse($connexion, $reqSeq);
            $ordre2 = oci_parse($connexion, $reqSpecie);
            $ordre3 = oci_parse($connexion, $reqProtName);
            $ordre4 = oci_parse($connexion, $reqGeneName);
            $ordre5 = oci_parse($connexion, $reqComment);
            $ordre6 = oci_parse($connexion, $reqKw);
            $ordre7 = oci_parse($connexion, $reqGO);


            $tabOrdre = array($ordre0, $ordre1, $ordre2, $ordre3, $ordre4, $ordre5, $ordre6, $ordre7);

            /*
            oci_bind_by_name($ordre0, ":acces", $ac);
            oci_bind_by_name($ordre1, ":acces", $ac);
            oci_bind_by_name($ordre2, ":acces", $ac);
            oci_bind_by_name($ordre3, ":acces", $ac);
            oci_bind_by_name($ordre4, ":acces", $ac);
            oci_bind_by_name($ordre5, ":acces", $ac);
            oci_bind_by_name($ordre6, ":acces", $ac);
            oci_bind_by_name($ordre7, ":acces", $ac);
            */

            foreach ($tabOrdre as $ord){
                oci_bind_by_name($ord, ":acces", $ac);
            }
            // Exécution des requêtes
            /*
            oci_execute($ordre0);
            while (($row = oci_fetch_array($ordre0, OCI_BOTH)) !=false) {
                echo '<br> ' . $row[0] . ' ' . $row[1] ;
            }
            oci_free_statement($ordre0);
            */

            oci_execute($ordre1);
            echo '<h5>Information de séquence</h5>';
            while (($row = oci_fetch_array($ordre1, OCI_BOTH)) !=false) {
                echo 'Accession : ' . $row[0] . ' <br>Sequence : ' . $row[1]
                . '<br> Longueur : ' . $row[2] . ' Masse : ' . $row[3];
            }
            oci_free_statement($ordre1);

            oci_execute($ordre2);
            echo '<br> <h5> Specie : </h5>';
            while (($row = oci_fetch_array($ordre2, OCI_BOTH)) !=false) {
                echo '<a href="https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id='. $row[0] . '">' . $row[0] . '</a>' ;
            }
            oci_free_statement($ordre2);

            oci_execute($ordre3);
            echo '<h5>Liste des noms de protéines</h5>';
            while (($row = oci_fetch_array($ordre3, OCI_BOTH)) !=false) {
                echo 'Nom : ' . $row[0] . ' Type : ' . $row[1] . ' Sorte : ' . $row[2];
            }
            oci_free_statement($ordre3);

            oci_execute($ordre4);
            echo '<h5>Liste des noms de gène</h5>';
            while (($row = oci_fetch_array($ordre4, OCI_BOTH)) !=false) {
                echo 'Nom : ' . $row[0] . ' Type : ' . $row[1];
            }
            oci_free_statement($ordre4);

            oci_execute($ordre5);
            echo '<h5> Commentaires </h5> <ul>';
            while (($row = oci_fetch_array($ordre5, OCI_BOTH)) !=false) {
                echo '<li> Type de commentaire : ' . $row[0]
                 . '<br> <i>' . $row[1] .'</i><br><br> </li>' ;
            }
            echo '</ul>';
            oci_free_statement($ordre5);

            oci_execute($ordre6);
            echo '<h5> Keywords </h5>';
            while (($row = oci_fetch_array($ordre6, OCI_BOTH)) !=false) {
                echo $row[0] . '<br>' ;
            }
            oci_free_statement($ordre6);

            oci_execute($ordre7);
            echo '<h5> Data Base Reference </h5>';
            while (($row = oci_fetch_array($ordre7, OCI_BOTH)) !=false) {
                echo '<a href="https://www.ebi.ac.uk/QuickGO/term/GO:' . $row[0] .'">' . $row[0] . '</a><br>' ;
            }
            oci_free_statement($ordre7);


            oci_close($connexion);

        ?>

	<a href="index.html" > <button value="Nouvelle recherche">Nouvelle recherche </button></a>
    </body>
</html>
