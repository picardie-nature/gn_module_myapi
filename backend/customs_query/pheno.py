from . import CustomQuery

class MyQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        #ajouter un "mode hiver", qui place le début de l'année le 1er juillet
        self.sql_text = """
           SELECT 
                tx.cd_nom,
                tx.lb_nom,
                min(EXTRACT(DOY FROM date_min)) AS "min",
            	percentile_cont(0.01) WITHIN GROUP ( ORDER BY (  EXTRACT(DOY FROM date_min) ) ) AS "low",
		        percentile_cont(0.25) WITHIN GROUP ( ORDER BY (EXTRACT(DOY FROM date_min ) ) ) AS q1,
		        percentile_cont(0.5) WITHIN GROUP ( ORDER BY (EXTRACT(DOY FROM date_min  ) ) ) AS q2,
                percentile_cont(0.75) WITHIN GROUP ( ORDER BY (EXTRACT(DOY FROM date_min ) ) ) AS q3,
                percentile_cont(0.99) WITHIN GROUP ( ORDER BY (EXTRACT(DOY FROM date_min ) ) ) AS "high",
                max(EXTRACT(DOY FROM date_min)) AS "max",
                array_agg(DISTINCT EXTRACT(DOY FROM date_min::date)::int ORDER BY EXTRACT(DOY FROM date_min::date)::int ) as doy
            FROM gn_synthese.synthese_usable s
            JOIN taxonomie.taxref tx ON tx.cd_nom = taxonomie.find_cdref_sp(s.cd_nom)
            WHERE 
                tx.cd_nom IN (SELECT cd_nom FROM taxonomie.find_all_taxons_children((:cd_nom)::int))
                AND date_min=date_max AND date_min >=now()-'10 years'::interval
            GROUP BY tx.cd_nom
           ORDER BY percentile_cont(0.5) WITHIN GROUP ( ORDER BY (EXTRACT(DOY FROM date_min  ) ) )
        LIMIT 500; """
        
        self.args_default = {'cd_nom':186206} #Mammalia
        self.help="""
            Renvoi la phénologie des espèces pour dessiner des boites à moustaches [0.05,0.25,0.5,0.75,0.95]
        """
    
_qr = MyQuery
