import time
from datetime import datetime, timezone, timedelta
import time

from function.func_connection import ConnectionManager
from function.func_touch import TouchManager

from config.config_map import ConfigModbusMap as ecm

class ModbusLabels:

    touch_manager = TouchManager()
    # connect_manager = ConnectionManager()

    def __init__(self):
        self.connect_manager = ConnectionManager()

    def demo_test_setting(self):
        test_mode = "Demo"
        self.touch_manager.uitest_mode_start()
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client is not None: 
            for value in values:
                self.response = self.connect_manager.setup_client.write_register(ecm.addr_setup_lock.value, value)
                time.sleep(0.6)
            vol_value_32bit = 1900
            high_word = (vol_value_32bit >> 16) & 0xFFFF
            low_word = vol_value_32bit & 0xFFFF
            self.response = self.connect_manager.setup_client.read_holding_registers(6000, 100)
            self.response = self.connect_manager.setup_client.read_holding_registers(6100, 100)
            self.response = self.connect_manager.setup_client.read_holding_registers(6200, 3)
            if self.response.isError():
                print(f"Error reading registers: {self.response}")
                return
            self.response = self.connect_manager.setup_client.write_register(6001, 0)
            self.response = self.connect_manager.setup_client.write_registers(6003, [high_word, low_word])
            self.response = self.connect_manager.setup_client.write_registers(6005, [high_word, low_word])
            self.response = self.connect_manager.setup_client.write_registers(6007, 1900)
            self.response = self.connect_manager.setup_client.write_register(6009, 0)
            self.response = self.connect_manager.setup_client.write_register(6000, 1)
            time.sleep(0.6)
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(ecm.addr_control_lock.value, value_control)
                time.sleep(0.6)
            self.response = self.connect_manager.setup_client.write_register(4002, 0)
            self.response = self.connect_manager.setup_client.write_register(4000, 1)
            self.response = self.connect_manager.setup_client.write_register(4001, 1)
            print("Demo mode setting Done")
        else:
            # print(self.response.isError())
            print("setup_client가 연결되어 있지 않습니다.")
        return test_mode

    def noload_test_setting(self):
        test_mode = "NoLoad"
        self.touch_manager.uitest_mode_start()
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client:
            for value in values:
                self.response = self.connect_manager.setup_client.write_register(ecm.addr_setup_lock.value, value)
                time.sleep(0.6)
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(ecm.addr_control_lock.value, value_control)
                time.sleep(0.6)
            self.response = self.connect_manager.setup_client.write_register(4000, 0)
            self.response = self.connect_manager.setup_client.write_register(4001, 1)
            print("Noload Demo mode setting Done")
        return test_mode
    
    def setup_initialization(self):
        self.touch_manager.uitest_mode_start()
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]

        def value_32bit(value):
            return (value >> 16) & 0xFFFF, value & 0xFFFF

        if self.connect_manager.setup_client:
            for value in values:
                self.connect_manager.setup_client.write_register(ecm.addr_setup_lock.value, value)
                time.sleep(0.6)
            for value_control in values_control:
                self.connect_manager.setup_client.write_register(ecm.addr_control_lock.value, value_control)
                time.sleep(0.6)
            
            ### measurement setup ###
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_wiring.value, 0)
            self.connect_manager.setup_client.write_registers(ecm.addr_reference_voltage.value, [*value_32bit(1900)])
            self.connect_manager.setup_client.write_registers(ecm.addr_vt_primary_ll_voltage.value, [*value_32bit(1900)])
            self.connect_manager.setup_client.write_register(ecm.addr_vt_secondary_ll_voltage.value, 1900)
            self.connect_manager.setup_client.write_register(ecm.addr_min_measured_secondary_ln_voltage.value, 5)
            self.connect_manager.setup_client.write_register(ecm.addr_reference_voltage_mode.value, 0)
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_reference_voltage_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_reference_voltage_type.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_reference_voltage_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_rotating_sequence.value, 1)
            self.connect_manager.setup_client.write_registers(ecm.addr_ct_primary_current.value, [*value_32bit(50)])
            self.connect_manager.setup_client.write_register(ecm.addr_ct_secondary_current.value, 50)
            self.connect_manager.setup_client.write_registers(ecm.addr_reference_current.value, [*value_32bit(50)])
            self.connect_manager.setup_client.write_register(ecm.addr_min_measured_current.value, 5)
            self.connect_manager.setup_client.write_register(ecm.addr_tdd_reference.value, 1)
            self.connect_manager.setup_client.write_registers(ecm.addr_nominal_tdd_current.value, [*value_32bit(0)])
            self.connect_manager.setup_client.write_register(ecm.addr_sub_interval_time.value, 15)
            self.connect_manager.setup_client.write_register(ecm.addr_num_of_sub_interval.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_demand_power_type.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_demand_sync_mode.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_thermal_response_index.value, 90)
            self.connect_manager.setup_client.write_register(ecm.addr_phase_power_calculation.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_total_power_calculation.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_pf_sign.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_pf_value_at_no_load.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_reactive_power_sign.value, 1)

            self.connect_manager.setup_client.write_register(ecm.addr_setup_access.value, 1)

            ### meter event setup ###
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_dip_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_3phase_dip_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_swell_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_semi_event_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_itic_event_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_iec_event_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_dip.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_dip_threshold.value, 900)
            self.connect_manager.setup_client.write_register(ecm.addr_dip_hysteresis.value, 20)
            self.connect_manager.setup_client.write_register(ecm.addr_3phase_dip.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_dip_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_3phase_dip_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_swell.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_swell_threshold.value, 1100)
            self.connect_manager.setup_client.write_register(ecm.addr_swell_hysteresis.value, 20)
            self.connect_manager.setup_client.write_register(ecm.addr_swell_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_semi.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_semi_event_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_itic.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_itic_event_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_iec.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_iec_event_setup_access.value, 1)

            ### meter network setup ###
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_dhcp_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_dhcp.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_dhcp_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_rs485_map_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_device_address.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_bit_rate.value, 3)
            self.connect_manager.setup_client.write_register(ecm.addr_parity.value, 2)
            self.connect_manager.setup_client.write_register(ecm.addr_stop_bit.value, 0)
            self.connect_manager.setup_client.write_register(ecm.addr_rs485_map_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(ecm.addr_modbus_timeout_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ecm.addr_modbus_timeout.value, 600)
            self.connect_manager.setup_client.write_register(ecm.addr_modbus_timeout_setup_access.value, 1)
    
    def device_current_time(self):
        self.response = self.connect_manager.setup_client.read_holding_registers(3060, 3)
        high_word = self.connect_manager.setup_client.read_holding_registers(3061, 1).registers[0]
        low_word = self.connect_manager.setup_client.read_holding_registers(3062, 1).registers[0]
        unix_timestamp = (high_word << 16) | low_word

        utc_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        kst_time = utc_time + timedelta(minutes=540)
        device_current_time = kst_time
        return device_current_time

    def reset_max_min(self):
        self.touch_manager.uitest_mode_start()
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client:
            self.response = self.connect_manager.setup_client.read_holding_registers(3060, 3)
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(ecm.addr_control_lock.value, value_control)
                time.sleep(0.6)
            self.response = self.connect_manager.setup_client.write_register(ecm.addr_reset_max_min.value, 1)
            print("Max/Min Reset")
        else:
            print(self.response.isError())

        high_word = self.connect_manager.setup_client.read_holding_registers(3061, 1).registers[0]
        low_word = self.connect_manager.setup_client.read_holding_registers(3062, 1).registers[0]
        unix_timestamp = (high_word << 16) | low_word

        utc_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        kst_time = utc_time + timedelta(minutes=540)
        self.reset_time = kst_time
        print(kst_time)
        return self.reset_time
    
    def reset_demand(self):
        self.touch_manager.uitest_mode_start()
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client:
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(ecm.addr_control_lock.value, value_control)
                time.sleep(0.6)
            self.response = self.connect_manager.setup_client.write_register(ecm.addr_reset_demand.value, 1)
            print("Max/Min Reset")
        else:
            print(self.response.isError())
    
    def reset_demand_peak(self):
        self.touch_manager.uitest_mode_start()
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client:
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(ecm.addr_control_lock.value, value_control)
                time.sleep(0.6)
            self.response = self.connect_manager.setup_client.write_register(ecm.addr_reset_demand_peak.value, 1)
            print("Max/Min Reset")
        else:
            print(self.response.isError())
        self.reset_time = datetime.now()
        return self.reset_time
    
    def demo_test_demand(self):
        self.touch_manager.uitest_mode_start()
        addr_control_lock = 2901
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client:
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(addr_control_lock, value_control)
                time.sleep(0.6)
            if self.response.isError():
                print(f"Error reading registers: {self.response}")
                return
            self.response = self.connect_manager.setup_client.read_holding_registers(ecm.addr_meas_setup_access.value, 1)
            self.response = self.connect_manager.setup_client.write_register(ecm.addr_demand_sync_mode.value, 1)
            self.response = self.connect_manager.setup_client.write_register(ecm.addr_demand_sub_interval_time.value, 2)
            self.response = self.connect_manager.setup_client.write_register(ecm.addr_demand_num_of_sub_interval.value, 3)
            self.response = self.connect_manager.setup_client.write_register(ecm.addr_meas_setup_access.value, 1)
            demand_reset_time = self.reset_demand_peak()
            self.reset_demand()
            self.response = self.connect_manager.setup_client.write_register(ecm.addr_demand_sync.value, 1)
        else:
            print(self.response.isError())
            
        return demand_reset_time