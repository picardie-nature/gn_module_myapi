from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


from geonature.utils.env import DB
class CustomQuery(object) :
    def __init__(self):
        self.sql_text="SELECT * FROM gn_commons.t_modules"
        self.arg=dict()
        self.tokens=list()
        self.args_default=dict()
        self.rss_channel_info=dict(title='Geonature Flux', description='Flux fourni par GeoNature')
    
    def _make_query(self):
        r=DB.session.execute(self.sql_text,self.arg_process(self.arg))
        return [dict(row) for row in r]
    
    def execute(self):
        return self.result_process(x=self._make_query())
    
    def result_process(self,x): #surcoucheable, doit retourner une liste ou un dict
        return x

    def arg_process(self,x): #surcoucheable, doit retourner une liste ou un dict
        return x

    def set_args(self,a):
        self.arg=a

    def is_allowed(self, t):
        if len(self.tokens) == 0 or t in self.tokens :
            return True
        return False

    def tuplize(self,var):
        if type(var) is tuple:
            return var
        return tuple(var.split(','))
