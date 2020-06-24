from . import CustomQuery

class MyQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
          SELECT
	        "year"::int,
	        obs_created::int,obs_observed::int,new_sp_created::int,new_sp_observed::int,
	        (sum(obs_created ) OVER (ORDER BY "year"))::int AS obs_created_cumul,
	        (sum(obs_observed ) OVER (ORDER BY "year"))::int AS obs_observed_cumul,
	        (sum(new_sp_created ) OVER (ORDER BY "year"))::int AS new_sp_created_cumul,
	        (sum(new_sp_observed ) OVER (ORDER BY "year"))::int AS new_sp_created_cumul
        FROM shared.annual_stats 
        ORDER BY "year";
        """
        
        self.help="""
            Statistiques annuelles de la base
        """
    
_qr = MyQuery
