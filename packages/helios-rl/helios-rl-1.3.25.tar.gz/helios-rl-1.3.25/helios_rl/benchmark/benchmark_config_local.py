benchmark_local_config = {
    'sailing':{
        "env_select":"simple_river",
        "adapter_select": ["Language"],
        "training_action_cap": 100,
        "testing_action_cap":100,
        "reward_signal": [0.5,0,-0.1],
        "sub_goal": "None",
        "supervised_rewards":"False",
        "y_limit":25,
        "obs_precision":2
    }

}