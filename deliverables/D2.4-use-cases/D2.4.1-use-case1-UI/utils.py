
import geopandas as gpd
import pandas as pd
import numpy as np

import xarray as xr
import rasterio
import rasterio.mask
from affine import Affine
from rasterstats import zonal_stats
from rasterio.features import shapes
from shapely.geometry import shape
#### !pip install rioxarray
#### !pip install openpyxl

from constants import *


################################################################################
def clip_raster(admin_df,INPUT_RASTER_PATH,OUTPUT_RASTER_PATH):
    """
    Loads and clip a raster (INPUT_RASTER_PATH) to a given geometry (admin_df). This is done
    to speed-up computations during data processing. Doesn't return any value but
    exports resulting tiff file to OUTPUT_RASTER_PATH
    """
    with rasterio.open(INPUT_RASTER_PATH) as src:
    
        out_image, out_transform = rasterio.mask.mask(src, admin_df['geometry'], crop=True)
        out_meta = src.meta
    
    out_meta.update({"driver": "GTiff","height": out_image.shape[1],"width": out_image.shape[2],"transform": out_transform})
        
    with rasterio.open(OUTPUT_RASTER_PATH, "w", **out_meta) as dest:
        dest.write(out_image)

    return


################################################################################
def clip_vector(admin_df,INPUT_VECTOR_PATH,OUTPUT_VECTOR_PATH):
    """
    Loads and clip a vector (INPUT_VECTOR_PATH) to a given geometry (admin_df). This is done
    to speed-up computations during data processing. Doesn't return any value but
    exports resulting geojson file to OUTPUT_VECTOR_PATH
    """
    input_vector_df = gpd.read_file(INPUT_VECTOR_PATH)
    input_vector_df = input_vector_df.sjoin(admin_df, how="inner")
    input_vector_df.reset_index(drop = True, inplace = True)
    input_vector_df.drop(columns = ['index_right'], inplace = True)
    input_vector_df.to_file(OUTPUT_VECTOR_PATH, driver="GeoJSON")

    return


################################################################################
def prepare_raster_path(hazard, iso_code, return_period):
    """
    Rename raster path to specific hazard and country (iso_code) and return period.
    Default file paths for global rasters (file constants.py) have wrl (world) 
    as default iso-code.
    """
    raster_path = HAZARD_RASTER_PATH[hazard] 
    raster_path = raster_path.replace('XXX',str(return_period))
    country_raster_path = raster_path.replace('wrl',iso_code.lower())

    return(raster_path, country_raster_path)


################################################################################
def vectorize_raster(file_path):
    """
    Loads and transform a raster into a vector following iso-values.
    This is used wheh computing infrastructure location exposure. Returns a geodataframe
    with resulting geometries and classes. 
    """
    with rasterio.open(file_path) as src:
        data = src.read(1, masked=False)
        shape_gen = ((shape(s), v) for s, v in shapes(data, transform=src.transform))
        gdf = gpd.GeoDataFrame(dict(zip(["geometry", "class"], zip(*shape_gen))), crs=src.crs)

    return(gdf)



################################################################################
def compute_hazard_mask(hazard_raster,population_raster,hazard_threshold):
    """
    Returns a boolean raster mask where 1 indicates that the hazard layer is above
    a given threshold and 0 otherwise.
    """
    hazard_raster = hazard_raster.rio.reproject_match(population_raster)
    hazard_data = hazard_raster[0].values
    hazard_data = np.nan_to_num(hazard_data)
    hazard_data[hazard_data <= hazard_threshold] = 0
    hazard_data[hazard_data > hazard_threshold] = 1
    hazard_mask_raster = hazard_raster
    hazard_mask_raster.values = [hazard_data]
    
    return hazard_mask_raster
        

################################################################################
def compute_population_exposure(hazard_mask_raster, population_raster):
    """
    Compute how a exposed population raster based on hazard mask. This raster 
    will have the same value as original population for exposed zones and 
    0 otherwise. Population here maybe total population or a subset (by gender
    and / or age), depending on input file
    """
    pop_hazard_array = np.multiply(
        population_raster[0].values, hazard_mask_raster[0].values
    )
    pop_exp_raster = hazard_mask_raster
    pop_exp_raster.values = [pop_hazard_array]
    pop_exp_raster = pop_exp_raster.rio.write_crs("epsg:4326")
    
    return pop_exp_raster


################################################################################
def compute_zonal_stat(data_value,exp_affine,admin_df,agg):
    """
    Compute raster zonal statistics following "agg" aggreagation type (sum, mean, etc)
    and admin boundaries (admin_df)
    """
    stats = zonal_stats(admin_df, data_value, affine=exp_affine, stats=agg, nodata=-999)
    value_list = [x[agg] for x in stats]
    return value_list



################################################################################
def load_admin_data(use_gadm_boundaries, iso_code, admin_level):
    """
    Loads subnational admin boundaries into a DataFrame format. If 
    use_gadm_boundaries = True, loads global GADM file and filter to given country.
    Otherwise loads custom file defined in file constants.py
    """
    
    admin_pcode_list = {
    'admin0' : [REF_ADMIN_PCODE['admin0']],
    'admin1' : [REF_ADMIN_PCODE['admin0'],REF_ADMIN_PCODE['admin1']],
    'admin2' : [REF_ADMIN_PCODE['admin0'],REF_ADMIN_PCODE['admin1'],REF_ADMIN_PCODE['admin2']],
    }

    col_list = admin_pcode_list[admin_level] + ['geometry']
    
    if use_gadm_boundaries == True:
        ADMIN_VECTOR_PATH = GADM_ADMIN_VECTOR_PATH[admin_level]
        input_admin_df = gpd.read_file(ADMIN_VECTOR_PATH)
        admin_df = input_admin_df[input_admin_df['GID_0'] == iso_code]
        admin_df.reset_index(drop = True, inplace = True)
        
        admin_df = admin_df.rename(columns = {
            'GID_0': REF_ADMIN_PCODE['admin0'],
            'GID_1': REF_ADMIN_PCODE['admin1'],
            'NAME_1': 'ADM1_NAME',
            'GID_2': REF_ADMIN_PCODE['admin2'],
            'NAME_2': 'ADM2_NAME',
            })
    
    else:
        ADMIN_VECTOR_PATH = CUSTOM_ADMIN_VECTOR_PATH[iso_code][admin_level]
        admin_df = gpd.read_file(ADMIN_VECTOR_PATH)
        for adm in CUSTOM_ADMIN_PCODE[iso_code].keys():
            admin_df.rename(columns = {CUSTOM_ADMIN_PCODE[iso_code][adm] : REF_ADMIN_PCODE[adm]}, inplace = True)
        
    return(admin_df[col_list])


################################################################################
def load_infrastructure_data(iso_code, admin_df, admin_level, infrastructure_layer):
    """
    Loads infrastructure location file into a geodaframe.
    """

    INFRASTRUCTURE_LOCATION_PATH = GLOBAL_INFRASTRUCTURE_LOCATION_PATH[infrastructure_layer]
    COUNTRY_INFRASTRUCTURE_LOCATION_PATH = INFRASTRUCTURE_LOCATION_PATH.replace('wrl',iso_code.lower())

    infrastructure_df = gpd.read_file(COUNTRY_INFRASTRUCTURE_LOCATION_PATH)
    infrastructure_id = GLOBAL_INFRASTRUCTURE_UNIQUE_ID[infrastructure_layer]

    infrastructure_df['ISO'] = iso_code
    admin_pcode = REF_ADMIN_PCODE[admin_level]
    infrastructure_df = infrastructure_df.sjoin(admin_df[[admin_pcode,'geometry']], how = 'inner')
    infrastructure_df.drop_duplicates(subset=[infrastructure_id], inplace = True)
    
    return(infrastructure_df[['ISO',admin_pcode,infrastructure_id,'geometry']])
        


################################################################################
def process_infrastructure_exposure_single_hazard(infrastructure_df,hazard, iso_code, return_period,infrastructure_layer):
    """
    Compute individual infrastructure exposure for a given hazard and return_period (for cyclone, flood
    and earthquake). Returns a dataframe with exposure per infrastructure. Flood, cyclone and earthquake exposure
    depend on thresholds defined on file constants.py.
    """

    INPUT_RASTER_PATH, COUNTRY_HAZARD_RASTER_PATH = prepare_raster_path(hazard, iso_code, return_period)
    col_name = 'value_rp'
    hazard_df = vectorize_raster(COUNTRY_HAZARD_RASTER_PATH)
    hazard_df.fillna(0, inplace = True)
    
    hazard_df['class'] = (hazard_df['class'] > HAZARD_THRESHOLD[hazard])*1.

    hazard_df = hazard_df.dissolve(by='class').reset_index()
    infrastructure_exposure_df = infrastructure_df.sjoin(hazard_df, how="left")
    infrastructure_exposure_df[col_name] = infrastructure_exposure_df['class'].fillna(0)

    infrastructure_id = GLOBAL_INFRASTRUCTURE_UNIQUE_ID[infrastructure_layer]
    
    return(infrastructure_exposure_df[[infrastructure_id,col_name]])


################################################################################
def process_hazard_exposure(iso_code, hazard, admin_df, admin_pcode):
    """
    Process hazard data (cyclone and flood) by looping through all return periods. 
    This function is used for children exposure per region. Result value is 
    the Annual Avarage Exposed Population.
    """
    COUNTRY_POPULATION_RASTER_PATH = POPULATION_RASTER_PATH.replace('wrl',iso_code.lower())
    population_raster = xr.open_dataarray(COUNTRY_POPULATION_RASTER_PATH)
    [pop_arr,pop_affine]  = [population_raster[0].values,population_raster.rio.transform()]
    exposure_df = pd.DataFrame(admin_df[admin_pcode])
    exposure_df['pop_tot'] = compute_zonal_stat(pop_arr, pop_affine, admin_df, agg="sum")
    exposure_df['pop_exp'] = 0
    exposure_df['exp_ratio'] = 0
    
    prev_rp_col_name = ''
    
    for return_period in HAZARD_RETURN_PERIOD[hazard]:
        rp_col_name = 'RP_'+str(return_period)
        INPUT_RASTER_PATH, COUNTRY_HAZARD_RASTER_PATH = prepare_raster_path(hazard, iso_code, return_period)
        hazard_raster = xr.open_dataarray(COUNTRY_HAZARD_RASTER_PATH)
        hazard_mask_raster = compute_hazard_mask(hazard_raster, population_raster, HAZARD_THRESHOLD[hazard])
        population_exposure_raster = compute_population_exposure(hazard_mask_raster, population_raster)
        [exp_arr,exp_affine]  = [population_exposure_raster[0].values,population_exposure_raster.rio.transform()]      
        exposure_df[rp_col_name] = compute_zonal_stat(exp_arr, exp_affine, admin_df, agg="sum")
    
        if prev_rp_col_name == '':
            exposure_df['pop_exp'] = exposure_df[rp_col_name]/return_period
        else:
            exposure_df['pop_exp'] = exposure_df['pop_exp'] + (exposure_df[rp_col_name] - exposure_df[prev_rp_col_name])/return_period
    
        prev_rp_col_name = rp_col_name
    
    exposure_df[hazard] = exposure_df['pop_exp']/exposure_df['pop_tot']*100
    

    return(exposure_df[[admin_pcode, hazard]])
    




################################################################################
def hazard_columns_list(hazard_list):
    """
    Returns all possible exposure level (return periods 
    for cyclone and flood).
    """
    hazard_col_list = []
    hazard_col_list = hazard_col_list + ['num_facilities']
    
    
    for hazard in hazard_list:
        hazard_col_list = hazard_col_list + [hazard + '_' + 'no_exposure', hazard + '_' + 'exposure']
        for value in HAZARD_RETURN_PERIOD[hazard]:
            hazard_col_list = hazard_col_list + [hazard + '_' + str(value) + 'yr']
            
    return(hazard_col_list)