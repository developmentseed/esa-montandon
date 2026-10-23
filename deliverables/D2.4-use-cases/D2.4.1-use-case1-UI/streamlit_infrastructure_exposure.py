import os

import pandas as pd

from constants import *
from utils import (
    compute_zonal_stat,
    hazard_columns_list,
    load_infrastructure_data,
    process_infrastructure_exposure_single_hazard,
)
from streamlit_country_preparation import validate_iso_code


def process_all_hazards(infrastructure_df, iso_code, admin_level, hazard_list, infrastructure_layer):
    """Compute exposure for infrastructure features and export the results to Excel."""
    infrastructure_id = GLOBAL_INFRASTRUCTURE_UNIQUE_ID[infrastructure_layer]
    admin_pcode = REF_ADMIN_PCODE[admin_level]

    if infrastructure_id not in infrastructure_df.columns:
        infrastructure_df = infrastructure_df.copy()
        infrastructure_df[infrastructure_id] = range(1, len(infrastructure_df) + 1)

    infrastructure_exposure_df = pd.DataFrame(infrastructure_df[[admin_pcode, infrastructure_id]])
    infrastructure_exposure_df['ISO'] = iso_code

    for hazard in hazard_list:
        col_name = hazard
        exposure_df = pd.DataFrame(infrastructure_df[[infrastructure_id]])
        exposure_df[col_name] = 'no_exposure'

        for return_period in HAZARD_RETURN_PERIOD[hazard]:
            try:
                new_rp_df = process_infrastructure_exposure_single_hazard(
                    infrastructure_df.copy(), hazard, iso_code, return_period, infrastructure_layer
                )
                if infrastructure_id in new_rp_df.columns:
                    exposure_df = exposure_df.merge(new_rp_df[[infrastructure_id, 'value_rp']], on=infrastructure_id, how='left')
                    exposure_df.loc[
                        (exposure_df[col_name] == 'no_exposure') & (exposure_df['value_rp'] == 1), col_name
                    ] = str(return_period) + 'yr'
                    exposure_df.drop(columns='value_rp', inplace=True)
                else:
                    exposure_df[col_name] = exposure_df[col_name].replace('no_exposure', str(return_period) + 'yr')
            except Exception:
                pass

        infrastructure_exposure_df = infrastructure_exposure_df.merge(exposure_df, on=infrastructure_id, how='left')

    infrastructure_exposure_df = infrastructure_exposure_df.round(2)
    free_text = infrastructure_layer + '-facilities'
    output_path = ANALYSIS_OUTPUT_PATH.replace('wrl', iso_code.lower()).replace('XXX', free_text)
    infrastructure_exposure_df.to_excel(output_path.replace('.csv', '.xlsx'), index=False, sheet_name=free_text)

    return infrastructure_exposure_df, output_path


def aggregate_infrastructure_exposure(infrastructure_exposure_df, admin_df, admin_level, hazard, infrastructure_layer, iso_code):
    """Aggregate infrastructure exposure per admin unit for one hazard."""
    admin_infrastructure_df = admin_df.drop(columns=['geometry']).copy()
    admin_pcode = REF_ADMIN_PCODE[admin_level]

    infrastructure_hazard_df = infrastructure_exposure_df[[admin_pcode, hazard]].copy()
    hazard_col_list = hazard_columns_list([hazard])
    for col in hazard_col_list:
        admin_infrastructure_df[col] = 0

    infrastructure_hazard_df = infrastructure_hazard_df.value_counts().reset_index()
    infrastructure_hazard_df.rename(columns={hazard: 'hazard_value'}, inplace=True)
    infrastructure_hazard_df['hazard_value'] = str(hazard) + '_' + infrastructure_hazard_df['hazard_value']
    infrastructure_hazard_df = infrastructure_hazard_df.pivot(index=admin_pcode, columns='hazard_value', values='count').reset_index()

    admin_infrastructure_df = admin_infrastructure_df.merge(infrastructure_hazard_df, on=admin_pcode, how='left', suffixes=('', '_new'))
    admin_infrastructure_df.fillna(0, inplace=True)

    for col in hazard_col_list:
        if col + '_new' in admin_infrastructure_df.columns:
            admin_infrastructure_df[col] = admin_infrastructure_df[col + '_new']
            admin_infrastructure_df.drop(columns=[col + '_new'], inplace=True)

    admin_infrastructure_df['num_facilities'] = admin_infrastructure_df[hazard_col_list].sum(axis=1)
    admin_infrastructure_df[hazard + '_exposure'] = admin_infrastructure_df['num_facilities'] - admin_infrastructure_df[hazard + '_no_exposure']
    admin_infrastructure_df = admin_infrastructure_df.round(2)

    free_text = infrastructure_layer + '-facilities-' + admin_level + '-' + hazard.replace('_', '-')
    sheet_name_text = infrastructure_layer + '-facilities-' + hazard.replace('_', '-')
    output_path = ANALYSIS_OUTPUT_PATH.replace('wrl', iso_code.lower()).replace('XXX', free_text)
    admin_infrastructure_df.to_excel(output_path.replace('.csv', '.xlsx'), index=False, sheet_name=sheet_name_text)

    return admin_infrastructure_df, output_path


def run_infrastructure_exposure(iso_code, admin_level, hazard_list, infrastructure_layers, use_gadm_boundaries=True):
    """Run the infrastructure exposure workflow for the selected country and admin level."""
    validated_iso = validate_iso_code(iso_code)
    from utils import load_admin_data

    admin_df = load_admin_data(use_gadm_boundaries, validated_iso, admin_level)
    results = []

    for infrastructure_layer in infrastructure_layers:
        infrastructure_df = load_infrastructure_data(validated_iso, admin_df, admin_level, infrastructure_layer)
        exposure_df, output_path = process_all_hazards(infrastructure_df, validated_iso, admin_level, hazard_list, infrastructure_layer)

        hazard_summaries = []
        for hazard in hazard_list:
            aggregated_df, agg_path = aggregate_infrastructure_exposure(
                exposure_df.copy(), admin_df, admin_level, hazard, infrastructure_layer, validated_iso
            )
            hazard_summaries.append({
                'hazard': hazard,
                'aggregated_df': aggregated_df,
                'output_path': agg_path,
            })

        results.append({
            'infrastructure_layer': infrastructure_layer,
            'output_path': output_path,
            'exposure_df': exposure_df,
            'hazard_summaries': hazard_summaries,
        })

    return {
        'iso_code': validated_iso,
        'admin_level': admin_level,
        'hazards': hazard_list,
        'results': results,
    }
