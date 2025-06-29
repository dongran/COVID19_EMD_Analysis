#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COVID-19 EMD Analysis Simple Demo

Simple demonstration of EMD analysis using Tokyo COVID-19 infection data
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
from data_loader import DataLoader
from emd_analyzer import EMDAnalyzer
from visualization import EMDVisualizer


def main():
    """Simple demo using COVID-19 data"""
    print("=" * 50)
    print("COVID-19 EMD Analysis - Simple Demo")
    print("=" * 50)
    
    # 1. Load Tokyo COVID-19 data
    print("\n1. Loading Tokyo COVID-19 data...")
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    loader = DataLoader(data_path=data_path)
    covid_data = loader.load_tokyo_covid_data("20211006", days=300)
    
    daily_infections = covid_data['infections']
    dates = covid_data['formatted_dates']
    
    print(f"✅ Loaded {len(daily_infections)} days of infection data")
    print(f"   Data period: {dates[0]} to {dates[-1]}")
    print(f"   Max daily infections: {int(np.max(daily_infections))}")
    print(f"   Mean daily infections: {np.mean(daily_infections):.1f}")
    
    # 2. EMD analysis
    print("\n2. Performing EMD analysis...")
    analyzer = EMDAnalyzer()
    covid_results = analyzer.analyze_signal(daily_infections, "tokyo_covid_infections")
    
    print(f"✅ EMD decomposition completed:")
    print(f"   Number of IMFs: {covid_results['n_imfs']}")
    print(f"   Signal successfully decomposed")
    
    # 3. Display IMF statistics
    print("\n3. IMF Analysis Results:")
    stats = covid_results['statistics']
    for i, (freq, period, amp) in enumerate(zip(
        stats['mean_frequencies'], 
        stats['mean_periods'], 
        stats['mean_amplitudes']
    )):
        if freq > 0:
            print(f"   IMF {i+1}: Frequency={freq:.4f}/day, Period={period:.1f} days, Amplitude={amp:.1f}")
    
    # 4. Energy analysis
    print("\n4. Energy Analysis:")
    imfs = covid_results['imfs']
    energies = [np.sum(imf**2) for imf in imfs]
    total_energy = sum(energies)
    
    for i, energy in enumerate(energies[:-1]):  # Exclude residue
        percentage = (energy / total_energy) * 100
        print(f"   IMF {i+1}: {percentage:.1f}% of total energy")
    
    residue_percentage = (energies[-1] / total_energy) * 100
    print(f"   Residue: {residue_percentage:.1f}% of total energy")
    
    # 5. Visualization
    print("\n5. Creating visualizations...")
    visualizer = EMDVisualizer(figsize=(12, 8))
    
    # Date indices for plotting
    date_indices = list(range(0, len(dates), max(1, len(dates)//8)))
    
    # Plot original signal
    fig1 = visualizer.plot_original_signal(
        daily_infections,
        dates=dates,
        title="Tokyo COVID-19 Daily New Infections",
        ylabel="Daily New Cases",
        date_indices=date_indices
    )
    
    # Plot IMFs (first 5 components)
    n_plot_imfs = min(5, covid_results['n_imfs'])
    fig2 = visualizer.plot_imfs(
        covid_results['imfs'][:n_plot_imfs],
        dates=dates,
        date_indices=date_indices,
        title_prefix="COVID-19 IMF"
    )
    
    # Plot Hilbert spectrum
    fig3 = visualizer.plot_hilbert_spectrum(
        covid_results['frequencies'],
        covid_results['amplitudes'],
        dates=dates,
        date_indices=date_indices,
        title="COVID-19 Infection Hilbert Spectrum"
    )
    
    # Show summary statistics
    print("\n6. Summary:")
    print(f"   🔍 Analysis of {len(daily_infections)} days of COVID-19 infection data")
    print(f"   📊 Decomposed into {covid_results['n_imfs']} intrinsic mode functions")
    print(f"   📈 Frequency range: {stats['mean_frequencies'][-1]:.4f} - {stats['mean_frequencies'][0]:.4f} Hz")
    print(f"   ⏰ Period range: {stats['mean_periods'][0]:.1f} - {stats['mean_periods'][-1]:.1f} days")
    print(f"   📋 IMF components reveal different temporal scales in infection patterns")
    
    # Interpretation
    print("\n7. Interpretation:")
    print("   • High-frequency IMFs (IMF1-2): Daily fluctuations and noise")
    print("   • Medium-frequency IMFs (IMF3-4): Weekly patterns and short-term trends")
    print("   • Low-frequency IMFs (IMF5+): Long-term epidemic waves and trends")
    print("   • Residue: Overall epidemic progression trend")
    
    plt.show()
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main() 