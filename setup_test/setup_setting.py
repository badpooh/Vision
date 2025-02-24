from PySide6.QtWidgets import QVBoxLayout, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QTableWidgetItem, QTableWidget, QHeaderView
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression, Qt, Signal, QEvent

from setup_test.ui_setting import Ui_Form
from setup_test.ui_setup_ip import Ui_setup_ip
from setup_test.setup_db import IPDataBase


class SettingWindow(QWidget, Ui_Form):
    
	tcSelected = Signal(int, str)
  
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setObjectName("My Setting")
		self.current_row = None
		self.btn_menu_voltage.setChecked(True)
		self.vol_check_box.setHidden(True)
		self.btn_menu_current.setChecked(True)
		self.curr_check_box.setHidden(True)
		self.btn_menu_power.setChecked(True)
		self.pow_check_box.setHidden(True)
		self.btn_menu_analysis.setChecked(True)
		self.anal_check_box.setHidden(True)
		self.btn_menu_test_mode.setChecked(True)
		self.tm_check_box.setHidden(True)
		self.btn_menu_system.setChecked(True)
		self.sys_check_box.setHidden(True)
		self.checkbox_states = {
			"tm_all": False,
			"tm_balance": False,
			"tm_noload": False,
			"vol_all": False,
			"vol_rms": False,
			"vol_fund": False,
			"vol_thd": False,
			"vol_freq": False,
			"vol_residual": False,
			"vol_sliding": False,
			"curr_all": False,
			"curr_rms": False,
			"curr_fund": False,
			"curr_demand": False,
			"curr_thd": False,
			"curr_tdd": False,
			"curr_cf": False,
			"curr_kf": False,
			"curr_residual": False,
			"pow_all": False,
			"pow_p": False,
			"pow_q": False,
			"pow_s": False,
			"pow_pf": False,
			"pow_demand": False,
			"pow_energy": False,
			"anal_all": False,
			"anal_phasor": False,
			"anal_harmonics": False,
			"anal_waveform": False,
			"anal_volt_sym": False,
			"anal_volt_unbal": False,
			"anal_curr_sym": False,
			"anal_curr_unbal": False,
			"sys_all": False,
			"mea_vol": False,
			}
		self.btn_apply.clicked.connect(self.tc_apply)
		self.btn_cancel.clicked.connect(self.close)
		self.cb_tm_all.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "tm_all"))
		self.cb_tm_balance.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "tm_balance"))
		self.cb_tm_noload.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "tm_noload"))
		self.cb_vol_all.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "vol_all"))
		self.cb_vol_rms.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "vol_rms"))
		self.cb_vol_fund.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "vol_fund"))
		self.cb_vol_thd.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "vol_thd"))
		self.cb_vol_freq.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "vol_freq"))
		self.cb_vol_residual.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "vol_residual"))
		self.cb_vol_sliding.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "vol_sliding"))
		self.cb_curr_all.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "curr_all"))
		self.cb_curr_rms.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "curr_rms"))
		self.cb_curr_fund.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "curr_fund"))
		self.cb_curr_demand.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "curr_demand"))
		self.cb_curr_thd.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "curr_thd"))
		self.cb_curr_tdd.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "curr_tdd"))
		self.cb_curr_cf.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "curr_cf"))
		self.cb_curr_kf.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "curr_kf"))
		self.cb_curr_residual.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "curr_residual"))
		self.cb_pow_all.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "pow_all"))
		self.cb_pow_p.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "pow_p"))
		self.cb_pow_q.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "pow_q"))
		self.cb_pow_s.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "pow_s"))
		self.cb_pow_pf.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "pow_pf"))
		self.cb_pow_demand.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "pow_demand"))
		self.cb_pow_energy.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "pow_energy"))
		self.cb_anal_all.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "anal_all"))
		self.cb_anal_phasor.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "anal_phasor"))
		self.cb_anal_harmonics.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "anal_harmonics"))
		self.cb_anal_waveform.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "anal_waveform"))
		self.cb_anal_volt_sym.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "anal_volt_sym"))
		self.cb_anal_volt_unbal.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "anal_volt_unbal"))
		self.cb_anal_curr_unbal.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "anal_curr_sym"))
		self.cb_anal_curr_unbal.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "anal_curr_unbal"))
		self.cb_sys_all.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "sys_all"))
		self.mea_vol.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "mea_vol"))
   
	def open_new_window(self, row):
		instance_qwidget = SettingWindow()
		instance_qwidget.setWindowTitle(f"Setting {row}")
		instance_qwidget.resize(600, 600)
		instance_qwidget.current_row = row
		return instance_qwidget
	
	def on_checkbox_changed(self, state, key):
		self.checkbox_states[key] = state == 2  # 2는 체크됨, 0은 체크되지 않음
		print(f"{key.capitalize()} checkbox {'checked' if state == 2 else 'unchecked'}")

		if key == "tm_all":
			if state == 2:
				self.cb_tm_balance.setChecked(False)
				self.cb_tm_noload.setChecked(False)
				self.cb_vol_all.setChecked(False)
				self.cb_vol_rms.setChecked(False)
				self.cb_vol_fund.setChecked(False)
				self.cb_vol_thd.setChecked(False)
				self.cb_vol_freq.setChecked(False)
				self.cb_vol_residual.setChecked(False)
				self.cb_vol_sliding.setChecked(False)
				self.cb_curr_all.setChecked(False)
				self.cb_curr_rms.setChecked(False)
				self.cb_curr_fund.setChecked(False)
				self.cb_curr_demand.setChecked(False)
				self.cb_curr_thd.setChecked(False)
				self.cb_curr_tdd.setChecked(False)
				self.cb_curr_cf.setChecked(False)
				self.cb_curr_kf.setChecked(False)
				self.cb_curr_residual.setChecked(False)
				self.cb_curr_rms.setChecked(False)
				self.cb_curr_fund.setChecked(False)
				self.cb_curr_demand.setChecked(False)
				self.cb_curr_thd.setChecked(False)
				self.cb_curr_tdd.setChecked(False)
				self.cb_curr_cf.setChecked(False)
				self.cb_curr_kf.setChecked(False)
				self.cb_curr_residual.setChecked(False)
				self.cb_pow_all.setChecked(False)
				self.cb_pow_p.setChecked(False)
				self.cb_pow_q.setChecked(False)
				self.cb_pow_s.setChecked(False)
				self.cb_pow_pf.setChecked(False)
				self.cb_pow_demand.setChecked(False)
				self.cb_pow_energy.setChecked(False)
				self.cb_anal_all.setChecked(False)
				self.cb_anal_phasor.setChecked(False)
				self.cb_anal_harmonics.setChecked(False)
				self.cb_anal_waveform.setChecked(False)
				self.cb_anal_volt_sym.setChecked(False)
				self.cb_anal_volt_unbal.setChecked(False)
				self.cb_anal_curr_sym.setChecked(False)
				self.cb_anal_curr_unbal.setChecked(False)
				self.cb_sys_all.setChecked(False)

				self.cb_tm_balance.setEnabled(False)
				self.cb_tm_noload.setEnabled(False)
				self.cb_vol_all.setEnabled(False)
				self.cb_vol_rms.setEnabled(False)
				self.cb_vol_fund.setEnabled(False)
				self.cb_vol_thd.setEnabled(False)
				self.cb_vol_freq.setEnabled(False)
				self.cb_vol_residual.setEnabled(False)
				self.cb_vol_sliding.setEnabled(False)
				self.cb_curr_all.setEnabled(False)
				self.cb_curr_rms.setEnabled(False)
				self.cb_curr_fund.setEnabled(False)
				self.cb_curr_demand.setEnabled(False)
				self.cb_curr_thd.setEnabled(False)
				self.cb_curr_tdd.setEnabled(False)
				self.cb_curr_cf.setEnabled(False)
				self.cb_curr_kf.setEnabled(False)
				self.cb_curr_residual.setEnabled(False)
				self.cb_curr_rms.setEnabled(False)
				self.cb_curr_fund.setEnabled(False)
				self.cb_curr_demand.setEnabled(False)
				self.cb_curr_thd.setEnabled(False)
				self.cb_curr_tdd.setEnabled(False)
				self.cb_curr_cf.setEnabled(False)
				self.cb_curr_kf.setEnabled(False)
				self.cb_curr_residual.setEnabled(False)
				self.cb_pow_all.setEnabled(False)
				self.cb_pow_p.setEnabled(False)
				self.cb_pow_q.setEnabled(False)
				self.cb_pow_s.setEnabled(False)
				self.cb_pow_pf.setEnabled(False)
				self.cb_pow_demand.setEnabled(False)
				self.cb_pow_energy.setEnabled(False)
				self.cb_anal_all.setEnabled(False)
				self.cb_anal_phasor.setEnabled(False)
				self.cb_anal_harmonics.setEnabled(False)
				self.cb_anal_waveform.setEnabled(False)
				self.cb_anal_volt_sym.setEnabled(False)
				self.cb_anal_volt_unbal.setEnabled(False)
				self.cb_anal_curr_sym.setEnabled(False)
				self.cb_anal_curr_unbal.setEnabled(False)
				self.cb_sys_all.setEnabled(False)
			else:
				self.cb_tm_balance.setEnabled(True)
				self.cb_tm_noload.setEnabled(True)
				self.cb_vol_all.setEnabled(True)
				self.cb_vol_rms.setEnabled(True)
				self.cb_vol_fund.setEnabled(True)
				self.cb_vol_thd.setEnabled(True)
				self.cb_vol_freq.setEnabled(True)
				self.cb_vol_residual.setEnabled(True)
				self.cb_vol_sliding.setEnabled(True)
				self.cb_curr_all.setEnabled(True)
				self.cb_curr_rms.setEnabled(True)
				self.cb_curr_fund.setEnabled(True)
				self.cb_curr_demand.setEnabled(True)
				self.cb_curr_thd.setEnabled(True)
				self.cb_curr_tdd.setEnabled(True)
				self.cb_curr_cf.setEnabled(True)
				self.cb_curr_kf.setEnabled(True)
				self.cb_curr_residual.setEnabled(True)
				self.cb_curr_rms.setEnabled(True)
				self.cb_curr_fund.setEnabled(True)
				self.cb_curr_demand.setEnabled(True)
				self.cb_curr_thd.setEnabled(True)
				self.cb_curr_tdd.setEnabled(True)
				self.cb_curr_cf.setEnabled(True)
				self.cb_curr_kf.setEnabled(True)
				self.cb_curr_residual.setEnabled(True)
				self.cb_pow_all.setEnabled(True)
				self.cb_pow_p.setEnabled(True)
				self.cb_pow_q.setEnabled(True)
				self.cb_pow_s.setEnabled(True)
				self.cb_pow_pf.setEnabled(True)
				self.cb_pow_demand.setEnabled(True)
				self.cb_pow_energy.setEnabled(True)
				self.cb_anal_all.setEnabled(True)
				self.cb_anal_phasor.setEnabled(True)
				self.cb_anal_harmonics.setEnabled(True)
				self.cb_anal_waveform.setEnabled(True)
				self.cb_anal_volt_sym.setEnabled(True)
				self.cb_anal_volt_unbal.setEnabled(True)
				self.cb_anal_curr_sym.setEnabled(True)
				self.cb_anal_curr_unbal.setEnabled(True)
				self.cb_sys_all.setEnabled(True)


		elif key == "tm_balance":
			if state == 2:
				self.cb_tm_all.setChecked(False)
				self.cb_tm_noload.setChecked(False)
				self.cb_vol_all.setChecked(False)
				self.cb_vol_rms.setChecked(False)
				self.cb_vol_fund.setChecked(False)
				self.cb_vol_thd.setChecked(False)
				self.cb_vol_freq.setChecked(False)
				self.cb_vol_residual.setChecked(False)
				self.cb_vol_sliding.setChecked(False)
				self.cb_curr_all.setChecked(False)
				self.cb_curr_rms.setChecked(False)
				self.cb_curr_fund.setChecked(False)
				self.cb_curr_demand.setChecked(False)
				self.cb_curr_thd.setChecked(False)
				self.cb_curr_tdd.setChecked(False)
				self.cb_curr_cf.setChecked(False)
				self.cb_curr_kf.setChecked(False)
				self.cb_curr_residual.setChecked(False)
				self.cb_curr_rms.setChecked(False)
				self.cb_curr_fund.setChecked(False)
				self.cb_curr_demand.setChecked(False)
				self.cb_curr_thd.setChecked(False)
				self.cb_curr_tdd.setChecked(False)
				self.cb_curr_cf.setChecked(False)
				self.cb_curr_kf.setChecked(False)
				self.cb_curr_residual.setChecked(False)
				self.cb_pow_all.setChecked(False)
				self.cb_pow_p.setChecked(False)
				self.cb_pow_q.setChecked(False)
				self.cb_pow_s.setChecked(False)
				self.cb_pow_pf.setChecked(False)
				self.cb_pow_demand.setChecked(False)
				self.cb_pow_energy.setChecked(False)
				self.cb_anal_all.setChecked(False)
				self.cb_anal_phasor.setChecked(False)
				self.cb_anal_harmonics.setChecked(False)
				self.cb_anal_waveform.setChecked(False)
				self.cb_anal_volt_sym.setChecked(False)
				self.cb_anal_volt_unbal.setChecked(False)
				self.cb_anal_curr_sym.setChecked(False)
				self.cb_anal_curr_unbal.setChecked(False)
				self.cb_sys_all.setChecked(False)

				self.cb_tm_all.setEnabled(False)
				self.cb_tm_noload.setEnabled(False)
				self.cb_vol_all.setEnabled(False)
				self.cb_vol_rms.setEnabled(False)
				self.cb_vol_fund.setEnabled(False)
				self.cb_vol_thd.setEnabled(False)
				self.cb_vol_freq.setEnabled(False)
				self.cb_vol_residual.setEnabled(False)
				self.cb_vol_sliding.setEnabled(False)
				self.cb_curr_all.setEnabled(False)
				self.cb_curr_rms.setEnabled(False)
				self.cb_curr_fund.setEnabled(False)
				self.cb_curr_demand.setEnabled(False)
				self.cb_curr_thd.setEnabled(False)
				self.cb_curr_tdd.setEnabled(False)
				self.cb_curr_cf.setEnabled(False)
				self.cb_curr_kf.setEnabled(False)
				self.cb_curr_residual.setEnabled(False)
				self.cb_curr_rms.setEnabled(False)
				self.cb_curr_fund.setEnabled(False)
				self.cb_curr_demand.setEnabled(False)
				self.cb_curr_thd.setEnabled(False)
				self.cb_curr_tdd.setEnabled(False)
				self.cb_curr_cf.setEnabled(False)
				self.cb_curr_kf.setEnabled(False)
				self.cb_curr_residual.setEnabled(False)
				self.cb_pow_all.setEnabled(False)
				self.cb_pow_p.setEnabled(False)
				self.cb_pow_q.setEnabled(False)
				self.cb_pow_s.setEnabled(False)
				self.cb_pow_pf.setEnabled(False)
				self.cb_pow_demand.setEnabled(False)
				self.cb_pow_energy.setEnabled(False)
				self.cb_anal_all.setEnabled(False)
				self.cb_anal_phasor.setEnabled(False)
				self.cb_anal_harmonics.setEnabled(False)
				self.cb_anal_waveform.setEnabled(False)
				self.cb_anal_volt_sym.setEnabled(False)
				self.cb_anal_volt_unbal.setEnabled(False)
				self.cb_anal_curr_sym.setEnabled(False)
				self.cb_anal_curr_unbal.setEnabled(False)
				self.cb_sys_all.setEnabled(False)
			else:
				self.cb_tm_all.setEnabled(True)
				self.cb_tm_noload.setEnabled(True)
				self.cb_vol_all.setEnabled(True)
				self.cb_vol_rms.setEnabled(True)
				self.cb_vol_fund.setEnabled(True)
				self.cb_vol_thd.setEnabled(True)
				self.cb_vol_freq.setEnabled(True)
				self.cb_vol_residual.setEnabled(True)
				self.cb_vol_sliding.setEnabled(True)
				self.cb_curr_all.setEnabled(True)
				self.cb_curr_rms.setEnabled(True)
				self.cb_curr_fund.setEnabled(True)
				self.cb_curr_demand.setEnabled(True)
				self.cb_curr_thd.setEnabled(True)
				self.cb_curr_tdd.setEnabled(True)
				self.cb_curr_cf.setEnabled(True)
				self.cb_curr_kf.setEnabled(True)
				self.cb_curr_residual.setEnabled(True)
				self.cb_curr_rms.setEnabled(True)
				self.cb_curr_fund.setEnabled(True)
				self.cb_curr_demand.setEnabled(True)
				self.cb_curr_thd.setEnabled(True)
				self.cb_curr_tdd.setEnabled(True)
				self.cb_curr_cf.setEnabled(True)
				self.cb_curr_kf.setEnabled(True)
				self.cb_curr_residual.setEnabled(True)
				self.cb_pow_all.setEnabled(True)
				self.cb_pow_p.setEnabled(True)
				self.cb_pow_q.setEnabled(True)
				self.cb_pow_s.setEnabled(True)
				self.cb_pow_pf.setEnabled(True)
				self.cb_pow_demand.setEnabled(True)
				self.cb_pow_energy.setEnabled(True)
				self.cb_anal_all.setEnabled(True)
				self.cb_anal_phasor.setEnabled(True)
				self.cb_anal_harmonics.setEnabled(True)
				self.cb_anal_waveform.setEnabled(True)
				self.cb_anal_volt_sym.setEnabled(True)
				self.cb_anal_volt_unbal.setEnabled(True)
				self.cb_anal_curr_sym.setEnabled(True)
				self.cb_anal_curr_unbal.setEnabled(True)
				self.cb_sys_all.setEnabled(True)


		if key == "tm_noload":
			if state == 2:
				self.cb_tm_all.setChecked(False)
				self.cb_tm_balance.setChecked(False)
				self.cb_vol_all.setChecked(False)
				self.cb_vol_rms.setChecked(False)
				self.cb_vol_fund.setChecked(False)
				self.cb_vol_thd.setChecked(False)
				self.cb_vol_freq.setChecked(False)
				self.cb_vol_residual.setChecked(False)
				self.cb_vol_sliding.setChecked(False)
				self.cb_curr_all.setChecked(False)
				self.cb_curr_rms.setChecked(False)
				self.cb_curr_fund.setChecked(False)
				self.cb_curr_demand.setChecked(False)
				self.cb_curr_thd.setChecked(False)
				self.cb_curr_tdd.setChecked(False)
				self.cb_curr_cf.setChecked(False)
				self.cb_curr_kf.setChecked(False)
				self.cb_curr_residual.setChecked(False)
				self.cb_curr_rms.setChecked(False)
				self.cb_curr_fund.setChecked(False)
				self.cb_curr_demand.setChecked(False)
				self.cb_curr_thd.setChecked(False)
				self.cb_curr_tdd.setChecked(False)
				self.cb_curr_cf.setChecked(False)
				self.cb_curr_kf.setChecked(False)
				self.cb_curr_residual.setChecked(False)
				self.cb_pow_all.setChecked(False)
				self.cb_pow_p.setChecked(False)
				self.cb_pow_q.setChecked(False)
				self.cb_pow_s.setChecked(False)
				self.cb_pow_pf.setChecked(False)
				self.cb_pow_demand.setChecked(False)
				self.cb_pow_energy.setChecked(False)
				self.cb_anal_all.setChecked(False)
				self.cb_anal_phasor.setChecked(False)
				self.cb_anal_harmonics.setChecked(False)
				self.cb_anal_waveform.setChecked(False)
				self.cb_anal_volt_sym.setChecked(False)
				self.cb_anal_volt_unbal.setChecked(False)
				self.cb_anal_curr_sym.setChecked(False)
				self.cb_anal_curr_unbal.setChecked(False)
				self.cb_sys_all.setChecked(False)

				self.cb_tm_all.setEnabled(False)
				self.cb_tm_balance.setEnabled(False)
				self.cb_vol_all.setEnabled(False)
				self.cb_vol_rms.setEnabled(False)
				self.cb_vol_fund.setEnabled(False)
				self.cb_vol_thd.setEnabled(False)
				self.cb_vol_freq.setEnabled(False)
				self.cb_vol_residual.setEnabled(False)
				self.cb_vol_sliding.setEnabled(False)
				self.cb_curr_all.setEnabled(False)
				self.cb_curr_rms.setEnabled(False)
				self.cb_curr_fund.setEnabled(False)
				self.cb_curr_demand.setEnabled(False)
				self.cb_curr_thd.setEnabled(False)
				self.cb_curr_tdd.setEnabled(False)
				self.cb_curr_cf.setEnabled(False)
				self.cb_curr_kf.setEnabled(False)
				self.cb_curr_residual.setEnabled(False)
				self.cb_curr_rms.setEnabled(False)
				self.cb_curr_fund.setEnabled(False)
				self.cb_curr_demand.setEnabled(False)
				self.cb_curr_thd.setEnabled(False)
				self.cb_curr_tdd.setEnabled(False)
				self.cb_curr_cf.setEnabled(False)
				self.cb_curr_kf.setEnabled(False)
				self.cb_curr_residual.setEnabled(False)
				self.cb_pow_all.setEnabled(False)
				self.cb_pow_p.setEnabled(False)
				self.cb_pow_q.setEnabled(False)
				self.cb_pow_s.setEnabled(False)
				self.cb_pow_pf.setEnabled(False)
				self.cb_pow_demand.setEnabled(False)
				self.cb_pow_energy.setEnabled(False)
				self.cb_anal_all.setEnabled(False)
				self.cb_anal_phasor.setEnabled(False)
				self.cb_anal_harmonics.setEnabled(False)
				self.cb_anal_waveform.setEnabled(False)
				self.cb_anal_volt_sym.setEnabled(False)
				self.cb_anal_volt_unbal.setEnabled(False)
				self.cb_anal_curr_sym.setEnabled(False)
				self.cb_anal_curr_unbal.setEnabled(False)
				self.cb_sys_all.setEnabled(False)
			else:
				self.cb_tm_balance.setEnabled(True)
				self.cb_tm_all.setEnabled(True)
				self.cb_vol_all.setEnabled(True)
				self.cb_vol_rms.setEnabled(True)
				self.cb_vol_fund.setEnabled(True)
				self.cb_vol_thd.setEnabled(True)
				self.cb_vol_freq.setEnabled(True)
				self.cb_vol_residual.setEnabled(True)
				self.cb_vol_sliding.setEnabled(True)
				self.cb_curr_all.setEnabled(True)
				self.cb_curr_rms.setEnabled(True)
				self.cb_curr_fund.setEnabled(True)
				self.cb_curr_demand.setEnabled(True)
				self.cb_curr_thd.setEnabled(True)
				self.cb_curr_tdd.setEnabled(True)
				self.cb_curr_cf.setEnabled(True)
				self.cb_curr_kf.setEnabled(True)
				self.cb_curr_residual.setEnabled(True)
				self.cb_curr_rms.setEnabled(True)
				self.cb_curr_fund.setEnabled(True)
				self.cb_curr_demand.setEnabled(True)
				self.cb_curr_thd.setEnabled(True)
				self.cb_curr_tdd.setEnabled(True)
				self.cb_curr_cf.setEnabled(True)
				self.cb_curr_kf.setEnabled(True)
				self.cb_curr_residual.setEnabled(True)
				self.cb_pow_all.setEnabled(True)
				self.cb_pow_p.setEnabled(True)
				self.cb_pow_q.setEnabled(True)
				self.cb_pow_s.setEnabled(True)
				self.cb_pow_pf.setEnabled(True)
				self.cb_pow_demand.setEnabled(True)
				self.cb_pow_energy.setEnabled(True)
				self.cb_anal_all.setEnabled(True)
				self.cb_anal_phasor.setEnabled(True)
				self.cb_anal_harmonics.setEnabled(True)
				self.cb_anal_waveform.setEnabled(True)
				self.cb_anal_volt_sym.setEnabled(True)
				self.cb_anal_volt_unbal.setEnabled(True)
				self.cb_anal_curr_sym.setEnabled(True)
				self.cb_anal_curr_unbal.setEnabled(True)
				self.cb_sys_all.setEnabled(True)


		elif key == "vol_all":
			if state == 2:
				self.cb_vol_rms.setChecked(False)
				self.cb_vol_fund.setChecked(False)
				self.cb_vol_thd.setChecked(False)
				self.cb_vol_freq.setChecked(False)
				self.cb_vol_residual.setChecked(False)
				self.cb_vol_sliding.setChecked(False)

				self.cb_vol_rms.setEnabled(False)
				self.cb_vol_fund.setEnabled(False)
				self.cb_vol_thd.setEnabled(False)
				self.cb_vol_freq.setEnabled(False)
				self.cb_vol_residual.setEnabled(False)
				self.cb_vol_sliding.setEnabled(False)
			else: 
				self.cb_vol_rms.setEnabled(True)
				self.cb_vol_fund.setEnabled(True)
				self.cb_vol_thd.setEnabled(True)
				self.cb_vol_freq.setEnabled(True)
				self.cb_vol_residual.setEnabled(True)
				self.cb_vol_sliding.setEnabled(True)

		elif key == "curr_all":
			if state == 2:
				self.cb_curr_rms.setChecked(False)
				self.cb_curr_fund.setChecked(False)
				self.cb_curr_demand.setChecked(False)
				self.cb_curr_thd.setChecked(False)
				self.cb_curr_tdd.setChecked(False)
				self.cb_curr_cf.setChecked(False)
				self.cb_curr_kf.setChecked(False)
				self.cb_curr_residual.setChecked(False)

				self.cb_curr_rms.setEnabled(False)
				self.cb_curr_fund.setEnabled(False)
				self.cb_curr_demand.setEnabled(False)
				self.cb_curr_thd.setEnabled(False)
				self.cb_curr_tdd.setEnabled(False)
				self.cb_curr_cf.setEnabled(False)
				self.cb_curr_kf.setEnabled(False)
				self.cb_curr_residual.setEnabled(False)
			else: 
				self.cb_curr_rms.setEnabled(True)
				self.cb_curr_fund.setEnabled(True)
				self.cb_curr_demand.setEnabled(True)
				self.cb_curr_thd.setEnabled(True)
				self.cb_curr_tdd.setEnabled(True)
				self.cb_curr_cf.setEnabled(True)
				self.cb_curr_kf.setEnabled(True)
				self.cb_curr_residual.setEnabled(True)
		
		elif key == "pow_all":
			if state == 2:
				self.cb_pow_p.setChecked(False)
				self.cb_pow_q.setChecked(False)
				self.cb_pow_s.setChecked(False)
				self.cb_pow_pf.setChecked(False)
				self.cb_pow_demand.setChecked(False)
				self.cb_pow_energy.setChecked(False)

				self.cb_pow_p.setEnabled(False)
				self.cb_pow_q.setEnabled(False)
				self.cb_pow_s.setEnabled(False)
				self.cb_pow_pf.setEnabled(False)
				self.cb_pow_demand.setEnabled(False)
				self.cb_pow_energy.setEnabled(False)
			else:
				self.cb_pow_p.setEnabled(True)
				self.cb_pow_q.setEnabled(True)
				self.cb_pow_s.setEnabled(True)
				self.cb_pow_pf.setEnabled(True)
				self.cb_pow_demand.setEnabled(True)
				self.cb_pow_energy.setEnabled(True)
		
		elif key == "anal_all":
			if state == 2:
				self.cb_anal_phasor.setChecked(False)
				self.cb_anal_harmonics.setChecked(False)
				self.cb_anal_waveform.setChecked(False)
				self.cb_anal_volt_sym.setChecked(False)
				self.cb_anal_volt_unbal.setChecked(False)
				self.cb_anal_curr_sym.setChecked(False)
				self.cb_anal_curr_unbal.setChecked(False)

				self.cb_anal_phasor.setEnabled(False)
				self.cb_anal_harmonics.setEnabled(False)
				self.cb_anal_waveform.setEnabled(False)
				self.cb_anal_volt_sym.setEnabled(False)
				self.cb_anal_volt_unbal.setEnabled(False)
				self.cb_anal_curr_sym.setEnabled(False)
				self.cb_anal_curr_unbal.setEnabled(False)
			else:
				self.cb_anal_phasor.setEnabled(True)
				self.cb_anal_harmonics.setEnabled(True)
				self.cb_anal_waveform.setEnabled(True)
				self.cb_anal_volt_sym.setEnabled(True)
				self.cb_anal_volt_unbal.setEnabled(True)
				self.cb_anal_curr_sym.setEnabled(True)
				self.cb_anal_curr_unbal.setEnabled(True)

		else:
			pass
	
	def tc_apply(self):
		selected_keys = [key for key, val in self.checkbox_states.items() if val is True]
		if selected_keys:
			text = ", ".join(selected_keys)
			self.tcSelected.emit(self.current_row, text)
			print(f"선택된 tc: {selected_keys}, row={self.current_row}")
			self.close()
		else:
			print("선택된 항목이 없습니다.")
	
class SettingIP(QWidget, Ui_setup_ip):
	
	ipSelected = Signal(str)
	tpSelected = Signal(str)
	spSelected = Signal(str)
	
	def __init__(self):
		super().__init__()
		self.setObjectName("IP Setting")
		self.setupUi(self)
		regex = QRegularExpression(r"^[0-9.]*$")
		validator = QRegularExpressionValidator(regex, self)
		self.ip_typing.setValidator(validator)
		self.ip_list.verticalHeader().setVisible(False)
		self.ip_list.horizontalHeader().setVisible(False)
		self.ip_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		
		self.btn_ip_add.clicked.connect(self.add_ip)
		self.btn_ip_select.clicked.connect(self.select_ip)
		self.btn_ip_del.clicked.connect(self.del_ip)
		self.btn_tp_add.clicked.connect(self.add_touch_port)
		self.btn_tp_select.clicked.connect(self.select_touch_port)
		self.btn_tp_del.clicked.connect(self.del_touch_port)
		self.btn_sp_add.clicked.connect(self.add_setup_port)
		self.btn_sp_select.clicked.connect(self.select_setup_port)
		self.btn_sp_del.clicked.connect(self.del_setup_port)
		
		self.db = IPDataBase()
		
		self.load_ips()

		self.ip_list.viewport().installEventFilter(self)
		self.tp_list.viewport().installEventFilter(self)
		self.sp_list.viewport().installEventFilter(self)

	def eventFilter(self, source, event):
		if event.type() == QEvent.MouseButtonPress:
			# 1) ip_list 영역에서 발생한 클릭인지
			if source is self.ip_list.viewport():
				item = self.ip_list.itemAt(event.pos())
				if item is None:
					# 빈 공간 클릭 시 선택 해제
					self.ip_list.clearSelection()
					self.ipSelected.emit("")
			# 2) tp_list 영역에서 발생한 클릭인지
			elif source is self.tp_list.viewport():
				item = self.tp_list.itemAt(event.pos())
				if item is None:
					self.tp_list.clearSelection()
					self.tpSelected.emit("")
			# 3) sp_list 영역에서 발생한 클릭인지
			elif source is self.sp_list.viewport():
				item = self.sp_list.itemAt(event.pos())
				if item is None:
					self.sp_list.clearSelection()
					self.spSelected.emit("")

		return super().eventFilter(source, event)

	def open_ip_window(self):
		self.show()
		
	def load_ips(self):
		self.ip_list.setRowCount(0)
		self.tp_list.setRowCount(0)
		self.sp_list.setRowCount(0)

		all_data = self.db.get_all_ips()
		
		for row_data in all_data:
			row_id, row_type, row_value = row_data  # 예: (1, 'ip', '10.10.10.1')

			if row_type == 'ip':
				ip_row_position = self.ip_list.rowCount()
				self.ip_list.insertRow(ip_row_position)

				ip_item = QTableWidgetItem(row_value)
				ip_item.setTextAlignment(Qt.AlignCenter)
				self.ip_list.setItem(ip_row_position, 0, ip_item)

			elif row_type == 'tp':
				tp_row_position = self.tp_list.rowCount()
				self.tp_list.insertRow(tp_row_position)

				tp_item = QTableWidgetItem(row_value)
				tp_item.setTextAlignment(Qt.AlignCenter)
				self.tp_list.setItem(tp_row_position, 0, tp_item)

			elif row_type == 'sp':
				sp_row_position = self.sp_list.rowCount()
				self.sp_list.insertRow(sp_row_position)

				sp_item = QTableWidgetItem(row_value)
				sp_item.setTextAlignment(Qt.AlignCenter)
				self.sp_list.setItem(sp_row_position, 0, sp_item)

			else:
				print(f"알 수 없는 type: {row_type}, value: {row_value}")
			
	def add_ip(self):
		typed_text = self.ip_typing.text()
		if not typed_text:
			return
		row_position = self.ip_list.rowCount()
		self.ip_list.insertRow(row_position)
		item = QTableWidgetItem(typed_text)
		item.setTextAlignment(Qt.AlignCenter)
		self.ip_list.setItem(row_position, 0, item)
		self.db.add_ip(typed_text)

		all_ips = self.db.get_all_ips()
		print("=== 현재 저장된 IP 목록 ===")
		for ip_row in all_ips:
			print(ip_row)  # (id, ip) 형태

	def select_ip(self):
		row = self.ip_list.currentRow()
		if row < 0:
			return

		item = self.ip_list.item(row, 0)
		if item:
			selected_ip = item.text()
			print(f"선택된 IP: {selected_ip}")
			self.ipSelected.emit(selected_ip)

	def del_ip(self):
		row = self.ip_list.currentRow()
		if row < 0:
			return

		item = self.ip_list.item(row, 0)
		if item:
			selected_ip = item.text()
			# 1) DB에서 삭제
			self.db.delete_ip(selected_ip)
			# 2) 테이블에서도 삭제
			self.ip_list.removeRow(row)
			
	def add_touch_port(self):
		typed_text = self.tp_typing.text()
		if not typed_text:
			return
		row_position = self.tp_list.rowCount()
		self.tp_list.insertRow(row_position)
		item = QTableWidgetItem(typed_text)
		item.setTextAlignment(Qt.AlignCenter)
		self.tp_list.setItem(row_position, 0, item)
		self.db.add_touch_port(typed_text)

		all_ips = self.db.get_all_ips()
		print("=== 현재 저장된 IP 목록 ===")
		for ip_row in all_ips:
			print(ip_row)  # (id, ip) 형태
			
	def select_touch_port(self):
		row = self.tp_list.currentRow()
		if row < 0:
			return

		item = self.tp_list.item(row, 0)
		if item:
			selected_tp = item.text()
			print(f"선택된 TP: {selected_tp}")
			self.tpSelected.emit(selected_tp)
	
	def del_touch_port(self):
		row = self.tp_list.currentRow()
		if row < 0:
			return

		item = self.tp_list.item(row, 0)
		if item:
			selected_tp = item.text()
			self.db.delete_ip(selected_tp)
			self.tp_list.removeRow(row)
	
	def add_setup_port(self):
		typed_text = self.sp_typing.text()
		if not typed_text:
			return
		row_position = self.sp_list.rowCount()
		self.sp_list.insertRow(row_position)
		item = QTableWidgetItem(typed_text)
		item.setTextAlignment(Qt.AlignCenter)
		self.sp_list.setItem(row_position, 0, item)
		self.db.add_setup_port(typed_text)

		all_ips = self.db.get_all_ips()
		print("=== 현재 저장된 IP 목록 ===")
		for ip_row in all_ips:
			print(ip_row)  # (id, ip) 형태
			
	def select_setup_port(self):
		row = self.sp_list.currentRow()
		if row < 0:
			return

		item = self.sp_list.item(row, 0)
		if item:
			selected_sp = item.text()
			print(f"선택된 SP: {selected_sp}")
			self.spSelected.emit(selected_sp)
	
	def del_setup_port(self):
		row = self.sp_list.currentRow()
		if row < 0:
			return

		item = self.sp_list.item(row, 0)
		if item:
			selected_sp = item.text()
			self.db.delete_ip(selected_sp)
			self.sp_list.removeRow(row)
    