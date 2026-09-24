import os
import pickle
import numpy as np

def generate_prompt():
    traj_path = "./batch_simulation_results/double_lift_cloth_3/double_lift_cloth_3_trajectory.pkl"
    if not os.path.exists(traj_path):
        traj_path = "./collected_simulation_data/double_lift_cloth_3_trajectory.pkl"
    
    if not os.path.exists(traj_path):
        print("Dataset not found. Please run collection first.")
        return

    with open(traj_path, "rb") as f:
        trajectory_points = pickle.load(f)

    frames = len(trajectory_points)
    vertices = trajectory_points[0].shape[0]
    
    # Calculate spatial bounds across the trajectory
    all_pts = np.concatenate(trajectory_points, axis=0)
    min_bound = np.min(all_pts, axis=0)
    max_bound = np.max(all_pts, axis=0)

    prompt = f"""
I have successfully generated the headless simulation trajectory for 'double_lift_cloth_3' on my Mac. 
Here are the exact physics data specs captured from the dataset:
- Total Animation Frames: {frames}
- Mesh Vertex Count: {vertices} nodes
- Spatial Bounding Box (X, Y, Z):
  Min: {min_bound.tolist()}
  Max: {max_bound.tolist()}

Based on these exact trajectory coordinates, please provide a complete, production-ready Python script using OpenCV and NumPy that takes a background video of real cloth and projects these simulated 3D vertices as a textured/shaded digital twin mesh over the video frames.
"""
    
    print("\n" + "="*70)
    print("📋 COPY AND PASTE THIS PROMPT BACK INTO OUR CHAT:")
    print("="*70)
    print(prompt)
    print("="*70)

if __name__ == "__main__":
    generate_prompt()
