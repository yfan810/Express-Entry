import pandas as pd
import os

file_path_ee_trend = os.path.join(os.path.dirname(__file__), "../../data/raw/EE.csv")
file_path_ee_pool = os.path.join(os.path.dirname(__file__), "../../data/raw/EE_pool.csv")
file_path_2025_quota = os.path.join(os.path.dirname(__file__), "../../data/raw/2025_quota.csv")

def load_ee_data():
    """Loads dataset"""
    df = pd.read_csv(os.path.abspath(file_path_ee_trend))
    df["date"] = pd.to_datetime(df["date"])
    return df

def load_ee_pool_data():
    """Loads dataset"""
    df = pd.read_csv(os.path.abspath(file_path_ee_pool))
    df["date"] = pd.to_datetime(df["date"])
    return df

def load_2025_quota():
    """Loads dataset"""
    df = pd.read_csv(os.path.abspath(file_path_2025_quota))
    df["year"] = pd.to_datetime(df["year"])
    return df

ee_trend = load_ee_data()
ee_pool = load_ee_pool_data()
quota_2025 = load_2025_quota()

#ee_pool['timestamp'] = (ee_pool['date'].astype(int) / 10**9).astype(int)

ee_melt = pd.melt(ee_pool, 
                  id_vars='date', 
                  value_vars=['601_1200', '501_600', '491_500', '481_490', '471_480', '461_470', 
                              '451_460', '441_450','431_440', '421_430', '411_420', '401_410', '351_400', '301_350', '0_300'],
                  var_name='range',
                  value_name='number')
ee_melt['timestamp'] = (ee_melt['date'].astype(int) / 10**9).astype(int)

quota_2025_melt = pd.melt(quota_2025,
                          id_vars=['year', 'type'],
                          value_vars=['low', 'target', 'high'],
                          var_name='bar',
                          value_name='number')

#To get the cumulative number of invitations issued for each category
ee_pool_2025 = ee_trend[ee_trend['date'].dt.year == 2025]
ee_pool_2025 = ee_pool_2025[['type', 'invitations_issued']].groupby('type').agg('sum').reset_index()

total_invitations = ee_pool_2025['invitations_issued'].sum()
summary_row = pd.DataFrame({'type': ['Overall'], 'invitations_issued': [total_invitations]})
ee_pool_2025 = pd.concat([ee_pool_2025, summary_row], ignore_index=True)

#print(ee_melt)
