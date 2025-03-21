from enum import Enum

class ConfigTextRef(Enum):
    ### measuremnet ###
    rms_vol_ll =  ["RMS Voltage L-L L-N Min Max", "AB", "BC", "CA", "Average"]
    rms_vol_ln = ["RMS Voltage L-L L-N Min Max", "A", "B", "C", "Average"]
    fund_vol_ll = ["Fund. Volt. L-L L-N Min Max", "AB", "BC", "CA", "Average"]
    fund_vol_ln = ["Fund. Volt. L-L L-N Min Max", "A", "B", "C", "Average"]
    thd_vol_ll = ["Total Harmonic Distortion L-L L-N Max", "AB", "BC", "CA"]
    thd_vol_ln = ["Total Harmonic Distortion L-L L-N Max", "A", "B", "C"]
    freq = ["Frequency Min Max", "Frequency"]
    residual_vol = ["Residual Voltage Min Max", "RMS", "Fund."]
    rms_curr = ["RMS Current Min Max", "A", "B", "C", "Average"]
    fund_curr = ["Fundamental Current Min Max", "A", "B", "C", "Average"]
    thd_curr = ["Total Harmonic Distortion Max", "A", "B", "C"]
    tdd_curr = ["Total Demand Distortion Max", "A", "B", "C"]
    cf_curr = ["Crest Factor Max", "A", "B", "C"]
    kf_curr = ["K-Factor Max", "A", "B", "C"]
    residual_curr = ["Residual Current Min Max", "RMS", "Fund."]
    active = ["Active Power Min Max", "A", "B", "C", "Total"]
    reactive = ["Reactive Power Min Max", "A", "B", "C", "Total"]
    apparent = ["Apparent Power Min Max", "A", "B", "C", "Total"]
    pf = ["Power Factor Min Max", "A", "B", "C", "Total"]
    phasor_ll = ["Phasor", "Voltage", "Current", "VLL", "VLN", "Voltage", "AB", "BC", "CA", "Current", "A", "B", "C"]
    phasor_ln = ["Phasor", "Voltage", "Current", "VLL", "VLN", "Voltage", "A", "B", "C", "Current", "A", "B", "C"]
    harmonics_for_img = ["Harmonics", "Voltage", "Current"]
    harmonics_vol_3p4w = ["Harmonics", "Voltage", "Current", "[v]", "Graph", "Fund.", "THD", "Fund.", "A", "B", "C", "A", "B", "C"]
    harmonics_curr = ["Harmonics", "Voltage", "Current", "[A]", "Graph", "Fund.", "THD", "Fund.", "A", "B", "C", "A", "B", "C"]
    harmonics_per_fund = ["Harmonics", "Voltage", "Current", "[%]Fund", "Graph", "THD", "Fund.", "Fund.", "A", "B", "C", "A", "B", "C"]
    harmonics_per_rms = ["Harmonics", "Voltage", "Current", "[%]RMS", "Graph", "THD", "Fund.", "Fund.", "A", "B", "C", "A", "B", "C"]
    waveform_3p4w = ["Waveform", "Voltage", "Current"]
    symm_vol_ll = ["Volt. Symm. Component L-L L-N Max", "Positive- Sequence", "Negative- Sequence"]
    symm_vol_ln = ["Volt. Symm. Component L-L L-N Max", "Positive- Sequence", "Negative- Sequence", "Zero- Sequence"]
    unbal_vol = ["Voltage Unbalance Max", "NEMA", "NEMA", "Negative- Sequence", "Zero- Sequence"]
    symm_curr = ["Curr. Symm. Component Max", "Positive- Sequence", "Negative- Sequence", "Zero- Sequence"]
    unbal_curr = ["Current Unbalance Max", "NEMA", "Negative- Sequence", "Zero- Sequence"]
    demand_current = ["Demand Current Peak", "A", "B", "C", "Average"]
    harmonics_text = ["Harmonics", "Voltage", "Current", "[v]", "Text", "A", "B", "C"]

    ### setup ###
    wiring = ["Wye", "Delta"]

class ConfigImgRef(Enum):
    img_ref_phasor_all_vll = r".\image_ref\11.img_ref_phasor_all_vll.png"
    img_ref_phasor_all_vll_none = r".\image_ref\11.img_ref_phasor_all_vll_none.png"
    img_ref_phasor_all_vln = r".\image_ref\12.img_ref_phasor_all_vln.png"
    img_ref_phasor_all_vln_none = r".\image_ref\12.img_ref_phasor_all_vln_none.png"
    img_ref_phasor_vol_vll = r".\image_ref\13.img_ref_phasor_vol_vll.png"
    img_ref_phasor_vol_vll_none = r".\image_ref\13.img_ref_phasor_vol_vll_none.png"
    img_ref_phasor_vol_vln = r".\image_ref\14.img_ref_phasor_vol_vln.png"
    img_ref_phasor_vol_vln_none = r".\image_ref\14.img_ref_phasor_vol_vln_none.png"
    img_ref_phasor_curr_vll = r".\image_ref\15.img_ref_phasor_curr_vll.png"
    img_ref_phasor_curr_vll_none = r".\image_ref\15.img_ref_phasor_curr_vll_none.png"
    img_ref_phasor_curr_vln = r".\image_ref\16.img_ref_phasor_curr_vln.png"
    img_ref_phasor_curr_vln_none = r".\image_ref\16.img_ref_phasor_curr_vln_none.png"
    img_ref_phasor_na_vll = r".\image_ref\17.img_ref_phasor_na_vll.png"
    img_ref_phasor_na_vln = r".\image_ref\17.img_ref_phasor_na_vln.png"
    img_ref_harmonics_vol_3p4w = r".\image_ref\21.img_ref_harmonics_vol_3p4w.png"
    img_ref_harmonics_vol_3p4w_none = r".\image_ref\21.img_ref_harmonics_vol_3p4w_none.png"
    img_ref_harmonics_curr = r".\image_ref\22.img_ref_harmonics_curr.png"
    img_ref_harmonics_curr_none = r".\image_ref\22.img_ref_harmonics_curr_none.png"
    img_ref_harmonics_vol_fund = r".\image_ref\23.img_ref_harmonics_vol_fund.png"
    img_ref_harmonics_vol_fund_none = r".\image_ref\23.img_ref_harmonics_vol_fund_none.png"
    img_ref_harmonics_vol_rms = r".\image_ref\24.img_ref_harmonics_vol_rms.png"
    img_ref_harmonics_vol_rms_none = r".\image_ref\24.img_ref_harmonics_vol_rms_none.png"
    img_ref_harmonics_curr_fund = r".\image_ref\25.img_ref_harmonics_curr_fund.png"
    img_ref_harmonics_curr_fund_none = r".\image_ref\25.img_ref_harmonics_curr_fund_none.png"
    img_ref_harmonics_curr_rms = r".\image_ref\26.img_ref_harmonics_curr_rms.png"
    img_ref_harmonics_curr_rms_none = r".\image_ref\26.img_ref_harmonics_curr_rms_none.png"
    img_ref_waveform_all = r".\image_ref\41.img_ref_waveform_all.png"
    img_ref_waveform_all_none = r".\image_ref\42.img_ref_waveform_all_none.png"

    ### AccuraSM
    img_ref_meas_refresh = r'.\image_ref\101.meas_compare_apply_refresh.png'
    img_ref_wiring_wye = r'.\image_ref\102.wiring_wye.png'
    img_ref_wiring_delta = r'.\image_ref\103.wiring_delta.png'
    img_ref_min_meas_secondary_ln_vol_0 = r'.\image_ref\104.min_meas_secondary_ln_vol_0.png'
    img_ref_min_meas_secondary_ln_vol_10 = r'.\image_ref\105.min_meas_secondary_ln_vol_10.png'
    img_ref_vt_primary_ll_vol_50 = r'.\image_ref\106.vt_primary_ll_vol_50.0.png'


