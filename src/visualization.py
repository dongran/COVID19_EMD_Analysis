# -*- coding: utf-8 -*-
"""
Visualization Module

Provides visualization functions for EMD analysis results
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple
import logging

# Set Chinese font support
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EMDVisualizer:
    """EMD visualizer"""
    
    def __init__(self, style: str = "default", figsize: Tuple[int, int] = (20, 15)):
        """
        Initialize visualizer
        
        Parameters:
        -----------
        style : str
            matplotlib style
        figsize : tuple
            figure size
        """
        self.style = style
        self.figsize = figsize
        self._setup_style()
        
    def _setup_style(self):
        """Set plotting style"""
        plt.style.use(self.style)
        
        # Set plotting parameters
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["font.size"] = 25
        plt.rcParams['axes.linewidth'] = 3
        plt.rcParams["xtick.direction"] = 'in'
        plt.rcParams["ytick.direction"] = 'in'
        plt.rcParams['xtick.major.width'] = 3
        plt.rcParams['ytick.major.width'] = 3
        plt.rcParams['xtick.minor.width'] = 3
        plt.rcParams['ytick.minor.width'] = 3
        plt.rcParams['xtick.major.size'] = 10
        plt.rcParams['ytick.major.size'] = 10
        plt.rcParams['xtick.minor.size'] = 10
        plt.rcParams['ytick.minor.size'] = 10
        
    def plot_original_signal(self, signal: np.ndarray, dates: List[str] = None, 
                           title: str = "Original Signal", ylabel: str = "Value",
                           events: Dict[str, List[str]] = None, 
                           date_indices: List[int] = None) -> plt.Figure:
        """
        Plot original signal
        
        Parameters:
        -----------
        signal : np.ndarray
            Original signal
        dates : List[str]
            Date labels
        title : str
            Plot title
        ylabel : str
            Y-axis label
        events : Dict[str, List[str]]
            Event dates
        date_indices : List[int]
            Date indices
            
        Returns:
        --------
        plt.Figure
            Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=200)
        
        t = np.arange(len(signal))
        ax.plot(t, signal, 'b-', linewidth=3, label="Original Signal")
        
        # Set date labels
        if dates and date_indices:
            values = [dates[i] for i in date_indices if i < len(dates)]
            ax.set_xticks(date_indices)
            ax.set_xticklabels(values, rotation=30)
        
        # Add event lines
        if events and dates:
            self._add_event_lines(ax, events, dates, signal)
        
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_imfs(self, imfs: np.ndarray, dates: List[str] = None,
                  date_indices: List[int] = None, title_prefix: str = "IMF") -> plt.Figure:
        """
        Plot all IMF components
        
        Parameters:
        -----------
        imfs : np.ndarray
            IMF components
        dates : List[str]
            Date labels
        date_indices : List[int]
            Date indices
        title_prefix : str
            Title prefix
            
        Returns:
        --------
        plt.Figure
            Figure object
        """
        n_imfs = imfs.shape[0]
        fig, axes = plt.subplots(n_imfs, 1, figsize=(self.figsize[0], self.figsize[1] * n_imfs // 5))
        
        if n_imfs == 1:
            axes = [axes]
        
        t = np.arange(imfs.shape[1])
        
        for i, ax in enumerate(axes):
            if i < n_imfs - 1:
                ax.plot(t, imfs[i], 'g-', linewidth=2)
                ax.set_title(f"{title_prefix} {i+1}")
            else:
                ax.plot(t, imfs[i], 'r-', linewidth=2)
                ax.set_title("Residual")
            
            ax.locator_params(axis='y', nbins=5)
            
            # Set date labels
            if dates and date_indices:
                values = [dates[i] for i in date_indices if i < len(dates)]
                ax.set_xticks(date_indices)
                ax.set_xticklabels(values, rotation=30)
            
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_hilbert_spectrum(self, frequencies: np.ndarray, amplitudes: np.ndarray,
                            dates: List[str] = None, date_indices: List[int] = None,
                            title: str = "Hilbert Spectrum") -> plt.Figure:
        """
        Plot Hilbert spectrum
        
        Parameters:
        -----------
        frequencies : np.ndarray
            Frequency array
        amplitudes : np.ndarray
            Amplitude array
        dates : List[str]
            Date labels
        date_indices : List[int]
            Date indices
        title : str
            Plot title
            
        Returns:
        --------
        plt.Figure
            Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=200)
        
        n_samples, n_imfs = frequencies.shape
        t = np.arange(n_samples)
        
        # Create time-frequency grid
        t_grid = np.zeros((n_samples, n_imfs))
        for i in range(n_imfs):
            t_grid[:, i] = t
        
        # Plot scatter plot
        scatter = ax.scatter(t_grid, frequencies, s=100, c=amplitudes, cmap='jet')
        
        ax.set_facecolor([0.0, 0.0, 0.5])
        ax.set_ylim(0, 0.4)
        ax.set_xlim(0, n_samples)
        
        # Set date labels
        if dates and date_indices:
            values = [dates[i] for i in date_indices if i < len(dates)]
            ax.set_xticks(date_indices)
            ax.set_xticklabels(values, rotation=30)
        
        ax.set_title(title)
        ax.set_ylabel('Frequency (cycle per day)')
        
        plt.colorbar(scatter)
        plt.tight_layout()
        return fig
    
    def plot_period_spectrum(self, frequencies: np.ndarray, amplitudes: np.ndarray,
                           dates: List[str] = None, date_indices: List[int] = None,
                           title: str = "Period Spectrum") -> plt.Figure:
        """
        Plot period spectrum
        
        Parameters:
        -----------
        frequencies : np.ndarray
            Frequency array
        amplitudes : np.ndarray
            Amplitude array
        dates : List[str]
            Date labels
        date_indices : List[int]
            Date indices
        title : str
            Plot title
            
        Returns:
        --------
        plt.Figure
            Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=200)
        
        n_samples, n_imfs = frequencies.shape
        t = np.arange(n_samples)
        
        # Create time-period grid
        t_grid = np.zeros((n_samples, n_imfs))
        periods = 1 / frequencies
        periods[frequencies == 0] = 0  # Avoid division by zero
        
        for i in range(n_imfs):
            t_grid[:, i] = t
        
        # Plot scatter plot
        scatter = ax.scatter(t_grid, periods, s=100, c=amplitudes, cmap='jet')
        
        ax.set_facecolor([0.0, 0.0, 0.5])
        ax.set_ylim(0, 500)
        ax.set_xlim(0, n_samples)
        
        # Set date labels
        if dates and date_indices:
            values = [dates[i] for i in date_indices if i < len(dates)]
            ax.set_xticks(date_indices)
            ax.set_xticklabels(values, rotation=30)
        
        ax.set_title(title)
        ax.set_ylabel('Period (day)')
        
        plt.colorbar(scatter)
        plt.tight_layout()
        return fig
    
    def plot_single_imf_spectrum(self, frequencies: np.ndarray, amplitudes: np.ndarray,
                               imf_index: int, dates: List[str] = None,
                               date_indices: List[int] = None) -> plt.Figure:
        """
        Plot single IMF spectrum
        
        Parameters:
        -----------
        frequencies : np.ndarray
            Frequency array
        amplitudes : np.ndarray
            Amplitude array
        imf_index : int
            IMF index
        dates : List[str]
            Date labels
        date_indices : List[int]
            Date indices
            
        Returns:
        --------
        plt.Figure
            Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=200)
        
        t = np.arange(frequencies.shape[0])
        
        # Plot scatter plot
        scatter = ax.scatter(t, frequencies[:, imf_index], s=100, 
                           c=amplitudes[:, imf_index], cmap='binary')
        
        ax.set_facecolor([0.0, 0.0, 0.5])
        ax.set_ylim(0, 0.1)
        ax.set_xlim(0, len(t))
        
        # Set date labels
        if dates and date_indices:
            values = [dates[i] for i in date_indices if i < len(dates)]
            ax.set_xticks(date_indices)
            ax.set_xticklabels(values, rotation=30)
        
        ax.set_title(f'IMF {imf_index + 1} Spectrum')
        ax.set_ylabel('Frequency (cycle per day)')
        
        plt.colorbar(scatter)
        plt.tight_layout()
        return fig
    

    
    def _add_event_lines(self, ax: plt.Axes, events: Dict[str, List[str]], 
                        dates: List[str], signal: np.ndarray):
        """Add event vertical lines"""
        event_styles = {
            'emergency_state_1': {'color': 'red', 'linestyle': (0, (5, 3, 1, 3, 1, 3)), 'alpha': 0.6, 'lw': 2},
            'emergency_state_2': {'color': 'green', 'linestyle': '-.', 'alpha': 0.6, 'lw': 2},
            'emergency_state_3': {'color': '#4b0082', 'linestyle': '--', 'alpha': 0.6, 'lw': 2},
            'stay_home': {'color': '#d2691e', 'linestyle': ':', 'alpha': 0.6, 'lw': 2},
            'new_year': {'color': '#9acd32', 'linestyle': (10, (5, 3, 1, 3, 1, 3)), 'alpha': 0.6, 'lw': 2},
            'go_to_travel': {'color': '#d1391e', 'linestyle': '--', 'alpha': 0.6, 'lw': 2},
            'tokyo_alert': {'color': '#6acd22', 'linestyle': '-.', 'alpha': 0.6, 'lw': 2},
            'go_to_eat': {'color': '#3acd17', 'linestyle': ':', 'alpha': 0.6, 'lw': 2}
        }
        
        y_min, y_max = ax.get_ylim()
        
        for event_type, event_dates in events.items():
            if event_type in event_styles:
                style = event_styles[event_type]
                try:
                    event_indices = [dates.index(date) for date in event_dates if date in dates]
                    ax.vlines(event_indices, y_min, y_max, **style)
                except ValueError:
                    continue  # Skip if date is not in the list
    
    def save_figure(self, fig: plt.Figure, filename: str, dpi: int = 300):
        """
        Save figure
        
        Parameters:
        -----------
        fig : plt.Figure
            Figure object
        filename : str
            Filename
        dpi : int
            Resolution
        """
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        logger.info(f"Figure saved to: {filename}")
    
    def show_figure(self, fig: plt.Figure):
        """Display figure (disabled for automated execution)"""
        # plt.show()  # Commented out for automated execution
        pass
    
    def close_figure(self, fig: plt.Figure):
        """Close figure"""
        plt.close(fig) 