import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class BirdVisualizer:
    @staticmethod
    def plot_temporal_trends(yearly: pd.DataFrame, monthly: pd.DataFrame) -> go.Figure:
        """Plot yearly and monthly trends"""
        fig = make_subplots(rows=1, cols=2, subplot_titles=('Yearly Trends', 'Monthly Trends'))
        
        # Yearly trends
        fig.add_trace(
            go.Scatter(
                x=yearly['Year'],
                y=yearly['Unique_Species'],
                name='Unique Species',
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=yearly['Year'],
                y=yearly['Total_Observations'],
                name='Total Observations',
                line=dict(color='green')
            ),
            row=1, col=1
        )
        
        # Monthly trends
        fig.add_trace(
            go.Bar(
                x=monthly['Month'],
                y=monthly['Unique_Species'],
                name='Unique Species',
                marker_color='blue'
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Bar(
                x=monthly['Month'],
                y=monthly['Total_Observations'],
                name='Total Observations',
                marker_color='green'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text='Temporal Analysis of Bird Observations',
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def plot_spatial_distribution(admin_unit: pd.DataFrame, location_type: pd.DataFrame) -> go.Figure:
        """Plot spatial distribution of observations"""
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'bar'}, {'type': 'pie'}]],
            subplot_titles=('By Admin Unit', 'By Location Type')
        )
        
        # Admin unit bar chart
        fig.add_trace(
            go.Bar(
                x=admin_unit['Admin_Unit_Code'],
                y=admin_unit['Unique_Species'],
                name='Unique Species',
                marker_color='blue'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=admin_unit['Admin_Unit_Code'],
                y=admin_unit['Total_Observations'],
                name='Total Observations',
                marker_color='green'
            ),
            row=1, col=1
        )
        
        # Location type pie chart
        fig.add_trace(
            go.Pie(
                labels=location_type['Location_Type'],
                values=location_type['Total_Observations'],
                name='Observations by Location'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text='Spatial Distribution of Bird Observations',
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def plot_species_distribution(common_species: pd.DataFrame, watchlist_species: pd.DataFrame) -> go.Figure:
        """Plot species distribution charts"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Most Common Species', 'Watchlist Species')
        )
        
        # Common species
        fig.add_trace(
            go.Bar(
                y=common_species['Common_Name'],
                x=common_species['Count'],
                orientation='h',
                name='Common Species',
                marker_color='blue'
            ),
            row=1, col=1
        )
        
        # Watchlist species
        fig.add_trace(
            go.Bar(
                y=watchlist_species['Common_Name'],
                x=watchlist_species['Count'],
                orientation='h',
                name='Watchlist Species',
                marker_color='red'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text='Species Distribution Analysis',
            showlegend=False,
            height=600
        )
        
        return fig
    
    @staticmethod
    def plot_environmental_factors(temp: pd.DataFrame, humidity: pd.DataFrame, sky: pd.DataFrame, wind: pd.DataFrame) -> go.Figure:
        """Plot environmental factor analysis"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Temperature Effect', 'Humidity Effect', 'Sky Conditions', 'Wind Conditions')
        )
        
        # Temperature
        fig.add_trace(
            go.Bar(
                x=temp['Temperature'].astype(str),
                y=temp['Unique_Species'],
                name='Unique Species',
                marker_color='blue'
            ),
            row=1, col=1
        )
        
        # Humidity
        fig.add_trace(
            go.Bar(
                x=humidity['Humidity'].astype(str),
                y=humidity['Unique_Species'],
                name='Unique Species',
                marker_color='green'
            ),
            row=1, col=2
        )
        
        # Sky conditions
        fig.add_trace(
            go.Bar(
                x=sky['Sky'],
                y=sky['Unique_Species'],
                name='Unique Species',
                marker_color='orange'
            ),
            row=2, col=1
        )
        
        # Wind conditions
        fig.add_trace(
            go.Bar(
                x=wind['Wind'],
                y=wind['Unique_Species'],
                name='Unique Species',
                marker_color='purple'
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text='Environmental Factors Analysis',
            showlegend=False,
            height=800
        )
        
        return fig