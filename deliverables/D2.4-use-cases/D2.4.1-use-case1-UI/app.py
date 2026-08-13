import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import constants
from utils import load_admin_data
from streamlit_country_preparation import build_preparation_summary, run_country_preparation
from streamlit_population_exposure import run_population_exposure
from streamlit_infrastructure_exposure import run_infrastructure_exposure

CASE_DESCRIPTION_PATH = PROJECT_DIR / "case.md"


def load_case_description():
    if CASE_DESCRIPTION_PATH.exists():
        text = CASE_DESCRIPTION_PATH.read_text(encoding="utf-8")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        title = lines[0] if lines else "Exposure Dashboard"

        if "1.1 Context and use case relevance" in text:
            excerpt = text.split("1.1 Context and use case relevance", 1)[1]
            excerpt = excerpt.split("1.2 Data sources", 1)[0].strip()
        else:
            excerpt = " ".join(lines[1:4]) if len(lines) > 1 else text.strip()

        if len(excerpt) > 2200:
            excerpt = excerpt[:2200].rstrip() + "..."

        return title, excerpt, text

    return "Exposure Dashboard", "No case description available.", ""


st.set_page_config(page_title="Exposure Dashboard", page_icon="🌍", layout="wide")

st.sidebar.title("Navigation")
page_options = ["Home", "Data Preparation", "Population Exposure", "Infrastructure Exposure"]
current_page = st.session_state.get("current_page", "Home")
if current_page not in page_options:
    current_page = "Home"
page = st.sidebar.radio("Select step", page_options, index=page_options.index(current_page))
st.session_state["current_page"] = page

st.sidebar.markdown("---")
st.sidebar.subheader("Shared inputs")
popular_iso_codes = list(getattr(constants, "POPULAR_ISO_CODES", []) or [])
if not popular_iso_codes:
    popular_iso_codes = ["AFG", "CMR", "COL", "ETH", "IRQ", "KEN", "MOZ", "NGA", "PAK", "PHL", "SOM", "SSD", "SYR", "UGA", "YEM"]
default_iso_code = str(getattr(constants, "DEFAULT_ISO_CODE", "MOZ")).upper()
if default_iso_code not in popular_iso_codes:
    popular_iso_codes = [default_iso_code] + popular_iso_codes
popular_iso_codes = list(dict.fromkeys(popular_iso_codes))
iso_default_index = popular_iso_codes.index(default_iso_code) if default_iso_code in popular_iso_codes else 0
iso_code_input = st.sidebar.selectbox(
    "ISO Code",
    options=popular_iso_codes,
    index=iso_default_index,
    key="iso_code_select",
)
st.sidebar.caption("Choose one of the suggested ISO codes. You can edit the list in constants.py.")
admin_level = st.sidebar.selectbox("Admin level", ["admin1", "admin2"], index=0)
hazard_options = ["earthquake", "cyclone_current", "cyclone_future", "flood_current", "flood_future"]
selected_hazards = st.sidebar.multiselect("Hazards", hazard_options, default=["flood_current", "earthquake"])
use_gadm_boundaries = st.sidebar.checkbox("Use GADM boundaries", value=True)

if page == "Home":
    st.title("Exposure Dashboard")

    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 45%, #2563eb 100%); border-radius: 24px; padding: 24px 24px 20px; margin-bottom: 18px; box-shadow: 0 10px 30px rgba(37, 99, 235, 0.25); position: relative; overflow: hidden;">
            <div style="position:absolute; inset:-20% 60% auto auto; width:220px; height:220px; background: radial-gradient(circle, rgba(255,255,255,0.25), transparent 70%); animation: pulse 4s ease-in-out infinite;"></div>
            <div style="position:absolute; inset:auto auto -20% -8%; width:260px; height:260px; background: radial-gradient(circle, rgba(56, 189, 248, 0.25), transparent 70%); animation: float 6s ease-in-out infinite;"></div>
            <h2 style="margin:0; color:white; font-size:1.6rem; font-weight:700;">Exposure Dashboard</h2>
        </div>
        <style>
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-12px); }
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 0.7; }
                50% { transform: scale(1.08); opacity: 1; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    case_title, case_excerpt, _ = load_case_description()
    st.subheader(case_title)
    st.write(case_excerpt)

    st.markdown("---")
    st.subheader("Workflow")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Step 1: Prepare country data and required input layers")
        if st.button("Go to Data Preparation", key="go_prep"):
            st.session_state["current_page"] = "Data Preparation"
            st.rerun()
    with col2:
        st.info("Step 2: Run population exposure analysis")
        if st.button("Go to Population Exposure", key="go_pop"):
            st.session_state["current_page"] = "Population Exposure"
            st.rerun()
    with col3:
        st.info("Step 3: Run infrastructure exposure analysis")
        if st.button("Go to Infrastructure Exposure", key="go_infra"):
            st.session_state["current_page"] = "Infrastructure Exposure"
            st.rerun()

elif page == "Data Preparation":
    st.title("Step 1: Data Preparation")
    st.write("This step reproduces the logic of the country_data_preparation notebook and prepares country-specific data files.")

    infrastructure_options = ["health"]
    selected_infrastructure = st.multiselect("Infrastructure layers", infrastructure_options, default=["health"])

    if st.button("Run data preparation"):
        with st.spinner("Preparing country data..."):
            try:
                iso_code_list = [iso_code_input.upper()]
                results = run_country_preparation(iso_code_list, selected_hazards, selected_infrastructure)
                summary = build_preparation_summary(results)

                st.success("Data preparation completed")

                for item in summary:
                    with st.expander(f"Country: {item['iso_code']}", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Population raster", "Created" if item['population_exists'] else "Missing")
                        col2.metric("Infrastructure layers", item['infrastructure_count'])
                        col3.metric("Hazard outputs", item['hazard_output_count'])

                        if item['file_details']:
                            file_df = pd.DataFrame(item['file_details'])
                            st.dataframe(file_df, use_container_width=True)
                        else:
                            st.info("No output files were generated.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

elif page == "Population Exposure":
    st.title("Step 2: Population Exposure")
    st.write("This section runs the logic of the population exposure notebook using the reusable Python functions.")

    if st.button("Run population exposure"):
        with st.spinner("Running population exposure analysis..."):
            try:
                result = run_population_exposure(iso_code_input, admin_level, selected_hazards, use_gadm_boundaries)
                st.success("Population exposure analysis completed")
                st.metric("ISO Code", result['iso_code'])
                st.metric("Admin level", result['admin_level'])
                st.metric("Output file", result['output_path'])
                st.dataframe(result['exposure_df'].head())
            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    st.title("Step 3: Infrastructure Exposure")
    st.write("This section runs the logic of the infrastructure exposure notebook using the reusable Python functions.")

    infrastructure_options = ["health"]
    selected_infrastructure = st.multiselect("Infrastructure layers", infrastructure_options, default=["health"], key="infra_layers")

    if st.button("Run infrastructure exposure"):
        with st.spinner("Running infrastructure exposure analysis..."):
            try:
                result = run_infrastructure_exposure(
                    iso_code_input, admin_level, selected_hazards, selected_infrastructure, use_gadm_boundaries
                )
                st.success("Infrastructure exposure analysis completed")
                st.metric("ISO Code", result['iso_code'])
                st.metric("Admin level", result['admin_level'])

                for item in result['results']:
                    with st.expander(f"Layer: {item['infrastructure_layer']}", expanded=True):
                        st.write("Output file:", item['output_path'])
                        if not item['exposure_df'].empty:
                            st.dataframe(item['exposure_df'].head())
                        for hazard_summary in item['hazard_summaries']:
                            st.write(f"Hazard: {hazard_summary['hazard']}")
                            st.dataframe(hazard_summary['aggregated_df'].head())
            except Exception as e:
                st.error(f"An error occurred: {e}")
