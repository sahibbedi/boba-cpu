import os
import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Force headless rendering backend
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import logging

logging.basicConfig(level=logging.INFO)

def export_video():
    # 1. Locate trajectory data
    traj_path = "./batch_simulation_results/double_lift_cloth_3/double_lift_cloth_3_trajectory.pkl"
    if not os.path.exists(traj_path):
        traj_path = "./collected_simulation_data/double_lift_cloth_3_trajectory.pkl"
    
    if not os.path.exists(traj_path):
        logging.error("Trajectory file not found! Please run your collection script first.")
        return

    with open(traj_path, "rb") as f:
        trajectory_points = pickle.load(f)

    num_frames = len(trajectory_points)
    logging.info(f"Loaded {num_frames} frames of trajectory data.")

    # 2. Create dedicated 'videos' folder in Boba-Public
    output_dir = "./videos"
    os.makedirs(output_dir, exist_ok=True)
    
    output_animation_path = os.path.join(output_dir, "composited_cloth_output.gif")
    logging.info(f"Rendering animation to: {os.path.abspath(output_animation_path)}")

    # 3. Setup Matplotlib 3D figure for animation
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(projection='3d')

    init_frame = trajectory_points[0]
    scat = ax.scatter(init_frame[:, 0], init_frame[:, 1], init_frame[:, 2], c=init_frame[:, 2], cmap='Blues', s=3)

    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_zlim(0.0, 2.0)
    ax.set_title("Composited Cloth Simulation")
    ax.axis('off')

    def update(frame_idx):
        coords = trajectory_points[frame_idx]
        scat._offsets3d = (coords[:, 0], coords[:, 1], coords[:, 2])
        return scat,

    anim = FuncAnimation(fig, update, frames=len(trajectory_points), interval=33, blit=False)
    
    # 4. Save as GIF using Pillow writer (Zero codec errors)
    anim.save(output_animation_path, writer='pillow', fps=30)
    plt.close(fig)
    
    logging.info(f">>> SUCCESS: Animation successfully saved to {os.path.abspath(output_animation_path)}")

if __name__ == "__main__":
    export_video()
