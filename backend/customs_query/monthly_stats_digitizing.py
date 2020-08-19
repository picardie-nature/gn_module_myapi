from . import CustomQuery

class MyQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
           SELECT to_char(create_date,'YYYY-MM-DD') AS create_date, n_occurences , n_digitisers, n_observers 
FROM shared.monthly_stats_digitizing ORDER BY create_date ASC  """
        
        self.args_default = {'cd_nom':186206} #Mammalia
        self.help="""
            Statistiques mensuelles concernant la saisie sur Clicnat (données d'import non inclues)
        """
    
_qr = MyQuery
