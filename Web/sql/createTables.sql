
/************************************************************************
 * Table principale entries = entr�es uniprot 
 ************************************************************************
 */
CREATE TABLE entries (accession VARCHAR2(10),
                        dateCreat DATE,                 
                        dateUpd DATE,
                        dataset varchar2(10),
                        entryVersion INT,
                        specie VARCHAR2(100),
                        CONSTRAINT pk_entries PRIMARY KEY (accession),
                        CONSTRAINT ck_dataset CHECK (dataset in ('Swiss-Prot', 'TrEMBL'))
                      );
                      


/************************************************************************
 * Table proteins = relation 1-1 avec entries, s�par� pour optimisation
 * sur taille CLOB 
 ************************************************************************
 */
CREATE TABLE proteins (accession varchar2(10),
						seq CLOB,
                        seqLength INT,
                        seqMass INT,
						CONSTRAINT pk_prot PRIMARY KEY (accession),
						CONSTRAINT fk_prot_entry FOREIGN KEY (accession) REFERENCES entries(accession),
						CONSTRAINT ck_seqL_nn CHECK (seqLength IS NOT NULL),
						CONSTRAINT ck_seq_m CHECK (seqMass IS NOT NULL)
					    );

/************************************************************************
 * Table protein_names : Noms de proteine / id automatique pour lien 
 * avec la table proteins en relation n-n via  prot_name_2_prot
 ************************************************************************
 */
CREATE TABLE protein_names (prot_name_id INT,
                            prot_name VARCHAR2(300), 
                            name_kind VARCHAR2(20), 
                            name_type VARCHAR2(20), 
                            CONSTRAINT pk_name_prot PRIMARY KEY (prot_name_id),
                            CONSTRAINT unique_p_name unique (prot_name, name_kind, name_type),
                            CONSTRAINT check_name_type CHECK (name_type IN ('fullName', 'shortName', 'ecNumber')),
                            CONSTRAINT check_name_kind CHECK (name_kind IN ('alternativeName', 'recommendedName', 'submittedName'))
                           );

/* Sequence pour id automatique noms de proteines */
CREATE SEQUENCE seq_prot_names START WITH 1 INCREMENT BY 1;


/************************************************************************
 * Table prot_name_2_prot : lien N-N entre proteines & noms de proteines
 ************************************************************************
 */
CREATE TABLE prot_name_2_prot(
                           accession VARCHAR (10),
                           prot_name_id INTEGER,
                           CONSTRAINT pk_prot_name_2_prot PRIMARY KEY(accession,prot_name_id),
                           CONSTRAINT fk_prot FOREIGN KEY(accession) REFERENCES proteins(accession),
                           CONSTRAINT fk_prot_name FOREIGN KEY(prot_name_id) REFERENCES protein_names(prot_name_id));

/************************************************************************
 * Table gene_names : Noms de genes / id automatique pour lien 
 * avec la table entries en relation n-n via  gene_name_2_entry
 ************************************************************************
 */
CREATE TABLE gene_names (gene_name_id INT, 
                            gene_name VARCHAR2(300), 
                            name_type VARCHAR2(100), 
                            CONSTRAINT pk_name_gene PRIMARY KEY (gene_name_id),
                            CONSTRAINT unique_gene_name UNIQUE (gene_name, name_type),
                            CONSTRAINT ck_type_gene CHECK (name_type IN ('primary', 'synonym', 'ordered locus', 'ORF'))
                        );

/* Sequence pour id automatique noms de genes */
CREATE SEQUENCE seq_gene_names START WITH 1 INCREMENT BY 1;


/************************************************************************
 * Table entry_2_gene_name : lien N-N entre entr�es & noms de genes
 ************************************************************************
 */
CREATE TABLE entry_2_gene_name(
                           accession VARCHAR (10),
                           gene_name_id INTEGER,
                           CONSTRAINT pk_entry_2_gene_name PRIMARY KEY(accession,gene_name_id),
                           CONSTRAINT fk_gname_entry FOREIGN KEY(accession) REFERENCES entries(accession),
                           CONSTRAINT fk_gene_name FOREIGN KEY(gene_name_id) REFERENCES gene_names(gene_name_id));




/************************************************************************
 * Table comments : lien 1-N entre entr�es & commentaires
 ************************************************************************
 */
CREATE TABLE comments (     comment_id INTEGER,
                            accession VARCHAR2(10),
                            type_c VARCHAR2(100),
                            txt_c VARCHAR2(4000),
                            CONSTRAINT pk_comments PRIMARY KEY (comment_id),
                            CONSTRAINT ck_comments_acc_nn CHECK (accession IS NOT NULL),
                            CONSTRAINT fk_comment_entry FOREIGN KEY (accession) REFERENCES entries(accession),
                            CONSTRAINT ck_comment_type CHECK (type_c in ('disease', 'function'))
                           );
                           

/* Sequence pour id automatique noms de genes */
CREATE SEQUENCE seq_comment_id START WITH 1 INCREMENT BY 1;

/************************************************************************
 * Table dbref : références associées à la fiche dans la base GO
 ************************************************************************
 */                   
CREATE TABLE dbref (
                    accession  VARCHAR2(10),
                    db_type VARCHAR2(10),
                    db_ref VARCHAR2(20),
                    CONSTRAINT pk_dbref PRIMARY KEY (accession, db_type, db_ref),
                    CONSTRAINT fk_debref_entries FOREIGN KEY (accession) REFERENCES entries(accession)
                    );

/************************************************************************
 * Table keywords : table de r�f�rences des mots cles
 ************************************************************************
 */
 CREATE TABLE keywords (kw_id VARCHAR2(20),
                            kw_label VARCHAR2(100),
                            CONSTRAINT pk_keywords PRIMARY KEY (kw_id),
                            CONSTRAINT ck_kw_label_nn CHECK (kw_label IS NOT NULL)
                        );
                        
 /************************************************************************
 * Table keywords : table de r�f�rences des mots cles
 ************************************************************************
 */
CREATE TABLE entries_2_keywords (accession VARCHAR2(10),
                                    kw_id VARCHAR2(20),
                                    CONSTRAINT pk_entries_2_keywords PRIMARY KEY (accession, kw_id),
                                    CONSTRAINT fk_e2k_entries FOREIGN KEY (accession) REFERENCES entries(accession),
                                    CONSTRAINT fk_e2k_keywords FOREIGN KEY (kw_id) REFERENCES keywords(kw_id)
                                );

COMMIT;