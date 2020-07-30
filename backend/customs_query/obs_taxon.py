"""
Flux RSS permettant de publier une entrée dès qu'un nouveau taxon est découvert sur un territoire (simple ou composé).
Exemple : https://geonature.clicnat.fr/api/myapi/rss/new_taxon_territory/?area=80730,80001
"""
from . import CustomQuery
from datetime import datetime as dt

from jinja2 import Template

from geonature.core.taxonomie.models import Taxref

class MyCustomQuery(CustomQuery) :
    def __init__(self,opt=None,**kwargs):
        super().__init__()
        cd_nom=opt or '183716'
        self.args_default=dict(cd_nom = cd_nom) #Animalia par defaut
        tx=Taxref.query.filter_by(cd_nom=cd_nom).first()
        self.rss_channel_info.update(dict(title='Observation de {}'.format(tx.lb_nom), link='https://clicnat.fr', description="Flux permettant de recevoir les observations d'un taxon" ))
        self.sql_text = """
    SELECT * FROM (
                    SELECT 
    s.unique_id_sinp,
    s.date_min AS date_obs,
    s.meta_create_date AS pub_date,
    (SELECT area_name FROM ref_geo.l_areas JOIN gn_synthese.cor_area_synthese USING (id_area) WHERE id_synthese=s.id_synthese AND id_type=25 LIMIT 1) AS commune_name ,
    (SELECT area_code FROM ref_geo.l_areas JOIN gn_synthese.cor_area_synthese USING (id_area) WHERE id_synthese=s.id_synthese AND id_type=25 LIMIT 1) AS commune_code ,
    (SELECT area_name FROM ref_geo.l_areas JOIN gn_synthese.cor_area_synthese USING (id_area) WHERE id_synthese=s.id_synthese AND id_type=36 LIMIT 1) AS epci_name ,
    (SELECT area_code FROM ref_geo.l_areas JOIN gn_synthese.cor_area_synthese USING (id_area) WHERE id_synthese=s.id_synthese AND id_type=36 LIMIT 1) AS epci_code ,
    s.observers,
    tx.lb_nom,
    tx.cd_nom,
    (SELECT lb_nom FROM taxonomie.taxref WHERE cd_nom=taxonomie.find_parent(tx.cd_nom,'CL')) AS classe,
    (SELECT lb_nom FROM taxonomie.taxref WHERE cd_nom=taxonomie.find_parent(tx.cd_nom,'OR')) AS ordre,
    (SELECT lb_nom FROM taxonomie.taxref WHERE cd_nom=taxonomie.find_parent(tx.cd_nom,'FM')) AS famille,
    id_media
	FROM gn_synthese.synthese s 
    JOIN taxonomie.taxref tx ON tx.cd_nom = taxonomie.find_cdref_sp(s.cd_nom)
    LEFT JOIN taxonomie.t_medias media ON media.cd_ref=tx.cd_nom AND media.id_type=1
    WHERE 
    	EXISTS (SELECT cd_nom FROM taxonomie.find_all_taxons_parents(tx.cd_nom) WHERE cd_nom = :cd_nom)
    	 AND s.meta_create_date >= now()-'15 days'::INTERVAL AND s.meta_create_date IS NOT null 
        AND tx.cd_nom NOT IN (SELECT cd_ref FROM gn_sensitivity.t_sensitivity_rules_cd_ref )
    GROUP BY s.id_synthese , tx.cd_nom, media.id_media 
    ORDER BY s.meta_create_date DESC 
    LIMIT 150
    ) as a ORDER BY pub_date DESC
        """

    def result_process(self, x): #TODO utilser les tempates jinja
        for i,e in enumerate(x) :
            template_description=Template(
                """<p><a href='https://clicnat.fr/espece/{{ cd_nom }}'><i>{{ lb_nom }}</i></a> observé le {{ date_obs.strftime('%d/%m/%Y') }} par {{observers}}. </p> 
                    <p> Localisation : <a href="https://clicnat.fr/territoire/{{epci_code}}">{{epci_name}}</a> > <a href="https://clicnat.fr/territoire/{{commune_code}}">{{commune_name}}</a> ({{commune_code}})</p>
                <table>
                    <tr><td>Classe</td><td><i>{{classe}}</i></td></tr>
                    <tr><td>Ordre</td><td><i>{{ordre}}</i></td></tr>
                    <tr><td>Famille</td><td><i>{{famille}}</i></td></tr>
                </table>
                <p><small>Observation saisie le : {{pub_date}}</small></p>
                {% if id_media is not none %}<img src="https://taxhub.clicnat.fr/api/tmedias/thumbnail/{{id_media}}?h=200">{% endif %}
                """
            )
            description=template_description.render(**e)            

            title="<i>{}</i> observé le {}".format(e['lb_nom'], e['date_obs'].strftime('%d/%m/%Y') )
            x[i].update(dict(
                unique_id_sinp=str(e['unique_id_sinp']),
                pub_date=e['pub_date'],
                title="{} observé le {}".format(e['lb_nom'],e['date_obs'].strftime('%d/%m/%Y') ),
                description=description,
                link='https://clicnat.fr/espece/{}'.format(e['cd_nom'])
            ))
        return x

_qr = MyCustomQuery

