"""
Flux RSS permettant de publier une entrée dès qu'un nouveau taxon est découvert sur un territoire (simple ou composé).
Exemple : https://geonature.clicnat.fr/api/myapi/rss/new_taxon_territory/?area=80730,80001
"""
from . import CustomQuery
from datetime import datetime as dt

from jinja2 import Template

class MyCustomQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.args_default=dict(cd_nom='183716') #Animalia par defaut
        self.rss_channel_info.update(dict(title='Clicnat - Nouvelles observations', link='https://clicnat.fr', description="Ce flux permet de recevoir les dernières observations saisies en base. Il est possible de filter les taxons concernés avec le paramètre ""cd_nom""." ))
        self.sql_text = """
                    SELECT 
    s.unique_id_sinp,
    s.date_min AS date_obs,
    s.meta_create_date AS pub_date,
    string_agg(ar.area_name,',') AS commune ,
    string_agg(ar.area_code,',') AS commune_code ,
    s.observers,
    tx.lb_nom,
    tx.cd_nom,
    (SELECT lb_nom FROM taxonomie.taxref WHERE cd_nom=taxonomie.find_parent(tx.cd_nom,'CL')) AS classe,
    (SELECT lb_nom FROM taxonomie.taxref WHERE cd_nom=taxonomie.find_parent(tx.cd_nom,'OR')) AS ordre,
    (SELECT lb_nom FROM taxonomie.taxref WHERE cd_nom=taxonomie.find_parent(tx.cd_nom,'FM')) AS famille,
    id_media
	FROM gn_synthese.synthese s 
    JOIN taxonomie.taxref tx ON tx.cd_nom = taxonomie.find_cdref_sp(s.cd_nom)
    LEFT JOIN gn_synthese.cor_area_synthese cas ON cas.id_synthese = s.id_synthese 
    LEFT JOIN ref_geo.l_areas ar ON ar.id_area = cas.id_area AND ar.id_type = 25
    LEFT JOIN taxonomie.t_medias media ON media.cd_ref=tx.cd_nom AND media.id_type=1
    WHERE 
    	EXISTS (SELECT cd_nom FROM taxonomie.find_all_taxons_parents(tx.cd_nom) WHERE cd_nom IN  :cd_nom)
    	 AND s.meta_create_date >= now()-'3 month'::INTERVAL AND s.meta_create_date IS NOT null 
        AND tx.cd_nom NOT IN (SELECT cd_ref FROM gn_sensitivity.t_sensitivity_rules_cd_ref )
    GROUP BY s.id_synthese , tx.cd_nom, media.id_media 
    ORDER BY s.meta_create_date DESC 
    LIMIT 150
        """
       
    def arg_process(self, x):
        x.update({'cd_nom': self.tuplize(x['cd_nom'] )   })
        return x

    def result_process(self, x): #TODO utilser les tempates jinja
        for i,e in enumerate(x) :
            template_description=Template(
                """<p><a href='https://clicnat.fr/espece/{{ cd_nom }}'><i>{{ lb_nom }}</i></a> (<i>{{ fm }}</i>) observé le {{date_obs}} par {{observers}}. </p> 
                {% if commune_name is not none %}<p>Commune de <a href="https://clicnat.fr/territoire/{{commune_code}}">{{commune_name}}</a> ({{commune_code}}).</p>{% endif %}
                <table>
                    <tr><td>Classe</td><td><i>{{cl}}</i></td></tr>
                    <tr><td>Ordre</td><td><i>{{ordre}}</i></td></tr>
                    <tr><td>Famille</td><td><i>{{fm}}</i></td></tr>
                </table>
                <p><small>Observation saisie le : {{pubDate}}</small></p>
                {% if id_media is not none %}<img src="https://taxhub.clicnat.fr/api/tmedias/thumbnail/{{id_media}}?h=200">{% endif %}
                """
            )
            description=template_description.render( 
                cd_nom=e['cd_nom'], lb_nom=e['lb_nom'], cl=e['classe'], ordre=e['ordre'], fm=e['famille'], date_obs=e['date_obs'].strftime('%d/%m/%Y'), observers=e['observers'], id_media=e['id_media'], commune_name=e['commune'], commune_code=e['commune_code'], pubDate=e['pub_date'].strftime('%d/%m/%Y')
            )
            
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

