from . import CustomQuery

class MyQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
          SELECT
                *
        FROM shared.annual_stats ;
        """
        
        self.help="""
            Statistiques annuelles de la base
        """
    
_qr = MyQuery
