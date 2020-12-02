from . import CustomQuery

class MyQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
                 SELECT DISTINCT ON (date_obs)
	            date_obs::text,
	            (SELECT COUNT(DISTINCT cd_ref) FROM shared.oiseaux_de_chez_moi odcm2 WHERE odcm2.date_obs <=odcm.date_obs ) AS nb_taxon,
	            (SELECT COUNT(DISTINCT insee_com) FROM shared.oiseaux_de_chez_moi odcm2 WHERE odcm2.date_obs <=odcm.date_obs ) AS nb_commune,
	            count(*) OVER (ORDER BY date_obs ASC) AS nb_obs
            FROM shared.oiseaux_de_chez_moi odcm 
            ORDER BY date_obs 
            """
        
        self.help="""
           Pour graphique
        """
    
_qr = MyQuery
