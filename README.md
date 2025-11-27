# Climate Stress Analysis in Maize (Iran, 2071–2090)
This project analyzes how future climate scenarios might affect the most temperature sensitive stages of maize (flowering and grain filling) across 8 regions in Iran. Using CMIP6-based climate projections generated with LARS-WG for the period 2071–2090, together with cultivar-specific growth durations, I evaluated whether critical growth stages will overlap with periods of high temperature stress.
This is a data analysis + visualization project meant to show my ability to work with climate data, time alignment, agronomic concepts, and multi-scenario comparisons. The goal isn’t reproducibility, it’s demonstration of skill, reasoning, and clarity.


## Motivation
Flowering and grain filling are the most vulnerable stages in maize. Exposure to extreme heat during these periods affects pollination, kernel set, grain development, and final yield.
The goal of this project was to determine whether, by 2071–2090, these sensitive phases begin to overlap with hotter temperature periods under:

- SSP4.5 (stabilization scenario)
- SSP8.5 (high emission scenario)

for two cultivars with different maturity durations, across eight different climatic zones in Iran.
This analysis integrates agronomic knowledge, climate data processing, and Python-based visualization.

## What This Project Does

### 1. **Climate Data Processing**
- Load and clean daily maximum temperature projections  
- Align time-series across scenarios  
- Check for missing values and time continuity  
- Subset data for eight Iranian maize-growing regions  

### 2. **Growth Stage Modeling**
Using cultivar-specific thermal durations (based on my thesis work) to approximate:

- Emergence  
- Vegetative period  
- Flowering (silking)  
- Grain filling
- Physiological maturity  

Flowering and grain-filling periods were mapped onto the future climate time series for each location.

### 3. **Heat Stress Evaluation**
For each location, cultivar, and climate scenario:

- Calculate mean/max temperature during flowering and grain filling  
- Compare to known physiological maize thresholds  
- Detect overlap between growth stages and projected heat waves  

### 4. **Visualizations**
Created grids of plots summarizing:

- Scenario differences (SSP4.5 vs SSP8.5)  
- Cultivar differences (short vs long duration)  
- Geographic variability  

Only the two strongest grid figures are included in this repo.


## License
The analysis results and plots are shared under:

**Creative Commons BY-NC 4.0**

This means:
-  You may view and reference them  
-  You may not use them commercially  
-  You may not republish or repurpose them as your own work

## Notes
This project is meant to show **skill, clarity, and reasoning**, not provide a full research pipeline.  
Everything included here reflects the final clean, professional version of my analysis.



