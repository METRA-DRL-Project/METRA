# METRA SETUP

## GT PACE Cluster

We are using GT's [PACE](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042102) cluster for high performance computing resources. To be able to set that up:
- Go to knowledge > all knowledge and you can search up. This compute is free (and theoretically unlimited -- students are queued though) for all GT Students (or at least CoC students).
-  We use ICE clusters because Phoenix is used by Research people. To connect to the cluster, you need to be on eduroam wifi or have VPN. For VPN, you can use Global Connect’s desktop VPN.

## Steps to Reproduce on PACE
1. Logging into the cluster:
  - in your terminal type in `ssh [gburdell]@login-ice.pace.gatech.edu`. When pressed enter it will ask your password which will be your GT password.
  - Within your directory, /home/hice1/[gburdell]/ will be a scratch folder -- it is a temporary folder, don't put useful stuff in it. 
2.  Clone the official implementation given [here]()
3.  Go to requirements.txt of METRA project
    - You can use Remote SSH on VSCode for that and change the instal==x.x.x to pip-install==x.x.x (the package name has been changed -- version need not be changed)
   

4. Now run, `salloc --gres=gpu:A40:1 --ntasks-per-node=1` ← This allocated A40 GPU to you. There are many other GPUs which you might be able to switch between (I have not tested yet.). You need to have GPU on so that the environment we are going to create runs on GPU -- it cannot run on CPUs and installing libraries that are not GPU compatible will give you a hard time.

5. Then run `module load anaconda3` to load conda.
6. Then, `conda create --name metra python=3.8` (3.8 is important… newer versions of python have dependency issues)
7. `conda activate metra`
8. `pip install -r requirements.txt --no-deps`
9. Now, step inside the METRA folder (i.e. cd METRA) and run `pip install -e .` -- This might result in some dependencies conflict between protobuf, scipy, tensorboard and joblib. We will resolve that soon
   - If it says couldn’t find swig, run `pip install swig`

10. Being inside the folder run `pip install -e garaged`
    -  If it says couldn’t find swig, run `pip install swig`

11. Solving protobuf and joblib error: run `pip install -U protobuf==3.19.4` and `pip install -U joblib==1.2.0`
12. Setting up mujoco simulator (in the next many steps). You can download Mujocu for linux on mac using the link on the third step of [here](https://gist.github.com/saratrajput/60b1310fe9d9df664f9983b38b50d5da)
13. Create a .mujoco folder at the same level as METRA and scratch. And transfer the .tar.gz file in this folder (You can use FileZilla for transfer)
14. Unzip the .tar.gz file by `tar -xvf mujoco210-linux-x86_64.tar.gz` (Assuming you are now inside the .mujoco folder)
15. Add mujoco simulator to the path so that it can be found by METRA by typing: ` echo 'export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}/home/hice1/{username}/.mujoco/mujoco210/bin"' >> .bashrc` (assuming you are at your username folder -- i.e. ls-ing gives METRA and scratch)
16. Link nvidia drivers with the simulator by: `echo 'export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}/usr/lib/nvidia"' >> .bashrc` (assuming you are at your username folder)
17.  `source .bashrc` to activate the updates on the bashrc files.
18.  You should be done with the setup. Feel free to run any experiment as shown in the README of the official implementation of the METRA project

```
python tests/main.py --run_group Debug --env ant --max_path_length 200 --seed 0 --traj_batch_size 8 --n_parallel 1 --normalizer_type preset --eval_plot_axis -50 50 -50 50 --trans_optimization_epochs 50 --n_epochs_per_log 100 --n_epochs_per_eval 1000 --n_epochs_per_save 10000 --sac_max_buffer_size 1000000 --algo metra --discrete 0 --dim_option 2
```

## Dependencies 
### Python and Package Management
- python 3.8
- Conda (Anaconda3)

### Python Packages
- `protobuf==3.19.4`
- `joblib==1.2.0`
- `swig`
- `pip install -e .` (for METRA)
- `pip install -e garaged`

### Additional Dependencies
- Mujoco 2.1.0 (for Linux / MacOS)

### Cluster Specific
- `module load anaconda3`
- `salloc --gres=gpu:A40:1 --ntasks-per-node=1`


    
