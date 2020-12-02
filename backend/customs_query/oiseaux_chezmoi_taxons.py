from . import CustomQuery

class MyQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
          SELECT
            t.cd_nom AS cd_ref,
            t.lb_nom AS lb_nom,
            t.nom_vern AS nom_vern,
            count(DISTINCT unique_id_sinp) AS nb_obs,
            count(DISTINCT unique_id_sinp) FILTER (WHERE now() - odcm.date_obs <='7 days' ) AS nb_obs_7_days,
            count(DISTINCT unique_id_sinp) FILTER (WHERE now() - odcm.date_obs BETWEEN '7 days' AND '14 days' ) AS nb_obs_prev_7_days,
            (array_agg(tm.id_media ORDER BY id_type) )[1] AS id_media
            FROM shared.oiseaux_de_chez_moi odcm
            JOIN taxonomie.taxref_cdref_sp tcs ON tcs.cd_nom = odcm.cd_ref
            JOIN taxonomie.taxref t ON t.cd_nom = tcs.cd_ref_sp 
            LEFT JOIN taxonomie.t_medias tm ON t.cd_nom = tm.cd_ref 
           GROUP BY t.cd_nom
            """
        
        self.help="""
           Pour tableau et camenbert
        """
    
_qr = MyQuery
