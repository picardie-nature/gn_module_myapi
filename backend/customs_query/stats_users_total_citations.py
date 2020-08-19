from . import CustomQuery

class MyQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
          SELECT
                *
        FROM shared.stats_users_total_citations ORDER BY year, n_users;
        """
        
        self.help="""
            Statistiques annuelles de la base
        """
    
_qr = MyQuery
