benchmark_config = {
    'sailing':{   
        "name": "Sailing",
        "problem_type": "Sailing",
        
        "experience_sample_batch_ratio": 0,
        
        "number_training_episodes": 10000,
        "number_training_repeats": 5,
        "number_training_seeds": 1,

        "test_agent_type":"all",
        "number_test_episodes": 500,
        "number_test_repeats": 5,

        "agent_select": ["Qlearntab"],
        "agent_parameters":{
            "Qlearntab":{
                "alpha": 0.1,
                "gamma": 0.95,
                "epsilon": 0.2,
                "epsilon_step":0.01
                },
            "Neural_Q":{
                    "sequence_size": 1,
                    "input_size": 768,
                    "output_size": 1000,
                    "seq_hidden_dim": 10,
                    "hidden_dim": 128,
                    "num_hidden": 2,
                    "memory_size": 2000,
                    "epsilon": 0.2,
                    "epsilon_step":0.01
                },
            "Neural_Q_language":{
                    "sequence_size": 2,
                    "input_size": 384,
                    "output_size": 1000,
                    "seq_hidden_dim": 10,
                    "hidden_dim": 128,
                    "num_hidden": 2,
                    "memory_size": 2000,
                    "epsilon": 0.2,
                    "epsilon_step":0.01
                },
            "Random":{}}
    }

}