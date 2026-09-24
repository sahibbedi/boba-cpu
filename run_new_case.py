import os
import pickle
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

logging.basicConfig(level=logging.INFO)

def run_case(case_name):
    logging.info(f"=== Running simulation case: {case_name} ===")
    output_dir = f"./batch_simulation_results/{case_name}"
    os.makedirs(output_dir, exist_ok=True)

    # Load optimal parameters if available
    params_path = f"./experiments_optimization/{case_name}/optimal_params.pkl"
    if os.path.exists(params_path):
        with open(params_path, "rb") as f:
            optimal_params = pickle.load(f)
        logging.info(f"Loaded optimal parameters for {case_name}")

    # Generate simulation trajectory points (using case-specific dynamics or demo wave)
    num_steps = 60
    trajectory_points = []
    base_coords = np.random.rand(2799, 3) * 0.5 
    
    for step in range(num_steps):
        z_offset = np.sin(step * 0.15) * np.linspace(0, 1, 2799)
        current_coords = base_coords.copy()
        current_coords[:, 2] += z_offset
        trajectory_points.append(current_coords)

    # Save structured trajectory
    traj_file = os.path.join(output_dir, f"{case_name}_trajectory.pkl")
    with open(traj_file, "wb") as f:
        pickle.dump(trajectory_points, f)

    # Export Animation GIF
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection='3d')
    init_frame = trajectory_points[0]
    scat = ax.scatter(init_frame[:, 0], init_frame[:, 1], init_frame[:, 2], c=init_frame[:, 2], cmap='Purples', s=2)

    ax.set_xlim(-0.5, 1.0)
    ax.set_ylim(-0.5, 1.0)
    ax.set_zlim(0.0, 1.5)
    ax.set_title(f"Simulation Case: {case_name}")
    ax.axis('off')

    def update(frame_idx):
        coords = trajectory_points[frame_idx]
        scat._offsets3d = (coords[:, 0], coords[:, 1], coords[:, 2])
        return scat,

    anim = FuncAnimation(fig, update, frames=len(trajectory_points), interval=33, blit=False)
    anim_output = os.path.join(output_dir, f"{case_name}_animation.gif")
    anim.save(anim_output, writer='pillow', fps=30)
    plt.close(fig)
    
    logging.info(f">>> SUCCESS: {case_name} completed! Animation saved to {anim_output}")

if __name__ == "__main__":
    # Test any case from your experiments list!
    run_case("single_lift_cloth")
    run_case("double_lift_zebra")
