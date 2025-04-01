import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class BirdAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def temporal_analysis(self) -> Dict:
        """Analyze temporal patterns in the data"""
        # Yearly trends
        yearly = self.df.groupby('Year').agg({
            'Scientific_Name': 'nunique',
            'Common_Name': 'count'
        }).rename(columns={
            'Scientific_Name': 'Unique_Species',
            'Common_Name': 'Total_Observations'
        }).reset_index()
        
        # Monthly trends
        monthly = self.df.copy()
        monthly['Month'] = monthly['Date'].dt.month
        monthly = monthly.groupby('Month').agg({
            'Scientific_Name': 'nunique',
            'Common_Name': 'count'
        }).rename(columns={
            'Scientific_Name': 'Unique_Species',
            'Common_Name': 'Total_Observations'
        }).reset_index()
        
        return {
            'yearly': yearly,
            'monthly': monthly
        }
    
    def spatial_analysis(self) -> Dict:
        """Analyze spatial patterns in the data"""
        # By admin unit
        admin_unit = self.df.groupby('Admin_Unit_Code').agg({
            'Scientific_Name': 'nunique',
            'Common_Name': 'count',
            'Plot_Name': 'nunique'
        }).rename(columns={
            'Scientific_Name': 'Unique_Species',
            'Common_Name': 'Total_Observations',
            'Plot_Name': 'Unique_Plots'
        }).reset_index()
        
        # By location type
        location_type = self.df.groupby('Location_Type').agg({
            'Scientific_Name': 'nunique',
            'Common_Name': 'count'
        }).rename(columns={
            'Scientific_Name': 'Unique_Species',
            'Common_Name': 'Total_Observations'
        }).reset_index()
        
        return {
            'admin_unit': admin_unit,
            'location_type': location_type
        }
    
    def species_analysis(self) -> Dict:
        """Analyze species patterns"""
        # Most common species
        common_species = self.df['Common_Name'].value_counts().reset_index()
        common_species.columns = ['Common_Name', 'Count']
        
        # Watchlist species
        watchlist = self.df[self.df['PIF_Watchlist_Status']]
        watchlist_species = watchlist['Common_Name'].value_counts().reset_index()
        watchlist_species.columns = ['Common_Name', 'Count']
        
        # Conservation status
        conservation = self.df.groupby(['PIF_Watchlist_Status', 'Regional_Stewardship_Status']).size().reset_index()
        conservation.columns = ['PIF_Watchlist', 'Regional_Stewardship', 'Count']
        
        return {
            'common_species': common_species.head(20),
            'watchlist_species': watchlist_species.head(20),
            'conservation': conservation
        }
    
    def environmental_analysis(self) -> Dict:
        """Analyze environmental factors"""
        # Temperature and humidity effects
        temp_bins = pd.cut(self.df['Temperature'], bins=5)
        humidity_bins = pd.cut(self.df['Humidity'], bins=5)
        
        temp_effect = self.df.groupby(temp_bins).agg({
            'Scientific_Name': 'nunique',
            'Common_Name': 'count'
        }).rename(columns={
            'Scientific_Name': 'Unique_Species',
            'Common_Name': 'Total_Observations'
        }).reset_index()
        
        humidity_effect = self.df.groupby(humidity_bins).agg({
            'Scientific_Name': 'nunique',
            'Common_Name': 'count'
        }).rename(columns={
            'Scientific_Name': 'Unique_Species',
            'Common_Name': 'Total_Observations'
        }).reset_index()
        
        # Sky and wind conditions
        sky_effect = self.df.groupby('Sky').agg({
            'Scientific_Name': 'nunique',
            'Common_Name': 'count'
        }).rename(columns={
            'Scientific_Name': 'Unique_Species',
            'Common_Name': 'Total_Observations'
        }).reset_index()
        
        wind_effect = self.df.groupby('Wind').agg({
            'Scientific_Name': 'nunique',
            'Common_Name': 'count'
        }).rename(columns={
            'Scientific_Name': 'Unique_Species',
            'Common_Name': 'Total_Observations'
        }).reset_index()
        
        return {
            'temperature': temp_effect,
            'humidity': humidity_effect,
            'sky': sky_effect,
            'wind': wind_effect
        }