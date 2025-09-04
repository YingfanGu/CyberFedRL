"""
For this document, we will setup a basic RL pipeline using our SinglePolicySumoEnv environment.

Refer to this recent and similar SumoRL tool that has an example for MARL using RlLib:
https://github.com/LucasAlegre/sumo-rl/blob/master/experiments/a3c_4x4grid.py

Ray RlLib agent training example.
https://github.com/ray-project/ray/blob/master/rllib/examples/custom_train_fn.py
"""
import os
from netfiles import *
from seal.logging import *
from seal.trainer.fed_agent import FedPolicyTrainer
from seal.trainer.multi_agent import MultiPolicyTrainer
from seal.trainer.single_agent import SinglePolicyTrainer
from os.path import join

# This prefix is for the resubmission (aiming for SMARTCOMP).

'''
Yes, 3600 steps would be much better for traffic simulation!
360 steps = ~6 minutes (too short for meaningful traffic patterns)
3600 steps = ~60 minutes (1 hour episode, much more realistic)
This gives the RL agent time to:
Experience full traffic cycles
Learn proper signal timing strategies
See the impact of decisions over longer periods
Handle varying traffic conditions throughout the day


'''




# prefix output artifact names 
OUT_PREFIX = "Cyber"
random_routes_config = {}
trainer_kwargs = {
    # # =========================================================== #
    # # Non-Algorithm Trainer Arguments (i.e., not related to PPO). #
    # # =========================================================== #
    # "horizon": 3600,  # 1 hour episode
    # # "timesteps_per_iteration":  240,
    # # "batch_mode": "truncate_episodes",
    # # "rollout_fragment_length": 240,
    # # "train_batch_size": 240,

    # # ====================== #
    # # PPO Trainer Arguments. #
    # # ====================== #
    # # "sgd_minibatch_size": 30,
    
    
    # "timesteps_per_iteration": 3600,  # Match horizon
    # "batch_mode": "complete_episodes",  # Better for traffic control
    # "rollout_fragment_length": 1800,   # 30-minute fragments
    # "train_batch_size": 7200,          # 2 episodes worth
    # "sgd_minibatch_size": 64,          # Standard PPO setting
    
    # =========================================================== #
    # Non-Algorithm Trainer Arguments (i.e., not related to PPO). #
    # =========================================================== #
    "horizon": 360,  # 240, # NOTE: Maybe disable this?
    # "timesteps_per_iteration":  240,
    # "batch_mode": "truncate_episodes",
    # "rollout_fragment_length": 240,
    # "train_batch_size": 240,

    # ====================== #
    # PPO Trainer Arguments. #
    # ====================== #
    # "sgd_minibatch_size": 30,
    
    
}


if __name__ == "__main__":
    # Choose your network configuration directory from configs folder
    # Available options: "SMARTCOMP", "ICGPS", "CA_allred", or any other subdirectory
    # All networks must be located in: F:\Research\networkCA\0811\SUMO-FedRL\configs
    
    #
    NETWORK_CONFIG_DIR = "CA_4waystop"  # Change this to switch between configs
    
    # Training parameters
    n_episodes = 1
    fed_step = 1
    
    # Network file selection based on configuration directory
    if NETWORK_CONFIG_DIR == "SMARTCOMP":
        # SMARTCOMP network configurations (existing networks)
        NET_FILES = {
            "grid_3x3": f"configs/{NETWORK_CONFIG_DIR}/grid-3x3.net.xml",
            "grid_5x5": f"configs/{NETWORK_CONFIG_DIR}/grid-5x5.net.xml",
            "grid_7x7": f"configs/{NETWORK_CONFIG_DIR}/grid-7x7.net.xml",
        }
        print(f"Using {NETWORK_CONFIG_DIR} network configuration")
        print(f"Available networks: {list(NET_FILES.keys())}")
    elif NETWORK_CONFIG_DIR == "ICGPS":
        # ICCPS network configurations
        NET_FILES = {
            "grid_3x3": f"configs/{NETWORK_CONFIG_DIR}/grid-3x3.net.xml",
            "grid_5x5": f"configs/{NETWORK_CONFIG_DIR}/grid-5x5.net.xml",
            "grid_7x7": f"configs/{NETWORK_CONFIG_DIR}/grid-7x7.net.xml",
            "grid_9x9": f"configs/{NETWORK_CONFIG_DIR}/grid-9x9.net.xml",
            "double_loop": f"configs/{NETWORK_CONFIG_DIR}/double_loop/"
                           f"double.net.xml",
        }
        print(f"Using {NETWORK_CONFIG_DIR} network configuration")
        print(f"Available networks: {list(NET_FILES.keys())}")
    elif NETWORK_CONFIG_DIR == "CA_allred":
        # CA_allred network configurations (with all-red center intersections)
        NET_FILES = {
            "grid_3x3": f"configs/{NETWORK_CONFIG_DIR}/grid-3x3.net.xml",
            "grid_5x5": f"configs/{NETWORK_CONFIG_DIR}/grid-5x5.net.xml",
            "grid_7x7": f"configs/{NETWORK_CONFIG_DIR}/grid-7x7.net.xml",
        }
        print(f"Using {NETWORK_CONFIG_DIR} network configuration")
        print(f"Available networks: {list(NET_FILES.keys())}")
        print("NOTE: Center intersections have all-red traffic signals!")
    elif NETWORK_CONFIG_DIR == "CA_4waystop":
        # CA_4waystop network configurations (with 4-way stop center intersections)
        NET_FILES = {
            "grid_3x3": f"configs/{NETWORK_CONFIG_DIR}/grid-3x3.net.xml",
            "grid_5x5": f"configs/{NETWORK_CONFIG_DIR}/grid-5x5.net.xml",
            "grid_7x7": f"configs/{NETWORK_CONFIG_DIR}/grid-7x7.net.xml",
        }
        print(f"Using {NETWORK_CONFIG_DIR} network configuration")
        print(f"Available networks: {list(NET_FILES.keys())}")
        print("NOTE: Center intersections have 4-way stop traffic signals!")
        
        
    elif NETWORK_CONFIG_DIR == "CA_disconnected":
        # CA_disconnected network configurations (with disconnected center intersections)
        NET_FILES = {
            "grid_3x3": f"configs/{NETWORK_CONFIG_DIR}/grid-3x3.net.xml",
            "grid_5x5": f"configs/{NETWORK_CONFIG_DIR}/grid-5x5.net.xml",
            "grid_7x7": f"configs/{NETWORK_CONFIG_DIR}/grid-7x7.net.xml",
        }
        print(f"Using {NETWORK_CONFIG_DIR} network configuration")
        print(f"Available networks: {list(NET_FILES.keys())}")
        print("NOTE: Center intersections are disconnected!")
    else:
        # Custom configuration directory - add your own here
        # You can create any subdirectory structure you want in configs/
        NET_FILES = {
            "custom_network": f"configs/{NETWORK_CONFIG_DIR}/your_network.net.xml",
            # Add more networks from your custom config directory:
            # "network1": f"configs/{NETWORK_CONFIG_DIR}/network1.net.xml",
            # "network2": f"configs/{NETWORK_CONFIG_DIR}/network2.net.xml",
        }
        print(f"Using custom {NETWORK_CONFIG_DIR} network configuration")
        print(f"Available networks: {list(NET_FILES.keys())}")
        print(f"Make sure your networks exist in: configs/{NETWORK_CONFIG_DIR}/")

    RANKED = [
        True,
        False
    ]

    status = "Training with `{}`! (netfile='{}', ranked={})"
    
    
    
    
    # yingfan test
    intersection = "grid_3x3"
    ranked = True
    net_file = NET_FILES[intersection]
    
        # SinglePolicy Trainer.
    logging.info(status.format(
        "SinglePolicyTrainer", intersection, ranked
    ))
    SinglePolicyTrainer(
        net_file=net_file, ranked=ranked,
        out_prefix=OUT_PREFIX, trainer_kwargs=trainer_kwargs
    ).train(n_episodes)
    
    
    
    
    
    
    
    
'''
    
    #for loop below
    for (intersection, net_file) in NET_FILES.items():
        for ranked in RANKED:
            """
            # Federated trainer using the 'traffic' aggregation function.
            logging.info(status.format(
                "FedPolicyTrainer (aggr='traffic')", intersection, ranked
            ))
            traffic_aggr_prefix = f"{OUT_PREFIX}_traffic-aggr"
            FedPolicyTrainer(
                fed_step=fed_step, net_file=net_file, ranked=ranked,
                out_prefix=traffic_aggr_prefix,
                trainer_kwargs=trainer_kwargs,
                weight_fn="traffic"
            ).train(n_episodes)

            # Federated Trainer using the 'negative reward' aggregation function.
            logging.info(status.format(
                "FedPolicyTrainer (aggr='neg_reward')", intersection, ranked
            ))
            traffic_aggr_prefix = f"{OUT_PREFIX}_neg-reward-aggr"
            FedPolicyTrainer(
                fed_step=fed_step, net_file=net_file, ranked=ranked,
                out_prefix=traffic_aggr_prefix,
                trainer_kwargs=trainer_kwargs,
                weight_fn="neg_reward"
            ).train(n_episodes)
            """

            # Federated Trainer using the 'positive reward' aggregation function.
            
            
            # logging.info(status.format(
            #     "FedPolicyTrainer (aggr='pos_reward')", intersection, ranked
            # ))
            # traffic_aggr_prefix = f"{OUT_PREFIX}_pos-reward-aggr"
            # FedPolicyTrainer(
            #     fed_step=fed_step, net_file=net_file, ranked=ranked,
            #     out_prefix=traffic_aggr_prefix,
            #     trainer_kwargs=trainer_kwargs,
            #     weight_fn="pos_reward"
            # ).train(n_episodes)





            # # Federated Trainer using the 'naive' weighting aggregation function.
            # logging.info(status.format(
            #     "FedPolicyTrainer (aggr='naive')", intersection, ranked
            # ))
            # traffic_aggr_prefix = f"{OUT_PREFIX}_naive-aggr"
            # FedPolicyTrainer(
            #     fed_step=fed_step, net_file=net_file, ranked=ranked,
            #     out_prefix=traffic_aggr_prefix,
            #     trainer_kwargs=trainer_kwargs,
            #     weight_fn="naive"
            # ).train(n_episodes)





            # # MultiPolicy Trainer.
            # logging.info(status.format(
            #     "MultiPolicyTrainer", intersection, ranked
            # ))
            # MultiPolicyTrainer(
            #     net_file=net_file, ranked=ranked,
            #     out_prefix=OUT_PREFIX, trainer_kwargs=trainer_kwargs
            # ).train(n_episodes)



            # SinglePolicy Trainer.
            logging.info(status.format(
                "SinglePolicyTrainer", intersection, ranked
            ))
            SinglePolicyTrainer(
                net_file=net_file, ranked=ranked,
                out_prefix=OUT_PREFIX, trainer_kwargs=trainer_kwargs
            ).train(n_episodes)



'''