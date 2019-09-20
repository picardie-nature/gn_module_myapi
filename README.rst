Fonctionnalités
===============

Mettre en place rapidement et simplement une API à partir d'une requête SQL. Utile pour les échanges de données.
Il suffit pour cela de dupliquer, renomer, et éditer le modèle fourni.
Par choix, le module n'utilise pas l'ORM SQLAlchemy. Le but est de permettre à des administrateurs de base de données GeoNature de mettre en place rapidement une API.

Fonctionnalités
===============

* Ecriture en SQL (SELECT cd_nom,count(*) FROM gn_synthese.synthese group by cd_nom ORDER BY count(*) DESC LIMIT :limit;
)
* Définire des paramètres obligatoires ou facultatifs (*?limit=40&cd_nom=123*)
* Possibilité d'ajouter un script python pour modifier la sortie de la requête
* Possibilité d'ajouter des tokens pour limiter l'accès (*?token=maclesupersecrete*)

Limitations
===========

* Une erreur de syntaxe sur un script fait planter l'ensemble du module 
* Attention de ne pas écrire de reqûetes trop longues à executé (ajoutez des indexes ou des vues matérialisés si besoin, ou imposez une limite)

Valeurs modifiables
==================
* ``self.sql_text`` <string>: La requête à exécuter, les paramètres sont ajoutés dans la requête comme ``:nomduparameter``
* ``self.tokens`` <[string]>(optionnel) Une liste de chaines de caractères à utiliser pour sécuriser l'API
* ``self.args_default`` <{}> (optionnel) Un dictionnaire comportant les valeurs par défaut pour les paramètres optionnels
 ``self.result_process(x)`` (optionnel) Une fonction qui modifie le résultats de la requête (doit retourner une liste ou un dictionnaire)
 ``self.arg_process(x)`` (optionnel) Une fonction qui modifie les paramètres avant execution de la requête (doit retourner une liste)
