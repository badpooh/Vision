
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
            #popup title ~ popup button(enter, cancel)
            "17": [n*x for x in [250, 20, 300, 55]],
            "18": [n*x for x in [262, 88, 273, 44]],
            "19": [n*x for x in [250, 138, 273, 44]],
            #popup_number title ~ popup button(enter, cancel)
            "20": [n*x for x in [280, 30, 240, 40]],
            "21": [n*x for x in [280, 75, 240, 40]],
            #measurement ocr
            "main_view_1": [n*x for x in [160, 120, 625, 48]], #rms voltage l-l l-m min max
            "main_view_2": [n*x for x in [165, 185, 120, 55]], # AB
            "main_view_3": [n*x for x in [320, 215, 190, 30]], # time stamp
            "main_view_4": [n*x for x in [540, 190, 160, 55]], # 190.0
            "main_view_5": [n*x for x in [720, 200, 35, 40]], # V
            "main_view_6": [n*x for x in [165, 270, 120, 40]], # BC
            "main_view_7": [n*x for x in [320, 290, 190, 30]], # time stamp
            "main_view_8": [n*x for x in [540, 260, 160, 60]], # 190.0
            "main_view_9": [n*x for x in [720, 270, 35, 40]], # V
            "main_view_10": [n*x for x in [165, 340, 120, 40]], # CA
            "main_view_11": [n*x for x in [320, 360, 190, 35]], # time stamp
            "main_view_12": [n*x for x in [540, 340, 160, 50]], # 190.0
            "main_view_13": [n*x for x in [720, 350, 35, 40]], # V
            "main_view_14": [n*x for x in [165, 415, 120, 40]], # Average
            "main_view_15": [n*x for x in [320, 430, 190, 35]], # time stamp
            "main_view_16": [n*x for x in [540, 410, 160, 60]], # 190.0
            "main_view_17": [n*x for x in [720, 420, 35, 40]], # V
            #test mode confirm
            "999" : [n*x for x in [220, 105, 350, 40]],
        }
        return params
    
    def match_m_setup_labels(self):
        m_home = {
        "RMS" : ["RMS Voltage", "L-L", "L-N", "Min", "Max"],
        "L-L" : ["AB", "BC", "CA", "Average"],
        "L-N" : ["A", "B", "C", "Average"],
        "L_Min" : ["AB", "BC", "CA", "Average", ],
        "L_Max" : ["AB", "BC", "CA", "Average", ],
        "N_Min" : ["A", "B", "C", "Average"],
        "N_Max" : ["A", "B", "C", "Average"],   
        }
        
        m_setup = {
        #voltage 
        "1" : ["Wiring", "Min. Meas. Secondary L-N Volt. [V]", "VT Primary L-L Voltage [V]", "VT Secondary L-L Voltage [V]", 
               "Primary Reference Voltage [V]", "Sliding Reference Voltage", "Rotating Sequence"],
        #current 
        "2" : ["CT Primary Current [A]", "CT Secondary Current [A]", "Reference Current [A]", "Min. Measured Current [mA]", "TDD Reference Selection", "TDD Nominal Current [A]"],
        #demand 
        "3" : ["Sub-Interval Time [min]", "Number of Sub-Intervals", "Power Type", "Sync Mode", "Thermal Response Index [%]"],
        #power 
        "4" : ["Phase Power Calculation", "Total Power Calculation", "PF Sign", "PF Value at No Load", "Reactive Power Sign"],
        #dip 
        "5" : ["Dip", "Threshold [%]", "Hysteresis [%]", "3-Phase Dip"],
        #swell 
        "6" : ["Swell", "Threshold [%]", "Hysteresis [%]"],
        #pqcurve 
        "7" : ["SEMI F47-0706", "IEC 61000-4-11/34 Class 3", "ITIC"],
        #Ethernet 
        "8" : ["IP Address", "Subnet Mask", "Gateway", "MAC Address", "DHCP", "USB IP Address"],
        #RS485 
        "9" : ["Device Address", "Bit Rate", "Parity", "Stop Bit"],
        #Advanced 
        "10" : ["Modbus TCP Timeout [sec]", "RSTP", "Storm Control", "Remote Control Lock Mode"],
        #test mode"
        "999" : ["Password"]
        }
        return m_home, m_setup
    
    def match_pop_labels(self):

        pop_params = {
            "1" : ["Wiring", "3P4W", "3P3W"], #wiring
            "2" : ["Min. Meas. Secondary L-N Volt. [V]", "Range 1 - 10"], #Min. Meas. Secondary L-N Volt. [V]
            "3" : ["VT Primary L-L Voltage", "Range 50.0 - 999999.0"], #VT Primary L-L Voltage
            "4" : ["VT Secondary L-L Voltage [V]", "Range 50.0 - 220.0"], #VT Secondary L-L Voltage [V]
            "5" : ["Primary Reference Voltage [V]", "Line-to-Line", "Line-to-Neutral", "Range 50.0 - 999999.0"], #Primary Reference Voltage [V]
            "6" : ["Sliding Reference Voltage", "Disable", "Enable"], #Sliding Reference Voltage
            "7" : ["Rotating Sequence", "Positive", "Negative"], #Rotating Sequence
        }
        
        return pop_params
    
    def color_detection_data(self):
        
        coordinates = {
        "measurement": [5, 70, 10, 10, 47, 180, 139],
        "mea_voltage": [110, 130, 10, 10, 255, 255, 255],
        "mea_current": [110, 170, 10, 10, 255, 255, 255],
        "mea_demand": [110, 220, 10, 10, 255, 255, 255],
        "mea_power": [110, 270, 10, 10, 255, 255, 255],
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
        "btn_number_clear": [485, 340],
        "btn_num_pw_1" : [255, 230],
        "btn_num_pw_2" : [315, 230],
        "btn_num_pw_3" : [370, 230],
        "btn_num_pw_4" : [430, 230],
        "btn_num_pw_5" : [485, 230],
        "btn_num_pw_6" : [255, 290],
        "btn_num_pw_7" : [315, 290],
        "btn_num_pw_8" : [370, 290],
        "btn_num_pw_9" : [430, 290],
        "btn_num_pw_0" : [485, 290],
        "btn_num_pw_enter" : [340, 345],
        "btn_testmode_1" : [270, 100],
        "btn_testmode_2" : [270, 160],

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
        "touch_mode": 57112,
        "setup_button_bit": 57120,
        "setup_button": 57121,
        }
        
        return coordinates