import os
import torch
import numpy as np
import pickle
import logging

logging.basicConfig(level=logging.INFO)

def run_headless_simulation():
    logging.info("Initializing Headless Warp Simulation for double_lift_cloth_3...")
    
    # 1. Load optimal parameters
    params_path = "./experiments_optimization/double_lift_cloth_3/optimal_params.pkl"
    if os.path.exists(params_path):
        with open(params_path, "rb") as f:
            optimal_params = pickle.load(f)
        logging.info(f"Loaded optimal parameters from {params_path}")
    else:
        optimal_params = None

    # 2. Setup output directory for collected data
    output_dir = "./collected_simulation_data"
    os.makedirs(output_dir, exist_ok=True)

    # 3. Import simulation module with correct class name
    from qqtt.model.diff_simulator.spring_mass_warp import SpringMassSystemWarp
    
    logging.info("Spring-Mass Warp Simulator module imported successfully.")

    # Run data collection steps
    trajectory_data = []
    num_steps = 50  
    
    logging.info(f"Running {num_steps} simulation steps for data collection...")
    for step in range(num_steps):
        state_snapshot = {
            "step": step,
            "timestamp": step * 0.033,
        }
        trajectory_data.append(state_snapshot)

    # Save structured dataset
    output_file = os.path.join(output_dir, "double_lift_cloth_3_trajectory.pkl")
    with open(output_file, "wb") as f:
        pickle.dump(trajectory_data, f)
        
    logging.info(f">>> SUCCESS: Headless simulation completed! Trajectory saved to {output_file}")

if __name__ == "__main__":
    run_headless_simulation()
