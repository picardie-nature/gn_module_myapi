from . import CustomQuery

class MyQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
          SELECT
                interv::text, n_login, n_saisisseur
        FROM shared.stats_users_activity ;
        """
        
        self.help="""
            Utilisateurs loguée sur clicnat
        """
    
_qr = MyQuery
