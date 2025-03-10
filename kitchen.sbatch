#!/bin/bash
#SBATCH -JKitchenv1               # Job name  
#SBATCH -N1 --ntasks-per-node=1          # Number of nodes and cores per node required 
#SBATCH --gres=gpu:H100:1                # GPU type (H100) and number of GPUs 
#SBATCH --mem-per-gpu=224GB              # Memory per CPU core, 8 CPUs/GPU 
#SBATCH -t2:30:00                        # Duration of the job (Ex: 1 hour) 
#SBATCH -oReport-kitchen-%j.out
#SBATCH --mail-type=BEGIN,END,FAIL       # Mail preferences 
#SBATCH --mail-user=vmaheshwari32@gatech.edu # E-mail address for notifications 
cd /home/hice1/vmaheshwari32/METRA/
module load anaconda3
conda activate metra
python tests/main.py --run_group Debug --env kitchen --max_path_length 50 --seed 0 --traj_batch_size 8 --n_parallel 4 --normalizer_type off --num_video_repeats 1 --frame_stack 3 --sac_max_buffer_size 100000 --algo metra --sac_lr_a -1 --trans_optimization_epochs 100 --n_epochs_per_log 25 --n_epochs_per_eval 250 --n_epochs_per_save 1000 --n_epochs_per_pt_save 1000 --discrete 1 --dim_option 24 --encoder 1 --sample_cpu 0
