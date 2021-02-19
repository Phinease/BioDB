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
        $geneString = $_REQUEST['geneS'];
        $protString = $_REQUEST['protS'];
        $commentString = $_REQUEST['commentS'];



        // On se connecte à la base de donnée
        $connexion = oci_connect('c##aadamia_a', 'aadamia_a', 'dbinfo');

        // En cas d'erreur, on affiche un message
        if (!$connexion){
            $msg = oci_error();
            trigger_error(htmlentities($msg['message']), E_USER_ERROR);
        }


        // Notre requetes va trouver tout les entries (a partir des accession)
        $requete = " select * from entries e"
        . " where e.accession in "
            // On regarde par rapport au nom de gene donné
            . "( select distinct accession from entry_2_gene_name e2gn where e2gn.gene_name_id in "
                    // On recuper les id des genes qui ont un nom correspondant à celui rentré par l'utilisateur
                    // Si l'utilisateur ne rentre rien dans la zone de texte, cela fait like '%%' , et cela renvoie tout les cas possible
                 . " (select gene_name_id from gene_names gn where gn.gene_name like '%' || :gene_S || '%' )) "
        . "or e.accession in "
            // Ou par rapport au nom de protéine donné
            . "( select distinct accession from prot_name_2_prot pn2p where pn2p.prot_name_id in "
                    // Sinon, on récuper les id des proteine qui ont un nom correspondant
                . "(select prot_name_id from protein_names pn where pn.prot_name like '%' || :prot_S || '%')) "
        . "or e.accession in "
            // Ou par rapport au commentaire donné
            . "( select distinct accession from comments c where txt_c like '%' || :comment_S || '%')";






        // Pour débugger on affiche le texte de la requête:
	/*
        echo "<i>(debug : ".$requete.")</i><br>";
	*/




        // On parse les requetes
        $ordre1 = oci_parse($connexion, $requete);


	

        // On associe aux variables oracle une variable php
        oci_bind_by_name($ordre1, ":gene_S", $geneString);
        oci_bind_by_name($ordre1, ":prot_S", $protString);
        oci_bind_by_name($ordre1, ":comment_S", $commentString);


        // Exécution des requêtes

        oci_execute($ordre1);
        // On affiche les resultats de la recherche sous forme d'un tableau
        echo '<h5>Résultat de la recherche</h5>';
        echo '<table> <thead> <tr> <th> Accession </th> <th>Date de Création</th> <th>Date de Mise à Jour</th> <th> Data Set </th> <th>Version de l\'entry</th> <th> Espece </th> </tr> </thead>';
        while (($row = oci_fetch_array($ordre1, OCI_BOTH)) !=false) {
            // Il faut qu'on recupère l'accession pour que l'utilisateur fasse une recherche precise
            $accession = $row[0];
            // Lien de notre recherche avec la variable accession passé dans l'URL
            $link = "testBioSimple.php?accession=" . $accession;
            echo '<tr><td><a href="' . $link . '" >' . $row[0] . '</a></td><td>'. $row[1]  .'</td><td>' .$row[2] .  '</td><td>' . $row[3]
                . '</td><td>'. $row[4] .'</td><td>'. $row[5] . '</td></tr>';
        }
	    echo '</table>';
        oci_free_statement($ordre1);




        oci_close($connexion);

        ?>


        <!-- On met un boutton pour revenir en arrière et faire une nouvelle recherche -->
        <a href="index.html"><button value="Nouvelle recherche" >Nouvelle recherche</button></a>
    </body>
</html>
