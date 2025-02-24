from enum import Enum

class ConfigModbusMap(Enum):
    addr_reset_max_min = 12002

    ### measurement setup ###
    addr_meas_setup_access = 6000
    addr_meas_wiring = 6001
    addr_meas_reference_voltage = 6003
    addr_meas_vt_primary_ll_voltage = 6005
    addr_meas_vt_secondary_ll_voltage = 6007
    addr_meas_min_measured_secondary_ln_voltage = 6008
    addr_meas_reference_voltage_mode = 6009
    addr_meas_reference_current = 6015
    addr_meas_ct_primary_current = 6017
    addr_meas_ct_secondary_current = 6019


    addr_demand_sync_mode = 6028
    addr_demand_num_of_sub_interval = 6029
    addr_demand_sub_interval_time = 6030
    addr_reset_demand = 12000
    addr_reset_demand_peak = 12001
    addr_demand_sync = 12015
    
    addr_setup_lock = 2900
    addr_control_lock = 2901