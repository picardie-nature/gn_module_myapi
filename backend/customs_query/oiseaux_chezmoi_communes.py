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
                WITH b AS (
              SELECT insee_com, jsonb_agg(taxons ORDER BY nom_vern) AS taxons FROM 
             ( SELECT DISTINCT ON(t.cd_ref,odcm.insee_com) odcm.insee_com , t.lb_nom,t.nom_vern, json_build_object('cd_ref',t.cd_ref, 'lb_nom',t.lb_nom, 'nom_vern', t.nom_vern) AS taxons
                	FROM shared.oiseaux_de_chez_moi odcm
                	JOIN taxonomie.taxref_cdref_sp tcs ON tcs.cd_nom = odcm.cd_ref 
                	JOIN taxonomie.taxref t ON t.cd_nom = tcs.cd_ref_sp
	             ) x
              GROUP BY insee_com ) 
              SELECT 
                    la.area_code as insee_com, la.area_name as nom_com,
                    count(DISTINCT odcm.cd_ref) AS nb_especes,
                    b.taxons AS taxons,
                    max(date_obs) AS date_last_obs,
                    st_transform(la.geom,4326) AS geom
                FROM shared.oiseaux_de_chez_moi odcm
                JOIN ref_geo.l_areas la ON id_type=25 AND area_code = insee_com
                JOIN taxonomie.taxref_cdref_sp tcs ON tcs.cd_nom = odcm.cd_ref 
                JOIN taxonomie.taxref t ON t.cd_nom = tcs.cd_ref_sp
                JOIN b ON b.insee_com=odcm.insee_com 
                GROUP BY la.id_area, b.taxons
            ) AS t
            """
        
        self.help="""
           Pour carto
        """
        
    def result_process(self, x):
        return x[0].get('json_build_object')
    
_qr = MyQuery
