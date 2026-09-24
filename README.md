# boba-cpu

# Boba CPU: Headless Digital Twin Simulation & Telemetry Engine

A CPU/Metal (MPS) port and headless telemetry pipeline for Boba (ECCV 2026). This repository decouples spring-mass physics simulation from native CUDA and desktop OpenGL display requirements, enabling automated, reproducible digital twin experiments on commodity silicon (macOS Apple Silicon/Intel & Linux CPU).

---

## Features

- **Decoupled Architecture:** Runs physics solvers and kinematics headless without an active window server or display backend.
- **Hardware Agnostic:** Replaces CUDA/CUSOLVER linear algebra bindings with PyTorch CPU / Apple Metal Performance Shaders (MPS) routines.
- **Batch Experimentation:** Programmatic runner for multi-scenario digital twin parameter sweeps.
- **Kinematic Telemetry & Prompt Synthesis:** Extracts real-time simulation metrics (velocities, energy, bounding trajectories) and formats them into structured prompts for downstream AI video generators.

---

## 1. Environment Setup

### Prerequisites
- macOS (Apple Silicon or Intel) or Linux
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda
- System packages (macOS via Homebrew):
  ```bash
  brew install glfw

# 2 Create and Activate the Conda Environment
Create the phystwin-mac environment with Python 3.10 and core scientific libraries:

conda create -y -n phystwin-mac -c pytorch -c conda-forge \
  python=3.10 pytorch torchvision torchaudio \
  glfw pyopengl "numpy<2" scipy ninja tqdm
conda activate phystwin-mac

Install Python Dependencies
pip install scipy matplotlib imageio imageio-ffmpeg plyfile trimesh opencv-python gdown

# 3a Run a Headless Digital Twin Simulation

Execute single headless simulation cases without opening an interactive GUI window:
python run_headless_simulation.py \
  --mode perf \
  --case_name double_lift_cloth_3 \
  --headless

  
# 3b Batch Simulation & Trajectory Collection

Run parameter sweeps across configured scenarios and automatically generate trajectory animations:
python batch_collect_and_animate.py \
  --config data_config.csv \
  --output_dir batch_simulation_results


# 3c Run Custom / New Experiment Cases

Execute targeted runs with parameterized physics bounds:
python run_new_case.py \
  --case_name double_lift_cloth_3 \
  --steps 500 \
  --save_telemetry

  
# 4 Telemetry & AI Prompt Synthesis
Transform collected physical simulation trajectories into structured descriptive prompts and video overlays:

Generate AI Video Prompts from Physical Metrics
python generate_ai_video_prompt_with_stats.py \
  --data_dir batch_simulation_results/double_lift_cloth_3 \
  --output prompt_output.txt

Render and Composite Digital Twin Visualizations

Render digital twin viewpoint
python render_digital_twin.py --case_name double_lift_cloth_3

Composite trajectory tracking overlay onto video captures
python composite_onto_video.py \
  --input_video assets/sample_input.mp4 \
  --telemetry_data batch_simulation_results/double_lift_cloth_3/telemetry.json \
  --output_video results/composited_output.mp4


# 5 Repository Structure

├── mac_patch.py                     # Metal/CPU emulation and CUDA hook overrides
├── run_headless_simulation.py       # Standalone headless execution driver
├── batch_collect_and_animate.py     # Automated batch runner & 2D/3D animator
├── run_new_case.py                  # Entrypoint for custom parameter testcases
├── data_config.csv                  # Experiment scenario registry
├── generate_ai_video_prompt_with_stats.py # Kinematics-to-prompt synthesis
├── composite_onto_video.py          # Video overlay and telemetry compositor
├── render_digital_twin.py           # Offline digital twin renderer
├── qqtt/                            # Core physics and spring-mass solvers
├── simple_knn/                      # Spatial neighbor lookup routines
├── gaussian_splatting/              # Splatting data representations & math utilities
├── configs/                         # Physical parameter YAML/JSON manifests
└── benchmarks/                      # Benchmark evaluation setups


# 6 Citation & Attribution

This engine builds upon the Boba dynamic simulation framework (ECCV 2026). See NOTICE and LICENSE for details.
---

### How to update it on GitHub

1. Go to your repository at **[https://github.com/sahibbedi/boba-cpu](https://github.com/sahibbedi/boba-cpu)**[cite: 5].
2. Click on `README.md`.
3. Click the **pencil icon (Edit)** in the top-right corner of the file viewer[cite: 5].
4. Paste the text above to replace the file contents.
5. Click **Commit changes...** at the top right and commit directly to `main`[cite: 5].

