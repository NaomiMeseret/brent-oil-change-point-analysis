"""
Data Processing Utilities for Brent Oil Price Change Point Analysis

This module provides functions for data loading, cleaning, and preparation
for the Bayesian change point analysis of Brent oil prices.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')


class BrentOilDataProcessor:
    """
    A class for processing Brent oil price data and geopolitical events
    """
    
    def __init__(self):
        self.brent_data = None
        self.events_data = None
        self.merged_data = None
    
    def download_brent_data(self, start_date='1987-05-20', end_date='2022-09-30'):
        """
        Download Brent crude oil data using yfinance
        
        Parameters:
        -----------
        start_date : str
            Start date in 'YYYY-MM-DD' format
        end_date : str
            End date in 'YYYY-MM-DD' format
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with Date and Price columns
        """
        try:
            print(f"Downloading Brent oil data from {start_date} to {end_date}...")
            
            # Download Brent crude futures data
            brent = yf.download('BZ=F', start=start_date, end=end_date)
            
            # Reset index to get Date as column
            brent = brent.reset_index()
            
            # Select relevant columns and rename
            brent_data = brent[['Date', 'Close']].copy()
            brent_data.columns = ['Date', 'Price']
            
            # Convert Date to datetime
            brent_data['Date'] = pd.to_datetime(brent_data['Date'])
            
            # Remove any rows with missing prices
            brent_data = brent_data.dropna(subset=['Price'])
            
            # Sort by date
            brent_data = brent_data.sort_values('Date').reset_index(drop=True)
            
            self.brent_data = brent_data
            
            print(f"✓ Successfully downloaded {len(brent_data)} observations")
            print(f"  Date range: {brent_data['Date'].min()} to {brent_data['Date'].max()}")
            
            return brent_data
            
        except Exception as e:
            print(f"✗ Error downloading data: {e}")
            return None
    
    def load_events_data(self, file_path):
        """
        Load geopolitical events data from CSV file
        
        Parameters:
        -----------
        file_path : str
            Path to the events CSV file
            
        Returns:
        --------
        pd.DataFrame
            Events data with proper date formatting
        """
        try:
            print(f"Loading events data from {file_path}...")
            
            events_data = pd.read_csv(file_path)
            
            # Convert Date to datetime
            events_data['Date'] = pd.to_datetime(events_data['Date'])
            
            # Sort by date
            events_data = events_data.sort_values('Date').reset_index(drop=True)
            
            self.events_data = events_data
            
            print(f"✓ Successfully loaded {len(events_data)} events")
            print(f"  Date range: {events_data['Date'].min()} to {events_data['Date'].max()}")
            
            return events_data
            
        except Exception as e:
            print(f"✗ Error loading events data: {e}")
            return None
    
    def calculate_returns(self, price_col='Price'):
        """
        Calculate log returns and simple returns
        
        Parameters:
        -----------
        price_col : str
            Name of the price column
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with additional return columns
        """
        if self.brent_data is None:
            print("✗ Brent data not loaded. Please download data first.")
            return None
        
        print("Calculating returns...")
        
        # Calculate simple returns
        self.brent_data['Simple_Return'] = self.brent_data[price_col].pct_change()
        
        # Calculate log returns
        self.brent_data['Log_Return'] = np.log(self.brent_data[price_col] / 
                                               self.brent_data[price_col].shift(1))
        
        # Calculate absolute returns (volatility measure)
        self.brent_data['Abs_Return'] = abs(self.brent_data['Log_Return'])
        
        print("✓ Returns calculated successfully")
        
        return self.brent_data
    
    def add_rolling_statistics(self, price_col='Price', windows=[252, 63, 21]):
        """
        Add rolling statistics for different time windows
        
        Parameters:
        -----------
        price_col : str
            Name of the price column
        windows : list
            List of window sizes in trading days
            (252 ~ 1 year, 63 ~ 3 months, 21 ~ 1 month)
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with rolling statistics
        """
        if self.brent_data is None:
            print("✗ Brent data not loaded. Please download data first.")
            return None
        
        print("Calculating rolling statistics...")
        
        for window in windows:
            # Rolling mean
            self.brent_data[f'Rolling_Mean_{window}'] = (
                self.brent_data[price_col].rolling(window=window).mean()
            )
            
            # Rolling standard deviation
            self.brent_data[f'Rolling_Std_{window}'] = (
                self.brent_data[price_col].rolling(window=window).std()
            )
            
            # Rolling minimum and maximum
            self.brent_data[f'Rolling_Min_{window}'] = (
                self.brent_data[price_col].rolling(window=window).min()
            )
            
            self.brent_data[f'Rolling_Max_{window}'] = (
                self.brent_data[price_col].rolling(window=window).max()
            )
        
        print("✓ Rolling statistics calculated successfully")
        
        return self.brent_data
    
    def merge_events_with_prices(self, event_window_days=5):
        """
        Merge events data with price data, adding price information around event dates
        
        Parameters:
        -----------
        event_window_days : int
            Number of days before and after event to analyze
            
        Returns:
        --------
        pd.DataFrame
            Merged dataset with event and price information
        """
        if self.brent_data is None or self.events_data is None:
            print("✗ Both Brent data and events data must be loaded first.")
            return None
        
        print("Merging events with price data...")
        
        merged_events = []
        
        for _, event in self.events_data.iterrows():
            event_date = event['Date']
            
            # Define window around event
            start_date = event_date - timedelta(days=event_window_days)
            end_date = event_date + timedelta(days=event_window_days)
            
            # Get price data in the window
            price_window = self.brent_data[
                (self.brent_data['Date'] >= start_date) & 
                (self.brent_data['Date'] <= end_date)
            ].copy()
            
            if len(price_window) > 0:
                # Find the price closest to event date
                closest_idx = (price_window['Date'] - event_date).abs().idxmin()
                event_price = price_window.loc[closest_idx, 'Price']
                
                # Calculate price changes in the window
                pre_event_price = price_window[price_window['Date'] < event_date]['Price'].iloc[-1] if len(price_window[price_window['Date'] < event_date]) > 0 else event_price
                post_event_price = price_window[price_window['Date'] > event_date]['Price'].iloc[0] if len(price_window[price_window['Date'] > event_date]) > 0 else event_price
                
                # Calculate percentage changes
                pre_change = ((event_price - pre_event_price) / pre_event_price * 100) if pre_event_price != 0 else 0
                post_change = ((post_event_price - event_price) / event_price * 100) if event_price != 0 else 0
                total_change = ((post_event_price - pre_event_price) / pre_event_price * 100) if pre_event_price != 0 else 0
                
                # Create event record with price information
                event_record = event.copy()
                event_record['Event_Price'] = event_price
                event_record['Pre_Event_Price'] = pre_event_price
                event_record['Post_Event_Price'] = post_event_price
                event_record['Pre_Event_Change_%'] = pre_change
                event_record['Post_Event_Change_%'] = post_change
                event_record['Total_Change_%'] = total_change
                event_record['Price_Window_Size'] = len(price_window)
                
                merged_events.append(event_record)
        
        self.merged_data = pd.DataFrame(merged_events)
        
        print(f"✓ Successfully merged {len(self.merged_data)} events with price data")
        
        return self.merged_data
    
    def detect_outliers(self, price_col='Price', method='iqr', threshold=3):
        """
        Detect outliers in the price data
        
        Parameters:
        -----------
        price_col : str
            Name of the price column
        method : str
            Method for outlier detection ('iqr' or 'zscore')
        threshold : float
            Threshold for outlier detection
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with outlier indicators
        """
        if self.brent_data is None:
            print("✗ Brent data not loaded. Please download data first.")
            return None
        
        print(f"Detecting outliers using {method} method...")
        
        if method == 'iqr':
            Q1 = self.brent_data[price_col].quantile(0.25)
            Q3 = self.brent_data[price_col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = (self.brent_data[price_col] < lower_bound) | (self.brent_data[price_col] > upper_bound)
            
        elif method == 'zscore':
            z_scores = np.abs((self.brent_data[price_col] - self.brent_data[price_col].mean()) / self.brent_data[price_col].std())
            outliers = z_scores > threshold
        
        self.brent_data['Outlier'] = outliers
        
        print(f"✓ Detected {outliers.sum()} outliers ({outliers.sum()/len(outliers)*100:.2f}% of data)")
        
        return self.brent_data
    
    def get_summary_statistics(self):
        """
        Generate comprehensive summary statistics
        
        Returns:
        --------
        dict
            Dictionary containing summary statistics
        """
        if self.brent_data is None:
            print("✗ Brent data not loaded. Please download data first.")
            return None
        
        stats = {
            'total_observations': len(self.brent_data),
            'date_range_start': self.brent_data['Date'].min(),
            'date_range_end': self.brent_data['Date'].max(),
            'price_stats': {
                'min': self.brent_data['Price'].min(),
                'max': self.brent_data['Price'].max(),
                'mean': self.brent_data['Price'].mean(),
                'median': self.brent_data['Price'].median(),
                'std': self.brent_data['Price'].std(),
                'skewness': self.brent_data['Price'].skew(),
                'kurtosis': self.brent_data['Price'].kurtosis()
            }
        }
        
        # Add return statistics if available
        if 'Log_Return' in self.brent_data.columns:
            stats['return_stats'] = {
                'mean': self.brent_data['Log_Return'].mean(),
                'std': self.brent_data['Log_Return'].std(),
                'skewness': self.brent_data['Log_Return'].skew(),
                'kurtosis': self.brent_data['Log_Return'].kurtosis(),
                'volatility': self.brent_data['Log_Return'].std() * np.sqrt(252)  # Annualized
            }
        
        return stats
    
    def save_processed_data(self, brent_path='../data/brent_processed.csv', 
                          events_path='../data/events_processed.csv',
                          merged_path='../data/merged_data.csv'):
        """
        Save processed data to CSV files
        
        Parameters:
        -----------
        brent_path : str
            Path to save processed Brent data
        events_path : str
            Path to save processed events data
        merged_path : str
            Path to save merged data
        """
        if self.brent_data is not None:
            self.brent_data.to_csv(brent_path, index=False)
            print(f"✓ Brent data saved to {brent_path}")
        
        if self.events_data is not None:
            self.events_data.to_csv(events_path, index=False)
            print(f"✓ Events data saved to {events_path}")
        
        if self.merged_data is not None:
            self.merged_data.to_csv(merged_path, index=False)
            print(f"✓ Merged data saved to {merged_path}")


def create_sample_data():
    """
    Create sample data for testing purposes
    """
    print("Creating sample data for testing...")
    
    # Create sample Brent data
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
    n_days = len(dates)
    
    # Simulate price with trend and volatility
    price = 50 + np.cumsum(np.random.normal(0.1, 2, n_days))
    price = np.maximum(price, 10)  # Ensure positive prices
    
    sample_brent = pd.DataFrame({
        'Date': dates,
        'Price': price
    })
    
    # Create sample events
    sample_events = pd.DataFrame({
        'Date': pd.to_datetime(['2020-03-15', '2020-11-03', '2021-01-06', '2022-02-24']),
        'Event': ['COVID Pandemic Declared', 'US Election', 'Capitol Riot', 'Ukraine Invasion'],
        'Type': ['Health Crisis', 'Political Event', 'Political Unrest', 'Military Conflict'],
        'Description': ['WHO declares global pandemic', 'US Presidential Election', 'US Capitol attack', 'Russia invades Ukraine'],
        'Expected_Impact': ['High', 'Medium', 'Medium', 'High']
    })
    
    print("✓ Sample data created successfully")
    
    return sample_brent, sample_events


if __name__ == "__main__":
    # Example usage
    processor = BrentOilDataProcessor()
    
    # Download data
    brent_data = processor.download_brent_data()
    
    # Load events
    events_data = processor.load_events_data('../data/geopolitical_events.csv')
    
    if brent_data is not None and events_data is not None:
        # Process data
        processor.calculate_returns()
        processor.add_rolling_statistics()
        processor.merge_events_with_prices()
        
        # Get summary statistics
        stats = processor.get_summary_statistics()
        print("\nSummary Statistics:")
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        # Save processed data
        processor.save_processed_data()
