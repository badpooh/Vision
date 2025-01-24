from enum import Enum

class ConfigTouch(Enum):
    ### 상단 메뉴 ###
    touch_main_menu_1 = [100, 85]
    touch_main_menu_2 = [260, 85]
    touch_main_menu_3 = [390, 85]
    touch_main_menu_4 = [560, 85]
    touch_main_menu_5 = [720, 85]
    
	### 왼쪽 사이드 메뉴 ###
    touch_side_menu_1 = [80, 135]
    touch_side_menu_2 = [80, 180]
    touch_side_menu_3 = [80, 225]
    touch_side_menu_4 = [80, 270]
    touch_side_menu_5 = [80, 315]
    touch_side_menu_6 = [80, 360]
    touch_side_menu_7 = [80, 405]
    touch_side_menu_8 = [80, 450]

    touch_toggle_ll = [410, 150]
    touch_toggle_ln = [510, 150]
    touch_toggle_thd_ll = [520, 150]
    touch_toggle_thd_ln = [620, 150]
    touch_toggle_max = [720, 150]
    touch_toggle_min = [620, 150]
    touch_toggle_phasor_vll = [620, 210]
    touch_toggle_phasor_vln = [720, 210]
    
	### phasor, harmonics, waveform 공통 ###
    touch_toggle_analysis_vol = [590, 150]
    touch_toggle_analysis_curr = [720, 150]
    
    touch_toggle_harmonics_fund = [510, 200]
    touch_dropdown_harmonics_1 = [230, 200]
    touch_dropdown_harmonics_2 = [360, 200]
    touch_toggle_waveform_vol_a = [360, 200]
    touch_toggle_waveform_vol_b = [430, 200]
    touch_toggle_waveform_vol_c = [490, 200]
    
	### harmonics a,b,c 와 공통 ###
    touch_toggle_waveform_curr_a = [620, 200]
    touch_toggle_waveform_curr_b = [680, 200]
    touch_toggle_waveform_curr_c = [740, 200]
    
	### harmonics dropdown menu의 선택지 ###
    touch_harmonics_sub_v = [230, 240]
    touch_harmonics_sub_fund = [230, 285]
    touch_harmonics_sub_rms = [230, 330]
    touch_harmonics_sub_graph = [360, 240]
    touch_harmonics_sub_text = [360, 285]
    
    ### touch 동작관련 address ###
    touch_addr_ui_test_mode = 57100
    touch_addr_pos_x = 57110
    touch_addr_pos_y = 57111
    touch_addr_touch_mode = 57112
    touch_addr_screen_capture = 57101
    touch_addr_setup_button_bit = 57120
    touch_addr_setup_button = 57121