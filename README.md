# METRA: Scalable Unsupervised RL with Metric-Aware Abstraction

This repository contains the official implementation of **METRA: Scalable Unsupervised RL with Metric-Aware Abstraction**.
The implementation is based on
[Lipschitz-constrained Unsupervised Skill Discovery](https://github.com/seohongpark/LSD).

Visit [the authors' project page](https://seohong.me/projects/metra/) for more results including videos.


# Setup on GT PACE Cluster
We will be using Georgia Tech's [PACE ICE](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042102) cluster for GPU compute resources.
For any questions: refer to knowledge > all knowledge. To connect to the cluster, you need to be on eduroam wifi or be connected to the Global Connect VPN.

1. Log into the cluster `ssh [gburdell]@login-ice.pace.gatech.edu` and enter your GT password. 
2. Clone the repository `git clone https://github.com/METRA-DRL-Project/METRA.git`.
3. Allocate A40 GPU `salloc --gres=gpu:A40:1 --ntasks-per-node=1`. Optionally use A100 or H100.
5. Load Conda `module load anaconda3`.
6. Create conda env `conda create --name metra python=3.8` (3.8 is important… newer versions of python have dependency issues).
7. Activate conda env `conda activate metra`.
8. Install dependencies `cd METRA && pip install -r requirements.txt --no-deps`
9. Run `pip install -e .` If swig not found, run `pip install swig`
9. Run `pip install -e garaged`
10. Solving protobuf and joblib error: `pip install -U protobuf==3.19.4` and `pip install -U joblib==1.2.0`

## Setup Mujoco 
10. `cd.. && mkdir .mujoco && cd .mujoco` in the same root directory as METRA.
11. Download Mujocu for linux using the link [here](https://gist.github.com/saratrajput/60b1310fe9d9df664f9983b38b50d5da)
12. Unzip the .tar.gz file `tar -xvf mujoco210-linux-x86_64.tar.gz`
13. Add mujoco simulator to the path ` echo 'export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}/home/hice1/{username}/.mujoco/mujoco210/bin"' >> .bashrc` 
14. Add nvidia drivers to the path `echo 'export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}/usr/lib/nvidia"' >> .bashrc`
15. Run `source .bashrc`
16. You should be done with the setup. You should be able to run ant and cheetah experiments as shown below.
17. For pixel based environments (like humanoid, kitchen, and quadraped) you have to change mujoco version to 2.2 (installation steps are same as before).

# Reproduced Experiment Runs
You can view the [Code Demonstration folder](https://drive.google.com/drive/folders/1cmt6VuAH89VTA2ug0ZBflqTvUKEzJ7lO?usp=sharing) for the runs. We didn’t run the experiments to completion, as individual environment runs took the authors 16-24 hours on A5000 clusters. Instead, we ran them on a single A100 GPU with a 2-hour cap. The initial trajectories and plots (available in the linked Google Drive) align with the authors' results.

# Dependencies
## Python and Package Management
- Python 3.8
- Conda (Anaconda3)

## Additional Dependencies
- Mujoco 2.1.0 (Linux/macOS)

## Installation

```
conda create --name metra python=3.8
conda activate metra
pip install -r requirements.txt --no-deps
pip install -e .
pip install -e garaged
```

## Examples

```
# METRA on state-based Ant (2-D skills)
python tests/main.py --run_group Debug --env ant --max_path_length 200 --seed 0 --traj_batch_size 8 --n_parallel 1 --normalizer_type preset --eval_plot_axis -50 50 -50 50 --trans_optimization_epochs 50 --n_epochs_per_log 100 --n_epochs_per_eval 1000 --n_epochs_per_save 10000 --sac_max_buffer_size 1000000 --algo metra --discrete 0 --dim_option 2

# LSD on state-based Ant (2-D skills)
python tests/main.py --run_group Debug --env ant --max_path_length 200 --seed 0 --traj_batch_size 8 --n_parallel 1 --normalizer_type preset --eval_plot_axis -50 50 -50 50 --trans_optimization_epochs 50 --n_epochs_per_log 100 --n_epochs_per_eval 1000 --n_epochs_per_save 10000 --sac_max_buffer_size 1000000 --algo metra --dual_reg 0 --spectral_normalization 1 --discrete 0 --dim_option 2

# DADS on state-based Ant (2-D skills)
python tests/main.py --run_group Debug --env ant --max_path_length 200 --seed 0 --traj_batch_size 8 --n_parallel 1 --normalizer_type preset --eval_plot_axis -50 50 -50 50 --trans_optimization_epochs 50 --n_epochs_per_log 100 --n_epochs_per_eval 1000 --n_epochs_per_save 10000 --sac_max_buffer_size 1000000 --algo dads --inner 0 --unit_length 0 --dual_reg 0 --discrete 0 --dim_option 2

# DIAYN on state-based Ant (2-D skills)
python tests/main.py --run_group Debug --env ant --max_path_length 200 --seed 0 --traj_batch_size 8 --n_parallel 1 --normalizer_type preset --eval_plot_axis -50 50 -50 50 --trans_optimization_epochs 50 --n_epochs_per_log 100 --n_epochs_per_eval 1000 --n_epochs_per_save 10000 --sac_max_buffer_size 1000000 --algo metra --inner 0 --unit_length 0 --dual_reg 0 --discrete 0 --dim_option 2

# METRA on state-based HalfCheetah (16 skills)
python tests/main.py --run_group Debug --env half_cheetah --max_path_length 200 --seed 0 --traj_batch_size 8 --n_parallel 1 --normalizer_type preset --trans_optimization_epochs 50 --n_epochs_per_log 100 --n_epochs_per_eval 1000 --n_epochs_per_save 10000 --sac_max_buffer_size 1000000 --algo metra --discrete 1 --dim_option 16

# METRA on pixel-based Quadruped (4-D skills)
python tests/main.py --run_group Debug --env dmc_quadruped --max_path_length 200 --seed 0 --traj_batch_size 8 --n_parallel 4 --normalizer_type off --video_skip_frames 2 --frame_stack 3 --sac_max_buffer_size 300000 --eval_plot_axis -15 15 -15 15 --algo metra --trans_optimization_epochs 200 --n_epochs_per_log 25 --n_epochs_per_eval 125 --n_epochs_per_save 1000 --n_epochs_per_pt_save 1000 --discrete 0 --dim_option 4 --encoder 1 --sample_cpu 0

# METRA on pixel-based Humanoid (2-D skills)
python tests/main.py --run_group Debug --env dmc_humanoid --max_path_length 200 --seed 0 --traj_batch_size 8 --n_parallel 4 --normalizer_type off --video_skip_frames 2 --frame_stack 3 --sac_max_buffer_size 300000 --eval_plot_axis -15 15 -15 15 --algo metra --trans_optimization_epochs 200 --n_epochs_per_log 25 --n_epochs_per_eval 125 --n_epochs_per_save 1000 --n_epochs_per_pt_save 1000 --discrete 0 --dim_option 2 --encoder 1 --sample_cpu 0

# METRA on pixel-based Kitchen (24 skills)
python tests/main.py --run_group Debug --env kitchen --max_path_length 50 --seed 0 --traj_batch_size 8 --n_parallel 4 --normalizer_type off --num_video_repeats 1 --frame_stack 3 --sac_max_buffer_size 100000 --algo metra --sac_lr_a -1 --trans_optimization_epochs 100 --n_epochs_per_log 25 --n_epochs_per_eval 250 --n_epochs_per_save 1000 --n_epochs_per_pt_save 1000 --discrete 1 --dim_option 24 --encoder 1 --sample_cpu 0
```
