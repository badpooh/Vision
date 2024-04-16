
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

        label_voltage = ["Wiring", "Min. Measured Secondary Voltage [V]", "VT Primary L-L Voltage [V]", 
                            "VT Secondary L-L Voltage [V]", "Primary Reference Voltage [V]", "Sliding Reference Voltage",
                            "Rotating Sequence"
                            ]
        label_current = ["CT Primary Current [A]", "CT Secondary Current [A]", "Reference Current [A]", "Min. Measured Current [mA]", "TDD Reference Selection", "TDD Nominal Current [A]"]
        
        return label_voltage, label_current
    
    
    def color_detection_data(self):
        
        measurement = [5, 70, 10, 10, 47, 180, 139]
        mea_voltage = [110, 130, 10, 10, 255, 255, 255]
        mea_current = [110, 170, 10, 10, 255, 255, 255]
        mea_demand = [110, 220, 10, 10, 255, 255, 255]
        mea_power = [110, 270, 10, 10, 255, 255, 255]
        
        return measurement, mea_voltage, #mea_current,mea_demand, mea_power
    
    def touch_data(self):
        
        main_menu_1 = [100, 85]
        main_menu_2 = [260, 85]
        main_menu_3 = [390, 85]
        main_menu_4 = [560, 85]
        main_menu_5 = [720, 85]
        side_menu_1 = [80, 135]
        side_menu_2 = [80, 180]
        side_menu_3 = [80, 225]
        side_menu_4 = [80, 270]
        side_menu_5 = []
        side_menu_6 = []
        side_menu_7 = []
        side_menu_8 = []
        data_view_1 = [320, 210]
        data_view_2 = [620, 210]
        data_view_3 = [320, 280]
        data_view_4 = [620, 280]
        data_view_5 = [320, 360]
        data_view_6 = [620, 360]
        data_view_7 = [320, 430]
        data_view_8 = [620, 430]
        
        
        return main_menu_1, side_menu_1, data_view_1, # main_menu_2, main_menu_3, main_menu_4, main_menu_5,  side_menu_2, side_menu_3, side_menu_4, side_menu_5, side_menu_6, side_menu_7, side_menu_8,  data_view_2, data_view_3, data_view_4, data_view_5, data_view_6, data_view_7, data_view_8
    
    def setup_mapping(self):
        
        #### smartsheet의 address는 1-based
        #### 아래의 address는 0-based
        mappings_value = {
        6001: {"description": "Wiring", "values": {0: "3P4W", 1: "3P3W"}},
        6009: {"description": "Reference voltage mode", "values": {0:"Line-to-Line", 1:"Line-to-Neutral"}},
        6040: {"description": "Rotating sequence", "values": {0:"Auto", 1:"Positive", 2:"Negative"}},
        6051: {"description": "Sliding reference voltage type", "values": {0: "Reference voltage", 1: "Sliding reference voltage"}},
        }

        mappings_uint16 = {
        6007: {"description": "PT Secondary Voltage", "type": "uint16"},
        6008: {"description": "Minimum measured secondary voltage", "type": "uint16"},
        }
        
        mappings_uint32 = {
        6003: {"description": "Reference voltage", "type": "uint32"},
        6005: {"description": "PT Primary Voltage", "type": "uint32"},
        }
        
        return mappings_value, mappings_uint16, mappings_uint32
    

    
    def touch_address_data(self):
        
        ui_test_mode = 57100
        screen_capture = 57101
        pos_x = 57110
        pos_y = 57111
        touch_mode = 57112
        
        return ui_test_mode, screen_capture, pos_x, pos_y, touch_mode