
from types import coroutine


class ConfigSetup:

    def roi_params(self):
        n=3
        params = {
            "1": [n*x for x in [176, 181, 298, 35]],
            "2": [n*x for x in [477, 181, 298, 35]],
            "3": [n*x for x in [176, 215, 298, 35]],
            "4": [n*x for x in [477, 215, 298, 35]],
            "5": [n*x for x in [176, 253, 298, 35]],
            "6": [n*x for x in [477, 253, 298, 35]],
            "7": [n*x for x in [176, 287, 298, 35]],
            "8": [n*x for x in [477, 287, 298, 35]],
            "9": [n*x for x in [176, 325, 298, 35]],
            "10": [n*x for x in [477, 325, 298, 35]],
            "11": [n*x for x in [176, 359, 298, 35]],
            "12": [n*x for x in [477, 359, 298, 35]],
            "13": [n*x for x in [176, 397, 298, 35]],
            "14": [n*x for x in [477, 397, 298, 35]],
            "15": [n*x for x in [176, 431, 298, 35]],
            "16": [n*x for x in [477, 431, 298, 35]],
        }
        return params
    
    def match_labels(self):

        label_voltage = ["Wiring", "Min. Meas. Secondary L-N Volt. [V]", "VT Primary L-L Voltage [V]", 
                            "VT Secondary L-L Voltage [V]", "Primary Reference Voltage [V]", "Sliding Reference Voltage",
                            "Rotating Sequence"]
        label_current = ["CT Primary Current [A]", "CT Secondary Current [A]", "Reference Current [A]", "Min. Measured Current [mA]", "TDD Reference Selection", "TDD Nominal Current [A]"]
        label_demand = ["Sub-Interval Time [min]", "Number of Sub-Intervals", "Power Type", "Sync Mode", 
                         "Thermal Response Index [%]"]
        label_power = ["Phase Power Calculation", "Total Power Calculation", "PF Sign", "PF Value at No Load", 
                        "Reactive Power Sign"]
        label_dip = ["Dip", "Threshold [%]", "Hysteresis [%]", "3-Phase Dip"]
        label_swell = ["Swell", "Threshold [%]", "Hysteresis [%]"]
        label_pqcurve = ["SEMI F47-0706", "IEC 61000-4-11/34 Class 3", "ITIC"]
        label_Ethernet = ["IP Address", "Subnet Mask", "Gateway", "MAC Address", "DHCP", "USB IP Address"]
        label_RS485 = ["Device Address", "Bit Rate", "Parity", "Stop Bit"]
        label_Advanced = ["Modbus TCP Timeout [sec]", "RSTP", "Storm Control", "Remote Control Lock Mode"]
        
        
        return label_voltage, label_current, label_demand, label_power, label_dip, label_swell, label_pqcurve, label_Ethernet, label_RS485, label_Advanced
    
    
    def color_detection_data(self):
        
        coordinates = {
        "measurement": [5, 70, 10, 10, 47, 180, 139],
        "mea_voltage": [110, 130, 10, 10, 255, 255, 255],
        "mea_current": [110, 170, 10, 10, 255, 255, 255],
        "mea_demand": [110, 220, 10, 10, 255, 255, 255],
        "mea_power": [110, 270, 10, 10, 255, 255, 255]
        }
        
        return coordinates
    
    def touch_data(self):
        coordinates = {
        "main_menu_1": [100, 85],
        "main_menu_2": [260, 85],
        "main_menu_3": [390, 85],
        "main_menu_4": [560, 85],
        "main_menu_5": [720, 85],
        "side_menu_1": [80, 135],
        "side_menu_2": [80, 180],
        "side_menu_3": [80, 225],
        "side_menu_4": [80, 270],
        "side_menu_5": [80, 315],
        "side_menu_6": [80, 360],
        "side_menu_7": [],
        "side_menu_8": [],
        "data_view_1": [320, 210],
        "data_view_2": [620, 210],
        "data_view_3": [320, 280],
        "data_view_4": [620, 280],
        "data_view_5": [320, 360],
        "data_view_6": [620, 360],
        "data_view_7": [320, 430],
        "data_view_8": [620, 430],
        "btn_apply": [620, 150],
        "btn_cancel": [720, 150],
        "btn_popup_1": [400, 110],
        "btn_popup_2": [400, 160],
        "btn_popup_3": [400, 215],
        "btn_popup_4": [400, 265],
        "btn_popup_5": [400, 315],
        "btn_popup_enter": [340, 430],
        "btn_popup_cancel": [450, 430],
        "btn_number_1": [310, 200],
        "btn_number_2": [370, 200],
        "btn_number_3": [430, 200],
        "btn_number_4": [310, 255],
        "btn_number_5": [370, 255],
        "btn_number_6": [430, 255],
        "btn_number_7": [310, 310],
        "btn_number_8": [370, 310],
        "btn_number_9": [430, 310],
        "btn_number_0": [310, 370],
        "btn_number_dot": [370, 370],
        "btn_number_back": [490, 225],
        "btn_number_clear": [485, 340]
    }
        return coordinates

    
    def meter_m_vol_mapping(self):
        
        #### smartsheet의 address는 1-based
        #### 아래의 address는 0-based
        meter_m_vol_mappings_value = {
        6001: {"description": "Wiring", "values": {0: "3P4W", 1: "3P3W"}},
        6009: {"description": "Reference voltage mode", "values": {0:"Line-to-Line", 1:"Line-to-Neutral"}}, #명칭 예외처리
        6040: {"description": "Rotating Sequence", "values": {0:"Auto", 1:"Positive", 2:"Negative"}},
        6051: {"description": "Sliding Reference Voltage", "values": {0: "Disable", 1: "Enable"}},
        }

        meter_m_vol_mappings_uint16 = {
        6007: {"description": "VT Secondary L-L Voltage[V]", "type": "uint16"},
        6008: {"description": "Min. Measured Secondary Voltage", "type": "uint16"},
        }
        
        meter_m_vol_mappings_uint32 = {
        6003: {"description": "Primary Reference Voltage[V]", "type": "uint32"},
        6005: {"description": "VT Primary L-L Voltage [V]", "type": "uint32"},
        }
        
        return meter_m_vol_mappings_value, meter_m_vol_mappings_uint16, meter_m_vol_mappings_uint32
    
    def meter_m_cur_mapping(self):
        
        meter_m_cur_mappings_value = {
        6023: {"description": "TDD Reference Selection", "values": {0: "Nominal Current", 1: "Peak Demand Current"}}
        }
        
        meter_m_cur_mappings_uint16 = {
        6021: {"description": "Min. Measured Current [mA]", "type": "uint16"},    
        }
        
        meter_m_cur_mappings_uint32 = {
        6015: {"description": "Reference Current [A]", "type": "uint32"},
        6017: {"description": "CT Primary Current [A]", "type": "uint32"},
        6019: {"description": "CT Secondary Current [A]", "type": "uint32"},
        6021: {"description": "TDD Nominal current [A]", "type": "uint32"},
        }
        
        return meter_m_cur_mappings_value, meter_m_cur_mappings_uint16, meter_m_cur_mappings_uint32
    

    
    def touch_address_data(self):
        
        coordinates = {
        "ui_test_mode": 57100,
        "screen_capture": 57101,
        "pos_x": 57110,
        "pos_y": 57111,
        "touch_mode": 57112
        }
        
        return coordinates