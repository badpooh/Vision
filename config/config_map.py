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
    addr_reference_voltage_setup_access = 6050
    addr_reference_voltage_type = 6051
    ### UINT32 ###
    addr_reference_voltage = 6003
    addr_vt_primary_ll_voltage = 6005
    addr_reference_current = 6015
    addr_ct_primary_current = 6017
    addr_nominal_tdd_current = 6021

    ### meter event setup ###
    addr_dip_setup_access = 5100
    addr_dip = 5101
    addr_dip_threshold = 5102
    addr_dip_hysteresis = 5103
    addr_3phase_dip_setup_access = 5110
    addr_3phase_dip = 5111
    addr_swell_setup_access = 5120
    addr_swell = 5121
    addr_swell_threshold = 5122
    addr_swell_hysteresis = 5123
    addr_semi_event_setup_access = 5160
    addr_semi = 5161
    addr_itic_event_setup_access = 5190
    addr_itic = 5191
    addr_iec_event_setup_access = 5220
    addr_iec = 5221

    ### meter network setup ###
    addr_dhcp_setup_access = 3720
    addr_dhcp = 3721
    addr_rs485_setup_access = 3700
    addr_device_address = 3701
    addr_bit_rate = 3702
    addr_parity = 3703
    addr_stop_bit = 3704
    addr_modbus_timeout_setup_access = 3620
    addr_modbus_timeout = 3621
    addr_rstp_setup_access = 3640
    addr_rstp = 3641
    addr_storm_control_setup_access = 3680
    addr_storm_control = 3681
    addr_rs485_map_setup_access = 3630
    addr_rs485_map = 3631
    addr_remote_control_lock_mode_access = 3400
    addr_remote_control_lock_mode = 3401

    ### meter control ###
    addr_meter_test_mode = 4000
    addr_meter_demo_mode_timeout_setup_access = 4001
    addr_meter_demo_mode_timeout = 4002

    ### meter system ###
    addr_description_setup_access = 3300
    addr_installation_year = 3331
    addr_installation_month = 3332
    addr_installation_day = 3333
    addr_locale_setup_access = 3020
    addr_timezone_offset = 3021
    addr_temperature_unit = 3022
    addr_energy_unit = 3023
    addr_date_display_format = 3024
    addr_system_time_setup_access = 3060
    addr_summer_time_setup_access = 3000
    addr_summer_time = 3001
    addr_start_month = 3002
    addr_start_nth_day_of_month = 3003
    addr_start_day_of_week = 3004
    addr_start_minute = 3005
    addr_end_month = 3006
    addr_end_nth_day_of_month = 3007
    addr_end_day_of_week = 3008
    addr_end_minute = 3009
    addr_summer_time_offset = 3010
    addr_ntp_setup_access = 3040
    addr_ntp_ip = 3041
    addr_sync_mode = 3043
    addr_sync_period = 3044
    addr_sync_max_drift = 3045
    addr_lcd_buzzer_setup_access = 3800
    addr_lcd_backlight_timeout = 3801
    addr_lcd_backlight_low_level = 3802
    addr_buzzer_for_button = 3803
    ### UINT32 ###
    addr_system_time_sec = 3061
    addr_system_time_usec = 3063
    
    
    addr_reset_demand = 12000
    addr_reset_demand_peak = 12001
    addr_demand_sync = 12015
    
    addr_setup_lock = 2900
    addr_control_lock = 2901