#!/usr/bin/env python3
import os
import sys
import torch
import numpy as np
import argparse
import datetime
import tempfile
import platform
import functools
import wandb
import multiprocessing as mp

from garage import wrap_experiment
from garage.torch.modules import GaussianMLPTwoHeadedModuleEx, GaussianMLPModuleEx, GaussianMLPIndependentStdModuleEx
from garage.torch.modules import ParameterModule
from garage.torch.distributions import TanhNormal
from garage.torch import global_device
from garage.torch.policies import PolicyEx
from garage.sampler import OptionMultiprocessingSampler
from garage.experiment.deterministic import set_seed
from garage.torch.utils import xavier_normal_ex

from iod.metra import METRA
from iod.utils import consistent_normalize, get_normalizer_preset
from envs.custom_dmc_tasks import dmc
from envs.custom_dmc_tasks.pixel_wrappers import RenderWrapper, FrameStackWrapper

# Constants
EXP_DIR = 'exp'
START_METHOD = 'spawn'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default='dmc_cheetah')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--n_epochs', type=int, default=1000)
    parser.add_argument('--max_path_length', type=int, default=200)
    parser.add_argument('--dim_option', type=int, default=2)
    parser.add_argument('--encoder', type=int, default=1)
    parser.add_argument('--use_gpu', type=int, default=1)
    return parser.parse_args()




if __name__ == '__main__':
    mp.set_start_method(START_METHOD)
    run()
