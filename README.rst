Fonctionnalités
===============

Mettre en place rapidement et simplement une API à partir d'une requête SQL. Utile pour les échanges de données.
Il suffit pour cela de dupliquer, renomer, et éditer le modèle fourni.
Par choix, le module n'utilise pas l'ORM SQLAlchemy. Le but est de permettre à des administrateurs de base de données GeoNature de mettre en place rapidement une API.

Fonctionnalités
===============

* Ecriture en SQL (*SELECT cd_nom,count(id_synthese) FROM gn_synthese.synthese group by cd_nom ORDER BY count(id_synthese) DESC LIMIT :limit*)
* Définire des paramètres obligatoires ou facultatifs (*?limit=40&cd_nom=123*)
* Possibilité d'ajouter un script python pour modifier la sortie de la requête
* Possibilité d'ajouter des tokens pour limiter l'accès (*?token=maclesupersecrete*)

 exemple de requete : ..geonature/api/myapi/masuperrequetedelamort/?token=clesecrete&param1=toto&param2=tata


Limitations
===========

* Attention de ne pas écrire de reqûetes trop longues à executer : risque de timeout (ajoutez des indexes ou des vues matérialisés si besoin, ou imposez une limite)
* Sortie en JSON uniquement
* La modification d'une API nécessite le redemarrage de geonature ``sudo supervisorctl restart geonature2``

Valeurs modifiables
===================
* ``self.sql_text`` <string>: La requête à exécuter, les paramètres sont ajoutés dans la requête comme ``:nomDuParametre``
* ``self.tokens`` <[string]>(optionnel) Une liste de chaines de caractères à utiliser pour sécuriser l'API
* ``self.args_default`` <{}> (optionnel) Un dictionnaire comportant les valeurs par défaut pour les paramètres optionnels
* ``self.result_process(x)`` (optionnel) Une fonction qui modifie le résultats de la requête (doit retourner une liste ou un dictionnaire). Par exemple pour ajouter des métadonnées.
* ``self.arg_process(x)`` (optionnel) Une fonction qui modifie ou ajoute des paramètres avant execution de la requête (doit retourner une liste)

Les scripts doivent être ajouté dans le dossier ``customs_query``. Le plus simple est de partir d'un exemple existant. Le nom du fichier sera le nom pour accéder à l'API. *../geonature/api/myapi/NOMDUFICHIER/?token=clesecrete&param1=toto&param2=tata*
