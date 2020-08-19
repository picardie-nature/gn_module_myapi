from . import CustomQuery

class MyCountQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = "SELECT module_code FROM gn_commons.t_modules LIMIT :limit"
        self.args_default = {'limit':5}
    
    def result_process(self, x):
        x.append({'module_code':'MODULE FICTIF AJOUTE'})
        return x

    def arg_process(self, x):
        x.update({'unArgumentEnPlus': 4 })
        return x

_qr = MyCountQuery



