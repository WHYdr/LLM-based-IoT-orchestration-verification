#!/usr/bin/env python3
"""
Performance Charts Generator for IoT Configuration Validation Framework
Generates comprehensive performance visualization charts including type accuracy,
verification accuracy, and time consumption analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
import argparse
import sys

class PerformanceChartGenerator:
    """
    Performance chart generator for IoT configuration validation framework.
    Creates comprehensive visualization charts from test result data.
    """
    
    def __init__(self, csv_file_path=None):
        """
        Initialize the chart generator with data source and configuration.
        
        Args:
            csv_file_path (str): Path to the CSV file containing test results
        """
        self.csv_file_path = r"C:\Users\LENOVO\Desktop\LLM based IoT orchestration & verification\enhanced_test_report_20251013_122455.csv" #an example path and file
        self.df = None
        self.type_mapping = {
            'SD': 'Sensor Device',
            'AD': 'Actuator Device', 
            'GW': 'Gateway',
            'CP': 'Communication Protocol',
            'SC': 'Security Configuration'
        }
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        plt.rcParams['font.size'] = 20
        plt.rcParams['axes.titlesize'] = 22
        plt.rcParams['axes.labelsize'] = 20
        plt.rcParams['xtick.labelsize'] = 18
        plt.rcParams['ytick.labelsize'] = 18
        plt.rcParams['legend.fontsize'] = 18
        
    def load_data(self, csv_file_path=None):
        """
        Load test result data from CSV file.
        
        Args:
            csv_file_path (str): Path to CSV file containing test results
            
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        if csv_file_path:
            self.csv_file_path = csv_file_path
            
        if not self.csv_file_path:
            raise ValueError("No CSV file path provided")
            
        try:
            self.df = pd.read_csv(self.csv_file_path)
            print(f"Successfully loaded data from: {self.csv_file_path}")
            print(f"Total records: {len(self.df)}")
            return True
        except FileNotFoundError:
            print(f"Error: CSV file not found at {self.csv_file_path}")
            return False
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return False
    
    def prepare_data(self):
        """
        Prepare and clean the data for analysis.
        Handles data cleaning, type conversion, and feature engineering.
        """
        if self.df is None:
            raise ValueError("Data not loaded. Please call load_data() first.")
            
        # Clean the data
        self.df = self.df.dropna(subset=['Expected Type', 'Type Accuracy', 'Verification Accuracy'])
        
        # Convert boolean columns
        self.df['Type Accuracy'] = self.df['Type Accuracy'].astype(bool)
        self.df['Verification Accuracy'] = self.df['Verification Accuracy'].astype(bool)
        
        # Add full type names
        self.df['Type Full Name'] = self.df['Expected Type'].map(self.type_mapping)
        
        print(f"Data prepared. Clean records: {len(self.df)}")
        
    def calculate_accuracy_stats(self):
        """
        Calculate accuracy statistics by verification type.
        
        Returns:
            pd.DataFrame: Accuracy statistics for each verification type
        """
        accuracy_stats = []
        
        for vtype in ['SD', 'AD', 'GW', 'CP', 'SC']:
            type_data = self.df[self.df['Expected Type'] == vtype]
            
            if len(type_data) > 0:
                type_accuracy = type_data['Type Accuracy'].mean() * 100
                verification_accuracy = type_data['Verification Accuracy'].mean() * 100
                total_tests = len(type_data)
                
                accuracy_stats.append({
                    'Type': vtype,
                    'Type Full Name': self.type_mapping[vtype],
                    'Type Accuracy (%)': type_accuracy,
                    'Verification Accuracy (%)': verification_accuracy,
                    'Total Tests': total_tests
                })
        
        return pd.DataFrame(accuracy_stats)
    
    def calculate_time_stats(self):
        """
        Calculate average time statistics by verification type.
        
        Returns:
            pd.DataFrame: Time statistics for each verification type
        """
        time_stats = []
        
        for vtype in ['SD', 'AD', 'GW', 'CP', 'SC']:
            type_data = self.df[self.df['Expected Type'] == vtype]
            
            if len(type_data) > 0:
                avg_total_time = type_data['Total Time'].mean()
                avg_translate_time = type_data['Translate Time'].mean()
                avg_config_time = type_data['Config Time'].mean()
                avg_verify_time = type_data['Verify Time'].mean()
                
                time_stats.append({
                    'Type': vtype,
                    'Type Full Name': self.type_mapping[vtype],
                    'Total Time (s)': avg_total_time,
                    'Translate Time (s)': avg_translate_time,
                    'Config Time (s)': avg_config_time,
                    'Verify Time (s)': avg_verify_time
                })
        
        return pd.DataFrame(time_stats)
    
    
    
    def create_combined_accuracy_chart(self, save_path=None):
        """
        Create combined type accuracy and verification accuracy visualization chart.
        Sorted by Verification Accuracy from high to low.
        
        Args:
            save_path (str): Path to save the chart image
            
        Returns:
            matplotlib.figure.Figure: Generated chart figure
        """
        accuracy_df = self.calculate_accuracy_stats()
        
        # Sort by Verification Accuracy from high to low
        accuracy_df = accuracy_df.sort_values('Verification Accuracy (%)', ascending=False).reset_index(drop=True)
        
        # Set up the plot with larger figure size
        fig, ax = plt.subplots(figsize=(18, 12))
        
        # Create grouped bar chart
        x = np.arange(len(accuracy_df))
        width = 0.35  # Increased width of the bars for better visibility
        
        # Create bars for both accuracy types with hatch pattern only for Type Accuracy
        bars1 = ax.bar(x - width/2, accuracy_df['Type Accuracy (%)'], 
                      width, label='Type Accuracy', color='#2E8B57', alpha=0.8, hatch='/')
        bars2 = ax.bar(x + width/2, accuracy_df['Verification Accuracy (%)'], 
                      width, label='Verification Accuracy', color='#4169E1', alpha=0.8)
        
        # Customize the chart
        ax.set_xlabel('Verification Types', fontsize=30, fontweight='bold')
        ax.set_ylabel('Accuracy (%)', fontsize=30, fontweight='bold')
        ax.set_title('Type Accuracy vs Verification Accuracy by IoT Configuration Type', 
                    fontsize=34, fontweight='bold', pad=25)
        ax.set_xticks(x)
        ax.set_xticklabels(accuracy_df['Type'], rotation=0, ha='center', fontsize=30, fontweight='bold')
        ax.legend(fontsize=30, loc='upper right', bbox_to_anchor=(0.98, 0.98))
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 140)  # 设置Y轴上限为140
        
        # Add more space at the bottom for labels
        ax.margins(y=0.1)
        
        # Add value labels on bars with better positioning
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                # 将所有数字标签移到柱子上面
                ax.annotate(f'{height:.1f}%',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 10),
                           textcoords="offset points",
                           ha='center', va='bottom', fontsize=24, fontweight='bold')
        
        # Add test count annotations
        for i, (idx, row) in enumerate(accuracy_df.iterrows()):
            ax.annotate(f'n={row["Total Tests"]}',
                       xy=(i, -8),
                       xytext=(0, -20),
                       textcoords="offset points",
                       ha='center', va='top', fontsize=14, style='italic')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Combined accuracy chart saved to: {save_path}")
        
        plt.show()
        return fig

    def create_time_chart(self, save_path=None):
        """
        Create time consumption analysis chart.
        
        Args:
            save_path (str): Path to save the chart image
            
        Returns:
            matplotlib.figure.Figure: Generated chart figure
        """
        time_df = self.calculate_time_stats()
        
        # Set up the plot
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Create stacked bar chart for different time components
        x = np.arange(len(time_df))
        
        # Define colors for different time components
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        # Create stacked bars with adjusted width
        bottom = np.zeros(len(time_df))
        bar_width = 0.6  # 增加柱子宽度
        
        bars1 = ax.bar(x, time_df['Translate Time (s)'], label='Translate Time', 
                      color=colors[0], alpha=0.8, width=bar_width)
        bottom += time_df['Translate Time (s)']
        
        bars2 = ax.bar(x, time_df['Config Time (s)'], bottom=bottom, label='Config Time',
                      color=colors[1], alpha=0.8, width=bar_width, hatch='/')
        bottom += time_df['Config Time (s)']
        
        bars3 = ax.bar(x, time_df['Verify Time (s)'], bottom=bottom,
                      color=colors[2], alpha=0.8, width=bar_width)
        
        # Customize the chart
        ax.set_xlabel('Verification Types', fontsize=22, fontweight='bold')
        ax.set_ylabel('Time (seconds)', fontsize=22, fontweight='bold')
        ax.set_title('Average Time Consumption by IoT Configuration Type', 
                    fontsize=24, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(time_df['Type'], rotation=0, ha='center', fontsize=24, fontweight='bold')
        ax.legend(fontsize=24)
        ax.grid(True, alpha=0.3)
        
        # Set Y-axis range to accommodate labels
        max_time = time_df['Total Time (s)'].max()
        ax.set_ylim(0, max_time * 1.5)  # 增加Y轴上限，使柱子显得更矮
        
        # Add total time labels on top of bars
        for i, total_time in enumerate(time_df['Total Time (s)']):
            ax.annotate(f'{total_time:.1f}s',
                       xy=(i, total_time),
                       xytext=(0, 10),  # 将数字移到柱子上面
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=22, fontweight='bold')
        
        # Adjust layout to prevent text from being cut off
        plt.tight_layout()
        plt.subplots_adjust(top=0.90)  # 增加顶部空间，确保数字标签不被截断
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Time chart saved to: {save_path}")
        
        plt.show()
        return fig
    
    
    def generate_all_charts(self, output_dir="Graphs"):
        """
        Generate all performance charts and save them to specified directory.
        Generates combined accuracy chart and time consumption chart.
        
        Args:
            output_dir (str): Directory to save generated charts
        """
        if self.df is None:
            raise ValueError("Data not loaded. Please call load_data() first.")
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        # Generate combined accuracy chart
        print("Generating combined accuracy chart...")
        combined_accuracy_path = Path(output_dir) / "combined_accuracy.png"
        self.create_combined_accuracy_chart(save_path=str(combined_accuracy_path))
        
        print("Generating time consumption chart...")
        time_path = Path(output_dir) / "time_consumption.png"
        self.create_time_chart(save_path=str(time_path))
        
        print(f"\nAll charts generated successfully!")
        print(f"Charts saved in: {output_dir}/")
        
        # Print summary statistics
        self.print_summary_stats()
    
    def print_summary_stats(self):
        """
        Print comprehensive summary statistics for all verification types.
        Displays accuracy metrics, performance data, and test counts.
        """
        accuracy_df = self.calculate_accuracy_stats()
        time_df = self.calculate_time_stats()
        
        print("\n" + "="*60)
        print("PERFORMANCE SUMMARY STATISTICS")
        print("="*60)
        
        for _, row in accuracy_df.iterrows():
            print(f"\n{row['Type Full Name']} ({row['Type']}):")
            print(f"  Type Accuracy: {row['Type Accuracy (%)']:.1f}%")
            print(f"  Verification Accuracy: {row['Verification Accuracy (%)']:.1f}%")
            print(f"  Average Time: {time_df[time_df['Type'] == row['Type']]['Total Time (s)'].iloc[0]:.2f}s")
            print(f"  Total Tests: {row['Total Tests']}")
        
        print(f"\nOverall Statistics:")
        print(f"  Average Type Accuracy: {accuracy_df['Type Accuracy (%)'].mean():.1f}%")
        print(f"  Average Verification Accuracy: {accuracy_df['Verification Accuracy (%)'].mean():.1f}%")
        print(f"  Average Total Time: {time_df['Total Time (s)'].mean():.2f}s")

def main():
    """
    Main function to execute the performance chart generation process.
    Handles command line arguments, data loading, and chart generation.
    """
    parser = argparse.ArgumentParser(description='Generate performance charts from IoT test results')
    parser.add_argument('--csv', type=str, 
                       default='enhanced_test_report_20251012_205731.csv',
                       help='Path to CSV file containing test results')
    parser.add_argument('--output', type=str, default='Graphs',
                       help='Output directory for charts')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = PerformanceChartGenerator(args.csv)
    
    # Load and prepare data
    if not generator.load_data():
        print("Failed to load data. Exiting.")
        sys.exit(1)
    
    generator.prepare_data()
    
    # Generate all charts
    generator.generate_all_charts(args.output)

if __name__ == "__main__":
    main()
