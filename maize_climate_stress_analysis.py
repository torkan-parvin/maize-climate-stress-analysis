"""
Maize Climate Stress Temperature Analysis (2071–2090)
-----------------------------------------------------

This script reads future climate projections and Mean.xlsx data for 8 locations
and 2 maize cultivars (KSC260 and KSC704) under SSP2-4.5 and SSP5-8.5 scenarios.

It generates 2×2 plot grids showing:
- Daily minimum and maximum temperature from sowing to maturity
- Flowering and maturity timing (with ± standard deviation)
- Scenario-based comparisons for each location and cultivar

Required input folders:
- data/daily_averages/<Location>/<Scenario>/daily_averages.csv
- data/future/KSC260-Future/<Location>/(2071-2090)(scenario)-<Location>-260.csv
- data/future/KSC704-Future/<Location>/(2071-2090)(scenario)-<Location>-704.csv
- data/Mean.xlsx (with one sheet per location)

Outputs:
- plot_grid_1.png
- plot_grid_2.png
- plot_grid_3.png
- plot_grid_4.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Locations are grouped for plotting 2x2 grids
location_groups = [
    ['Dezful', 'Shushtar'],  # Group 1
    ['Lamerd', 'Kermanshah'],  # Group 2
    ['Zarqan', 'Ravansar'],  # Group 3
    ['Parsabad', 'Ilam']  # Group 4
]
all_locations = [loc for group in location_groups for loc in group]

# File paths
mean_excel_file = r'data/Mean.xlsx'
daily_avg_base_path = r'data/daily_averages/{location}/{scenario}/daily_averages.csv'
future_data_paths = {
    '260': r'data/future/KSC260-Future/{location}/(2071-2090)({scenario})-{location}-260.csv',
    '704': r'data/future/KSC704-Future/{location}/(2071-2090)({scenario})-{location}-704.csv'
}
scenarios = ['ssp245', 'ssp585']   # SSP2-4.5 and SSP5-8.5
cultivars = ['260', '704']         # Maize cultivars

# Row indices for Mean.xlsx; Map cultivar and scenario to row index in Excel containing FloweringDAS and MaturityDAS
row_indices = {
    '260': {'ssp245': 3, 'ssp585': 6},   # Excel rows 4 and 7
    '704': {'ssp245': 13, 'ssp585': 16}  # Excel rows 14 and 17
}

# Plotting parameters
start_index = 142  # May 22 = Julian day 142 in dataset (0-based index)
max_days = 200     # Number of days to plot after start_index (Maximum days after sowing across the 8 different locations)
color_schemes = {
    '260': {
        'ssp245': {'mint': 'lightpink', 'maxt': 'crimson', 'marker_mint': '^', 'marker_maxt': 's'},
        'ssp585': {'mint': 'mediumpurple', 'maxt': 'darkcyan', 'marker_mint': 'o', 'marker_maxt': 'd'}
    },
    '704': {
        'ssp245': {'mint': 'blue', 'maxt': 'orange', 'marker_mint': '^', 'marker_maxt': 's'},
        'ssp585': {'mint': 'cyan', 'maxt': 'red', 'marker_mint': 'o', 'marker_maxt': 'd'}
    }
}

# Get the global y-axis range which ensures all subplots share the same y-axis for comparison
y_min = float('inf')
y_max = float('-inf')

for location in all_locations:
    for scenario in scenarios:
        daily_avg_file = daily_avg_base_path.format(location=location, scenario=f'(2071-2090)({scenario})')
        if not os.path.exists(daily_avg_file):
            raise FileNotFoundError(f"Missing file: {daily_avg_file}")

        daily_df = pd.read_csv(daily_avg_file)
        daily_df.columns = daily_df.columns.str.strip().str.lower()

        if 'avg_mint' not in daily_df.columns or 'avg_maxt' not in daily_df.columns:
            raise KeyError(f"Missing 'avg_mint' or 'avg_maxt' in {daily_avg_file}")

        end_index = start_index + max_days
        if end_index > len(daily_df):
            raise IndexError(f"Only {len(daily_df)} days in {daily_avg_file}, need {end_index + 1}")

        temp_data = daily_df[['avg_mint', 'avg_maxt']].iloc[start_index:end_index]
        y_min = min(y_min, temp_data.min().min())
        y_max = max(y_max, temp_data.max().max())

# Add padding to avoid lines touching plot edges
y_min -= 2  # Add 2°C padding
y_max += 2

# Process each group of locations
for group_idx, locations in enumerate(location_groups, start=1):
    num_locations = len(locations)
    # Set figure size for 2x2 grid
    figsize = (24, 12)  # Consistent size for 2x2 grid
    fig, axes = plt.subplots(num_locations, 2, figsize=figsize, sharex=True, sharey=True)
    axes = axes.ravel()  # Flatten for easier indexing

    for loc_idx, location in enumerate(locations):
        # Read Mean.xlsx sheet
        try:
            mean_df = pd.read_excel(mean_excel_file, sheet_name=location, engine='openpyxl')
        except ValueError as e:
            raise ValueError(f"Error reading sheet '{location}' from {mean_excel_file}: {str(e)}")

        for cult_idx, cultivar in enumerate(cultivars):
            ax = axes[loc_idx * 2 + cult_idx]

            # Check row count
            max_row = max(row_indices[cultivar].values())
            if len(mean_df) <= max_row:
                print(f"Sheet data for {location}:\n{mean_df}")
                raise IndexError(f"Sheet '{location}' has {len(mean_df)} rows, need at least {max_row + 1}")

            # Verify scenario labels and check NaNs
            for scenario, row_idx in row_indices[cultivar].items():
                if str(mean_df.iloc[row_idx, 0]).strip() != f'(2071-2090)({scenario})':
                    print(f"Sheet data for {location}:\n{mean_df}")
                    raise ValueError(f"Row {row_idx + 1} in '{location}' does not contain expected scenario")
                print(f"Inspecting {location} row {row_idx + 1} ({cultivar}, {scenario}):")
                print(mean_df.iloc[row_idx][['FloweringDAS', 'MaturityDAS']])
                for col in ['FloweringDAS', 'MaturityDAS']:
                    if pd.isna(mean_df.loc[row_idx, col]):
                        print(f"Sheet data for {location}:\n{mean_df}")
                        raise ValueError(
                            f"NaN in '{col}' at row {row_idx + 1} ({cultivar}, {scenario}) in '{location}'")

            # Get MaturityDAS and FloweringDAS values
            maturity_das = {
                scenario: int(round(mean_df.loc[row_indices[cultivar][scenario], 'MaturityDAS']))
                for scenario in scenarios
            }
            flowering_das = {
                scenario: int(round(mean_df.loc[row_indices[cultivar][scenario], 'FloweringDAS']))
                for scenario in scenarios
            }

            # Calculate standard deviation for FloweringDAS
            flowering_std = {}
            for scenario in scenarios:
                future_df = pd.read_csv(future_data_paths[cultivar].format(location=location, scenario=scenario),
                                        header=2)
                flowering_std[scenario] = pd.to_numeric(future_df.iloc[4:]['FloweringDAS'], errors='coerce').std()

            # Plot data
            max_maturity_das = max(maturity_das.values())
            days = range(1, max_maturity_das + 1)

            for idx, (scenario, linestyle, scenario_label) in enumerate([
                ('(2071-2090)(ssp245)', '-', 'ssp245'),
                ('(2071-2090)(ssp585)', '--', 'ssp585')
            ]):
                daily_avg_file = daily_avg_base_path.format(location=location, scenario=scenario)
                daily_df = pd.read_csv(daily_avg_file)
                daily_df.columns = daily_df.columns.str.strip().str.lower()

                end_index = start_index + max_maturity_das
                if end_index > len(daily_df):
                    raise IndexError(f"Only {len(daily_df)} days in {daily_avg_file}, need {end_index + 1}")

                mint_values = daily_df['avg_mint'].iloc[start_index:start_index + max_maturity_das].values
                maxt_values = daily_df['avg_maxt'].iloc[start_index:start_index + max_maturity_das].values

                # Plot min and temperatures
                ax.plot(days[:maturity_das[scenario_label]], mint_values[:maturity_das[scenario_label]],
                        label=f'Min Temp ({scenario_label})',
                        color=color_schemes[cultivar][scenario_label]['mint'],
                        marker=color_schemes[cultivar][scenario_label]['marker_mint'],
                        linestyle=linestyle)
                ax.plot(days[:maturity_das[scenario_label]], maxt_values[:maturity_das[scenario_label]],
                        label=f'Max Temp ({scenario_label})',
                        color=color_schemes[cultivar][scenario_label]['maxt'],
                        marker=color_schemes[cultivar][scenario_label]['marker_maxt'],
                        linestyle=linestyle)

                # Flowering and Maturity annotations
                if flowering_das[scenario_label] <= maturity_das[scenario_label]:
                    flowering_index = flowering_das[scenario_label] - 1
                    y_coord_flower = (mint_values[flowering_index] + maxt_values[flowering_index]) / 2
                    y_offset = idx * 6
                    x_offset = 10 if abs(flowering_das['ssp245'] - flowering_das['ssp585']) < 20 else 5
                    ax.axvline(x=flowering_das[scenario_label], color='green', linestyle='--', alpha=0.5)
                    ax.annotate(
                        f'Flowering ({scenario_label}): {flowering_das[scenario_label]} ± {flowering_std[scenario_label]:.1f}',
                        xy=(flowering_das[scenario_label], y_coord_flower + y_offset),
                        xytext=(flowering_das[scenario_label] + x_offset, y_coord_flower + y_offset + 2),
                        arrowprops=dict(facecolor='black', shrink=0.05),
                        bbox=dict(facecolor='white', edgecolor='black', pad=0.3),
                        fontsize=16)

                if maturity_das[scenario_label] <= max_maturity_das:
                    maturity_index = maturity_das[scenario_label] - 1
                    y_coord_maturity = mint_values[maturity_index] - (1 if scenario_label == 'ssp245' else -1)
                    ax.axvline(x=maturity_das[scenario_label], color='black', linestyle='--', alpha=0.5)
                    ax.annotate(f'Maturity ({scenario_label}): {maturity_das[scenario_label]}',
                                xy=(maturity_das[scenario_label], y_coord_maturity),
                                xytext=(maturity_das[scenario_label] + 1,
                                        y_coord_maturity + (-2 if scenario_label == 'ssp245' else 2)),
                                arrowprops=dict(facecolor='black', shrink=0.1),
                                bbox=dict(facecolor='white', edgecolor='black', pad=0.3),
                                fontsize=16)

            # Subplot settings
            ax.set_title(f"{location} ({cultivar})", fontsize=18)
            ax.set_xlabel("Days After Sowing", fontsize=16)
            ax.set_ylabel("Temperature (°C)", fontsize=16)
            ax.tick_params(axis='both', labelsize=14)
            ax.set_xlim(0, 200)
            ax.set_ylim(y_min, y_max)
            ax.grid(True)
            ax.legend(fontsize=14)

    # Figure settings
    fig.suptitle("Daily Avg Temp Until Maturity (2071-2090)", fontsize=20)
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to accommodate suptitle

    # Save plot
    output_file = f"plot_grid_{group_idx}.png"
    plt.savefig(output_file, dpi=300)
    plt.close()
    print(f"Output saved to {output_file}")