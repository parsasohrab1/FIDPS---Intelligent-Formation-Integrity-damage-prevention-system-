#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIDPS Dataset Generator - Main Script
=====================================

Main script for generating the integrated dataset of the Formation Integrity Damage Prevention System (FIDPS)
Includes LWD/MWD sensor data and related borehole images with various types of formation damage

Author: FIDPS Development Team
Version: 1.0
Date: 2024
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add the dataset folder path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_dataset_generator import UnifiedDatasetGenerator

def load_config(config_file):
    """Load the configuration from a JSON file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file {config_file} not found. Using default settings.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing configuration file: {e}")
        return None

def create_default_config(config_file):
    """Create the default configuration file"""
    default_config = {
        "dataset_settings": {
            "name": "FIDPS Formation Integrity Dataset",
            "version": "1.0",
            "description": "Comprehensive dataset for formation integrity damage prevention system"
        },
        "time_settings": {
            "start_date": "2024-01-01",
            "duration_days": 30,
            "timezone": "UTC"
        },
        "sensor_data_settings": {
            "sampling_rate_minutes": 1,
            "include_anomalies": True,
            "damage_probability": 0.001,
            "noise_level": 0.02
        },
        "image_settings": {
            "images_per_day": 20,
            "image_dimensions": {
                "min_size": [256, 128],
                "max_size": [512, 256]
            },
            "damage_probability": 0.7,
            "include_normal_images": True
        },
        "output_settings": {
            "base_path": "fidps_dataset",
            "formats": ["csv", "parquet", "json"],
            "compress_images": False,
            "create_summary": True
        },
        "correlation_settings": {
            "method": "temporal_and_risk_based",
            "correlation_threshold": 0.1,
            "max_time_diff_minutes": 30
        }
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    print(f"Default configuration created: {config_file}")
    return default_config

def validate_config(config):
    """Validate the configuration"""
    errors = []
    
    # Check the start date
    try:
        datetime.fromisoformat(config['time_settings']['start_date'])
    except (ValueError, KeyError):
        errors.append("Invalid start_date format. Use YYYY-MM-DD")
    
    # Check the duration
    if config.get('time_settings', {}).get('duration_days', 0) <= 0:
        errors.append("duration_days must be positive")
    
    # Check the number of images
    if config.get('image_settings', {}).get('images_per_day', 0) <= 0:
        errors.append("images_per_day must be positive")
    
    return errors

def print_dataset_info(config):
    """Display dataset information before generation"""
    print("\n" + "="*60)
    print("FIDPS Dataset Generation Configuration")
    print("="*60)
    
    # General information
    dataset_info = config.get('dataset_settings', {})
    print(f"Dataset Name: {dataset_info.get('name', 'N/A')}")
    print(f"Version: {dataset_info.get('version', 'N/A')}")
    print(f"Description: {dataset_info.get('description', 'N/A')}")
    
    # Time settings
    time_settings = config.get('time_settings', {})
    start_date = time_settings.get('start_date', 'N/A')
    duration = time_settings.get('duration_days', 0)
    print(f"\nTime Range: {start_date} to {start_date} + {duration} days")
    
    # Sensor data settings
    sensor_settings = config.get('sensor_data_settings', {})
    sampling_rate = sensor_settings.get('sampling_rate_minutes', 1)
    estimated_sensor_records = duration * 24 * 60 // sampling_rate
    print(f"\nSensor Data:")
    print(f"  Sampling Rate: {sampling_rate} minute(s)")
    print(f"  Estimated Records: {estimated_sensor_records:,}")
    print(f"  Include Anomalies: {sensor_settings.get('include_anomalies', True)}")
    
    # Image settings
    image_settings = config.get('image_settings', {})
    images_per_day = image_settings.get('images_per_day', 0)
    total_images = duration * images_per_day
    print(f"\nImage Data:")
    print(f"  Images per Day: {images_per_day}")
    print(f"  Total Images: {total_images:,}")
    print(f"  Damage Probability: {image_settings.get('damage_probability', 0.7)*100:.1f}%")
    
    # Output settings
    output_settings = config.get('output_settings', {})
    print(f"\nOutput Settings:")
    print(f"  Base Path: {output_settings.get('base_path', 'N/A')}")
    print(f"  Formats: {', '.join(output_settings.get('formats', []))}")
    
    print("="*60)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='FIDPS Dataset Generator - Generate comprehensive formation integrity datasets',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Generate with default settings
  %(prog)s --config my_config.json  # Use custom configuration
  %(prog)s --create-config          # Create default configuration file
  %(prog)s --days 7 --images 50     # Quick generation: 7 days, 50 images/day
        """
    )
    
    parser.add_argument('--config', '-c', 
                       default='fidps_config.json',
                       help='Configuration file path (default: fidps_config.json)')
    
    parser.add_argument('--create-config', 
                       action='store_true',
                       help='Create default configuration file and exit')
    
    parser.add_argument('--output', '-o',
                       help='Output directory (overrides config)')
    
    parser.add_argument('--days', '-d', 
                       type=int,
                       help='Duration in days (overrides config)')
    
    parser.add_argument('--images', '-i',
                       type=int, 
                       help='Images per day (overrides config)')
    
    parser.add_argument('--start-date', '-s',
                       help='Start date in YYYY-MM-DD format (overrides config)')
    
    parser.add_argument('--quiet', '-q',
                       action='store_true',
                       help='Suppress detailed output')
    
    parser.add_argument('--dry-run',
                       action='store_true',
                       help='Show configuration without generating data')
    
    args = parser.parse_args()
    
    # Create the default configuration if requested
    if args.create_config:
        create_default_config(args.config)
        return 0
    
    # Load the configuration
    config = load_config(args.config)
    if config is None:
        print("Creating default configuration...")
        config = create_default_config(args.config)
    
    # Apply command-line settings
    if args.output:
        config['output_settings']['base_path'] = args.output
    
    if args.days:
        config['time_settings']['duration_days'] = args.days
    
    if args.images:
        config['image_settings']['images_per_day'] = args.images
    
    if args.start_date:
        config['time_settings']['start_date'] = args.start_date
    
    # Validate the configuration
    validation_errors = validate_config(config)
    if validation_errors:
        print("Configuration errors:")
        for error in validation_errors:
            print(f"  - {error}")
        return 1
    
    # Display dataset information
    if not args.quiet:
        print_dataset_info(config)
    
    # Dry run (display the configuration without generating)
    if args.dry_run:
        print("\nDry run completed. No data generated.")
        return 0
    
    # User confirmation for generation
    if not args.quiet:
        response = input("\nProceed with dataset generation? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Dataset generation cancelled.")
            return 0
    
    try:
        # Create the generator
        generator = UnifiedDatasetGenerator()
        
        # Extract parameters from the configuration
        start_date = datetime.fromisoformat(config['time_settings']['start_date'])
        duration_days = config['time_settings']['duration_days']
        images_per_day = config['image_settings']['images_per_day']
        output_path = config['output_settings']['base_path']
        
        # Generate the dataset
        print(f"\nStarting dataset generation...")
        sensor_data, image_metadata, correlations = generator.generate_unified_dataset(
            start_date=start_date,
            duration_days=duration_days,
            num_images_per_day=images_per_day,
            output_path=output_path
        )
        
        # Save the configuration used
        config_output_path = os.path.join(output_path, 'generation_config.json')
        with open(config_output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Dataset generation completed successfully!")
        print(f"📁 Output directory: {os.path.abspath(output_path)}")
        print(f"📊 Sensor records: {len(sensor_data):,}")
        print(f"🖼️  Images generated: {len(image_metadata):,}")
        print(f"🔗 Correlations: {len(correlations):,}")
        print(f"⚙️  Configuration saved: {config_output_path}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nDataset generation interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Error during dataset generation: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)