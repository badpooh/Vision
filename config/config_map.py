from enum import Enum

class ConfigModbusMap(Enum):
    ### modbus map 에서 -1 값 ###
    addr_reset_max_min = 12002

    ### measurement setup ###
    ### UINT16 ###
    addr_setup_access = 6000
    addr_wiring = 6001
    addr_vt_secondary_ll_voltage = 6007
    addr_min_measured_secondary_ln_voltage = 6008
    addr_reference_voltage_mode = 6009
    addr_ct_secondary_current = 6019
    addr_min_measured_current = 6020
    addr_tdd_reference = 6023
    addr_demand_sync_mode = 6028
    addr_num_of_sub_interval = 6029
    addr_sub_interval_time = 6030
    addr_thermal_response_index = 6031
    addr_demand_power_type = 6032
    addr_phase_power_calculation = 6033
    addr_total_power_calculation = 6034
    addr_pf_value_at_no_load = 6035
    addr_pf_sign = 6036
    addr_reactive_power_sign = 6037
    addr_default_frequency = 6038
    addr_max_harmonic_order = 6039
    addr_rotating_sequence = 6040

    ### UINT32 ###
    addr_reference_voltage = 6003
    addr_vt_primary_ll_voltage = 6005
    addr_reference_current = 6015
    addr_ct_primary_current = 6017
    addr_nominal_tdd_current = 6021


    
    
    
    addr_reset_demand = 12000
    addr_reset_demand_peak = 12001
    addr_demand_sync = 12015
    
    addr_setup_lock = 2900
    addr_control_lock = 2901