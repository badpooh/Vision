from enum import Enum

class ConfigROI(Enum):
    title_view = ["RMS Voltage L-L L-N Min Max", "AB", "BC", "CA", "Average"]
    a_ab = "meas_a_phase_name"
    a_time_stamp = "meas_a_time_stamp"
    a_meas = "meas_a_measurement_value"
    b_bc = "meas_b_phase_name"
    b_time_stamp = "meas_b_time_stamp"
    b_meas = "meas_b_measurement_value"
    c_ca = "meas_c_phase_name"
    c_time_stamp = "meas_c_time_stamp"
    c_meas = "meas_c_measurement_value"
    aver = "meas_aver_phase_name"
    aver_time_stamp = "meas_aver_time_stamp"
    aver_meas = "meas_aver_measurement_value"
    curr_per_a = "meas_curr_percent_a"
    curr_per_b = "meas_curr_percent_b"
    curr_per_c = "meas_curr_percent_c"
    curr_per_aver = "meas_curr_percent_aver"
    
    phasor_img_cut = "phasor_img_cut"
    phasor_title = "phasor_title"
    phasor_title_2 = "phasor_title_2"
    phasor_view_2 = "phasor_view_2"
    phasor_vl_vn = "phasor_vl_vn"
    phasor_voltage = "phasor_voltage"
    phasor_a_c_vol = "phasor_a_c_vol"
    phasor_a_meas = "phasor_a_meas"
    phasor_a_angle = "phasor_a_angle"
    phasor_b_meas = "phasor_b_meas"
    phasor_b_angle = "phasor_b_angle"
    phasor_c_meas = "phasor_c_meas"
    phasor_c_angle = "phasor_c_angle"
    phasor_a_c_angle_vol = "phasor_a_c_angle_vol"
    phasor_current = "phasor_current"
    phasor_a_c_cur = "phasor_a_c_cur"
    phasor_a_meas_cur = "phasor_a_meas_cur"
    phasor_a_angle_cur = "phasor_a_angle_cur"
    phasor_b_meas_cur = "phasor_b_meas_cur"
    phasor_b_angle_cur = "phasor_b_angle_cur"
    phasor_c_meas_cur = "phasor_c_meas_cur"
    phasor_c_angle_cur = "phasor_c_angle_cur"
    phasor_a_c_angle_cur = "phasor_a_c_angle_cur"
    
    waveform_title = "waveform_title"
    waveform_all_img_cut = "waveform_img_cut"
    waveform_graph_img_cut = "waveform_graph_img_cut"
    
    harmonics_img_cut = "harmonics_img_cut"
    harmonics_title = "harmonics_title"
    harmonics_sub_title_1 = "harmonics_sub_title_1"
    harmonics_sub_title_2 = "harmonics_sub_title_2"
    harmonics_sub_title_3 = "harmonics_sub_title_3"
    harmonics_graph_img_cut = "harmonics_graph_img_cut"
    harmonics_chart_img_cut = "harmonics_graph_with_bar_img_cut"
    harmonics_graph_a = "harmonics_graph_a"
    harmonics_graph_b = "harmonics_graph_b"
    harmonics_graph_c = "harmonics_graph_c"
    harmonics_text_title = "harmonics_text_title"
    harmonics_text_img = "harmonics_text_image"
    harmonics_text_number_title_1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    harmonics_text_number_meas_1 = "measurement result"
    harmonics_text_chart_img_cut_3 = ["6, 0.000, 15, 0.000, 24, 0.000, 33, 0.000, 42, 0.000, 7, 0.000, 16, 0.000, 25, 0.000, 34, 0.000, 43, 0.000, 8, 0.000, 17, 0.000, 26, 0.000, 35, 0.000, 44, 0.000"]
    harmonics_text_sub_title = "harmonics_text_sub_title"
    harmonics_text_sub_abc = "harmonics_text_sub_a"
    harmonics_thd_a = "harmonics_thd_a"
    harmonics_thd_b = "harmonics_thd_b"
    harmonics_thd_c = "harmonics_thd_c"
    harmonics_fund_a = "harmonics_fund_a"
    harmonics_fund_b = "harmonics_fund_b"
    harmonics_fund_c = "harmonics_fund_c"

    ### for meter setup test
    s_wiring_1 = ["Wiring"]
    s_wiring_2 = ["Wye", "Delta"]
    s_min_meas_sec_ln_vol_1 = ['Min. Meas. Secondary L-N Volt. [V]']
    s_min_meas_sec_ln_vol_2 = ['0', '10']
    s_vt_primary_ll_vol_1 = ['VT Primary L-L Voltage [V]']
    s_vt_primary_ll_vol_2 = ['50.0', '999999.0']
    s_vt_secondary_ll_vol_1 = ['VT Secondary L-L Voltage [V]']
    s_vt_secondary_ll_vol_2 = ['50.0', '220.0']
    s_primary_reference_vol_1 = ['Primary Reference Voltage [V]']
    s_primary_reference_vol_2 = ['Line-to-Line', 'Line-to-Neutral']
    s_primary_reference_vol_3 = ['50.0', '999999.0']
    s_sliding_reference_vol_1 = ['Sliding Reference Voltage']
    s_sliding_reference_vol_2 = ['Disable', 'Enable']
    s_rotation_sequence_1 = ['Rotating Sequence']
    s_rotation_sequence_2 = ['Positive', 'Negative']
    s_ct_primary_curr_1 = ['CT Primary Current [A]']
    s_ct_primary_curr_2 = ['5', '99999']
    s_ct_secondary_curr_1 = ['CT Secondary Current [A]']
    s_ct_secondary_curr_2 = ['5', '10']
    s_reference_curr_1 = ['Reference Current [A]']
    s_reference_curr_2 = ['5', '99999']
    s_min_meas_curr_1 = ['Min. Measured Current [mA]']
    s_min_meas_curr_2 = ['0', '100']
    s_tdd_reference_selection_1 = ['TDD Reference Selection']
    s_tdd_reference_selection_2 = ['TDD Nominal Current', 'Peak Demand Current']
    s_tdd_nominal_curr_1 = ['TDD Nominal Current [A]']
    s_tdd_nominal_curr_2 = ['Reference Current', 'Reference Current']
    s_tdd_nominal_curr_3 = ['1', '99999']

    
    color_main_menu_vol = [10, 70, 10, 10, 67, 136, 255]
    color_main_menu_curr = [170, 70, 10, 10, 67, 136, 255]
    color_rms_vol_ll = [380, 140, 10, 10, 67, 136, 255]
    color_rms_vol_ln = [480, 140, 10, 10, 67, 136, 255]
    color_vol_thd_ll = [480, 140, 10, 10, 67, 136, 255]
    color_vol_thd_ln = [580, 140, 10, 10, 67, 136, 255]
    color_phasor_vll = [580, 200, 10, 10, 67, 136, 255]
    color_phasor_vln = [680, 200, 10, 10, 67, 136, 255]
    color_symm_thd_vol_ll = [480, 140, 10, 10, 67, 136, 255]
    color_symm_thd_vol_ln = [580, 140, 10, 10, 67, 136, 255]
    ### A상 버튼 눌러서 A상이 안보이는 지 확인 / 앞 4자리는 검사할 그래프 영역###
    ### 뒤 3자리는 RGB ###
    color_waveform_vol_a = [313, 253, 411, 203, 0, 0, 0]
    color_waveform_vol_b = [313, 253, 411, 203, 255, 29, 37]
    color_waveform_vol_c = [313, 253, 411, 203, 0, 0, 255]
    color_waveform_curr_a = [313, 253, 411, 203, 153, 153, 153]
    color_waveform_curr_b = [313, 253, 411, 203, 255, 180, 245]
    color_waveform_curr_c = [313, 253, 411, 203, 54, 175, 255]
    color_harmonics_vol_a = [313, 283, 455, 173, 0, 0, 0]
    color_harmonics_vol_b = [313, 283, 455, 173, 255, 29, 37]
    color_harmonics_vol_c = [313, 283, 455, 173, 0, 0, 255]
    color_harmonics_curr_a = [313, 283, 455, 173, 153, 153, 153]
    color_harmonics_curr_b = [313, 283, 455, 173, 255, 180, 245]
    color_harmonics_curr_c = [313, 283, 455, 173, 54, 175, 255]

    ### harmonics voltage, current 활성화 판별 ###
    ### 앞 4자리는 색판별 영역 / 뒤 3자리는 RGB ###
    color_harmonics_vol = [540, 140, 10, 10, 67, 136, 255]
    color_harmonics_curr = [660, 140, 10, 10, 67, 136, 255]

class Configs():
    
    def __init__(self, n=3):
        self.n = n

    def update_n(self, new_n):
        self.n = new_n

    def roi_params(self):
        n = self.n
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
            # popup title ~ popup button(enter, cancel)
            "17": [n*x for x in [250, 20, 300, 55]],
            "18": [n*x for x in [262, 88, 273, 44]],
            "19": [n*x for x in [250, 138, 273, 44]],
            # popup_number title ~ popup button(enter, cancel)
            "20": [n*x for x in [280, 30, 240, 40]],
            "21": [n*x for x in [280, 75, 240, 40]],

            # OCR 결과를 위한 좌표
            # rms voltage l-l l-m min max
            ConfigROI.title_view: [n*x for x in [160, 120, 620, 53]],
            ConfigROI.a_ab: [n*x for x in [175, 179, 135, 70]],  # AB
            ConfigROI.a_time_stamp: [n*x for x in [320, 220, 190, 25]], # time stamp
            ConfigROI.a_meas: [n*x for x in [540, 190, 230, 55]],  # 190.0 V
            ConfigROI.b_bc: [n*x for x in [165, 253, 135, 69]],  # BC
            ConfigROI.b_time_stamp: [n*x for x in [320, 293, 190, 25]], # time stamp
            ConfigROI.b_meas: [n*x for x in [540, 260, 230, 60]],  # 190.0 V
            ConfigROI.c_ca: [n*x for x in [165, 326, 135, 69]],  # CA
            ConfigROI.c_time_stamp: [n*x for x in [320, 365, 190, 25]], # time stamp
            ConfigROI.c_meas: [n*x for x in [540, 340, 230, 50]],  # 190.0 V
            ConfigROI.aver: [n*x for x in [165, 399, 135, 69]],  # Average
            ConfigROI.aver_time_stamp: [n*x for x in [320, 438, 190, 25]], # time stamp
            ConfigROI.aver_meas: [n*x for x in [540, 410, 230, 60]],  # 190.0

            ### 확인 후 제거 ###
            "main_view_5": [n*x for x in [720, 200, 35, 40]],  # V
            "main_view_9": [n*x for x in [720, 270, 35, 40]],  # V
            "main_view_13": [n*x for x in [720, 350, 35, 40]],  # V
            "main_view_17": [n*x for x in [720, 420, 35, 40]],  # V

            # current % meas 수치 해야됨
            ConfigROI.curr_per_a: [n*x for x in [360, 190, 120, 30]],
            ConfigROI.curr_per_b: [n*x for x in [360, 265, 120, 30]],
            ConfigROI.curr_per_c: [n*x for x in [360, 335, 120, 30]],
            ConfigROI.curr_per_aver: [n*x for x in [360, 405, 120, 35]],

            # test mode confirm
            "999": [n*x for x in [220, 105, 350, 40]],

            # Phasor
            ConfigROI.phasor_img_cut: [176, 179, 425, 295],
            ConfigROI.phasor_title: [n*x for x in [160, 130, 140, 40]], # Phasor
            ConfigROI.phasor_title_2: [n*x for x in [530, 130, 246, 40]], # [V]Voltage, [V]Current
            ConfigROI.phasor_view_2: [n*x for x in [480, 120, 310, 53]], # [V]Voltage, [V]Current
            ConfigROI.phasor_vl_vn: [n*x for x in [570, 190, 210, 39]],  # VLL VLN
            ConfigROI.phasor_voltage: [n*x for x in [465, 235, 80, 27]],  # Voltage
            ConfigROI.phasor_a_c_vol: [n*x for x in [550, 234, 55, 76]], # AB,BC,CA or A,B,C
            ConfigROI.phasor_a_meas: [n*x for x in [610, 236, 95, 23]],  # A-전압수치
            ConfigROI.phasor_a_angle: [n*x for x in [705, 236, 58, 23]],  # A-각도수치
            ConfigROI.phasor_b_meas: [n*x for x in [610, 260, 95, 23]],  # B-전압수치
            ConfigROI.phasor_b_angle: [n*x for x in [705, 260, 58, 23]],  # B-각도수치
            ConfigROI.phasor_c_meas: [n*x for x in [610, 284, 95, 23]],  # C-전압수치
            ConfigROI.phasor_c_angle: [n*x for x in [705, 284, 58, 23]],  # C-각도수치
            ConfigROI.phasor_a_c_angle_vol: [763, 236, 14, 66],  # A~C-각도기호
            ConfigROI.phasor_current: [n*x for x in [465, 345, 80, 24]],  # Current
            ConfigROI.phasor_a_c_cur: [n*x for x in [550, 345, 55, 76]],  # A,B,C
            ConfigROI.phasor_a_meas_cur: [n*x for x in [610, 346, 95, 23]],  # A-전류수치
            ConfigROI.phasor_a_angle_cur: [n*x for x in [705, 346, 58, 23]],  # A-각도수치
            ConfigROI.phasor_b_meas_cur: [n*x for x in [610, 370, 95, 23]],  # B-전류수치
            ConfigROI.phasor_b_angle_cur: [n*x for x in [705, 370, 58, 23]],  # B-각도수치
            ConfigROI.phasor_c_meas_cur: [n*x for x in [610, 394, 95, 23]],  # C-전류수치
            ConfigROI.phasor_c_angle_cur: [n*x for x in [705, 394, 58, 23]],  # C-각도수치
            ConfigROI.phasor_a_c_angle_cur: [763, 394, 14, 21], # A~C-각도기호

            # harmonics
            ConfigROI.harmonics_img_cut: [170, 260, 600, 213],
            ConfigROI.harmonics_text_img: [n*x for x in [165, 230, 620, 240]],
            ConfigROI.harmonics_title: [n*x for x in [160, 120, 630, 53]],
            ConfigROI.harmonics_sub_title_1: [n*x for x in [160, 180, 270, 80]], # dropdown 버튼 + THD Fund.
            ConfigROI.harmonics_sub_title_2: [n*x for x in [440, 180, 130, 40]], # Fund.
            ConfigROI.harmonics_sub_title_3: [n*x for x in [580, 180, 2000, 40]], # Fund.
            ConfigROI.harmonics_text_title: [n*x for x in [160, 180, 620, 40]],
            ConfigROI.harmonics_text_sub_title : [n*x for x in [160, 180, 270, 40]],
            ConfigROI.harmonics_text_sub_abc : [n*x for x in [590, 180, 190, 40]],
            ConfigROI.harmonics_graph_a : [n*x for x in [435, 220, 15, 21]],
            ConfigROI.harmonics_graph_b : [n*x for x in [555, 220, 15, 21]],
            ConfigROI.harmonics_graph_c : [n*x for x in [675, 220, 15, 21]],
            ConfigROI.harmonics_thd_a : [n*x for x in [465, 220, 70, 21]],
            ConfigROI.harmonics_thd_b : [n*x for x in [585, 220, 70, 21]],
            ConfigROI.harmonics_thd_c : [n*x for x in [705, 220, 70, 21]],
            ConfigROI.harmonics_fund_a : [n*x for x in [465, 241, 70, 23]],
            ConfigROI.harmonics_fund_b : [n*x for x in [585, 241, 70, 23]],
            ConfigROI.harmonics_fund_c : [n*x for x in [705, 241, 70, 23]],

            #Waveform
            ConfigROI.waveform_all_img_cut: [170, 179, 610, 286],
            ConfigROI.waveform_graph_img_cut: [313, 253, 411, 203],
            ConfigROI.waveform_title: [n*x for x in [160, 120, 630, 53]],
            ConfigROI.harmonics_graph_img_cut: [313, 283, 455, 173],
            ConfigROI.harmonics_chart_img_cut: [250, 260, 495, 214],
            ConfigROI.harmonics_text_number_title_1: [n*x for x in [175, 237, 30, 225]],
            ConfigROI.harmonics_text_number_meas_1: [n*x for x in [206, 238, 67, 232]],
            ConfigROI.harmonics_text_chart_img_cut_3: [n*x for x in [170, 389, 610, 240]],

            ConfigROI.s_wiring_1: [n*x for x in [175, 182, 298, 34]],
            ConfigROI.s_wiring_2: [n*x for x in [175, 216, 298, 35]],
            ConfigROI.s_min_meas_sec_ln_vol_1: [n*x for x in [476, 182, 298, 34]],
            ConfigROI.s_min_meas_sec_ln_vol_2: [n*x for x in [740, 216, 34, 35]],
            ConfigROI.s_vt_primary_ll_vol_1: [n*x for x in [175, 254, 298, 34]],
            # ConfigROI.s_vt_primary_ll_vol_2: [n*x for x in [175, 288, 298, 34]],
            ConfigROI.s_vt_primary_ll_vol_2: [n*x for x in [340, 292, 133, 28]],
            ConfigROI.s_vt_secondary_ll_vol_1: [n*x for x in [476, 254, 298, 34]],
            ConfigROI.s_vt_secondary_ll_vol_2: [n*x for x in [476, 288, 298, 35]],
            ConfigROI.s_primary_reference_vol_1: [n*x for x in [175, 326, 298, 34]],
            ConfigROI.s_primary_reference_vol_2: [n*x for x in [175, 360, 298, 35]],
            ConfigROI.s_primary_reference_vol_3: [n*x for x in [175, 360, 298, 35]],
            ConfigROI.s_sliding_reference_vol_1: [n*x for x in [476, 326, 298, 34]],
            ConfigROI.s_sliding_reference_vol_2: [n*x for x in [476, 360, 298, 35]],
            ConfigROI.s_rotation_sequence_1: [n*x for x in [175, 398, 298, 34]],
            ConfigROI.s_rotation_sequence_2: [n*x for x in [175, 432, 298, 35]],
            ConfigROI.s_ct_primary_curr_1: [n*x for x in [175, 182, 298, 69]],
            ConfigROI.s_ct_primary_curr_2: [n*x for x in [175, 216, 298, 35]],
            ConfigROI.s_ct_secondary_curr_1: [n*x for x in [476, 182, 298, 34]],
            ConfigROI.s_ct_secondary_curr_2: [n*x for x in [476, 216, 298, 35]],
            ConfigROI.s_reference_curr_1: [n*x for x in [175, 254, 298, 34]],
            ConfigROI.s_reference_curr_2: [n*x for x in [175, 288, 298, 35]],
            ConfigROI.s_min_meas_curr_1: [n*x for x in [476, 254, 298, 34]],
            ConfigROI.s_min_meas_curr_2: [n*x for x in [476, 288, 298, 35]],
            ConfigROI.s_tdd_reference_selection_1: [n*x for x in [175, 326, 298, 34]],
            ConfigROI.s_tdd_reference_selection_2: [n*x for x in [175, 360, 298, 35]],
            ConfigROI.s_tdd_nominal_curr_1: [n*x for x in [476, 326, 298, 34]],
            ConfigROI.s_tdd_nominal_curr_2: [n*x for x in [476, 360, 298, 35]],
            ConfigROI.s_tdd_nominal_curr_3: [n*x for x in [476, 360, 298, 35]],
             
        }
        return params