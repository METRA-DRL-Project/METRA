#!/bin/bash
#SBATCH -JHumanoidv1               # Job name  
#SBATCH -N1 --ntasks-per-node=1          # Number of nodes and cores per node required 
#SBATCH --gres=gpu:H100:1                # GPU type (H100) and number of GPUs 
#SBATCH --mem-per-gpu=224GB              # Memory per CPU core, 8 CPUs/GPU 
#SBATCH -t2:30:00                        # Duration of the job (Ex: 1 hour) 
#SBATCH -oReport-humanoid-%j.out
#SBATCH --mail-type=BEGIN,END,FAIL       # Mail preferences 
#SBATCH --mail-user=vmaheshwari32@gatech.edu # E-mail address for notifications 
cd /home/hice1/vmaheshwari32/METRA/
module load anaconda3
conda activate metra
python tests/main.py --run_group Debug --env dmc_humanoid --max_path_length 200 --seed 0 --traj_batch_size 8 --n_parallel 4 --normalizer_type off --video_skip_frames 2 --frame_stack 3 --sac_max_buffer_size 300000 --eval_plot_axis -15 15 -15 15 --algo metra --trans_optimization_epochs 200 --n_epochs_per_log 25 --n_epochs_per_eval 125 --n_epochs_per_save 1000 --n_epochs_per_pt_save 1000 --discrete 0 --dim_option 2 --encoder 1 --sample_cpu 0
