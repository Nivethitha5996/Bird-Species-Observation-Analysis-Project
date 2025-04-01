import pandas as pd
import numpy as np
import os
from typing import Dict, List

def load_all_sheets(file_path: str) -> Dict[str, pd.DataFrame]:
    """Load all sheets from an Excel file into a dictionary of DataFrames"""
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    return {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in sheet_names}

def combine_sheets(sheets_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Combine all sheets into a single DataFrame"""
    combined_df = pd.concat(sheets_dict.values(), ignore_index=True)
    return combined_df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the combined bird observation data"""
    # Convert date columns to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Year'].astype(int)
    
    # Handle time columns
    df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%H:%M:%S').dt.time
    df['End_Time'] = pd.to_datetime(df['End_Time'], format='%H:%M:%S').dt.time
    
    # Convert boolean columns
    bool_cols = ['Flyover_Observed', 'PIF_Watchlist_Status', 'Regional_Stewardship_Status']
    for col in bool_cols:
        df[col] = df[col].replace({'TRUE': True, 'FALSE': False, np.nan: False})
    
    # Standardize categorical columns
    df['Distance'] = df['Distance'].str.strip().replace('<= 50 Meters', '0-50 Meters')
    df['ID_Method'] = df['ID_Method'].str.strip().str.title()
    df['Sex'] = df['Sex'].str.strip().replace('Undetermined', 'Unknown')
    
    # Handle numeric columns
    df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
    df['Humidity'] = pd.to_numeric(df['Humidity'], errors='coerce')
    
    # Extract duration in minutes
    df['Duration_Minutes'] = df['Interval_Length'].str.extract(r'(\d+)').astype(float)
    
    return df

def preprocess_data(file_path: str, output_path: str = None) -> pd.DataFrame:
    """Full preprocessing pipeline"""
    print("Loading data...")
    sheets = load_all_sheets(file_path)
    
    print("Combining sheets...")
    combined = combine_sheets(sheets)
    
    print("Cleaning data...")
    cleaned = clean_data(combined)
    
    if output_path:
        print(f"Saving cleaned data to {output_path}")
        cleaned.to_parquet(output_path, index=False)
    
    return cleaned