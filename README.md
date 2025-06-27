# Multi-Vehicle Clustered Profitable Tour Problem - ILP Formulations

**Tinbergen Institute - Business Data Science (Operations Analytics Track)**  
**Integer Linear Programming Course (2024–2025)**  
**Programming Assignment**

**Student:** Batuhan Ataş (726476)  
**Instructor:** M. Leitner  
**Course Period:** 2024–2025

## Project Overview
This repository contains the implementation, experimentation, and analysis of three Integer Linear Programming (ILP) formulations—Miller–Tucker–Zemlin (MTZ), Single-Commodity Flow (SCF), and Multi-Commodity Flow (MCF)—for the Multi-Vehicle Clustered Profitable Tour Problem (CPTP). 

The main objective is to identify multiple vehicle routes from a common depot, maximizing the total score collected from clusters of nodes, with constraints on vehicle capacities (maximum tour duration).

## Formulations Implemented
1. **MTZ (Miller–Tucker–Zemlin)** formulation
2. **SCF (Single-Commodity Flow)** formulation
3. **MCF (Multi-Commodity Flow)** formulation

These formulations were compared based on:
- Computational performance (runtime, scalability)
- Solution quality (objective values, optimality gap)

## Repository Structure

ILP/
├── instances/ # TSPLIB instances and problem data
├── results/ # Solution results and output files
├── results_mcf/ # MCF formulation results
├── results_mtz/ # MTZ formulation results
├── results_scf/ # SCF formulation results
├── results_scf_default/ # Default SCF results
├── assignment2025.pdf # Original assignment document
├── data.py # Data loading and parsing script
├── checkmtz.py # Feasibility checker for MTZ solutions
├── checkscf.py # Feasibility checker for SCF solutions
├── checkmcf.py # Feasibility checker for MCF solutions
├── mainmtz.py # Main execution script for MTZ formulation
├── mainscf.py # Main execution script for SCF formulation
├── mainmcf.py # Main execution script for MCF formulation
├── modelmtz.py # MTZ model formulation (Gurobi)
├── modelscf.py # SCF model formulation (Gurobi)
├── modelmcf.py # MCF model formulation (Gurobi)
└── plot.py # Visualization script for tour results

## Software and Libraries Used
- **Python 3.x**
- **Gurobi Optimizer** (version 12.0)
- **gurobipy** interface for Python
- Standard libraries (`numpy`, `pandas`, `matplotlib`)


