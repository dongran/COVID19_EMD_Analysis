# -*- coding: utf-8 -*-
"""
Data Loading Module

Responsible for loading and preprocessing COVID-19 related data
"""

import numpy as np
import pandas as pd
from csv import reader
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """COVID-19 data loader"""
    
    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        self.date_formats = {
            "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
            "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", 
            "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
        }
        
    def load_tokyo_covid_data(self, date_folder: str = "20211006", days: int = 525) -> Dict[str, np.ndarray]:
        """
        Load Tokyo COVID-19 data
        
        Parameters:
        -----------
        date_folder : str
            Data folder name (e.g., "20211006") 
        days : int
            Number of days to load
            
        Returns:
        --------
        Dict[str, np.ndarray]
            Dictionary containing various COVID-19 data
        """
        try:
            # Load infection data
            infection_file = f'{self.data_path}/{date_folder}/130001_tokyo_covid19_details_testing_positive_cases.csv'
            with open(infection_file, 'r', encoding="utf-8-sig") as csv_file:
                csv_reader = reader(csv_file)
                list_of_rows = list(csv_reader)
            
            date = []
            for i in range(1, len(list_of_rows)):
                date.append(list_of_rows[i][3])
            
            # Calculate daily new infections
            infect = [0]
            hosp = [0]
            mild = [0]
            severe = [0]
            
            for i in range(1, len(list_of_rows)-1):
                infect.append(int(list_of_rows[i + 1][4]) - int(list_of_rows[i][4]))
                hosp.append(int(list_of_rows[i + 1][5]) - int(list_of_rows[i][5]))
                mild.append(int(list_of_rows[i + 1][6]) - int(list_of_rows[i][6]))
                severe.append(int(list_of_rows[i + 1][7]) - int(list_of_rows[i][7]))
            
            # Try to load testing data (might not exist in all datasets)
            try:
                test_file = f'{self.data_path}/{date_folder}/130001_tokyo_covid19_positivity_rate_in_testing.csv'
                with open(test_file, 'r', encoding="utf-8-sig") as csv_file:
                    csv_reader = reader(csv_file)
                    list_of_rows = list(csv_reader)
                    
                test_num = []
                test_positive = []
                test_pos_rate = []
                
                for i in range(1, len(list_of_rows)):
                    test_positive.append(int(list_of_rows[i][4]))
                    test_num.append(int(list_of_rows[i][6]))
                    
                    if list_of_rows[i][6] == "0":
                        test_pos_rate.append(0.0)
                    else:
                        test_pos_rate.append(int(list_of_rows[i][4]) / int(list_of_rows[i][6]))
            except FileNotFoundError:
                # If testing data doesn't exist, create dummy data
                logger.warning("Testing data file not found, using dummy data")
                test_positive = [0] * len(infect)
                test_num = [0] * len(infect)
                test_pos_rate = [0.0] * len(infect)
            
            # Format dates
            formatted_dates = self._format_dates(date)
            
            # Extract data for specified number of days
            data = {
                'dates': date[-days:],
                'formatted_dates': formatted_dates[-days:],
                'infections': np.array(infect[-days:], dtype='float64'),
                'hospitalizations': np.array(hosp[-days:], dtype='float64'),
                'mild_cases': np.array(mild[-days:], dtype='float64'),
                'severe_cases': np.array(severe[-days:], dtype='float64'),
                'test_positive': np.array(test_positive[-days:], dtype='float64'),
                'test_numbers': np.array(test_num[-days:], dtype='float64'),
                'positivity_rate': np.array(test_pos_rate[-days:], dtype='float64')
            }
            
            logger.info(f"Successfully loaded COVID-19 data for {days} days from {date_folder}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load COVID-19 data: {e}")
            raise
    
    def _format_dates(self, dates: List[str]) -> List[str]:
        """
        Format dates from YYYY-MM-DD to human-readable format
        
        Parameters:
        -----------
        dates : List[str]
            List of date strings in YYYY-MM-DD format
            
        Returns:
        --------
        List[str]
            List of formatted date strings
        """
        formatted = []
        for date in dates:
            parts = date.split('-')
            if len(parts) == 3:
                year, month, day = parts
                month_name = self.date_formats.get(month, month)
                formatted.append(f"{month_name} {day}, {year}")
            else:
                formatted.append(date)
        return formatted
    
    def get_event_dates(self) -> Dict[str, List[str]]:
        """
        Get important event dates during COVID-19 pandemic
        
        Returns:
        --------
        Dict[str, List[str]]
            Dictionary with event names and corresponding dates
        """
        return {
            'state_of_emergency': ['2020-04-07', '2021-01-07', '2021-04-25'],
            'olympics': ['2021-07-23', '2021-08-08'],
            'vaccination_start': ['2021-02-17'],
            'new_variants': ['2021-01-01', '2021-05-01']
        } 