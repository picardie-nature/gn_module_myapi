from . import CustomQuery

class MyQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
            select json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(ST_AsGeoJSON(t.*, maxdecimaldigits:=7)::json)
                )
            from (
	            SELECT 
		            la.area_code as insee_com, la.area_name as nom_com,
		            count(DISTINCT odcm.cd_ref) AS nb_especes,
		            max(date_obs) AS date_last_obs,
		            st_transform(la.geom,4326) AS geom
	            FROM shared.oiseaux_de_chez_moi odcm
	            JOIN ref_geo.l_areas la ON id_type=25 AND area_code = insee_com
	            GROUP BY la.id_area 
            ) AS t
            """
        
        self.help="""
           Pour carto
        """
        
    def result_process(self, x):
        return x[0].get('json_build_object')
    
_qr = MyQuery
