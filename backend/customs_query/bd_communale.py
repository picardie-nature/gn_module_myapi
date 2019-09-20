from . import CustomQuery

class MyCountQuery(CustomQuery) :
    def __init__(self):
        super().__init__()
        self.sql_text = """
        SELECT 
                CASE WHEN
             		sens.cd_ref IS NOT NULL THEN '0'
             	ELSE taxref.cd_ref END as cd_ref,
                 max(date_part('year',s.date_max)) AS last_obs, 
                 bool_or(CASE WHEN id_nomenclature_valid_status IN (get_id_nomenclature('STATUT_VALID','1'),get_id_nomenclature('STATUT_VALID','2')) THEN TRUE ELSE FALSE END) AS "valid"
            FROM gn_synthese.synthese s
            JOIN taxonomie.taxref taxref ON taxref.cd_nom=s.cd_nom
            LEFT JOIN gn_sensitivity.t_sensitivity_rules_cd_ref sens ON sens.cd_ref = taxref.cd_ref
            JOIN gn_synthese.cor_area_synthese cas ON s.id_synthese=cas.id_synthese
            JOIN ref_geo.l_areas a ON a.id_area=cas.id_area
            JOIN ref_geo.li_municipalities m ON m.id_area=a.id_area
            WHERE 
                m.insee_com = :insee_com
                AND id_nomenclature_valid_status NOT IN (get_id_nomenclature('STATUT_VALID','3'),get_id_nomenclature('STATUT_VALID','4'))
            GROUP BY taxref.cd_ref,sens.cd_ref;"""
        self.tokens = ['nffRL49S9','kC3Xa7wT3']
    
    def result_process(self, x):
        x.append('abc')
        return x

    def arg_process(self, x):
        x.update({'unArgumentEnPlus': 4 })
        return x

_qr = MyCountQuery()



