import os
import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Force headless Agg backend
import matplotlib.pyplot as plt
import cv2
import logging

logging.basicConfig(level=logging.INFO)

def composite_simulation_onto_video():
    traj_path = "./batch_simulation_results/double_lift_cloth_3/double_lift_cloth_3_trajectory.pkl"
    if not os.path.exists(traj_path):
        logging.error("Trajectory file not found! Run batch_collect_and_animate.py first.")
        return
    
    with open(traj_path, "rb") as f:
        trajectory_points = pickle.load(f)

    num_frames = len(trajectory_points)
    logging.info(f"Loaded {num_frames} frames of trajectory data.")

    # 1. Ensure output directory exists explicitly
    output_dir = "./batch_simulation_results/double_lift_cloth_3"
    os.makedirs(output_dir, exist_ok=True)
    
    output_video_path = os.path.join(output_dir, "composited_cloth_output.mp4")
    width, height = 800, 600
    fps = 30
    
    # 2. Initialize VideoWriter and check if it opened successfully
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    if not video_writer.isOpened():
        logging.error("Failed to open OpenCV VideoWriter. Trying alternative codec ('XVID')...")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_video_path = os.path.join(output_dir, "composited_cloth_output.avi")
        video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    logging.info(f"Writing video frames to: {os.path.abspath(output_video_path)}")

    for i, coords in enumerate(trajectory_points):
        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(projection='3d')
        
        ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=coords[:, 2], cmap='Blues', s=3)
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-0.5, 1.5)
        ax.set_zlim(0.0, 2.0)
        ax.axis('off')
        
        fig.canvas.draw()
        img_buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
        plt.close(fig)

        cloth_frame = cv2.cvtColor(img_buf, cv2.COLOR_RGB2BGR)
        cloth_frame = cv2.resize(cloth_frame, (width, height))

        bg_frame = np.full((height, width, 3), 240, dtype=np.uint8)
        mask = np.any(cloth_frame < 235, axis=-1, keepdims=True)
        composited_frame = np.where(mask, cloth_frame, bg_frame)

        video_writer.write(composited_frame.astype(np.uint8))

    video_writer.release()
    logging.info(f">>> SUCCESS: Composited video successfully saved and verified at {output_video_path}")

if __name__ == "__main__":
    composite_simulation_onto_video()
