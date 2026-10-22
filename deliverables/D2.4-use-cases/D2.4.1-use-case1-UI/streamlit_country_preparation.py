import os
import re

import geopandas as gpd

from constants import *
from utils import clip_raster, clip_vector, prepare_raster_path


def validate_iso_code(iso_code):
    """Validate the ISO code before running the preparation workflow."""
    if not isinstance(iso_code, str):
        raise ValueError("ISO code must be a string")

    iso_code = iso_code.strip().upper()
    if not re.fullmatch(r"[A-Z]{3}", iso_code):
        raise ValueError("ISO code must be 3 letters only, for example MOZ or AFG")

    admin_gdf = gpd.read_file(GADM_ADMIN_VECTOR_PATH['admin0'])
    if iso_code not in set(admin_gdf['GID_0']):
        raise ValueError(f"ISO code '{iso_code}' was not found in the GADM country dataset")

    return iso_code


def create_folder_structure(iso_code):
    """Create the folder structure needed for a country-specific data preparation run."""
    newpath = PATH + iso_code.lower()
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for subfolder in FOLDER_STRUCTURE_LIST:
        newpath = PATH + iso_code.lower() + '/' + subfolder
        if not os.path.exists(newpath):
            os.makedirs(newpath)

    return True


def prepare_population_data(iso_code):
    """Crop the global population raster to the country boundary and save a country-specific raster."""
    input_admin_df = gpd.read_file(GADM_ADMIN_VECTOR_PATH['admin0'])
    country_admin_df = input_admin_df[input_admin_df['GID_0'] == iso_code]
    country_population_raster_path = POPULATION_RASTER_PATH.replace('wrl', iso_code.lower())
    clip_raster(country_admin_df, POPULATION_RASTER_PATH, country_population_raster_path)
    return country_population_raster_path


def prepare_infrastructure_data(iso_code, infrastructure_layer):
    """Crop the global infrastructure vector layer to the country boundary and save a country-specific file."""
    input_admin_df = gpd.read_file(GADM_ADMIN_VECTOR_PATH['admin0'])
    country_admin_df = input_admin_df[input_admin_df['GID_0'] == iso_code]
    infrastructure_location_path = GLOBAL_INFRASTRUCTURE_LOCATION_PATH[infrastructure_layer]
    country_infrastructure_path = infrastructure_location_path.replace('wrl', iso_code.lower())
    clip_vector(country_admin_df, infrastructure_location_path, country_infrastructure_path)
    return country_infrastructure_path


def prepare_hazard_data(iso_code, hazard):
    """Crop hazard raster data to the country boundary and save the country-specific raster files."""
    input_admin_df = gpd.read_file(GADM_ADMIN_VECTOR_PATH['admin0'])
    country_admin_df = input_admin_df[input_admin_df['GID_0'] == iso_code]

    if hazard == 'heatwave_future':
        return {'hazard': hazard, 'status': 'skipped', 'message': 'No raster available for heatwave_future'}
    elif hazard == 'heatwave_current':
        return_period_list = ['']
    else:
        return_period_list = HAZARD_RETURN_PERIOD[hazard]

    created_files = []
    for return_period in return_period_list:
        input_raster_path, country_hazard_raster_path = prepare_raster_path(hazard, iso_code, return_period)
        clip_raster(country_admin_df, input_raster_path, country_hazard_raster_path)
        created_files.append(country_hazard_raster_path)

    return {'hazard': hazard, 'status': 'completed', 'files': created_files}


def run_country_preparation(iso_code_list, hazard_list, infrastructure_list):
    """Run the country preparation workflow for one or more countries and selected hazards."""
    results = []

    for iso_code in iso_code_list:
        validated_iso = validate_iso_code(iso_code)
        step_result = {
            'iso_code': validated_iso,
            'folders_created': create_folder_structure(validated_iso),
            'population_file': None,
            'infrastructure_files': [],
            'hazard_results': [],
        }

        step_result['population_file'] = prepare_population_data(validated_iso)

        for infrastructure_layer in infrastructure_list:
            output_path = prepare_infrastructure_data(validated_iso, infrastructure_layer)
            step_result['infrastructure_files'].append({infrastructure_layer: output_path})

        for hazard in hazard_list:
            hazard_result = prepare_hazard_data(validated_iso, hazard)
            step_result['hazard_results'].append(hazard_result)

        results.append(step_result)

    return results


def build_preparation_summary(results):
    """Build a human-readable summary of generated files from the preparation run."""
    summaries = []

    for result in results:
        file_details = []

        if result.get('population_file'):
            file_details.append({
                'type': 'Population raster',
                'path': result['population_file'],
                'exists': os.path.exists(result['population_file']),
            })

        for infrastructure_item in result.get('infrastructure_files', []):
            for layer, path in infrastructure_item.items():
                file_details.append({
                    'type': f'Infrastructure: {layer}',
                    'path': path,
                    'exists': os.path.exists(path),
                })

        for hazard_result in result.get('hazard_results', []):
            hazard_name = hazard_result.get('hazard', 'unknown')
            if hazard_result.get('status') == 'completed':
                for path in hazard_result.get('files', []):
                    file_details.append({
                        'type': f'Hazard: {hazard_name}',
                        'path': path,
                        'exists': os.path.exists(path),
                    })
            else:
                file_details.append({
                    'type': f'Hazard: {hazard_name}',
                    'path': hazard_result.get('message', 'No output'),
                    'exists': False,
                })

        summaries.append({
            'iso_code': result.get('iso_code'),
            'population_exists': bool(result.get('population_file')) and os.path.exists(result.get('population_file')),
            'infrastructure_count': len(result.get('infrastructure_files', [])),
            'hazard_output_count': len([item for item in result.get('hazard_results', []) if item.get('status') == 'completed']),
            'file_details': file_details,
        })

    return summaries
