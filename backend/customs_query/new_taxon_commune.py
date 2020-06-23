"""
Flux RSS permettant de publier une entrée dès qu'un nouveau taxon est découvert sur un territoire (simple ou composé).
Exemple : https://geonature.clicnat.fr/api/myapi/rss/new_taxon_commune/?area=80730,80001
TODO ajouter la possiblité de filter les taxons
"""
from . import CustomQuery
from datetime import datetime as dt


class MyCustomQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
                 WITH a AS(
SELECT DISTINCT ON (tx.cd_nom)
	tx.lb_nom,
	tx.cd_nom,
	s.date_min AS date_decouverte,
	s.id_synthese,
	COALESCE(s.meta_create_date,'2009-01-01') AS date_publish
    FROM gn_synthese.synthese s
    JOIN taxonomie.taxref tx ON tx.cd_nom = taxonomie.find_cdref_sp(s.cd_nom)
    JOIN gn_synthese.cor_area_synthese cas ON cas.id_synthese = s.id_synthese 
    JOIN ref_geo.l_areas ar ON ar.id_area = cas.id_area 
    WHERE 
        s.date_min >= now()-'2 years'::interval
        AND ar.area_code IN :area 
        AND EXISTS (SELECT cd_nom FROM taxonomie.find_all_taxons_parents(tx.cd_nom) WHERE cd_nom IN :cd_nom )
    ORDER BY tx.cd_nom, COALESCE(s.meta_create_date,'2009-01-01') ASC
    )
    SELECT 
    s.unique_id_sinp,
    s.date_min AS date_obs,
    s.meta_create_date AS pub_date,
    string_agg(ar.area_name,',') AS commune ,
    s.observers,
    tx.lb_nom,
    tx.cd_nom,
    (SELECT lb_nom FROM taxonomie.taxref WHERE cd_nom=taxonomie.find_parent(tx.cd_nom,'FM')) AS famille,
    (SELECT string_agg(area_name,',') FROM ref_geo.l_areas WHERE area_code IN :area ) AS ref_area
    FROM a
    JOIN gn_synthese.synthese s ON a.id_synthese=s.id_synthese 
    JOIN taxonomie.taxref tx ON tx.cd_nom = a.cd_nom
    JOIN gn_synthese.cor_area_synthese cas ON cas.id_synthese = a.id_synthese 
    JOIN ref_geo.l_areas ar ON ar.id_area = cas.id_area AND ar.id_type = 25
    WHERE s.meta_create_date IS NOT null
    GROUP BY s.id_synthese , tx.cd_nom 
    ORDER BY s.meta_create_date DESC 
    LIMIT 50
        """
    def arg_process(self, x):
        x.update({'area': tuple(x['area'].split(',')) })
        x.update({'cd_nom': tuple(x.get('cd_nom','183716').split(',')) })
        return x

    def result_process(self, x):
        for i,e in enumerate(x) :
            description="""<p><a href='https://clicnat.fr/espece/{}'><i>{}</i></a> (<i>{}</i>) observé le {} par {}. </p>
                <p>Commune de {}.</p> <p>Il s'agit d'une nouvelle espèce pour le territoire de {}.</p>""".format(e['cd_nom'], e['lb_nom'], e['famille'], e['date_obs'].strftime('%d/%m/%Y'), e['observers'], e['commune'],e['ref_area'])
            title="<i>{}</i> observé le {}".format(e['lb_nom'], e['date_obs'].strftime('%d/%m/%Y') ),
            x[i].update(dict(
                unique_id_sinp=str(e['unique_id_sinp']),
                date_obs=str(e['date_obs']),
                title="{} observé le {}".format(e['lb_nom'],e['date_obs'].strftime('%d/%m/%Y') ),
                description=description,
                link='https://clicnat.fr'
            ))
        return x

_qr = MyCustomQuery()

