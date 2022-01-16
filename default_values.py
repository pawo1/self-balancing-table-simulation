values = {}
SI_base = 0.01

Impulse = 0
Sinusoidal = 1
Positional = 0
Incremental = 1

values["Simulation 1"] = {"x": {}, "y": {}}
values["Simulation 2"] = {"x": {}, "y": {}}

# Global values, same for all Simulations
values["Global"] = {"set_tp": 0.01, "set_simulation_time": 60}

""" Starting values for Simulation 1 """

# PID config
values["Simulation 1"]["set_pid_type"] = Positional
values["Simulation 1"]["set_kp"] = 1.0
values["Simulation 1"]["set_ti"] = 0.145
values["Simulation 1"]["set_td"] = 0.25

# Servo config
values["Simulation 1"]["set_angle_min"] = -30.0
values["Simulation 1"]["set_angle_max"] = 30.0
values["Simulation 1"]["set_voltage_min"] = -10.0
values["Simulation 1"]["set_voltage_max"] = 10.0

# Table config
values["Simulation 1"]["set_acceleration"] = "Earth (9.81)"

values["Simulation 1"]["x"]["set_pos_init"] = 0.05
values["Simulation 1"]["x"]["set_speed_init"] = 0
values["Simulation 1"]["x"]["set_asked_value"] = 1

values["Simulation 1"]["y"]["set_pos_init"] = -0.10
values["Simulation 1"]["y"]["set_speed_init"] = 0
values["Simulation 1"]["y"]["set_asked_value"] = 0.5

# Noise config
values["Simulation 1"]["set_noise_active"] = False

values["Simulation 1"]["x"]["set_noise_type"] = Impulse
values["Simulation 1"]["x"]["set_noise_level"] = 10
values["Simulation 1"]["x"]["set_noise_period"] = 60
values["Simulation 1"]["x"]["set_noise_frequency"] = 1

values["Simulation 1"]["y"]["set_noise_type"] = Impulse
values["Simulation 1"]["y"]["set_noise_level"] = 10
values["Simulation 1"]["y"]["set_noise_period"] = 60
values["Simulation 1"]["y"]["set_noise_frequency"] = 1

# Starting values for Simulation 2
values["Simulation 2"]["set_pid_type"] = Positional
values["Simulation 2"]["set_kp"] = 1.0
values["Simulation 2"]["set_ti"] = 0.145
values["Simulation 2"]["set_td"] = 0.25

# Servo config
values["Simulation 2"]["set_angle_min"] = -30.0
values["Simulation 2"]["set_angle_max"] = 30.0
values["Simulation 2"]["set_voltage_min"] = -10.0
values["Simulation 2"]["set_voltage_max"] = 10.0

# Table config
values["Simulation 2"]["set_acceleration"] = "Earth (9.81)"

values["Simulation 2"]["x"]["set_pos_init"] = 0.05
values["Simulation 2"]["x"]["set_speed_init"] = 0
values["Simulation 2"]["x"]["set_asked_value"] = 1

values["Simulation 2"]["y"]["set_pos_init"] = -0.10
values["Simulation 2"]["y"]["set_speed_init"] = 0
values["Simulation 2"]["y"]["set_asked_value"] = 0.5

# Noise config
values["Simulation 2"]["set_noise_active"] = False

values["Simulation 2"]["x"]["set_noise_type"] = Impulse
values["Simulation 2"]["x"]["set_noise_level"] = 10
values["Simulation 2"]["x"]["set_noise_period"] = 60.0
values["Simulation 2"]["x"]["set_noise_frequency"] = 1.0

values["Simulation 2"]["y"]["set_noise_type"] = Impulse
values["Simulation 2"]["y"]["set_noise_level"] = 10
values["Simulation 2"]["y"]["set_noise_period"] = 60.0
values["Simulation 2"]["y"]["set_noise_frequency"] = 1.0
