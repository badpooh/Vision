from os import error
import re
import threading
import time
import numpy as np
import cv2
from datetime import datetime, timezone, timedelta
import time
from pymodbus.client import ModbusTcpClient as ModbusClient
import threading
import shutil
# import torch
import os
import pandas as pd
from paddleocr import PaddleOCR
from collections import Counter
from itertools import chain

from demo_test.demo_config import ConfigSetup
from demo_test.demo_config import ConfigTextRef as ec
from demo_test.demo_config import ConfigROI as ecr
from demo_test.demo_config import ConfigImgRef as ecir
from demo_test.demo_config import ConfigModbusMap as ecm
from demo_test.demo_config import ConfigTouch as ect

config_data = ConfigSetup()

class TouchManager:

    mobus_manager = ModbusManager()
    hex_value = int("A5A5", 16)

    def __init__(self):
        self.client_check = self.mobus_manager.touch_client
        self.coords_touch = config_data.touch_data()
        self.coords_color = config_data.color_detection_data()

    def touch_write(self, address, value, delay=0.6):
        attempt = 0
        # print("Touching", end='', flush=True)
        while attempt < 2:
            self.client_check.write_register(address, value)
            read_value = self.client_check.read_holding_registers(address)
            time.sleep(delay)
            if read_value == value:
                print("\nTouched")
                return
            else:
                attempt += 1
                # print(".", end='', flush=True) 
        # print(f"Failed to write value {value} to address {
        #       address}. Read back {read_value} instead.")

    def uitest_mode_start(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_ui_test_mode.value, 1)
        else:
            print("client Error")

    def screenshot(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_screen_capture.value, self.hex_value)
        else:
            print("client Error")

    def menu_touch(self, menu_key):
        if self.client_check:
            data_view_x, data_view_y = menu_key
            self.touch_write(ect.touch_addr_pos_x.value, data_view_x)
            self.touch_write(ect.touch_addr_pos_y.value, data_view_y)
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Menu Touch Error")

    def btn_popup_touch(self, btn_popup_key):
        if self.client_check:
            btn_x, btn_y = self.coords_touch[btn_popup_key]
            self.touch_write(ect.touch_addr_pos_x.value, btn_x)
            self.touch_write(ect.touch_addr_pos_y.value, btn_y)
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Button Popup Touch Error")

    def number_1_touch(self, number_key):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(
                ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def number_2_touch(self, number_key1, number_key2):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key1]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_a, number_b = self.coords_touch[number_key2]
            self.touch_write(ect.touch_addr_pos_x.value, number_a)
            self.touch_write(ect.touch_addr_pos_y.value, number_b)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def number_3_touch(self, number_key1, number_key2, number_key3):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key1]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_a, number_b = self.coords_touch[number_key2]
            self.touch_write(ect.touch_addr_pos_x.value, number_a)
            self.touch_write(ect.touch_addr_pos_y.value, number_b)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_c, number_d = self.coords_touch[number_key3]
            self.touch_write(ect.touch_addr_pos_x.value, number_c)
            self.touch_write(ect.touch_addr_pos_y.value, number_d)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def btn_apply_touch(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_apply"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_apply"][1])
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Button Apply Touch Error")

    def btn_front_setup(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 2)
        else:
            print("Button Apply Touch Error")

    def btn_front_meter(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 64)
        else:
            print("Button Apply Touch Error")

    def btn_front_home(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 1)
        else:
            print("Button Apply Touch Error")
