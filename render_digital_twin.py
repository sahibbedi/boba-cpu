import os
import pickle
import numpy as np
import cv2
import logging

logging.basicConfig(level=logging.INFO)

def render_digital_twin_video():
    # 1. Locate the trajectory dataset
    traj_path = "./batch_simulation_results/double_lift_cloth_3/double_lift_cloth_3_trajectory.pkl"
    if not os.path.exists(traj_path):
        traj_path = "./collected_simulation_data/double_lift_cloth_3_trajectory.pkl"
    
    if not os.path.exists(traj_path):
        logging.error("Trajectory dataset not found! Please run your simulation collection script first.")
        return

    with open(traj_path, "rb") as f:
        trajectory_points = pickle.load(f)

    num_frames = len(trajectory_points)
    logging.info(f"Loaded {num_frames} frames of simulation trajectory data.")

    # 2. Create dedicated 'videos' folder
    output_dir = "./videos"
    os.makedirs(output_dir, exist_ok=True)
    output_video_path = os.path.join(output_dir, "digital_twin_overlay.mp4")

    # 3. Setup Video Writer (HD 720p at 30 FPS)
    width, height = 1280, 720
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    if not video_writer.isOpened():
        logging.error("Default mp4v writer failed. Trying XVID (.avi)...")
        output_video_path = os.path.join(output_dir, "digital_twin_overlay.avi")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    logging.info(f"Rendering digital twin projection frames to: {os.path.abspath(output_video_path)}")

    # 4. Camera Projection Loop (3D to 2D Pinhole Camera Model)
    for frame_idx, coords in enumerate(trajectory_points):
        # Create professional dark studio background plate (can be replaced with cap.read() for real video)
        canvas = np.full((height, width, 3), 25, dtype=np.uint8)

        if coords is not None and len(coords) > 0:
            # Extract 3D coordinates and apply camera translation (push back along Z axis)
            X = coords[:, 0]
            Y = coords[:, 1]
            Z = coords[:, 2] + 2.0  

            # Camera intrinsics (Focal length and principal point)
            fx, fy = 900.0, 900.0
            cx, cy = width / 2.0, height / 2.0

            # Perspective projection formula
            u = (fx * (X / Z) + cx).astype(np.int32)
            v = (fy * (Y / Z) + cy).astype(np.int32)

            # Filter vertices within screen boundaries
            valid = (u >= 0) & (u < width) & (v >= 0) & (v < height)

            # Draw projected cloth mesh vertices with depth shading
            for i in np.where(valid)[0]:
                px, py = u[i], v[i]
                depth_val = coords[i, 2]
                # Color gradient mapping based on node height/deformation
                blue_channel = int(np.clip(depth_val * 120 + 100, 50, 255))
                red_channel = int(np.clip(255 - (depth_val * 80), 50, 255))
                color = (blue_channel, 120, red_channel) # OpenCV BGR format
                
                cv2.circle(canvas, (px, py), 2, color, -1)

            # Add frame info overlay text
            cv2.putText(canvas, f"Digital Twin | Case: double_lift_cloth_3 | Frame: {frame_idx+1}/{num_frames}", 
                        (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2, cv2.LINE_AA)

        video_writer.write(canvas)

    video_writer.release()
    logging.info(f">>> SUCCESS: Digital twin video baked and saved to {os.path.abspath(output_video_path)}")

if __name__ == "__main__":
    render_digital_twin_video()
