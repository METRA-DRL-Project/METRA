def make_env(args):
    env = dmc.make('cheetah_run_forward_color', obs_type='states', frame_stack=1, action_repeat=2, seed=args.seed)
    env = RenderWrapper(env)
    env = FrameStackWrapper(env, 3)
    env = consistent_normalize(env, normalize_obs=False)
    return env

@wrap_experiment
def run(ctxt=None):
    args = get_args()
    set_seed(args.seed)
    
    # Initialize environment
    env = make_env(args)
    obs_dim = env.spec.observation_space.flat_dim
    action_dim = env.spec.action_space.flat_dim
    
    # Initialize policy and Q functions
    device = torch.device('cuda' if args.use_gpu else 'cpu')
    
    policy_module = GaussianMLPTwoHeadedModuleEx(
        input_dim=obs_dim + args.dim_option,
        output_dim=action_dim,
        hidden_sizes=[1024, 1024],
        hidden_nonlinearity=torch.relu,
        normal_distribution_cls=TanhNormal
    )
    
    option_policy = PolicyEx(
        module=policy_module,
        name='option_policy',
        option_info={'dim_option': args.dim_option}
    )

    qf1 = GaussianMLPModuleEx(
        input_dim=obs_dim + args.dim_option,
        output_dim=action_dim,
        hidden_sizes=[1024, 1024],
        hidden_nonlinearity=torch.relu
    )
    
    qf2 = GaussianMLPModuleEx(
        input_dim=obs_dim + args.dim_option,
        output_dim=action_dim,
        hidden_sizes=[1024, 1024],
        hidden_nonlinearity=torch.relu
    )

    log_alpha = ParameterModule(torch.Tensor([0.0]))

    # Initialize algorithm
    algo = METRA(
        env_spec=env.spec,
        option_policy=option_policy,
        qf1=qf1,
        qf2=qf2,
        log_alpha=log_alpha,
        tau=5e-3,
        scale_reward=1.0,
        target_coef=1.0,
        replay_buffer=None,
        min_buffer_size=10000,
        inner=True,
        num_alt_samples=100,
        split_group=65536,
        dual_reg=True,
        dual_slack=1e-3,
        dual_dist='one',
        max_path_length=args.max_path_length,
        device=device
    )

    # Initialize runner
    runner = OptionLocalRunner(ctxt)
    runner.setup(
        algo=algo,
        env=env,
        sampler_cls=OptionMultiprocessingSampler,
        n_workers=4
    )

    # Train
    runner.train(n_epochs=args.n_epochs, batch_size=8)