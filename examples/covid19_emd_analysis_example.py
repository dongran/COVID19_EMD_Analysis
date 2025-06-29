#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COVID-19 EMD Analysis Example

This example demonstrates how to use the COVID-19 EMD Analysis package
to analyze COVID-19 infection data using Empirical Mode Decomposition.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add the src directory to the path to import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import DataLoader
from emd_analyzer import EMDAnalyzer
from visualization import EMDVisualizer

def main():
    """Main analysis function"""
    
    print("🦠 COVID-19 EMD Analysis Example")
    print("=" * 50)
    
    # Initialize data loader
    data_loader = DataLoader(data_path="data")
    
    # Load COVID-19 data
    print("\n📊 Loading COVID-19 data...")
    covid_data = data_loader.load_tokyo_covid_data(
        date_folder="20211006",
        days=525
    )
    
    # Display data info
    print(f"✅ Data loaded successfully:")
    print(f"   - Time period: {covid_data['dates'][0]} to {covid_data['dates'][-1]}")
    print(f"   - Total days: {len(covid_data['infections'])}")
    print(f"   - Max daily infections: {int(np.max(covid_data['infections']))}")
    print(f"   - Average daily infections: {int(np.mean(covid_data['infections']))}")
    
    # Perform EMD analysis
    print("\n🔍 Performing EMD analysis...")
    emd_analyzer = EMDAnalyzer()
    
    # Analyze infections data
    covid_results = emd_analyzer.analyze_signal(covid_data['infections'], "tokyo_covid_infections")
    covid_imfs = covid_results['imfs']
    
    print(f"✅ EMD decomposition completed:")
    print(f"   - Number of IMFs: {len(covid_imfs) - 1}")  # Exclude residue
    print(f"   - IMF shapes: {[imf.shape for imf in covid_imfs]}")
    
    # Analyze frequency characteristics
    print("\n📈 Analyzing frequency characteristics...")
    freq_analysis = covid_results['statistics']
    
    print("\n🎯 Frequency Analysis Results:")
    for i, (freq, period) in enumerate(zip(freq_analysis['mean_frequencies'], 
                                         freq_analysis['mean_periods'])):
        if freq > 0:
            print(f"   IMF{i+1}: {freq:.4f} Hz (Period: {period:.1f} days)")
    
    # Create visualizations
    print("\n🎨 Creating visualizations...")
    visualizer = EMDVisualizer()
    
    # Create results directory if it doesn't exist
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # 1. Plot original signal
    date_indices = list(range(0, len(covid_data['formatted_dates']), 30))
    fig1 = visualizer.plot_original_signal(
        covid_data['infections'],
        dates=covid_data['formatted_dates'],
        title="COVID-19 Daily Infections - Original Signal",
        ylabel="Daily New Cases",
        date_indices=date_indices
    )
    
    output_file1 = os.path.join(results_dir, "covid19_original_signal.png")
    fig1.savefig(output_file1, dpi=300, bbox_inches='tight')
    print(f"   📁 Original signal plot saved: {output_file1}")
    
    # 2. Plot IMF components
    fig2 = visualizer.plot_imfs(
        covid_imfs,
        dates=covid_data['formatted_dates'],
        date_indices=date_indices,
        title_prefix="COVID-19 IMF"
    )
    
    output_file2 = os.path.join(results_dir, "covid19_imf_components.png")
    fig2.savefig(output_file2, dpi=300, bbox_inches='tight')
    print(f"   📁 IMF components plot saved: {output_file2}")
    
    # 3. Plot Hilbert spectrum
    fig3 = visualizer.plot_hilbert_spectrum(
        covid_results['frequencies'],
        covid_results['amplitudes'],
        dates=covid_data['formatted_dates'],
        date_indices=date_indices,
        title="COVID-19 IMFs - Hilbert Spectrum"
    )
    
    output_file3 = os.path.join(results_dir, "covid19_hilbert_spectrum.png")
    fig3.savefig(output_file3, dpi=300, bbox_inches='tight')
    print(f"   📁 Hilbert spectrum plot saved: {output_file3}")
    
    # Statistical analysis
    print("\n📊 Statistical Analysis:")
    print(f"   - Total variance: {np.var(covid_data['infections']):.2f}")
    
    # Calculate variance contribution of each IMF
    imf_variances = [np.var(imf) for imf in covid_imfs]
    total_variance = sum(imf_variances)
    
    print("\n📈 IMF Variance Contributions:")
    for i, var in enumerate(imf_variances[:-1]):  # Exclude residue
        percentage = (var / total_variance) * 100
        print(f"   IMF{i+1}: {percentage:.1f}% (variance: {var:.2f})")
    
    # Residue
    residue_var = imf_variances[-1]
    residue_percentage = (residue_var / total_variance) * 100
    print(f"   Residue: {residue_percentage:.1f}% (variance: {residue_var:.2f})")
    
    # Energy analysis
    print("\n⚡ Energy Analysis:")
    imf_energies = [np.sum(imf**2) for imf in covid_imfs]
    total_energy = sum(imf_energies)
    
    for i, energy in enumerate(imf_energies[:-1]):  # Exclude residue
        percentage = (energy / total_energy) * 100
        print(f"   IMF{i+1}: {percentage:.1f}% (energy: {energy:.0f})")
    
    residue_energy = imf_energies[-1]
    residue_energy_percentage = (residue_energy / total_energy) * 100
    print(f"   Residue: {residue_energy_percentage:.1f}% (energy: {residue_energy:.0f})")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 Analysis Summary:")
    print(f"   - COVID-19 infection data successfully decomposed into {len(covid_imfs)-1} IMFs")
    print(f"   - Frequency range: {freq_analysis['mean_frequencies'][-1]:.4f} - {freq_analysis['mean_frequencies'][0]:.4f} Hz")
    print(f"   - Period range: {freq_analysis['mean_periods'][0]:.1f} - {freq_analysis['mean_periods'][-1]:.1f} days")
    print(f"   - All visualizations saved to '{results_dir}' directory")
    
    # Show the plots
    plt.show()
    
    print("\n✅ Analysis completed successfully!")

if __name__ == "__main__":
    main() 