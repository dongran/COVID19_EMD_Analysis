# -*- coding: utf-8 -*-
"""
EMD Analysis Core Module

Using Empirical Mode Decomposition to analyze COVID-19 data
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
from scipy.signal import hilbert
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EMD:
    """Empirical Mode Decomposition implementation"""
    
    def __init__(self, max_iterations: int = 1000, std_threshold: float = 0.2):
        self.max_iterations = max_iterations
        self.std_threshold = std_threshold
        
    def __call__(self, signal: np.ndarray) -> np.ndarray:
        """Execute EMD decomposition"""
        return self.emd(signal)
    
    def emd(self, signal: np.ndarray) -> np.ndarray:
        """
        Execute Empirical Mode Decomposition
        
        Parameters:
        -----------
        signal : np.ndarray
            Input signal
            
        Returns:
        --------
        np.ndarray
            IMF components, shape (n_imfs, signal_length)
        """
        try:
            from PyEMD import EMD as PyEMD_EMD
            emd = PyEMD_EMD()
            imfs = emd(signal)
            logger.info(f"EMD decomposition completed, generated {imfs.shape[0]} IMF components")
            return imfs
        except ImportError:
            logger.warning("PyEMD not installed, using simplified EMD implementation")
            return self._simple_emd(signal)
    
    def _simple_emd(self, signal: np.ndarray) -> np.ndarray:
        """Simplified EMD implementation (for when PyEMD is not available)"""
        # This provides a basic EMD implementation
        # For production use, it's recommended to use the PyEMD library
        imfs = []
        residue = signal.copy()
        
        for i in range(10):  # Maximum 10 IMFs
            if len(residue) < 4:
                break
                
            # Simple sifting process
            imf = self._sift(residue)
            if np.std(imf) < 1e-10:
                break
                
            imfs.append(imf)
            residue = residue - imf
            
        if np.std(residue) > 1e-10:
            imfs.append(residue)
            
        return np.array(imfs)
    
    def _sift(self, signal: np.ndarray) -> np.ndarray:
        """Simple sifting process"""
        # This is a very simplified implementation
        # For real applications, please use complete EMD algorithm
        return signal * 0.1  # Placeholder implementation


class HilbertTransform:
    """Hilbert Transform analysis"""
    
    @staticmethod
    def compute_instantaneous_frequency(imfs: np.ndarray, dt: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute instantaneous frequency and amplitude
        
        Parameters:
        -----------
        imfs : np.ndarray
            IMF components
        dt : float
            Sampling interval
            
        Returns:
        --------
        Tuple[np.ndarray, np.ndarray]
            Frequency and amplitude arrays
        """
        n_imfs = imfs.shape[0]
        frequencies = []
        amplitudes = []
        
        for i in range(n_imfs - 1):  # Exclude residue term
            # Compute analytic signal
            analytic_signal = hilbert(imfs[i])
            amplitude = np.abs(analytic_signal)
            phase = np.unwrap(np.angle(analytic_signal))
            
            # Compute instantaneous frequency
            freq = (1/dt) * np.diff(phase) / (2 * math.pi)
            freq = np.append(freq, freq[-1])  # Keep consistent length
            
            # Ensure amplitude and frequency arrays have consistent length
            if len(amplitude) > len(freq):
                amplitude = amplitude[:len(freq)]
            elif len(freq) > len(amplitude):
                freq = freq[:len(amplitude)]
            
            frequencies.append(freq)
            amplitudes.append(amplitude)
            
        return np.array(frequencies).T, np.array(amplitudes).T
    
    @staticmethod
    def wafa_smoothing(frequencies: np.ndarray, amplitudes: np.ndarray, window: int = 30) -> np.ndarray:
        """
        WAFA smoothing processing
        
        Parameters:
        -----------
        frequencies : np.ndarray
            Frequency array
        amplitudes : np.ndarray
            Amplitude array
        window : int
            Smoothing window size
            
        Returns:
        --------
        np.ndarray
            Smoothed frequency
        """
        smoothed_freq = frequencies.copy()
        n_samples, n_imfs = frequencies.shape
        
        for i in range(n_imfs):
            for j in range(window//2, n_samples - window//2):
                weights = amplitudes[j-window//2:j+window//2+1, i]
                freqs = frequencies[j-window//2:j+window//2+1, i]
                
                if np.sum(weights) > 0:
                    smoothed_freq[j, i] = np.sum(weights * freqs) / np.sum(weights)
                    
        return smoothed_freq


class EMDAnalyzer:
    """Main EMD analyzer class"""
    
    def __init__(self):
        self.emd = EMD()
        self.hilbert = HilbertTransform()
        self.results = {}
        
    def analyze_signal(self, signal: np.ndarray, signal_name: str = "signal", 
                      dt: float = 1.0) -> Dict:
        """
        Analyze signal
        
        Parameters:
        -----------
        signal : np.ndarray
            Input signal
        signal_name : str
            Signal name
        dt : float
            Sampling interval
            
        Returns:
        --------
        Dict
            Analysis results
        """
        logger.info(f"Starting signal analysis: {signal_name}")
        
        # EMD decomposition
        imfs = self.emd(signal)
        
        # Hilbert transform
        frequencies, amplitudes = self.hilbert.compute_instantaneous_frequency(imfs, dt)
        
        # WAFA smoothing
        smoothed_frequencies = self.hilbert.wafa_smoothing(frequencies, amplitudes)
        
        # Compute statistics
        statistics = self._compute_statistics(imfs, smoothed_frequencies, amplitudes)
        
        # Store results
        result = {
            'signal_name': signal_name,
            'original_signal': signal,
            'imfs': imfs,
            'n_imfs': imfs.shape[0],
            'frequencies': smoothed_frequencies,
            'amplitudes': amplitudes,
            'statistics': statistics,
            'dt': dt
        }
        
        self.results[signal_name] = result
        logger.info(f"Signal analysis completed: {signal_name}")
        
        return result
    
    def _compute_statistics(self, imfs: np.ndarray, frequencies: np.ndarray, 
                          amplitudes: np.ndarray) -> Dict:
        """
        Compute statistical measures
        
        Parameters:
        -----------
        imfs : np.ndarray
            IMF components
        frequencies : np.ndarray
            Frequency array
        amplitudes : np.ndarray
            Amplitude array
            
        Returns:
        --------
        Dict
            Statistical results
        """
        n_imfs = frequencies.shape[1]
        
        mean_frequencies = []
        mean_periods = []
        mean_amplitudes = []
        
        for i in range(n_imfs):
            # Mean frequency (weighted by amplitude)
            freq = frequencies[:, i]
            amp = amplitudes[:, i]
            
            if np.sum(amp) > 0:
                mean_freq = np.sum(amp * freq) / np.sum(amp)
            else:
                mean_freq = 0
            
            mean_frequencies.append(mean_freq)
            
            # Mean period
            if mean_freq > 0:
                mean_periods.append(1.0 / mean_freq)
            else:
                mean_periods.append(0)
            
            # Mean amplitude
            mean_amplitudes.append(np.mean(amp))
        
        return {
            'mean_frequencies': mean_frequencies,
            'mean_periods': mean_periods,
            'mean_amplitudes': mean_amplitudes
        }
    
    def get_analysis_results(self, signal_name: str) -> Optional[Dict]:
        """Get analysis results for a specific signal"""
        return self.results.get(signal_name)
    
    def list_analyzed_signals(self) -> List[str]:
        """List all analyzed signal names"""
        return list(self.results.keys()) 