import os

import pandas as pd

from constants import *
from utils import process_hazard_exposure
from streamlit_country_preparation import validate_iso_code


def process_all_hazards(admin_df, iso_code, admin_level, hazard_list):
    """Compute population exposure for a set of hazards and export the results to Excel."""
    admin_pcode_list = {
        'admin0': [REF_ADMIN_PCODE['admin0']],
        'admin1': [REF_ADMIN_PCODE['admin0'], REF_ADMIN_PCODE['admin1']],
        'admin2': [REF_ADMIN_PCODE['admin0'], REF_ADMIN_PCODE['admin1'], REF_ADMIN_PCODE['admin2']],
    }

    admin_pcode = REF_ADMIN_PCODE[admin_level]
    current_exposure_df = admin_df[admin_pcode_list[admin_level]].copy()

    for hazard in hazard_list:
        exposure_df = process_hazard_exposure(iso_code, hazard, admin_df, admin_pcode)
        current_exposure_df = current_exposure_df.merge(exposure_df, on=admin_pcode)

    current_exposure_df = current_exposure_df.round(2)
    free_text = 'population-' + admin_level
    output_path = ANALYSIS_OUTPUT_PATH.replace('wrl', iso_code.lower()).replace('XXX', free_text)
    current_exposure_df.to_excel(output_path.replace('.csv', '.xlsx'), index=False, sheet_name='population')

    return current_exposure_df, output_path


def run_population_exposure(iso_code, admin_level, hazard_list, use_gadm_boundaries=True):
    """Run the population exposure workflow for the selected country and admin level."""
    validated_iso = validate_iso_code(iso_code)
    from utils import load_admin_data

    admin_df = load_admin_data(use_gadm_boundaries, validated_iso, admin_level)
    exposure_df, output_path = process_all_hazards(admin_df, validated_iso, admin_level, hazard_list)

    return {
        'iso_code': validated_iso,
        'admin_level': admin_level,
        'hazards': hazard_list,
        'output_path': output_path,
        'exposure_df': exposure_df,
    }
