import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add project root to Python path (BEFORE any src imports)
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))  # Use insert(0) instead of append

# Now import from src
from src.data_processing import preprocess_data
from src.analysis import BirdAnalysis
from src.visualization import BirdVisualizer

# Page configuration
st.set_page_config(
    page_title="Bird Species Observation Analysis",
    page_icon="🐦",
    layout="wide"
)

# Title and description
st.title("🐦 Bird Species Observation Analysis")
st.markdown("""
This interactive dashboard analyzes bird species observations across different habitats, 
focusing on forests and grasslands. Explore temporal trends, spatial distribution, 
species diversity, and environmental factors affecting bird populations.
""")

# Sidebar for data upload and filters
with st.sidebar:
    st.header("Data Configuration")
    uploaded_file = st.file_uploader("Upload Bird Observation Data (Excel)", type=["xlsx"])
    
    if uploaded_file is not None:
        st.success("Data uploaded successfully!")
        st.session_state['data_uploaded'] = True
    else:
        st.warning("Please upload data to proceed")
        st.session_state['data_uploaded'] = False
        st.stop()

# Load and process data
@st.cache_data
def load_data(uploaded_file):
    # Process the data
    df = preprocess_data(uploaded_file)
    return df

try:
    df = load_data(uploaded_file)
    analysis = BirdAnalysis(df)
    visualizer = BirdVisualizer()
    
    # Show data summary
    st.subheader("Data Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Observations", len(df))
    col2.metric("Unique Species", df['Scientific_Name'].nunique())
    col3.metric("Observation Years", f"{df['Year'].min()} - {df['Year'].max()}")
    
    # Temporal Analysis Section
    st.subheader("Temporal Analysis")
    temporal_results = analysis.temporal_analysis()
    fig_temporal = visualizer.plot_temporal_trends(
        temporal_results['yearly'],
        temporal_results['monthly']
    )
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Spatial Analysis Section
    st.subheader("Spatial Distribution")
    spatial_results = analysis.spatial_analysis()
    fig_spatial = visualizer.plot_spatial_distribution(
        spatial_results['admin_unit'],
        spatial_results['location_type']
    )
    st.plotly_chart(fig_spatial, use_container_width=True)
    
    # Species Analysis Section
    st.subheader("Species Distribution")
    species_results = analysis.species_analysis()
    fig_species = visualizer.plot_species_distribution(
        species_results['common_species'],
        species_results['watchlist_species']
    )
    st.plotly_chart(fig_species, use_container_width=True)
    
    # Conservation Status
    st.subheader("Conservation Status")
    conservation_df = species_results['conservation']
    st.dataframe(conservation_df, use_container_width=True)
    
    # Environmental Factors Section
    st.subheader("Environmental Factors")
    env_results = analysis.environmental_analysis()
    fig_env = visualizer.plot_environmental_factors(
        env_results['temperature'],
        env_results['humidity'],
        env_results['sky'],
        env_results['wind']
    )
    st.plotly_chart(fig_env, use_container_width=True)
    
    # Raw Data Preview
    if st.checkbox("Show raw data"):
        st.subheader("Raw Data Preview")
        st.dataframe(df.head(100), use_container_width=True)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")