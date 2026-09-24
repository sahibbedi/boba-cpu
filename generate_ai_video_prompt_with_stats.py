import os
import pickle
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

def analyze_and_generate_prompt():
    # 1. Locate the trajectory dataset
    traj_path = "./batch_simulation_results/double_lift_cloth_3/double_lift_cloth_3_trajectory.pkl"
    if not os.path.exists(traj_path):
        traj_path = "./collected_simulation_data/double_lift_cloth_3_trajectory.pkl"
    
    if not os.path.exists(traj_path):
        logging.error("Trajectory dataset not found! Please run your simulation collection script first.")
        return

    with open(traj_path, "rb") as f:
        trajectory_points = pickle.load(f)

    # Convert list of frames into a numpy array for vectorised stats: (Frames, Vertices, 3)
    traj_array = np.array(trajectory_points)
    num_frames, num_vertices, _ = traj_array.shape
    
    # 2. Compute Advanced Statistics
    all_pts = traj_array.reshape(-1, 3)
    min_b = np.min(all_pts, axis=0)
    max_b = np.max(all_pts, axis=0)
    span = max_b - min_b

    # Calculate frame-to-frame velocity (displacement magnitude per step at ~30fps, dt = 0.033s)
    dt = 0.033
    frame_displacements = np.linalg.norm(np.diff(traj_array, axis=0), axis=-1) # shape: (frames-1, vertices)
    mean_velocity = np.mean(frame_displacements) / dt
    max_velocity = np.max(frame_displacements) / dt
    peak_movement_frame = int(np.argmax(np.mean(frame_displacements, axis=1))) + 1

    # Print Advanced Terminal Analytics Report
    print("\n" + "="*70)
    print("📊 ADVANCED PHYSICS & TRAJECTORY ANALYTICS REPORT")
    print("="*70)
    print(f"• Total Recorded Frames       : {num_frames}")
    print(f"• Total Mesh Vertices (Nodes) : {num_vertices:,}")
    print(f"• Spatial Bounding Box (Meters):")
    print(f"  - X Span: {min_b[0]:.3f}m to {max_b[0]:.3f}m (Width: {span[0]:.3f}m)")
    print(f"  - Y Span: {min_b[1]:.3f}m to {max_b[1]:.3f}m (Depth: {span[1]:.3f}m)")
    print(f"  - Z Span: {min_b[2]:.3f}m to {max_b[2]:.3f}m (Lift Height: {span[2]:.3f}m)")
    print(f"• Kinematic Metrics:")
    print(f"  - Mean Vertex Velocity     : {mean_velocity:.3f} m/s")
    print(f"  - Peak Velocity Magnitude  : {max_velocity:.3f} m/s")
    print(f"  - Peak Deformation Frame   : Frame #{peak_movement_frame} of {num_frames}")
    print("="*70 + "\n")

    # 3. Build the Precision Video Generation Prompt for Gemini
    ai_prompt = f"""
Generate a hyper-realistic, cinematic 4K video focusing strictly on a cloth simulation physics test ('double_lift_cloth_3'). 
The video must feature clean studio lighting against a neutral background, highlighting structural draping, tension, and cloth deformation without any UI overlays, text, or extraneous graphics.

Simulation Physics & Technical Parameters:
- Motion Sequence: A synchronized double-lift pulling maneuver on a flexible fabric sheet.
- Mesh Resolution: {num_vertices} tracked surface nodes across {num_frames} fluid animation frames (~30 FPS).
- Kinematic Profile: Mean velocity of {mean_velocity:.2f} m/s, peaking at frame {peak_movement_frame} with max velocity of {max_velocity:.2f} m/s.
- Spatial Bounding Volume (X, Y, Z meters): 
  - Width (X): [{min_b[0]:.2f}, {max_b[0]:.2f}]
  - Depth (Y): [{min_b[1]:.2f}, {max_b[1]:.2f}]
  - Height / Lift (Z): [{min_b[2]:.2f}, {max_b[2]:.2f}]
- Visual Style: Macro cinematography, soft shadows, realistic fabric self-collision, accurate wrinkling, and physical tension lines reflecting spring-mass dampening parameters.
"""

    print("="*70)
    print("📋 COPY AND PASTE THIS PROMPT INTO GEMINI FOR THE REAL VIDEO:")
    print("="*70)
    print(ai_prompt.strip())
    print("="*70 + "\n")

if __name__ == "__main__":
    analyze_and_generate_prompt()
