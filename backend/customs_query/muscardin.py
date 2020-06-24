from . import CustomQuery
from datetime import datetime as dt


class MyCustomQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
                  SELECT 
	                s.unique_id_sinp,
	                s.date_min,
	                s.observers,
	                s.meta_create_date AS pub_date,
	                'Muscardin observé le '||to_char(s.date_min,'DD/MM/YYYY') AS title,
	                'Sur la commune de '||string_agg(ar.area_name||'('||ar.area_code||')' ,', ') AS description
                FROM gn_synthese.synthese s
                --JOIN gn_synthese.synthese_usable su ON su.id_synthese =s.id_synthese
                LEFT JOIN gn_synthese.cor_area_synthese cas ON cas.id_synthese = s.id_synthese 
                LEFT JOIN ref_geo.l_areas ar ON ar.id_area = cas.id_area AND ar.id_type =25
                WHERE s.cd_nom=taxonomie.find_cdref_sp(61636) --filter invalides et No
                GROUP BY s.id_synthese 
                ORDER BY s.meta_create_date DESC NULLS LAST
                LIMIT 20
        """

    def result_process(self, x):
        for i,e in enumerate(x) :
            x[i].update(dict(
                #description='Ceci est une description ajoute',
                unique_id_sinp=str(e['unique_id_sinp']),
                date_min=str(e['date_min']),
                pub_date=str(e['pub_date'])
            ))
        return x

_qr = MyCustomQuery

