from enum import Enum

class ConfigModbusMap(Enum):
    addr_reset_max_min = 12002
    addr_meas_setup_access = 6000
    addr_demand_sync_mode = 6028
    addr_demand_num_of_sub_interval = 6029
    addr_demand_sub_interval_time = 6030
    addr_reset_demand = 12000
    addr_reset_demand_peak = 12001
    addr_demand_sync = 12015
    
    addr_setup_lock = 2900
    addr_control_lock = 2901