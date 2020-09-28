"""
Flux RSS permettant de publier une entrée dès qu'un nouveau taxon est découvert sur un territoire (simple ou composé).
Exemple : https://geonature.clicnat.fr/api/myapi/rss/new_taxon_territory/?area=80730,80001
"""
from . import CustomQuery
from datetime import datetime as dt

from geonature.core.ref_geo.models import LAreas

from jinja2 import Template

class MyCustomQuery(CustomQuery) :
    def __init__(self,opt, **kwargs):
        super().__init__()
        area_code = opt or '80021' #Amiens par defaut (?)
        self.args_default=dict(area = area_code) #Amiens par defaut (?)
        ar=LAreas.query.filter_by(area_code=area_code).first()
        self.rss_channel_info.update(dict(title='Territoire de {}'.format(ar.area_name), link='https://clicnat.fr', description="Flux permettant de recevoir les observations d'un territoire" )) #TODO ajouter le nom du territoire dans le titre
        self.sql_text = """
                 SELECT * FROM(
    SELECT DISTINCT ON (s.unique_id_sinp)
    s.unique_id_sinp,
    min(date_min) OVER (PARTITION BY tx.cd_nom, ar.id_area) AS date_first_obs,
    max(date_max) OVER (PARTITION BY tx.cd_nom, ar.id_area ORDER BY date_max ROWS UNBOUNDED PRECEDING EXCLUDE CURRENT ROW) AS date_previous_obs,
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
	JOIN taxonomie.taxref_cdref_sp sp ON sp.cd_nom = s.cd_nom 
    JOIN taxonomie.taxref tx ON tx.cd_nom = sp.cd_ref_sp
    JOIN gn_synthese.cor_area_synthese cas ON cas.id_synthese = s.id_synthese 
    JOIN ref_geo.l_areas ar ON ar.id_area = cas.id_area 
    LEFT JOIN taxonomie.t_medias media ON media.cd_ref=tx.cd_nom AND media.id_type=1
    WHERE 
    	ar.area_code = :area
    	 /*AND s.meta_create_date >= now()-'15 days'::INTERVAL*/ AND s.meta_create_date IS NOT null 
        AND tx.cd_nom NOT IN (SELECT cd_ref FROM gn_sensitivity.t_sensitivity_rules_cd_ref )
    ORDER BY s.unique_id_sinp
    LIMIT 150
) AS a ORDER BY pub_date DESC;
        """

    def result_process(self, x):
        for i,e in enumerate(x) :
            template_description=Template(
                """<p><a href='https://clicnat.fr/espece/{{ cd_nom }}'><i>{{ lb_nom }}</i></a> observé le {{date_obs.strftime('%d/%m/%Y')}} par {{observers}}. </p> 
                <p> Localisation : <a href="https://clicnat.fr/territoire/{{epci_code}}">{{epci_name}}</a> > <a href="https://clicnat.fr/territoire/{{commune_code}}">{{commune_name}}</a> ({{commune_code}})</p>
                <p>{% if date_first_obs == date_obs %} <b>Il s'agit d'un nouveau taxon pour le territoire ! </b>
                    {% elif date_previous_obs %} Le taxon avait déjà été observé sur le territoire le {{ date_previous_obs.strftime('%d/%m/%Y') }}.
                {% endif %}</p>
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
            title="<i>{}</i> observé le {}".format(e['lb_nom'], e['date_obs'].strftime('%d/%m/%Y') ),
            x[i].update(dict(
                unique_id_sinp=str(e['unique_id_sinp']),
                date_obs=str(e['date_obs']),
                title="{} observé le {}".format(e['lb_nom'],e['date_obs'].strftime('%d/%m/%Y') ),
                description=description,
                link='https://clicnat.fr'
            ))
        return x

_qr = MyCustomQuery

