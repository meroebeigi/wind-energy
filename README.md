# Wind Energy Project

## Overview
This project simulates and analyzes the performance of wind farms using Python. It includes models for wind turbine wakes, power output calculations, and optimization of turbine layouts and induction factors. The codebase is organized into several scripts and notebooks for different parts of the analysis.

## Features
- **Wake Modeling:** Simulates the velocity deficit behind wind turbines using analytical models.
- **Power Calculation:** Computes the power output of each turbine and the total wind farm.
- **Optimization:** Uses numerical optimization to maximize wind farm power output by adjusting induction factors.
- **Visualization:** Generates plots for power output, induction factors, and turbine layout.

## Main Files
- `main.py`: Core script for single-row wind farm simulation, power calculation, and optimization.
- `func.py`: Contains main functions for velocity deficit and power calculation.
- `partb.py`, `part2c.py`, `part2d.py`: Scripts for advanced modeling, including 2D layouts and overlap effects.
- `1e.py`: Script for optimization using `scipy.optimize`.
- `func2.ipynb`, `main2.ipynb`: Jupyter notebooks for interactive exploration and visualization.
- `celldata.dat`, `celldata2.dat`: Output data files for iterative optimization results.

## Requirements
- Python 3.x
- numpy
- matplotlib
- pandas
- scipy

Install dependencies with:
```bash
pip install numpy matplotlib pandas scipy
```

## Usage
1. **Run the main simulation:**
	```bash
	python main.py
	```
	This will generate plots for power output and induction factors for a row of turbines.

2. **Run optimization:**
	```bash
	python 1e.py
	```
	This script optimizes the induction factors to maximize total power.

3. **Explore advanced layouts:**
	Run `partb.py`, `part2c.py`, or `part2d.py` for 2D wind farm analysis and overlap modeling.

4. **Jupyter Notebooks:**
	Open `func2.ipynb` or `main2.ipynb` for interactive analysis and visualization.

## Project Structure
- `main.py` — Main simulation and optimization for a row of turbines
- `func.py` — Core functions for wake and power calculations
- `partb.py`, `part2c.py`, `part2d.py` — Advanced/2D wind farm modeling
- `1e.py` — Induction factor optimization
- `func2.ipynb`, `main2.ipynb` — Notebooks for exploration
- `celldata.dat`, `celldata2.dat` — Output data

## References
- [Wind Energy Explained: Theory, Design and Application by J.F. Manwell, J.G. McGowan, A.L. Rogers]
- [Relevant research papers on wind farm layout optimization and wake modeling]

---
*Developed for educational and research purposes.*
