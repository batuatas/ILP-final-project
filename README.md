# Multi-Vehicle Clustered Profitable Tour Problem - ILP Formulations

**Tinbergen Institute - Business Data Science (Operations Analytics Track)**  
**Integer Linear Programming Course (2024–2025)**  
**Programming Assignment**

**Student:** Batuhan Atas
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

## Software and Libraries Used
- **Python 3.x**
- **Gurobi Optimizer** (version 12.0)
- **gurobipy** interface for Python
- Standard libraries (`numpy`, `pandas`, `matplotlib`)


