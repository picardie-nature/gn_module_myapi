"""
Dates d'observations pour appli js https://cal-heatmap.com/
Ajouter les paramètres {{t:start}} et {{t:end}} ( https://cal-heatmap.com/#data )
"""
from . import CustomQuery

class MyQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        #ajouter un "mode hiver", qui place le début de l'année le 1er juillet
        self.sql_text = """
            SELECT
	            date_min::date::text AS "timestamp",
	            count(*) AS value
            FROM gn_synthese.synthese_usable 
            JOIN taxonomie.taxref_cdref_sp sp USING (cd_nom)

            WHERE sp.cd_ref_sp=:cd_nom
                 AND date_max::date = date_min::date
	           AND date_min BETWEEN :start AND :end
            GROUP BY date_min::date"""
        
        self.help="""
            Dates d'observations pour appli js https://cal-heatmap.com/
        """
    
_qr = MyQuery
