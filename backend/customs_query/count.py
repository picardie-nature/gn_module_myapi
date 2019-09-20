from . import CustomQuery

class MyCountQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = "SELECT * FROM gn_commons.t_modules LIMIT :limit"
        self.tokens = ['supersecret']
        self.args_default = {'limit':5}
    
    def result_process(self, x):
        x.append('abc')
        return x

    def arg_process(self, x):
        x.update({'unArgumentEnPlus': 4 })
        return x

_qr = MyCountQuery()



