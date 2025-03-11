# METRA: Scalable Unsupervised RL with Metric-Aware Abstraction

This repository contains the official implementation of **METRA: Scalable Unsupervised RL with Metric-Aware Abstraction**.
The implementation is based on
[Lipschitz-constrained Unsupervised Skill Discovery](https://github.com/seohongpark/LSD).

Visit [our project page](https://seohong.me/projects/metra/) for more results including videos.


# GT PACE Cluster
We will be using Georgia Tech's [PACE](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042102) cluster for resources and high performace computing.
For any questions: refer to knowledge > all knowledge and you can search it up. This compute is free (and theoretically unlimited -- students are queued though) for all GT Students (or at least CoC students). We use ICE clusters because Phoenix is used by Research people. To connect to the cluster, you need to be on eduroam wifi or have VPN. You can use Global Connect’s desktop VPN.

# Steps for Setup
1.  Logging into the cluster:
in the terminal type in: `ssh [gburdell]@login-ice.pace.gatech.edu`. When pressed enter it will ask your password which will be your GT password. 
- Within your directory, /home/hice1/[gburdell]/ will be a scratch folder -- it is a temporary folder, don't put useful stuff in it.

2. Clone the the official implementation.
3. Go to requirements.txt of METRA project (you can use Remote SSH on VSCode for that) and change the instal==x.x.x to pip-install==x.x.x (the package name has been changed -- version need not be changed)
4. Now run, `salloc --gres=gpu:A40:1 --ntasks-per-node=1` ← This allocates A40 GPU to you. There are many other GPUs which you might be able to switch between (I have not tested yet.). You need to have GPU on so that the environment we are going to create runs on GPU -- it cannot run on CPUs and installing libraries that are not GPU compatible will give you a hard time
5. Run `module load anaconda3` to load conda.
6.  Then, `conda create --name metra python=3.8` (3.8 is important… newer versions of python have dependency issues)
7.   `conda activate metra`
8.   `pip install -r requirements.txt --no-deps`
9.   Now, step inside the METRA folder (i.e. cd METRA) and run `pip install -e .` -- This might result in some dependencies conflict between protobuf, scipy, tensorboard and joblib. We will resolve that soon.
- If it says couldn’t find swig, run `pip install swig`

10. Being inside the folder run `pip install -e garaged`
- If it says couldn’t find swig, run `pip install swig`

11. Solving protobuf and joblib error: run `pip install -U protobuf==3.19.4` and `pip install -U joblib==1.2.0`
12. Setting up mujoco simulator (in the next many steps). You can download Mujocu for linux on macOS using the link on the third step of [here](https://gist.github.com/saratrajput/60b1310fe9d9df664f9983b38b50d5da)
13.  Create a .mujoco folder at the same level as METRA and scratch. And transfer the .tar.gz file in this folder (you can use FileZilla for transfer)
14.  Unzip the .tar.gz file by `tar -xvf mujoco210-linux-x86_64.tar.gz` (Assuming that you are now inside the .mujoco folder)
15.  Add mujoco simulator to the path so that it can be found by METRA by typing: ` echo 'export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}/home/hice1/{username}/.mujoco/mujoco210/bin"' >> .bashrc` (assuming you are at your username folder -- i.e. ls-ing gives METRA and scratch)
16.  Link nvidia drivers with the simulator by: `echo 'export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}/usr/lib/nvidia"' >> .bashrc`
17. `source .bashrc` to activate the updates on the bashrc files.
18. You should be done with the setup. Feel free to run any experiment as shown in the README of the metra project given at the start of this README. The one I ran is:
```
python tests/main.py --run_group Debug --env ant --max_path_length 200 --seed 0 --traj_batch_size 8 --n_parallel 1 --normalizer_type preset --eval_plot_axis -50 50 -50 50 --trans_optimization_epochs 50 --n_epochs_per_log 100 --n_epochs_per_eval 1000 --n_epochs_per_save 10000 --sac_max_buffer_size 1000000 --algo metra --discrete 0 --dim_option 2
```

# Dependencies
## Python and Package Management
- Python 3.8
- Conda (Anaconda3)

## Python Packages
- `protobuf==3.19.4`
- `joblib==1.2.0`
- `swig`

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
