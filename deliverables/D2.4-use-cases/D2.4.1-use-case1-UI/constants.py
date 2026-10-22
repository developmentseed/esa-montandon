
PATH = "../../2_Active_Data/"


# Editable list used by the Streamlit sidebar for ISO-code suggestions.
POPULAR_ISO_CODES = [
    "AFG", "CMR", "COL", "ETH", "IRQ", "KEN", "MOZ", "NGA", "PAK", "PHL",
    "SOM", "SSD", "SYR", "UGA", "YEM"
]
DEFAULT_ISO_CODE = "MOZ"


################################################################################################


GADM_ADMIN_VECTOR_PATH = {
    "admin0" : PATH + "wrl/202_admn/wrl_admn_py_gadm_countries.gpkg",
    "admin1" : PATH + "wrl/202_admn/wrl_admn_py_gadm_admin1.gpkg",
    "admin2" : PATH + "wrl/202_admn/wrl_admn_py_gadm_admin2.gpkg",
}


REF_ADMIN_PCODE = {
    "admin0": "ISO",    
    "admin1": "ADM1_PCODE",
    "admin2": "ADM2_PCODE",
}


GLOBAL_INFRASTRUCTURE_LOCATION_PATH = {
    'health' : PATH + "wrl/215_heal/wrl_heal_pt_healthsites.geojson"
}

GLOBAL_INFRASTRUCTURE_UNIQUE_ID = {
    'health' : 'osm_id'
}

FOLDER_STRUCTURE_LIST = ['202_admn','215_heal','216_hazard','223_popu','236_exposure']

################################################################################################

WRL_RISK_PATH = PATH + 'wrl/216_hazard/'

POPULATION_RASTER_PATH = PATH + "wrl/223_popu/wrl_pop_ras_worldpop.tif"
ANALYSIS_OUTPUT_PATH = PATH + "wrl/236_exposure/wrl_exposure_tab_mapaction_XXX.csv"


HAZARD_RASTER_PATH = {
    "earthquake": WRL_RISK_PATH + "wrl_risk_ras_gem_earthquake-rpXXXy.tif",
    "cyclone_current": WRL_RISK_PATH + "wrl_risk_ras_4tu_cyclone-rpXXXy.tif",
    "cyclone_future": WRL_RISK_PATH + "wrl_risk_ras_4tu_cyclone-future-rpXXXy.tif",
    "flood_current": WRL_RISK_PATH + "wrl_risk_ras_wri_flood-rpXXXy.tif",
    "flood_future": WRL_RISK_PATH + "wrl_risk_ras_wri_flood-future-rpXXXy.tif",
}

ADMIN_PCODE = {
    "admin0": "ISO",    
    "admin1": "ADM1_PCODE",
    "admin2": "ADM2_PCODE",
}



HAZARD_THRESHOLD = {
    "earthquake": 0.22, 
    "cyclone_current": 33., 
    "cyclone_future": 33., 
    "flood_current": 0.5,
    "flood_future": 0.5,
}

HAZARD_RETURN_PERIOD = {
    "earthquake": [475], 
    "cyclone_current": [10,50,100,500,1000], 
    "cyclone_future": [10,50,100,500,1000], 
    "flood_current": [10,50,100,500,1000], 
    "flood_future": [10,50,100,500,1000], 
}


